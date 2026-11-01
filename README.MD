# Video-Based Heart Rate Monitoring Using PPG and LLM

## 1. Project Overview

This project implements a video-based heart rate monitoring system using **Photoplethysmography (PPG) / Remote Photoplethysmography (rPPG)** techniques.

Users can upload a video through a web-based frontend. The backend processes the uploaded video, extracts PPG signals, estimates the user's heart rate (BPM), and sends the calculated results to a locally hosted Large Language Model (LLM) using Ollama.

The LLM analyzes the calculated heart rate and generates a human-readable interpretation.

## 2. Background – Photoplethysmography (PPG)

Photoplethysmography (PPG) is a non-invasive optical technique used to detect changes in blood volume within the microvascular tissue.

The technique works by shining visible or near-infrared light onto the skin and measuring the amount of light absorbed or reflected.

Since blood absorbs light differently from surrounding tissues, variations in blood volume caused by cardiac activity produce periodic changes in the reflected or transmitted light intensity.

**Remote Photoplethysmography (rPPG)** extends this concept by extracting physiological signals remotely, typically using a standard camera to capture subtle changes in skin color associated with blood circulation.

In this project, rPPG is used to extract a pulse signal from the uploaded video and estimate the heart rate.

## 3. System Architecture and Execution Flow

The application follows the workflow below:

1. **Video Upload:** The user uploads a video through the web frontend.
2. **Video Transmission:** The browser sends the uploaded video to the FastAPI backend.
3. **PPG Signal Extraction:** FastAPI processes the video and extracts the rPPG signal.
4. **Heart Rate Calculation:** The extracted PPG signal is processed to estimate heart rate in Beats Per Minute (BPM).
5. **LLM Integration:** The calculated heart rate is passed to the locally hosted LLM through Ollama.
6. **Health Interpretation:** The LLM generates a human-readable interpretation based on the calculated heart rate.
7. **Result Display:** The backend returns the interpretation to the frontend for display.

### High-Level Workflow

```text
        User
         |
         v
   Web Frontend
         |
         | Upload Video
         v
    FastAPI Backend
         |
         v
   Video Processing
         |
         v
   rPPG Signal Extraction
         |
         v
   Heart Rate Calculation
         |
         | Heart Rate (BPM)
         v
      Ollama LLM
         |
         v
  Health Interpretation
         |
         v
   Web Frontend
         |
         v
    Display Results
```

## 4. Technology Stack
Backend - Python, FastAPI 
LLM - Ollama
API Communication - REST API
Signal Processing - PPG/rPPG algorithms

## 5. Prerequisites

Ensure the following software is installed:

- Python 3.9 or above (or the version specified by the project dependencies).
- pip (Python package manager).
- Ollama.
- A compatible LLM model supported by your Ollama Modelfile.
- A modern web browser.

## 6. Installation and Setup

### Step 1: Clone or Download the Project

Download the project source code and navigate to the project root directory.

### Step 2: Install Python Dependencies

Run the following command from the project root directory:

```bash
pip install -r requirements.txt
```

This installs the Python dependencies required by the backend and signal-processing modules.

### Step 3: Configure the Ollama Model

Make sure Ollama is installed and running.

Create the custom model using the provided `Modelfile`:

```bash
ollama create mymodel -f Modelfile
```

Run the model:

```bash
ollama run mymodel
```

Ollama API endpoint:

```text
http://localhost:11434/api
```

The application uses this local Ollama service to generate heart rate interpretations.

**Note:** Keep the Ollama service running while executing the application.

## 7. Application Execution

The frontend and backend must be started separately.

### Step 1: Start the Frontend

Open a terminal and navigate to the frontend directory:

```bash
cd frontend
```

Start the Python HTTP server:

```bash
python -m http.server 5500
```

The frontend will be accessible at:

```text
http://localhost:5500
```

### Step 2: Start the Backend

Open a separate terminal and navigate to the project root directory.

Start the FastAPI application:

```bash
uvicorn backend.main:app --reload
```

The backend API will be accessible at:

```text
http://localhost:8000
```

FastAPI interactive API documentation:

```text
http://localhost:8000/docs
```

### Step 3: Verify Ollama

Ensure Ollama is accessible at:

```text
http://localhost:11434/api
```

Also verify that the custom model `mymodel` has been created successfully.

## 8. Accessing the Application

Once all three services are running:

| Service | URL |
|---|---|
| Frontend | http://localhost:5500 |
| FastAPI Backend | http://localhost:8000 |
| FastAPI Swagger Docs | http://localhost:8000/docs |
| Ollama API | http://localhost:11434/api |

### Application Workflow

1. Open the frontend in your browser.
2. Upload a supported video containing a clearly visible face.
3. Submit the video for processing.
4. The backend extracts the rPPG signal and estimates heart rate.
5. The calculated heart rate is passed to the LLM.
6. View the generated interpretation on the frontend.

## 9. Troubleshooting

| Issue | Suggested Resolution |
|---|---|
| Python dependency errors | Run `pip install -r requirements.txt` again. |
| Ollama connection refused | Ensure the Ollama service is running. |
| Model not found | Verify that `mymodel` was created successfully using the Modelfile. |
| Frontend cannot connect to backend | Ensure FastAPI is running on port 8000 and check frontend API configuration. |
| Video processing fails | Verify video format, quality, duration, and face visibility. |
| Invalid heart rate output | Check video quality and ensure sufficient frames are available for signal extraction. |

## 10. Important Notes and Limitations

- rPPG-based heart rate estimation depends on video quality, lighting conditions, camera stability, and visibility of the face.
- Motion, shadows, compression, and changes in illumination may affect signal extraction accuracy.
- The LLM interpretation is based on the estimated heart rate supplied by the backend.
- The generated interpretation is informational and should not be considered a medical diagnosis.
- Video-based heart rate estimation should not replace validated medical monitoring devices.

## 11. Project Execution Summary

Execute the following commands in separate terminals:

**Terminal 1 – Ollama**

```bash
ollama run mymodel
```

**Terminal 2 – Frontend**

```bash
cd frontend
python -m http.server 5500
```

**Terminal 3 – Backend**

```bash
uvicorn backend.main:app --reload
```

Open the application:

```text
http://localhost:5500
```

---

**End of README**
