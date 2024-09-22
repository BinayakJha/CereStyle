
# **MatchIt: Fashion with Confidence** ![Logo](./frontend/src/images/logo.png)

Welcome to **MatchIt**, an AI-powered fashion recommendation system that helps users discover outfits that enhance their natural features. By analyzing hair, skin, and eye color from uploaded photos, MatchIt compares these with reference images and suggests products worn by similar individuals. Whether you're looking for casual or professional attire, MatchIt offers personalized suggestions to help you feel confident in every setting.

---

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Requirements](#requirements)
3. [Backend Setup (FastAPI)](#backend-setup-fastapi)
   - [Step 1: Create a Virtual Environment](#step-1-create-a-virtual-environment-optional-but-recommended)
   - [Step 2: Install Backend Dependencies](#step-2-install-backend-dependencies)
   - [Step 3: Run the FastAPI Backend](#step-3-run-the-fastapi-backend)
4. [Frontend Setup (React)](#frontend-setup-react)
   - [Step 1: Install Frontend Dependencies](#step-1-install-frontend-dependencies)
   - [Step 2: Start the React Frontend](#step-2-start-the-react-frontend)
5. [How to Use the Project](#how-to-use-the-project)
6. [Project Directory Structure](#project-directory-structure)
7. [Key Commands](#key-commands)
8. [Contributors](#contributors)

---

## **Project Overview**

MatchIt is designed to solve the common struggle of finding clothing that perfectly matches individual features. With the power of color theory and AI, this platform provides fashion suggestions that complement users' natural attributes, helping them feel more confident in their fashion choices. By integrating advanced image processing and real-time product suggestions, MatchIt brings a personalized shopping experience to your fingertips.

---

## **Requirements**

Before setting up the project, ensure you have the following installed on your system:

- **Python 3.8+** (for the FastAPI backend)
- **Node.js** (for the React frontend)
- **pip** (Python package manager)

---

## **Backend Setup (FastAPI)**

The backend is built using **FastAPI** and handles tasks like file uploads, image analysis, and product recommendations.

### **Step 1: Create a Virtual Environment (Optional but Recommended)**

Creating a virtual environment ensures that the project dependencies are isolated from the global Python environment.

For **Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

For **macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Step 2: Install Backend Dependencies**

After activating the virtual environment, install the required packages for the backend:

```bash
pip install fastapi uvicorn python-multipart Pillow scikit-learn
```

### **Step 3: Run the FastAPI Backend**

Navigate to the `backend/` folder and start the FastAPI server:

```bash
cd backend
uvicorn main:app --reload
```

The backend will now be running at `http://127.0.0.1:8000`.

---

## **Frontend Setup (React)**

The frontend is built using **React**, offering an intuitive interface for uploading images and receiving fashion suggestions.

### **Step 1: Install Frontend Dependencies**

Navigate to the `react-frontend/` folder and install the required dependencies:

```bash
cd react-frontend
npm install
```

This command installs all necessary packages listed in the `package.json` file.

### **Step 2: Start the React Frontend**

Once dependencies are installed, start the React development server:

```bash
npm start
```

The React frontend will be accessible at `http://localhost:3000`.

---

## **How to Use the Project**

1. **Open the React App**:
   - Navigate to `http://localhost:3000` in your browser.
   
2. **Upload a Photo**:
   - Use the file upload form on the main page to upload a photo of yourself.
   - Click "Upload" to submit the photo for analysis.

3. **Get Recommendations**:
   - The backend will analyze the uploaded photo and suggest products based on the closest matching reference image.

---

## **Project Directory Structure**

Here’s an overview of the key folders and files in the project:

```
project_root/
│
├── backend/                      # Backend code (FastAPI)
│   ├── __pycache__/              # Python cache files
│   ├── main.py                   # Main FastAPI app
│   └── reference_images/         # Folder containing reference images for comparison
│
├── react-frontend/               # Frontend code (React)
│   ├── node_modules/             # Node.js modules
│   ├── public/                   # Public assets for React
│   ├── src/                      # React source code
│   ├── package.json              # Frontend dependencies list
│   ├── package-lock.json         # Lockfile for dependencies
│   └── README.md                 # Frontend README file
│
└── README.md                     # Main project README
```

---

## **Key Commands**

### **Backend Commands**:

- **Install Backend Dependencies**:
  ```bash
  pip install fastapi uvicorn python-multipart Pillow scikit-learn
  ```

- **Run the Backend Server**:
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

## **Contributors**

This project was created by a team of passionate developers:

- **[maheessh](https://github.com/maheessh)**
- **[BinayakJha](https://github.com/BinayakJha)**
- **[sujalshah0444](https://github.com/sujalshah0444)**

We hope you enjoy using **MatchIt** as much as we enjoyed building it!
