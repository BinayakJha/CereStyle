import os
import cv2
import shutil
import mediapipe as mp
import numpy as np
from sklearn.cluster import KMeans
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    api_key="csk-6f2yk2ytvkexfwnnchrxr6vyd8j2jmcetykmwd92xe3dcde9",  # Set in environment
)

# Paths
UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Mediapipe Face Detection and Landmark Modules
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Helper function to save the uploaded file
def save_uploaded_file(uploaded_file: UploadFile, folder: str):
    file_path = os.path.join(folder, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return file_path

# Extract skin color using face landmarks from Mediapipe
def extract_skin_color_mediapipe(image_path: str, num_clusters=5):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize Mediapipe Face Detection
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(image_rgb)

        if not results.detections:
            raise HTTPException(status_code=400, detail="No face detected")

        # Take the first detected face
        detection = results.detections[0]

        # Get the bounding box of the face
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = image.shape
        (x, y, w, h) = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

        # Extract the face region of interest (ROI)
        face_roi = image_rgb[y:y+h, x:x+w]

        # Reshape the face ROI to a 2D array of pixels (for K-Means clustering)
        face_pixels = face_roi.reshape(-1, 3)

        # Apply K-Means clustering to find the dominant skin color
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(face_pixels)
        dominant_color = kmeans.cluster_centers_.astype(int)
        return dominant_color[0]

# Use Cerebras API to get season and color palette recommendation
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
    return chat_completion.choices[0].message.content

# API endpoint for uploading a photo and suggesting outfits
@app.post("/upload")
async def upload_and_suggest(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = save_uploaded_file(file, UPLOAD_FOLDER)

    try:
        # Extract dominant skin tone color using Mediapipe
        skin_tone_color = extract_skin_color_mediapipe(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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