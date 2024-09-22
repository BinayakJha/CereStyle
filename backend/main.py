from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import numpy as np
from PIL import Image
import cv2
from sklearn.cluster import KMeans
from cerebras.cloud.sdk import Cerebras

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow requests from React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers, including content-type
)

# Initialize Cerebras API client
client = Cerebras(
    api_key="csk-6f2yk2ytvkexfwnnchrxr6vyd8j2jmcetykmwd92xe3dcde9",  # Make sure to set this in your environment
)

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder paths for uploaded and reference images
UPLOAD_FOLDER = "uploads/"
REFERENCE_FOLDER = "reference_images/"

# Ensure the directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REFERENCE_FOLDER, exist_ok=True)

# Helper function to save the uploaded file
def save_uploaded_file(uploaded_file: UploadFile, folder: str):
    file_path = os.path.join(folder, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return file_path

# Extract dominant colors from face using K-Means Clustering
def extract_colors_from_face(image_path: str, num_clusters=5):
    image = Image.open(image_path).convert('RGB')
    image_np = np.array(image)

    # Resize image for faster computation
    resized_image = cv2.resize(image_np, (100, 100))
    pixels = resized_image.reshape(-1, 3)

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)

    return colors

# Send the RGB skin tone to Cerebras API and get color recommendations
def get_color_recommendation(skin_tone_rgb):
    rgb_string = f"rgb({skin_tone_rgb[0]}, {skin_tone_rgb[1]}, {skin_tone_rgb[2]})"
    
    prompt = f"dont write code or any other explanation, just output the color recommendation. Given the RGB values of a person's skin tone ({rgb_string}), generate a season color (one word: autumn, summer, winter, spring) and three corresponding color codes (HEX) that best match their skin tone based on color theory. Output format should strictly only be: 'Season: <season> Colors: <color1>, <color2>, <color3>'."

    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="llama3.1-8b"
    )
    print(chat_completion)
    return chat_completion.choices[0].message.content

# API endpoint for uploading a photo and suggesting outfits
@app.post("/upload")
async def upload_and_suggest(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = save_uploaded_file(file, UPLOAD_FOLDER)
    
    # Extract dominant skin tone color
    face_colors = extract_colors_from_face(file_path)
    skin_tone_color = face_colors[np.argmax(face_colors.sum(axis=1))]

    # Use Cerebras API to get season and color palette
    color_recommendation = get_color_recommendation(skin_tone_color)

    return {
        "message": "Color recommendation generated",
        "color_recommendation": color_recommendation,
        "skinTone": f"rgb({skin_tone_color[0]}, {skin_tone_color[1]}, {skin_tone_color[2]})"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)