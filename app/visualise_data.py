from whatsapp_analyser import WhatsappAnalyser
import calmap
import pandas as pd
import plotly.express as px
from plotly_calplot import calplot
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import datetime

class VisualizeData(WhatsappAnalyser):
  
  def plot_chat_calender(self, year=False):
    daily_counts = super().count_daily()
    daily_counts.index = pd.DatetimeIndex(daily_counts.index)
    fig, ax = calmap.calendarplot(
      daily_counts, 
      cmap='Blues', 
      fillcolor='grey', 
      monthticks=3
    );
    fig.set_size_inches(18, 8)
    if year:
      current_year = datetime.datetime.now().year
      fig = plt.figure(figsize=(8, 4))
      calmap.yearplot(
        daily_counts,
        cmap='Blues', 
        fillcolor='grey', 
        monthticks=3,
        year=current_year
      )
    return fig

  def plot_hour_chart(self):
    hour_counts = super().count_hourly()
    fig = px.bar(hour_counts)
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Message Count",
        showlegend=False
    )
    return fig

  def plot_word_cloud(self, max_words=100):
    text_column = self.chat_df['text']
    text_column = text_column[~text_column.str.contains('Media omitted')]
    wordcloud = WordCloud(width=800, height=400, max_words=max_words).generate(' '.join(text_column))
    fig = plt.figure(figsize=(16, 9))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    return fig

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