#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
# import mimetypes
import socks
import config
from telethon import sync
import getpass
from telethon.errors import SessionPasswordNeededError


entity = 'VK_Music_Bot' #change to new created bon name
client = TelegramClient(entity, config.api_id, config.api_hash,proxy=(socks.SOCKS5,'104.238.97.44', 15888)) #update_workers=None,spawn_read_thread=False connection_retries =None
try:
    client.connect()
except Exception as e:
                print(e)
if not client.is_user_authorized():
    # client.send_code_request(config.phone) #при первом запуске - раскомментить, после авторизации для избежания FloodWait советую закомментить
    client.sign_in(config.phone)
    try:
        client.sign_in(code=input('Enter code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=getpass.getpass())
client.start()
def main(argv):
    file_path = argv[1]
    chat_id = argv[2]
    bot_name = argv[3]
    title=argv[4]
    artist = argv[5]
    # file_name = argv[1]
    # object_id = argv[4]
    # duration = argv[6]
    # mimetypes.add_type('audio/aac','.aac')
    # mimetypes.add_type('audio/ogg','.ogg')

    msg = client.send_file(
                        str(bot_name),
                        file_path,
                        caption=str(chat_id),
                        #    file_name=str(file_name),
                        allow_cache=False,
                        silent=True,
                        #part_size_kb=512
                        attributes=[DocumentAttributeAudio(
                                                    duration = 0,
                                                    voice=None,
                                                    title=title,
                                                    performer=artist)]
                        ) 
    msg.delete()
    client.disconnect()
    return 0

if __name__ == '__main__':
    import sys
    main(sys.argv[0:])
    
   