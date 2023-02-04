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

            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                [
                    'Overview', 
                    'Participants',
                    'Activity (Hours)', 
                    'Activity (Days)',
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
                
                st.write('Activity (Hours)')
                hour_count = wa_analysis.count_hourly() 
                peak_hour = hour_count.idxmax()
                max_texts = hour_count.max()
                max_percent = wa_analysis.count_hourly(True).max().round(4) * 100
                st.write(
                    'During the course of this conversation, the most '
                    f'active hour was {peak_hour} with {max_texts} texts sent. '
                    f'This makes up {max_percent}% of all texts sent.'
                )
                hour_plot = wa_visuals.plot_hour_chart()
                st.plotly_chart(hour_plot)

                st.write('Activity (Days)')
                days_cal_plot = wa_visuals.plot_chat_calender(True)
                st.pyplot(days_cal_plot)
                # st.plotly_chart(days_cal_plot)

                st.write('Word Cloud')
                word_cloud = wa_visuals.plot_word_cloud()
                st.pyplot(word_cloud)
                    
                
            with tab2:
                fig = wa_visuals.plot_chat_author_count(False)
                st.plotly_chart(fig)

            with tab3: #Activity (hours)
                pass

            with tab4: #Activity (days)
                pass

            with tab5: #Word Cloud
                pass

                    
                    
        