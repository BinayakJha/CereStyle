from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import numpy as np
from PIL import Image
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
PRODUCTS = {
    "reference1.jpg": ["Shampoo A", "Sunscreen B", "Moisturizer C"],
    "reference2.jpg": ["Shampoo X", "Sunscreen Y", "Moisturizer Z"],
    # Add more products for each reference image
}

# Ensure the directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REFERENCE_FOLDER, exist_ok=True)

# Helper function to save the uploaded file
def save_uploaded_file(uploaded_file: UploadFile, folder: str):
    file_path = os.path.join(folder, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return file_path

# Helper function to extract dominant colors using K-Means Clustering
def extract_colors(image_path: str, num_clusters=3):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((100, 100))  # Resize image to reduce computation time
    pixels = np.array(image).reshape(-1, 3)

    # K-Means clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)

    return colors

# Helper function to calculate color distance (Euclidean distance)
def color_distance(c1, c2):
    return np.sqrt(np.sum((c1 - c2) ** 2))

# Function to find the closest matching reference image
def find_closest_reference(uploaded_image_path: str):
    uploaded_colors = extract_colors(uploaded_image_path)

    closest_image = None
    min_distance = float('inf')

    for ref_image in os.listdir(REFERENCE_FOLDER):
        ref_image_path = os.path.join(REFERENCE_FOLDER, ref_image)
        reference_colors = extract_colors(ref_image_path)

        # Compare each corresponding color (hair, skin, eyes)
        total_distance = 0
        for i in range(3):  # 3 clusters for hair, skin, and eyes
            total_distance += color_distance(uploaded_colors[i], reference_colors[i])

        if total_distance < min_distance:
            min_distance = total_distance
            closest_image = ref_image

    return closest_image

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
