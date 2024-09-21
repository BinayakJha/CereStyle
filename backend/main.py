from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import numpy as np
from PIL import Image
import cv2
from sklearn.cluster import KMeans

app = FastAPI()

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

# Brightness adjustment using histogram equalization
def adjust_brightness(eye_region):
    eye_gray = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(eye_gray)
    return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

# Helper function to extract dominant colors using K-Means Clustering
def extract_colors_from_face_and_eyes(image_path: str, num_clusters=5):
    image = Image.open(image_path).convert('RGB')
    image_np = np.array(image)

    # Convert to OpenCV format (BGR)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Load the pre-trained Haar Cascades for face and eye detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Convert to grayscale for face and eye detection
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        raise HTTPException(status_code=404, detail="No face detected in the image")

    # Extract the first detected face
    x, y, w, h = faces[0]
    face_roi = image_np[y:y+h, x:x+w]  # Region of Interest (ROI) for the face

    # Resize the face region for faster computation and flatten the pixels
    face_roi_resized = cv2.resize(face_roi, (100, 100))
    face_pixels = face_roi_resized.reshape(-1, 3)

    # Apply K-Means clustering to find dominant colors in the face region
    kmeans_face = KMeans(n_clusters=num_clusters)
    kmeans_face.fit(face_pixels)
    face_colors = kmeans_face.cluster_centers_.astype(int)

    # Detect eyes within the face ROI
    face_gray = gray_image[y:y+h, x:x+w]
    face_color = image_cv[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))

    if len(eyes) == 0:
        raise HTTPException(status_code=404, detail="No eyes detected in the image")

    # Extract the first detected eye region and focus on the iris
    eye_x, eye_y, eye_w, eye_h = eyes[0]
    eye_roi = face_color[eye_y:eye_y+eye_h, eye_x:eye_x+eye_w]

    # Focus on the central portion (likely iris) of the detected eye region
    iris_radius = min(eye_w, eye_h) // 4
    center_x, center_y = eye_w // 2, eye_h // 2
    iris_roi = eye_roi[center_y - iris_radius:center_y + iris_radius, center_x - iris_radius:center_x + iris_radius]

    # Adjust brightness and apply Gaussian blur to the iris region
    adjusted_iris = adjust_brightness(iris_roi)
    blurred_iris = cv2.GaussianBlur(adjusted_iris, (7, 7), 0)

    # Flatten the iris pixels and apply K-Means clustering
    iris_pixels = blurred_iris.reshape(-1, 3)
    kmeans_iris = KMeans(n_clusters=5)  # Use more clusters for finer details
    kmeans_iris.fit(iris_pixels)
    eye_colors = kmeans_iris.cluster_centers_.astype(int)

    return face_colors, eye_colors

# New API endpoint to analyze skin tone and eye color
@app.post("/analyze_skin_tone")
async def analyze_skin_tone(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = save_uploaded_file(file, UPLOAD_FOLDER)
    
    # Extract dominant colors from the face and eyes in the image
    face_colors, eye_colors = extract_colors_from_face_and_eyes(file_path, num_clusters=5)

    # Get the dominant skin tone color
    skin_tone_color = face_colors[np.argmax(face_colors.sum(axis=1))]
    skin_tone_color = f"rgb({skin_tone_color[0]}, {skin_tone_color[1]}, {skin_tone_color[2]})"

    # Get the dominant eye color
    eye_color = eye_colors[np.argmax(eye_colors.sum(axis=0))]
    eye_color = f"rgb({eye_color[0]}, {eye_color[1]}, {eye_color[2]})"

    return {"message": "Skin tone and eye color detected", "skin_tone_color": skin_tone_color, "eye_color": eye_color}

# API endpoint for uploading a photo and suggesting products
@app.post("/upload")
async def upload_and_suggest(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = save_uploaded_file(file, UPLOAD_FOLDER)
    
    # Find the closest matching reference image
    closest_reference = find_closest_reference(file_path)

    # Suggest products based on the closest reference
    if closest_reference:
        suggested_products = PRODUCTS.get(closest_reference, [])
        return {"message": f"Closest match: {closest_reference}", "products": suggested_products}
    else:
        return {"message": "No match found"}

# New API endpoint to get the path of an uploaded photo
@app.get("/get_photo_path/{filename}")
async def get_photo_path(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return {"photo_path": file_path}
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
