from fastapi.testclient import TestClient
from main import app 
import os

client = TestClient(app)

# Test the /analyze_skin_tone endpoint with added debugging
def test_analyze_skin_tone():
    # Print the current path for debugging
    print("Current directory:", os.getcwd())
    image_path = "uploads/{img}.jpeg"  # Make sure this image exists in the folder
    
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        return
    
    with open(image_path, "rb") as image_file:
        response = client.post(
            "/analyze_skin_tone", 
            files={"file": image_file}
        )
    
    # Debug: Print the status code and response content
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content.decode()}")
    
    # Assert that the status code is 200
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    data = response.json()
    print(data)
    assert "skin_tone_color" in data

# Run the tests
test_analyze_skin_tone()
