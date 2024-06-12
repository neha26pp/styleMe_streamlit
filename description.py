import pathlib
import textwrap
import os 
import google.generativeai as genai
import dotenv

# my_api_key = st.secrets["api_keys"]['GOOGLE_API_KEY']
my_api_key = "AIzaSyAIO4KL1gDpl5OcPSzMj7O-lnHws-zdO_g"
genai.configure(api_key="AIzaSyAIO4KL1gDpl5OcPSzMj7O-lnHws-zdO_g")

model = genai.GenerativeModel('gemini-pro-vision')

def generate_description(img):
    response = model.generate_content(["Write a detailed description of the outfit shown in the image. It should include the following categories: top/bottom, color, texture, style, formality, other details. The description should be on one line, separate each category with semicolons.  I should be able to picture that outfit just by looking at the description.", img], stream=True)
    
    return response