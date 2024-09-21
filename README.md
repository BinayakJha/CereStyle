
---

# **Fashion Recommendation System**

This project is a fashion recommendation system where users upload photos, and the system automatically compares the hair, skin, and eye color of the uploaded photo with pre-stored reference photos. Based on the closest match, the system suggests products that were used by the person in the reference photo.

---

## **Table of Contents**

1. [Requirements](#requirements)
2. [Backend Setup (FastAPI)](#1-setting-up-the-backend-fastapi)
   - [Step 1: Create a Virtual Environment](#step-1-create-a-virtual-environment-optional-but-recommended)
   - [Step 2: Install Backend Dependencies](#step-2-install-backend-dependencies)
   - [Step 3: Run the FastAPI Backend](#step-3-run-the-fastapi-backend)
3. [Frontend Setup (React)](#2-setting-up-the-frontend-react)
   - [Step 1: Install Frontend Dependencies](#step-1-install-frontend-dependencies)
   - [Step 2: Start the React Frontend](#step-2-start-the-react-frontend)
4. [How to Use the Project](#3-how-to-use-the-project)
5. [Project Directory Structure](#project-directory-structure)
6. [Key Commands](#4-key-commands)
7. [Additional Tips](#5-additional-tips)

---

## **Requirements**

Before getting started, ensure you have the following installed:

1. **Python 3.8+** (for the FastAPI backend)
2. **Node.js** (for the React frontend)
3. **pip** (Python package manager)

---

## **1. Setting Up the Backend (FastAPI)**

The backend uses **FastAPI** to handle file uploads, image processing, and comparison with pre-uploaded reference images.

### **Step 1: Create a Virtual Environment (Optional but Recommended)**

A virtual environment keeps your project dependencies isolated from your global Python installation.

**For Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Step 2: Install Backend Dependencies**

After activating the virtual environment, install the necessary packages for the backend.

```bash
pip install fastapi uvicorn python-multipart Pillow scikit-learn
```

### **Step 3: Run the FastAPI Backend**

Navigate to the `backend/` folder (where the `main.py` file is located) and run the FastAPI server using Uvicorn:

```bash
cd backend
uvicorn main:app --reload
```

The backend should now be running at `http://127.0.0.1:8000`.

---

## **2. Setting Up the Frontend (React)**

The frontend is built with **React** and allows users to upload images, which are then sent to the backend for processing.

### **Step 1: Install Frontend Dependencies**

Navigate to the `react-frontend/` folder and install the required dependencies:

```bash
cd react-frontend
npm install
```

This will install all the required packages as listed in the `package.json` file.

### **Step 2: Start the React Frontend**

Once the dependencies are installed, start the development server:

```bash
npm start
```

The React app should now be running at `http://localhost:3000`.

---

## **3. How to Use the Project**

1. **Access the React Frontend**:
   - Open your browser and go to `http://localhost:3000`.
   
2. **Upload an Image**:
   - On the main page, use the file upload form to upload an image.
   - Click "Upload" to submit the image.

3. **Receive Suggestions**:
   - After uploading, the backend will process the image and compare it with pre-existing reference images.
   - You will receive product recommendations based on the closest matching reference image.

---

## **Project Directory Structure**

Here is a general overview of the project structure:

```
project_root/
│
├── backend/                      # FastAPI backend folder
│   ├── __pycache__/              # Python cache files
│   ├── main.py                   # Main FastAPI app
│   └── reference_images/         # Reference images for comparison
│
├── react-frontend/               # React frontend folder
│   ├── node_modules/             # Node.js modules
│   ├── public/                   # Public assets for React
│   ├── src/                      # Source code for React frontend
│   ├── package.json              # Frontend dependencies
│   ├── package-lock.json         # Lockfile for dependencies
│   └── README.md                 # Frontend readme
│
└── README.md                     # Overall project readme
```

---

## **4. Key Commands**

### **Backend Commands**:
- **Install Backend Dependencies**:
  ```bash
  pip install fastapi uvicorn python-multipart Pillow scikit-learn
  ```

- **Run the Backend**:
  ```bash
  uvicorn main:app --reload
  ```

### **Frontend Commands**:
- **Install Frontend Dependencies**:
  ```bash
  npm install
  ```

- **Run the Frontend**:
  ```bash
  npm start
  ```

---

## **5. Additional Tips**

- **Backend**: If you add new Python libraries in the future, make sure to update the backend's `requirements.txt` using:
  ```bash
  pip freeze > requirements.txt
  ```

- **Frontend**: If you encounter any issues with the frontend dependencies, try deleting the `node_modules/` folder and `package-lock.json` file, then run `npm install` again.

---

This guide should help anyone get the project up and running smoothly. Let me know if you need additional clarifications!

--- 

### **How to Add This README to GitHub:**

1. Add this file (`README.md`) to the root of your project directory.
2. If your project is not already on GitHub, follow these steps:
   - Initialize a Git repository:
     ```bash
     git init
     ```
   - Add files and commit:
     ```bash
     git add .
     git commit -m "Initial commit with README"
     ```
   - Push to GitHub:
     ```bash
     git remote add origin <your-repo-url>
     git push -u origin master
     ```

3. If your project is already on GitHub, simply commit and push the `README.md` file:
   ```bash
   git add README.md
   git commit -m "Add project README"
   git push
   ```

This will display the `README.md` file on your project's GitHub page!

Let me know if you need any further adjustments!