# Emprty Fridge: AI Pantry Assistant

This project is a computer vision and LLM-based application that identifies food ingredients from images and generates custom recipes. It uses Google Gemini for image analysis and content generation, with a Streamlit interface for the frontend.

## Features
* **Ingredient Detection:** Scans uploaded images to identify available food items using Gemini Vision.
* **Recipe Generation:** Creates recipes based on detected ingredients, user-selected cuisine, and dietary restrictions.
* **Analysis:** Provides estimated nutritional data and beverage pairing suggestions.
* **PDF Export:** Converts the generated recipe into a downloadable PDF format.

## Tech Stack
* **Python**
* **Streamlit** (Web UI)
* **Google Generative AI** (Gemini 2.5 Flash)
* **FPDF2 / xhtml2pdf** (PDF Generation)
* **pyngrok** (Tunneling for Colab)

## Setup & Usage

1.  **Open in Google Colab:**
    Upload the notebook (`.ipynb`) to Google Colab.

2.  **Dependencies:**
    Run the first cell to install required libraries (`google-generativeai`, `streamlit`, `fpdf2`, `pyngrok`).

3.  **API Configuration:**
    * A valid **Google Gemini API Key** is required in the app sidebar.
    * If running via tunnel, an **Ngrok Authtoken** must be provided in the launch cell.

4.  **Run the App:**
    Execute the final cell to start the Streamlit server and generate the public URL. Enter your preferences in the sidebar to start scanning.