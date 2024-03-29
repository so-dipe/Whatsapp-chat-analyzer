from whatsapp_analyser import WhatsappAnalyser
import calmap
import pandas as pd
import plotly.express as px
# from plotly_calplot import calplot
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import datetime
import nltk
import string
# from nltk.tokenize import word_tokenize, MWETokenizer

nltk.download('punkt')
nltk.download('stopwords')

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
    text_column = self.chat_df['text'].apply(remove_punctuation_and_stopwords).apply(remove_strings_from_text)
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

  def plot_top_ten_active_days(self):
    data = super().top_ten_most_active_days()
    fig = px.bar(data)
    return fig

  def plot_emojis(self, top_ten=True):
    if top_ten:
      data = super().emoji_counts().sort_values().tail(10)
      fig = px.bar(data, orientation='h')
      fig.update_layout(
        # height=len(data) * 50,
        xaxis_title='Emoji Count',
        yaxis_title='Emoji',
        showlegend=False,
      )
    else:
      data = super().emoji_counts().sort_values()
      fig = px.bar(data, orientation='h')
      fig.update_layout(
        height=len(data) * 20,
        xaxis_title='Emoji Count',
        yaxis_title='Emoji',
        showlegend=False,
      )
    return fig

  def plot_day_of_week_activity(self):
    data = super().count_day_of_week()
    fig = px.bar(data)
    fig.update_layout(
      xaxis_title='Day',
      yaxis_title='Message [Count]'
    )
    return fig
  
def remove_punctuation_and_stopwords(text):
  # Remove punctuation
  text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))    
      
  # Tokenize the text into words
  words = nltk.word_tokenize(text)
      
  # Remove stopwords
  stopwords = set(nltk.corpus.stopwords.words('english'))
  words = [word for word in words if word.lower() not in stopwords]
      
  # Join the words back into a single string
  cleaned_text = ' '.join(words)
      
  return cleaned_text

def remove_strings_from_text(text):
  strings_to_remove = ['sticker omitted', 'media omitted', 'video omitted', 'audio omitted', 'image omitted']
  cleaned_text = text
  for string in strings_to_remove:
    cleaned_text = cleaned_text.replace(string, '')
    
  return cleaned_text