import re
import pandas as pd
import calmap
from wordcloud import WordCloud

def check_txt_file(file):
    df = txt_to_dataframe(file)
    if 'author' not in df.columns:
        return 'This is not a whatsapp chat file'
    else:
        return df      

def txt_to_dataframe(txt_file):
    pattern = r"\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s*[ap]m - "
    chats = re.split(pattern, txt_file)[1:]
    date_time = re.findall(pattern, txt_file)

    messages = []
    for i in range(len(chats)):
        message = {}
        try:
            message['date'] = date_time[i].split(',')[0]
        except:
            message['date'] = ''

        try:
            message['time'] = date_time[i].split(', ')[-1].split('\u202f')[0] + date_time[i].split(', ')[-1].split('\u202f')[-1].split(' -')[0]
        except:
            message['time'] = ''

        try:
            message['author'] = chats[i].split(':')[0]
        except:
            message['author'] = ''
            
        try:
            message['text'] = chats[i].split(': ')[-1]
            if message['author'] == message['text']:
                message['author'] = ''
        except:
            message['text'] = ''
        messages.append(message)
    
    return pd.DataFrame(messages)

def clean_date_time(df):
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df['time'] = pd.to_datetime(df['time'], format='%I:%M%p').dt.time
    return df

def count_daily_texts(df, ascending=False):
    date_counts = df['date'].dt.date.value_counts()
    if ascending == True:
        return date_counts
    return date_counts.sort_index()

def count_hourly_texts(df):
    hour_counts = df['time'].apply(lambda x: x.hour).value_counts()
    hour_counts = hour_counts.sort_index()

    def format_hour(hour):
        return f"{hour}:00{'am' if hour < 12 else 'pm'}"
    hour_counts.index = hour_counts.index.map(format_hour)
    
    return hour_counts

def plot_calmap(daily_counts):
    daily_counts.index = pd.DatetimeIndex(daily_counts.index)
    fig, ax = calmap.calendarplot(daily_counts, cmap='Blues');
    fig.set_size_inches(18, 8)
    return fig

def extract_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001f600-\U0001f64f"  # emoticons
        u"\U0001f300-\U0001f5ff"  # symbols & pictographs
        u"\U0001f680-\U0001f6ff"  # transport & map symbols
        u"\U0001f1e0-\U0001f1ff"  # flags (iOS)
        u"\U00002702-\U000027b0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.findall(text)

def get_emoji_value_counts(text_column):
    emoji_series = text_column.apply(extract_emojis)
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

def build_word_cloud(text_column, max_words):
    text_column = text_column[~text_column.str.contains('Media omitted')]
    wordcloud = WordCloud(width=800, height=400, max_words=max_words).generate(' '.join(text_column))

    return wordcloud

def authors_chat_count(df, top_ten=True):
    chat_count = df['author'].value_counts()

    if top_ten == True:
        try:
            return chat_count.sort_values().tail(10).to_frame().drop(index='')
        except:
            return chat_count.sort_values().tail(10).to_frame()
    else:
        try:
            return chat_count.sort_values().to_frame().drop(index='')
        except:
            return chat_count.sort_values().to_frame()

def plot_chat_count(chat_count):
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
    return fig