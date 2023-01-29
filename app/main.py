import streamlit as st
import utils_file as uf

# Add a title to the app
st.title("WhatsApp Chat Analyzer")

# Add some content to the app
st.write("Welcome to the WhatsApp Chat app. This app visualizes your whatsapp chat, with in a group or with other individuals." 
            "All the processing and analysis is done in the browser and your data is not sent to any other source"
)

uploaded_file = st.file_uploader("Uplaod your WhatsApp chat", type="txt")
    
if uploaded_file is not None:
    st.write("File Uploaded")
    # with open(uploaded_file) as f:
    #     df = uf.check_txt_file(f)
    #     st.write(df.head())
    st.write(type(uploaded_file))