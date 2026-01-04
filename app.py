import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io
import datetime

class Vision:
  def __init__(self, model):
    self.model = model

  def scan_pantry(self, images):
    prompt = [
    "You are an expert pantry organizer with a sharp eye for food items.",
    "Carefully examine the provided images.",
    "List every distinct edible ingredient you see, using common everyday names.",
    "If you can estimate quantity or type (e.g., '3 red apples', 'half loaf of sourdough bread'), include it.",
    "Return ONLY a clean comma-separated list. Example: 'chicken thighs, cherry tomatoes, red onion, basil, cheddar cheese, eggs'.",
    "Ignore non-food items completely."
  ]
    prompt.extend(images)

    try:
      response = self.model.generate_content(prompt)
      return response.text.strip()
    except Exception as e:
      return f"Error: {e}"

class RecipeGenerator:
  def __init__(self, model):
    self.model = model

  def invent_recipe(self, ingredients, style, dietary, hero_img=None):
    instruction = f"""
    You are a warm, passionate home cook who loves turning whatever is in the pantry into something delicious and memorable. 
    Your recipes feel like they're shared over a kitchen counter—clear, encouraging, and full of little touches that make people excited to cook.

    Create an original, practical recipe based on these constraints:
    - Available ingredients: {ingredients}
    - Cuisine style/request: {style}
    - Dietary needs: {dietary}

    Guidelines:
    - Use as many of the available ingredients as possible.
    - Feel free to suggest 1–2 common pantry staples (salt, pepper, olive oil, garlic, butter, flour, sugar, etc.) only if truly needed.
    - Design the recipe for 4 servings (adjust if the ingredient list clearly suggests otherwise).
    - Include realistic approximate quantities in the ingredients list.
    - Write steps that are easy to follow, even for beginner cooks. Include approximate timings when helpful.
    - Give the dish a creative but approachable name that makes someone want to cook it right away.

    If a hero image is provided, take inspiration from its plating style, colors, and texture.

    Output exactly in this Markdown format (do not add extra text outside it):

    # [Creative Dish Name]

    **Serves:** 4 | **Prep Time:** XX minutes | **Cook Time:** XX minutes | **Total Time:** XX minutes | **Difficulty:** Easy / Medium / Hard

    ## Why You'll Love This
    A warm, appetizing 2–4 sentence story about the dish—its flavors, textures, why it's perfect for tonight, and what makes it special.

    ## Ingredients
    - [approximate quantity] [ingredient] (e.g., 400g chicken thighs, boneless)
    - [any suggested pantry staples marked as "(pantry staple, optional if you have it)"]

    ## Step-by-Step Instructions
    1. [Clear, friendly step with action verbs and helpful details]
    2. ...

    ## Pro Tip
    One genuine, useful tip—could be about flavor, technique, plating, or a simple variation.
    """

    content = [instruction]

    if hero_img:
      content.append("Reference Image (try to mimic it):")
      content.append(hero_img)
    response = self.model.generate_content(content)
    return response.text

class NutritionistAI:
  def __init__(self, model):
    self.model = model
  def analyze_health(self, recipe_text):
    prompt = f"""
    Act as a clinical nutritionist.
    Analyze this recipe text:
    '{recipe_text}'

    Provide a concise health breakdown in this specific format:
    Calories: [Approximation Number]
    Protein: [High/Medium/Low]
    Carbs: [High/Medium/Low]
    Health Verdict: [One Sentence Summary]
    """
    response = self.model.generate_content(prompt)
    return response.text

class Drink:
  def __init__(self, model):
    self.model = model
  def suggest_pairing(self, recipe_text):
    prompt = f"""
    You are a friendly beverage expert who helps people find the perfect everyday drink to enjoy with their meal—alcoholic or non-alcoholic, whatever complements the food best and is easy to find.

    Here is the full recipe:
    '{recipe_text}'

    Based on the flavors, ingredients, and likely regional style of the dish, recommend **ONE** beverage pairing that:
    - Feels natural to the cuisine or region (infer the country/region from ingredients and style).
    - Is widely available in local supermarkets, convenience stores, or common in homes there.
    - Prioritizes refreshing non-alcoholic options (soft drinks, juices, teas, sparkling water, lassi, horchata, etc.) unless an alcoholic drink is truly iconic and widely drunk with this dish.

    Output exactly in this format (nothing else):

    **Perfect Pairing: [Beverage Name]**

   [2–3 warm sentences explaining why it works so well with the dish's flavors and why it's easy to find locally.]
   """

    response = self.model.generate_content(prompt)
    return response.text

import markdown
from xhtml2pdf import pisa
from io import BytesIO

