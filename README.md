# Empty Fridge

Empty Fridge is a Streamlit application powered by Google's Gemini models that looks at photos of your ingredients (no matter how scarce and messy) and hallucinates (in a good way) a legitimate recipe you can actually cook.

## Features

- **AI Vision Chef:** Upload a photo of your messy pantry or fridge shelf. The app identifies the ingredients for you (so you don't have to type them out).

- **Creative Recipe Generation:** Uses the ingredients you have + your cravings (e.g., "Comfort Food", "Thai") to get a structured, easy-to-follow recipe.

- **Nutritionist Mode:** An AI agent analyzes the generated recipe to give you a rough health breakdown (Calories, Protein, Carbs).

- **Barista:** Suggests the perfect beverage pairing (alcoholic or non-alcoholic) based on the flavor profile of the dish.

- **PDF Export:** Generates a clean, downloadable PDF of the recipe so you can save it for later.

## Tech Stack

- **Python** (backend)

- **Streamlit** (frontend)

- **Google Gemini API** (Specifically `gemini-2.5-flash-lite` for speed and vision capabilities)

- **xhtml2pdf** (For generating the PDF reports)

## How to Run It

### Option 1: Google Colab (Easy Way)

If you don't want to mess with local environments, I included a Jupyter Notebook (`Empty Fridge.ipynb`) that handles everything.

1. Open the notebook in Colab.

2. Add your **Gemini API Key** when prompted in the app sidebar.

3. The notebook uses `ngrok` to tunnel the Streamlit app so you can view it in your browser.

### Option 2: Running Locally

1. Clone the repo.

2. Install requirements:
   
   ```
   pip install -q -U google-generativeai streamlit fpdf2 Pillow xhtml2pdf
   ```

3. Run the app:
   
   ```
   streamlit run app.py
   ```
