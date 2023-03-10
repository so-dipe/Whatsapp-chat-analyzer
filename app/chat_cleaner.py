import re
import pandas as pd

class WrangleChat:
    def __init__(self, chat, device_type):
        self.chat = chat
        self.device_type = device_type
        if device_type == 'Android':
            self.status = self.get_data_frame()
        elif device_type == 'iOS':
            self.status = self.get_data_frame_iOS()
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

    def get_data_frame_iOS(self):
        pattern = r'\[(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}:\d{2} [AP]M)\]'
        chats = re.split(pattern, self.chat)[1:]
        date_time = re.findall(pattern, self.chat)
        
        messages = []
        for i in range(len(chats)):
            message = {}
            try:
                message['date'] = date_time[i][0]
            except:
                message['date'] = ''

            try:
                message['time'] = date_time[i][1]
            except:
                message['time'] = ''

            try:
                main_content = chats[i*3 + 2].split(": ")
                try:
                    message['author'] = main_content[0]
                except:
                    message['author'] = ''
                    
                try:
                    if len(main_content) > 2:
                        message['text'] = result = ': '.join(main_content[1:])#chats[i*3 + 2].split(": ")[-1]
                    else:
                        message['text'] = main_content[-1]
                    if message['author'] == message['text']:
                        message['author'] = ''
                except:
                    message['text'] = ''
            except:
                ""
            messages.append(message)

        df = pd.DataFrame(messages).dropna()
        status = self.__check_data(df)
        if status:
            return status

        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')
        df['time'] = pd.to_datetime(df['time'], format='%I:%M:%S %p').dt.time
            
        self.chat_df = df
        return None

    def __check_data(self, df):
        if 'author' not in df.columns:
            return 'Error: The file is not a WhatsApp chat file!'
        else:
            return None

    def get_participants(self):
        if self.device_type=='Android':
            return self.chat_df['author'].unique()[1:].tolist()
        else:
            return self.chat_df['author'].unique().tolist()

    def filter_participants(self, participants=[]):
        if participants is not []:
            self.chat_df = self.chat_df[self.chat_df["author"] == participants]
        return self.chat_df.head()
