#import chat_cleaner
from utils import format_hour, find_emojis
import pandas as pd
from wordcloud import WordCloud

class WhatsappAnalyser:
  def __init__(self, chat_df):
    self.chat_df = chat_df

  def count_daily(self):
    date_counts = self.chat_df['date'].dt.date.value_counts()
    return date_counts.sort_index()

  def top_ten_most_active_days(self):
    data = self.count_daily().sort_values().tail(10)
    data.index = data.index.astype(str)
    return data

  def count_hourly(self, normalize=False):
    hour_counts = self.chat_df['time'].apply(lambda x: x.hour).value_counts(normalize=normalize)
    hour_counts = hour_counts.sort_index()
    hour_counts.index = hour_counts.index.map(format_hour)
    return hour_counts

  def emoji_counts(self):
    text_column = self.chat_df['text']
    emoji_series = text_column.apply(find_emojis)
    emoji_list = []
    for i in emoji_series:
        if len(i) != 0:
            for emoji in i:
                emoji_list.append(emoji)
    emojis = ''
    for i in emoji_list:
        emojis += i
    unique_emojis = set(emojis)
    emoji_value_counts = pd.Series(index=unique_emojis, name='value', dtype=int)
    for i in unique_emojis:
        emoji_value_counts[i] = emojis.count(i)
    return emoji_value_counts


  def word_cloud(self, max_words=100):
    text_column = self.chat_df['text']
    text_column = text_column[~text_column.str.contains('Media omitted')]
    wordcloud = WordCloud(width=800, height=400, max_words=max_words).generate(' '.join(text_column))
    return wordcloud

  def count_by_authors(self):
    chat_count = self.chat_df['author'].value_counts()
    try:
      return chat_count.sort_values().drop(index='')
    except:
      return chat_count.sort_values()

  def first_last_day_text(self):
    start_date = self.chat_df['date'].iloc[0].date()
    start_time = self.chat_df['time'].iloc[0]
    end_date = self.chat_df['date'].iloc[-1].date()
    end_time = self.chat_df['time'].iloc[-1]

    return (
      f"The conversation started on **{start_date}** by **{start_time}** and "
      f"ended on **{end_date}** by **{end_time}**, "
      f"lasting **{(end_date-start_date).days}** days."
    )
    
  def character_count(self):
    word_counts = self.chat_df['text'].str.split().str.len().sum()
    return word_counts

  def count_day_of_week(self):
    data = self.chat_df.set_index('date')
    data = data['text']
    activity_count = (
      data
      .resample('D')
      .count()
      .groupby(data.resample('D').count().index.dayofweek)
      .sum()
    )
    activity_count.index = [
      'Monday', 
      'Tuesday', 
      'Wednesday', 
      'Thursday',
      'Friday',
      'Saturday',
      'Sunday'
    ]
    return activity_count