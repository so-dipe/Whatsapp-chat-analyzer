import streamlit as st

# Add a title to the app
st.title("WhatsApp Chat Analyzer")

# Add some content to the app
st.write("Welcome to the WhatsApp Chat app. This app visualizes your whatsapp chat, with in a group or with other individuals." 
            "All the processing and analysis is done in the browser and your data is not sent to any other source"
)

st.set_page_config(page_title="File Upload", page_icon=":clipboard:", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type="txt")
    
if uploaded_file is not None:
    st.write("File Uploaded")