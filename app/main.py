import streamlit as st
import utils_file as uf
from io import StringIO

# Add a title to the app
st.title("WhatsApp Chat Analyzer")

# Add some content to the app
st.write("Welcome to the WhatsApp Chat app. This app visualizes your whatsapp chat, with in a group or with other individuals." 
            "All the processing and analysis is done in the browser and your data is not sent to any other source"
)

uploaded_file = st.file_uploader("Uplaod your WhatsApp chat", type="txt")
    
if uploaded_file is not None:
    st.write("File Uploaded")
    contents = uploaded_file.read().decode("utf-8")
    df = uf.check_txt_file(contents)
    if type(df) is str:
        st.write(df)
    else:
        analysis_tab, data_tab = st.tabs(['Analysis', 'Data'])

        with data_tab:
            st.dataframe(df)
        
        with analysis_tab:
            df = clean_date_time(df)
            overview_tab = st.tabs(['Overview'])

            with overview_tab:
                st.write(
                    f"The messages started on {df['date'][0]} by {df['time'][0]} and "
                    f"ended on {df['date'][-1]} by {df['time'][-1]}"
                )
    