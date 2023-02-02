import re
import pandas as pd

class WrangleChat:
    def __init__(self, chat):
        self.chat = chat
        self.status = self.get_data_frame()
        if self.status:
            self.chat_df = self.status
    
  
    def get_data_frame(self):
        pattern = r"\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s*[ap]m - "
        chats = re.split(pattern, self.chat)[1:]
        date_time = re.findall(pattern, self.chat)
        
        messages = []
        for i in range(len(chats)):
            message = {}
            try:
                message['date'] = date_time[i].split(',')[0]
            except:
                message['date'] = ''

            try:
                message['time'] = date_time[i].split(', ')[-1].split('\u202f')[0] +     date_time[i].split(', ')[-1].split('\u202f')[-1].split(' -')[0]
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

        df = pd.DataFrame(messages)
        status = self.__check_data(df)
        if status:
            return status

        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df['time'] = pd.to_datetime(df['time'], format='%I:%M%p').dt.time
            
        self.chat_df = df
        return None

    def __check_data(self, df):
        if 'author' not in df.columns:
            return 'Error: The file is not a WhatsApp chat file!'
        else:
            return None
