with open('/workspace/Whatsapp-chat-analyzer/Data/WhatsApp Chat with Class of 2021✊🏾.txt', 'r') as f:
    chat_file = f.read()


from chat_cleaner import WrangleChat
from whatsapp_analyser import WhatsappAnalyser
from visualise_data import VisualizeData

chat_wrangler = WrangleChat(chat_file)

chat_df = chat_wrangler.chat_df

wa_anal = WhatsappAnalyser(chat_df)

# va_data = VisualizeData(chat_df)


# print(va_data.plot_chat_author_count())

print(wa_anal.character_count())

import pandas as pd

# create a sample dataframe with a text column
# df = pd.DataFrame({'text_column': ['Hello world!', 'This is a sentence.']})

# # use str.split to split each string into a list of words, and str.len to count the number of words
# word_counts = df['text_column'].str.split().str.len().sum()

# print(word_counts)

print(wa_anal.chat_df.head())
