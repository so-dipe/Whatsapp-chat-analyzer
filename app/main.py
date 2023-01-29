import streamlit as st
import utils_file as uf
# from io import StringIO
import matplotlib.pyplot as plt
import plotly.express as px


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
            start_date = df['date'].iloc[0]
            start_time = df['time'].iloc[0]
            end_date = df['date'].iloc[-1]
            end_time = df['time'].iloc[-1]

            df = uf.clean_date_time(df)


            tab1, tab2, tab3 = st.tabs(
                [
                    'Overview', 
                    'Participants', 
                    'Word Cloud'
                ]
            )

            with tab1:
                st.write(
                    f"The conversation started on **{start_date}** by **{start_time}** and "
                    f"ended on **{end_date}** by **{end_time}**, "
                    f"lasting **{(df['date'].iloc[-1]-df['date'].iloc[0]).days}** days."
                )

                fig = px.bar(authors, y='author', orientation='h')
                st.plotly_chart(fig)
                
            
            with tab2:
                pass
                
                
    