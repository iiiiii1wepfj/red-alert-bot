# red-alert-bot
a telegram bot for red alerts in israel

# how to run
 
 git clone https://github.com/iiiiii1wepfj/message-view-counter-bot.git
 
 cd message-view-counter-bot
 
 pip3 install -U -r requirements.txt
 
 edit the api hash and api id and bot token in bot.py
 
 create the channel and add the bot to the channel as admin with post messages permission, copy the channel id to main_channel  in bot.py
 and if do you want to forward the message to other channels from the main channel add it to chats_to_forward like ["-100", "-100"]
 
python3 bot.py
