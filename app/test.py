with open('/workspace/Whatsapp-chat-analyzer/Data/WhatsApp Chat with Class of 2021✊🏾.txt', 'r') as f:
    chat_file = f.read()


from chat_cleaner import WrangleChat
from whatsapp_analyser import WhatsappAnalyser
from visualise_data import VisualizeData

chat_wrangler = WrangleChat(chat_file)

chat_df = chat_wrangler.chat_df

wa_anal = WhatsappAnalyser(chat_df)

va_data = VisualizeData(chat_df)

# print(wa_anal.count_by_authors())

print(va_data.plot_chat_author_count())