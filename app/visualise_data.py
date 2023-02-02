from whatsapp_analyser import WhatsappAnalyser
import calmap
import pandas as pd
import plotly.express as px

class VisualizeData(WhatsappAnalyser):
  
  def plot_chat_calender(self):
    daily_counts = super().count_daily()
    daily_counts.index = pd.DatetimeIndex(daily_counts.index)
    fig, ax = calmap.calendarplot(daily_counts, cmap='Blues');
    fig.set_size_inches(18, 8)
    return fig

  def plot_hour_chart(self):
    hour_counts = super().count_hourly()
    return hour_counts

  def plot_word_cloud(max_words):
    pass

  def plot_chat_author_count(self, top_ten=True):
    if top_ten:
      chat_count = super().count_by_authors().tail(10)
    else:
      chat_count = super().count_by_authors()
    new_index = []
    for index in chat_count.index:
        if index[0] == '+':
            index = f'({index})'
            new_index.append(index)
        else:
            new_index.append(index)
    chat_count.index = new_index
    
    fig = px.bar(chat_count, orientation='h')
    fig.update_layout(
        xaxis_title="Message Count",
        yaxis_title="Author",
        showlegend=False
    )
    if len(new_index) > 10:
        fig.update_layout(
            height=len(new_index) * 17,
            width=800
        )
    return fig   