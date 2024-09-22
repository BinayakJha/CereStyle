
# **CereStyle: Fashion with Confidence**


<p align="center">
  <img src="./frontend/src/images/logo.png" alt="Logo" width="200">
</p>

Welcome to **CereStyle**, an AI-powered fashion recommendation system that helps users discover outfits that enhance their natural features. By analyzing hair, skin, and eye color from uploaded photos, CereStyle compares these with reference images and suggests products worn by similar individuals. Whether you're looking for casual or professional attire, CereStyle offers personalized suggestions to help you feel confident in every setting.

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
8. [Tech Stack](#tech-stack)
9. [Contributors](#contributors)

---

## **Project Overview**

CereStyle is designed to solve the common struggle of finding clothing that perfectly matches individual features. By blending color theory and AI, this platform provides fashion suggestions that complement users' natural attributes, helping them feel more confident and positively impacting their mental health and confidence. CereStyle brings a personalized shopping experience to your fingertips with advanced image processing and real-time product recommendations.

---

## **Requirements**

Before setting up the project, ensure you have the following installed on your system:

- **Python 3.8+** (for the FastAPI backend)
- **Node.js** (for the React frontend)
- **pip** (Python package manager)

---

## **Backend Setup (FastAPI)**

The backend uses **FastAPI** to handle tasks like file uploads, image analysis, and product recommendations.

### **Step 1: Create a Virtual Environment (Optional but Recommended)**

Creating a virtual environment ensures that the project dependencies are isolated from your global Python environment.

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

After activating the virtual environment, install the necessary packages:

```bash
pip install fastapi uvicorn python-multipart Pillow scikit-learn
```

### **Step 3: Run the FastAPI Backend**

Navigate to the `backend/` folder and start the FastAPI server:

```bash
cd backend
uvicorn main:app --reload
```

The backend should now be running at `http://127.0.0.1:8000`.

---

## **Frontend Setup (React)**

The frontend is built using **React** and provides an intuitive interface for uploading images and receiving fashion suggestions.

### **Step 1: Install Frontend Dependencies**

Navigate to the `react-frontend/` folder and install the required dependencies:

```bash
cd react-frontend
npm install
```

### **Step 2: Start the React Frontend**

Once the dependencies are installed, start the development server:

```bash
npm start
```

The frontend should now be running at `http://localhost:3000`.

---

## **How to Use the Project**

1. **Open the React App**:
   - Open your browser and navigate to `http://localhost:3000`.

2. **Upload a Photo**:
   - Use the upload form on the main page to submit a photo of yourself.

3. **Get Recommendations**:
   - The backend analyzes the uploaded photo and suggests products based on the closest matching reference image.

---

## **Project Directory Structure**

Here's an overview of the project's directory structure:

```
project_root/
│
├── backend/                      # Backend code (FastAPI)
│   ├── __pycache__/              # Python cache files
│   ├── main.py                   # Main FastAPI app
│   └── reference_images/         # Reference images for comparison
│
├── react-frontend/               # Frontend code (React)
│   ├── node_modules/             # Node.js modules
│   ├── public/                   # Public assets for React
│   ├── src/                      # React source code
│   ├── package.json              # Frontend dependencies list
│   ├── package-lock.json         # Lockfile for dependencies
│   └── README.md                 # Frontend README
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

## **Tech Stack**

CereStyle is built with modern technologies to ensure efficiency, scalability, and an exceptional user experience. Here’s a breakdown of the tools and frameworks used:

### **Frontend**

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

- **React**: JavaScript library for building user interfaces.
- **JavaScript**: Primary programming language for client-side scripting.
- **HTML5**: For structuring web content.
- **CSS3**: For styling web components.

### **Backend**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-000000?style=for-the-badge&logo=uvicorn&logoColor=white)

- **FastAPI**: Fast web framework for building APIs in Python.
- **Python**: Backend processing, including image analysis.
- **Flask**: Lightweight framework for rapid prototyping.
- **Uvicorn**: ASGI server for running FastAPI applications.

### **AI/ML Processing**

![Cerebras](https://img.shields.io/badge/Cerebras-AI%20Processing-blue?style=for-the-badge)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-green?style=for-the-badge)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-FA7302?style=for-the-badge&logo=scikit-learn&logoColor=white)

- **Cerebras API**: AI-powered image analysis for skin tone, hair, and eye color detection.
- **Pillow**: Image processing library.
- **Scikit-learn**: Machine learning library for color matching and recommendations.

### **Version Control & CI/CD**

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

- **Git**: Version control system.
- **GitHub**: Code hosting platform for collaboration.

### **APIs**

![SerpAPI](https://img.shields.io/badge/SerpAPI-Google%20Search%20API-yellowgreen?style=for-the-badge)
![Pexels API](https://img.shields.io/badge/Pexels%20API-Image%20Sourcing-green?style=for-the-badge)

- **SerpAPI**: Real-time product recommendations.
- **Pexels API**: Image sourcing for fashion items.

### **Other Tools**

- **VS Code**: Code editor.


---

## **Contributors**

This project was created by a team of passionate developers:

- **[maheessh](https://github.com/maheessh)**
- **[BinayakJha](https://github.com/BinayakJha)**
- **[sujalshah0444](https://github.com/sujalshah0444)**

We hope you enjoy using **CereStyle** as much as we enjoyed building it!
```

