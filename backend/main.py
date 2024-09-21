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

# Helper function to calculate the histogram similarity between two images
def calculate_histogram_similarity(image1_path, image2_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert images to HSV color space
    hsv_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

    # Calculate the histogram for each image
    hist_image1 = cv2.calcHist([hsv_image1], [0, 1, 2], None, [50, 60, 50], [0, 180, 0, 256, 0, 256])
    hist_image2 = cv2.calcHist([hsv_image2], [0, 1, 2], None, [50, 60, 50], [0, 180, 0, 256, 0, 256])

    # Normalize the histograms
    cv2.normalize(hist_image1, hist_image1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist_image2, hist_image2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    # Compare the histograms using correlation
    similarity = cv2.compareHist(hist_image1, hist_image2, cv2.HISTCMP_CORREL)

    return similarity

# Define the find_closest_reference function
def find_closest_reference(uploaded_image_path):
    best_match = None
    best_similarity = -1  # Start with a very low similarity score
    
    # Iterate over all reference images in the REFERENCE_FOLDER
    for reference_image_name in os.listdir(REFERENCE_FOLDER):
        reference_image_path = os.path.join(REFERENCE_FOLDER, reference_image_name)
        
        # Calculate the similarity between the uploaded image and the reference image
        similarity = calculate_histogram_similarity(uploaded_image_path, reference_image_path)
        
        # If this image is a better match, update best_match and best_similarity
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = reference_image_name
    
    return best_match

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
    # suggested_products = PRODUCTS.get(closest_reference, [])

    # Extract dominant skin tone color (reusing analyze_skin_tone logic)
    face_colors, _ = extract_colors_from_face_and_eyes(file_path, num_clusters=5)
    skin_tone_color = face_colors[np.argmax(face_colors.sum(axis=1))]
    skin_tone_color = f"rgb({skin_tone_color[0]}, {skin_tone_color[1]}, {skin_tone_color[2]})"

    return {
        "message": f"Closest match: {closest_reference}",
        "products": "Hello",
        "skinTone": skin_tone_color
    }

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