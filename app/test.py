
import pandas as pd

with open('/workspaces/Whatsapp-chat-analyzer/Data/WhatsApp Chat with Wale Black🤴.txt', 'r') as f:
    chat_file = f.read()


from chat_cleaner import WrangleChat
from whatsapp_analyser import WhatsappAnalyser
from visualise_data import VisualizeData

chat_wrangler = WrangleChat(chat_file)

chat_df = chat_wrangler.chat_df

wa_anal = WhatsappAnalyser(chat_df)

print(remove_strings_from_text("image omitted"))

participants = wa_anal.get_participants()
print(participants)

print(wa_anal.filter_participants(participants))
