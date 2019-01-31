import requests
import time
import config
from telebot import AsyncTeleBot,TeleBot,types
import os
# import logging
# import traceback
import SQLighter
import utils
import authorization
from telebot import apihelper
from vk_audio import VkAudio
import audio_url_decoder
import subprocess

import telebot

import flask
from flask import Flask


from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)


# proxies = {'https':'https://194.87.148.222:1080'}
            


r = authorization.VKAuth(config.vkLogin,config.vkPassword,None)
time.sleep(1)
r.get_response()
bot = None
try:
    # bot = AsyncTeleBot(config.token, num_threads=4)
    bot = telebot.TeleBot(config.token,threaded = False) #thread=False чтобы небыло падения бота
    apihelper.proxy = {'https':'socks5://104.238.97.44:15888'}
except Exception as e:
    print(e)    


    
vkaudio = VkAudio(r.get_session())

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return '<h1>APP WORK</h1>'

@app.route('/',methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
    else:
        flask.abort(403)


# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start'])
def user_defenition(message):
    utils.set_user_id(message.from_user.id)
    utils.set_chat_id(message.from_user.id,message.chat.id)
    bot.send_message(message.chat.id, "current chat id = " + str(message.chat.id)+"\nmusic will download here")
    bot.send_message(message.chat.id, "Отправь свой id вконтакте")

@bot.message_handler(commands=["test"])
def chat_defenition(message):
    utils.set_user_id(message.from_user.id) 
    utils.set_chat_id(message.from_user.id,message.chat.id)
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "current chat id = " + str(message.chat.id)+"\nmusic will download here")
    bot.send_message(message.chat.id, "Отправь свой id вконтакте", reply_markup=markup)


@bot.message_handler(func=lambda message: utils.get_current_state(message.from_user.id) == utils.States.S_ENTER_VKID.value) #check user in DB and input of vk id from him
def user_entering_name(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
        return
    else:    
        bot.send_message(message.chat.id, "Ваш запрос обробатывается....")
        utils.set_vk_id(message.from_user.id,message.text)
        utils.set_state(message.from_user.id, utils.States.S_DOWNLOADING.value)
        music_data = vkaudio.get(int(message.text))
        d = Downloader(music_data)
        d.download_music(bot,message.chat.id)
        # download_music(music_data,message.chat.id)



@bot.message_handler(content_types=["audio"]) #https://habr.com/post/348234/
def test(message):
    client_chat_id = message.caption
    file_id = message.audio.file_id
    audio_title = message.audio.title
    if (int(client_chat_id) != None):
        print('big audio send')                                                 
        bot.send_audio(int(client_chat_id), #пересылаем конечному адресату
                                file_id,caption='',
                                # duration=int(duration_s),
                                title=audio_title,
                                performer='')                          
    return



   
def music_data(user_id):
    url = "https://vk.com/al_audio.php"#+userid
    data = {"act": "reload_audio", "al": "1", "ids": "8088876_456239679_9e07d2f0ba0f416483_1fd8f993ca65d41d9a"}
    session = r.get_session()
    result = session.post(url, data=data, headers=r.headers)

    res = result.content.decode('cp1251') # not necessary to use
    json_data = res.split('<!>')
    json_data = json_data[5].split(',')
    url = audio_url_decoder.decode_audio_url(json_data[2].strip('"'),user_id) #use decode function
    title = json_data[3].strip('"')
    artist = json_data[4].strip('"')
    d = {'title':title, 'artist':artist,'url':url} # make dictionary
    return d
    
class Downloader():
    def __init__(self,music_data):

        self.music_data = music_data
        
# падает с ошибкой - это либо проблема прокси
# обойти потерю соединения через прокси,возможно не понаобиться если задеплоить на сервере
    def download_music(self,bot: TeleBot,chat_id=None):

        self.bot = bot

        if chat_id is None:
            chat_id = 0#self.user_id
        if os.path.exists(config.notDownloaded):    
            os.remove(config.notDownloaded)
        for num, track in enumerate(self.music_data,1):
            file_path = config.folderMusic
            file_name = '{}-{}.mp3'.format(utils.clean(track['artist']),utils.clean(track['title']))
            print(str(num)+' Track Downloading :' + file_path + file_name)
            try:
                f=open(file_path + file_name,"wb") #open file in mode  wb
            except Exception as e:
                print(e)
                f = open(config.notDownloaded,"a") 
                f.write(file_name+'\n')
            else:
                try:
                    ufr = requests.get(track['url']) #do request
                except requests.exceptions.ConnectionError:
                    r.status_code = "Connection refused"
                
                f.write(ufr.content) #write content in file
                
                
                if file_path+file_name == f.name:
                    if (os.path.getsize(file_path+file_name) >> 20 >= 50):  #for send large file
                        call = f"python3.6 ./TelegramSubProcess.py {file_path + file_name}  {str(chat_id)} " \
                                f"{config.BOT_NAME} {utils.clean(track['title'])} {utils.clean(track['artist'])} "      
                        try:
                            event = subprocess.check_call(call,shell=True)
                        except Exception as e:   
                            print(e)
                            os.remove(file_path+file_name)
                        else:         
                            if event == 0:
                                os.remove(file_path+file_name)
                            else:
                                print("LOAD FAIL")
                                
                    else:
                        f = open(file_path + file_name,"rb")     
                        try:                           
                            msg = self.bot.send_audio(chat_id, f, None,None,utils.clean(track['artist']),utils.clean(track['title']),timeout=100)
                            # msg.wait()
                        except Exception as e:
                            print(e)
                            f.close()
                            os.remove(file_path+file_name)
                        else:
                            f.close()
                            os.remove(file_path+file_name)
                


        f = open(config.notDownloaded,"rb")  
        msg = self.bot.send_document(chat_id, f)   


def telegram_polling():
    global bot
    try:
        if(bot != None):
            bot.polling(none_stop=True, timeout=600) #constantly get messages from Telegram
        else :
            pass
            # bot = AsyncTeleBot(config.token)
            # bot = telebot.TeleBot(config.token)
    except:
        # traceback_error_string=traceback.format_exc()
        with open("/home/vova/WORK/test/echoBot/music/Error.Log", "a") as myfile:
            pass
            # myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<ERROR polling>>\r\n"+ traceback_error_string + "\r\n<<ERROR polling>>")
        # bot.stop_polling()
        # time.sleep(10)
        # telegram_polling()

if __name__ == '__main__':   
    app.run()
    # telegram_polling()
    # DM = vkaudio.get(vk_id)
    # download_music(DM)