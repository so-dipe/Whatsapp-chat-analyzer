import streamlit as st
# import app.utils as uf
# # from io import StringIO
# import matplotlib.pyplot as plt
# import plotly.express as px

from chat_cleaner import WrangleChat
from whatsapp_analyser import WhatsappAnalyser
from visualise_data import VisualizeData



# Add a title to the app
st.title("WhatsApp Chat Analyzer")

# Add some content to the app
st.write("Welcome to the WhatsApp Chat app. This app visualizes your whatsapp chat, with in a group or with other individuals." 
            "All the processing and analysis is done in the browser and your data is not sent to any other source"
)

uploaded_file = st.file_uploader("Uplaod your WhatsApp chat", type="txt")
    
if uploaded_file is not None:
    st.write("File Uploaded Successfully")
    contents = uploaded_file.read().decode("utf-8")
    chat_wrangler = WrangleChat(contents)
    df = chat_wrangler.chat_df
    if type(df) is str:
        st.write(df)
        # st.write(contents)
    else:

        analysis_tab, data_tab = st.tabs(['Analysis', 'Data'])

        with data_tab:
            st.dataframe(df)
            
        with analysis_tab:
            wa_analysis = WhatsappAnalyser(df)
            wa_visuals = VisualizeData(df)

            tab1, tab2, tab3 = st.tabs(
                [
                    'Overview', 
                    'Participants', 
                    'Word Cloud'
                ]
            )

            with tab1:
                st.write(
                    wa_analysis.first_last_day_text()
                )
                num_authors = len(wa_analysis.count_by_authors())
                st.write(
                    f'The conversation was between **{num_authors}** individuals.'
                )

                if num_authors > 10:
                    st.write(
                        f'Here are the top 10 contributors in this group:'
                    )
                else:
                    st.write(
                        f'Here is the activity chart of all members'
                    )
                fig = wa_visuals.plot_chat_author_count()
                                        
                st.plotly_chart(fig)
                if num_authors > 10:
                    st.write(
                        'You can check the activity of all members in Participants'
                    )
                    
                
            with tab2:
                fig = wa_visuals.plot_chat_author_count(False)
                st.plotly_chart(fig)

                    
                    
        