class PDFRec:
    def create_pdf(self, recipe_text):
        html_content = markdown.markdown(recipe_text, extensions=['extra'])
        full_html = f"""
        <html>
        <head>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: Helvetica, sans-serif;
                    font-size: 12pt;
                    line-height: 1.5;
                    color: #333333;
                }}
                h1 {{ color: #2E86C1; font-size: 24pt; border-bottom: 2px solid #2E86C1; padding-bottom: 5px; }}
                h2 {{ color: #2874A6; font-size: 18pt; margin-top: 20px; }}
                h3 {{ color: #1B4F72; font-size: 14pt; }}
                ul {{ margin-bottom: 15px; }}
                li {{ margin-bottom: 5px; }}
                strong {{ color: #000000; font-weight: bold; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        # PDF

        pdf_output = BytesIO()
        pisa_status = pisa.CreatePDF(
            src=full_html,
            dest=pdf_output
        )
        if pisa_status.err:
            return b"Error generating PDF"
        
        return pdf_output.getvalue()

class PantryApp:
  def __init__(self):
    st.set_page_config(page_title="Empty Fridge", layout="wide", page_icon="🍋")
    self.apply_theme()

    if 'history' not in st.session_state:
      st.session_state['history'] = []
    if 'generated_recipe' not in st.session_state:
      st.session_state['generated_recipe'] = None

  def apply_theme(self):
    st.markdown("""
    <style>
    .main-header { 
        font-size: 3em; 
        font-weight: 800; 
        color: #FF4B4B !important; 
        margin-bottom: 20px;
    }
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    /* FIX: Hide menus to prevent layout cutting off in Colab */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

  def sidebar_config(self):
    with st.sidebar:
      st.markdown("## Settings") 
      api_key = st.text_input("Gemini API Key", type="password")
      st.divider()
      st.markdown("### Preferences")
      cuisine = st.text_input("Cuisine Style (e.g., Italian, Thai, Comfort Food)", "Any")
      diet = st.radio("Dietary Requirement", ["None", "Vegetarian", "Vegan", "Keto", "Gluten-Free"])
      st.divider()
      st.info("System Ready.")
      return api_key, cuisine, diet

  def main_interface(self, api_key, cuisine, diet):
    st.markdown("<div class='main-header'>Empty Fridge</div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["The Kitchen", "History", "About"])

    with tab1:
      col1, col2 = st.columns([1, 1.5], gap="large")
      with col1:
        st.subheader("1. Scan Ingredients")
        uploaded_files = st.file_uploader("Upload Photos", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
        st.subheader("2. Inspiration (Optional)")
        hero_file = st.file_uploader("Upload Hero Dish Image", type=['jpg', 'png', 'jpeg'])

        if st.button("Generate Recipe..", type="primary", use_container_width=True):
          if not api_key:
            st.error("API Key Missing")
          elif not uploaded_files:
            st.warning("Please Upload Ingredients Photos")
          else:
            self.run_pipeline(api_key, uploaded_files, hero_file, cuisine, diet)

      with col2:
        if st.session_state['generated_recipe']:
          self.display_results()
        else:
          st.markdown("""
          <div style='padding: 50px; text-align: center; border: 2px dashed #444; border-radius: 10px; color: #888;'>
            <h3>Upload something...</h3>
            <p>Upload ingredients to start the pipeline.</p>
          </div>
          """, unsafe_allow_html=True)
    
    with tab2:
      st.subheader("Your Session History")
      for i, item in enumerate(st.session_state['history']):
        with st.expander(f"Recipe {i+1}: {item['title']}"):
          st.markdown(item['content'])

    with tab3:
      st.markdown("### AI Agent: Gemini Flash")

  def run_pipeline(self, api_key, files, hero_file, cuisine, diet):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
    v, r, n, s = Vision(model), RecipeGenerator(model), NutritionistAI(model), Drink(model)

    images = [Image.open(f) for f in files]
    hero = Image.open(hero_file) if hero_file else None

    with st.status("AI Agents Working...", expanded=True) as status:
      st.write("Scanning...")
      ingredients = v.scan_pantry(images)
      st.write("Drafting...")
      recipe = r.invent_recipe(ingredients, cuisine, diet, hero)
      st.write("Analyzing...")
      health = n.analyze_health(recipe)
      st.write("Pairing...")
      drink = s.suggest_pairing(recipe)
      status.update(label="Success!", state="complete", expanded=False)

    res = {"title": f"{cuisine} ({datetime.datetime.now().strftime('%H:%M')})", "ingredients": ingredients, "recipe": recipe, "health": health, "drink": drink}
    st.session_state['generated_recipe'] = res
    st.session_state['history'].append({"title": res['title'], "content": recipe})
    st.rerun()

  def display_results(self):
    data = st.session_state['generated_recipe']
    st.success(f"**Ingredients Detected:** {data['ingredients']}")
    st.markdown(data['recipe'])
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.info(f"**Nutrition:**\n\n{data['health']}")
    with c2: st.warning(f"**Drink:**\n\n{data['drink']}")
    
    publisher = PDFRec()
    try:
      pdf_out = publisher.create_pdf(data['recipe'])
      st.download_button("Download PDF", data=bytes(pdf_out), file_name="recipe.pdf", mime="application/pdf")
    except:
      st.warning("PDF could not be generated due to character encoding.")

if __name__ == "__main__":
  app= PantryApp()
  key, cuisine, diet = app.sidebar_config()
  app.main_interface(key, cuisine, diet)
