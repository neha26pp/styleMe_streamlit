# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import os 
import tempfile
from datetime import timedelta
import json
import description 
import textwrap
from IPython.display import Markdown
import agents
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



vibrant_blue = "#0099ff"
vibrant_green = "#00cc99"
vibrant_pink = "#ff66c2"

# Use HTML styling to set text color
st.markdown(f'<h1 style="color:{vibrant_blue};">StyleMe - Your Virtual Wardrobe</h1>', unsafe_allow_html=True)


def upload_file_to_firebase(file, local_base_name):
    if file:

        import PIL.Image

        img = PIL.Image.open(file)

        response = description.generate_description(img)
        response.resolve()
       
        print( response.text)

        with open("wardrobe.txt", "a") as f:
            f.write("\n" + response.text + "\n")  # Add a newline character for readability


    return None, None



uploaded_file = st.file_uploader("Upload your outfit!", type=["jpg", "jpeg", "png"])



if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""

user_input = st.text_area("Enter your message:", value=st.session_state.chat_input, key="chat_input_area")

if st.button("Send", key="send_button"):
    if user_input:
        chat_result = agents.rag_chat(user_input)
        response = chat_result.chat_history[1]["content"]
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(f"Stylist: {response}")
        st.session_state.chat_input = ""

for chat in st.session_state.chat_history:
    st.write(chat)

if uploaded_file is not None:
  
    upload_file_to_firebase(uploaded_file, "image")
    
    st.write("Outfit stored in wardrobe! ")

