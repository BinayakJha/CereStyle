import os
import cv2
import shutil
import mediapipe as mp
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from cerebras.cloud.sdk import Cerebras

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cerebras API client
client = Cerebras(
    api_key="csk-6f2yk2ytvkexfwnnchrxr6vyd8j2jmcetykmwd92xe3dcde9",
)

# Paths
UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Mediapipe Face Mesh module
mp_face_mesh = mp.solutions.face_mesh

# Helper function to save the uploaded file
def save_uploaded_file(uploaded_file: UploadFile, folder: str):
    file_path = os.path.join(folder, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return file_path

# Extract skin color from chin and nose using Mediapipe Face Mesh
def extract_chin_nose_skin_color(image_path: str):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize Mediapipe Face Mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            raise HTTPException(status_code=400, detail="No face detected")

        # Get the first detected face landmarks
        face_landmarks = results.multi_face_landmarks[0]

        # Define landmarks for the chin and nose
        chin_landmarks = [152, 377, 378, 379, 365]  # Chin points
        nose_landmarks = [1, 2, 3, 4, 5]  # Nose points

        chin_pixels = []
        nose_pixels = []

        ih, iw, _ = image.shape

        # Collect pixels for chin landmarks
        for landmark_idx in chin_landmarks:
            x = int(face_landmarks.landmark[landmark_idx].x * iw)
            y = int(face_landmarks.landmark[landmark_idx].y * ih)
            chin_pixels.append(image_rgb[y, x])

        # Collect pixels for nose landmarks
        for landmark_idx in nose_landmarks:
            x = int(face_landmarks.landmark[landmark_idx].x * iw)
            y = int(face_landmarks.landmark[landmark_idx].y * ih)
            nose_pixels.append(image_rgb[y, x])

        # Combine chin and nose pixels
        all_pixels = np.array(chin_pixels + nose_pixels)

        # Calculate the average skin tone color from these pixels
        avg_color = np.mean(all_pixels, axis=0)
        avg_color_int = tuple(map(int, avg_color))

        return avg_color_int

# Use Cerebras API to get season and color palette recommendation
def get_color_recommendation(skin_tone_rgb):
    rgb_string = f"rgb({skin_tone_rgb[0]}, {skin_tone_rgb[1]}, {skin_tone_rgb[2]})"

    prompt = f"dont write code or any other explanation, just output the color recommendation. Given the RGB values of a person's skin tone ({rgb_string}), generate a season color (one word: autumn, summer, winter, spring) and six corresponding color codes (HEX) that best match their skin tone based on color theory. Output format should strictly only be: 'Season: <season> Colors: <color1>, <color2>, <color3>, <color4>, <color5>, <color6>'."

    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="llama3.1-8b"
    )
    return chat_completion.choices[0].message.content

# Function to parse season and colors from Cerebras response
def parse_color_recommendation(response_text):
    # Expected format: 'Season: <season> Colors: <color1>, <color2>, <color3>, <color4>, <color5>, <color6>'
    try:
        season_part, colors_part = response_text.split('Colors: ')
        season = season_part.replace('Season: ', '').strip()
        colors = [color.strip() for color in colors_part.split(',')]
        return season, colors
    except Exception as e:
        raise ValueError("Error parsing the color recommendation response: " + str(e))

# API endpoint for uploading a photo and suggesting outfits
@app.post("/upload")
async def upload_and_suggest(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = save_uploaded_file(file, UPLOAD_FOLDER)

    try:
        # Extract skin tone color from chin and nose using Mediapipe
        skin_tone_color = extract_chin_nose_skin_color(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Use Cerebras API to get season and color palette
    color_recommendation = get_color_recommendation(skin_tone_color)

    try:
        season, colors = parse_color_recommendation(color_recommendation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "message": "Color recommendation generated",
        "color_recommendation": colors,
        "season": season,
        "skinTone": f"rgb({skin_tone_color[0]}, {skin_tone_color[1]}, {skin_tone_color[2]})"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
