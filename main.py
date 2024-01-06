import spotipy
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from youtubesearchpython import VideosSearch
from pprint import pprint
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from concurrent.futures import ThreadPoolExecutor
import os

TOKEN = '6317356905:AAGQ2p8Lo0Kc4mkChTmE7ZbI2p1bzw9cIO8'
# تنظیمات API Spotify
client_id = 'c4821cf4363c4c438110e04b0d50f59b'
client_secret = 'd8eac638fd604aa8849f6f929ef8b538'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
bot = telebot.TeleBot(TOKEN)
chanel_id=-1002097073432
userStep = {}

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'photo':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + "New photo recieved")
        elif m.content_type == 'document':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + 'New Document recieved')

bot.set_update_listener(listener)

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0

def download_song(song_name,cid):
    results = sp.search(q=song_name, type='track',limit=10,offset=0)
    if results["tracks"]["items"]:
        id=results['tracks']['items'][0]['id']
        markup=InlineKeyboardMarkup()
        for track in results["tracks"]["items"]:
            markup.add(InlineKeyboardButton(track['name'],callback_data=f"select_{track['name']}"))
        if len(results["tracks"]["items"])==10:
            markup.add(InlineKeyboardButton("آهنگ های بیشتر",callback_data=f"aadd_10_track_{song_name}"))
        
        bot.send_message(cid,"لطفا آهنگ مورد نظر خود را انتخاب کنید",reply_markup=markup)
    else:
        bot.send_message(cid,"هیچ نتیجه ای یافت نشد")

def download_artist_tracks(artist_name,cid):
    # جستجوی هنرمند بر اساس نام
    results = sp.search(q=artist_name, type='artist')
    if results['artists']['items']:
        artist_id = results['artists']['items'][0]['id']
        markup=InlineKeyboardMarkup()
        album_list=sp.artist_albums(artist_id,album_type="album",limit=5)
        for album in album_list['items']:
            markup.add(InlineKeyboardButton(album["name"],callback_data=f"chois_{album["id"]}"))
            # for track in ttrack['items']:
            #     markup.add(InlineKeyboardButton(track['name'],callback_data=f"select_{track['name']}"))
            #     print(track['name'])
        if len(album_list['items'])==5:
            markup.add(InlineKeyboardButton("آهنگ های بیشتر",callback_data=f"add_5_album_{artist_id}"))
        bot.send_message(cid,"لطفا آلبوم مورد نظر خود را انتخاب کنید",reply_markup=markup)
        # دریافت تمام آهنگ‌های هنرمند
        # tracks = sp.artist_top_tracks(artist_id)
        # markup=InlineKeyboardMarkup()
        # # دانلود تمام آهنگ‌ها
        # for track in tracks['tracks']:
        #     track_name = track['name']
        #     # print(track_name)
        #     markup.add(InlineKeyboardButton(track_name,callback_data=f"select_{track_name}"))
        #     # get_youtube_track_url(track_name,cid)
        #     # track_id = track['id']
        #     # download_track(track_id, f"{artist_name} - {track_name}")
        # bot.send_message(cid,"لطفا آهنگ مورد نظر را انتخاب کنید",reply_markup=markup)
    else:
        bot.send_message(cid,f"هیچ هنرمندی با نام {artist_name} یافت نشد.")
        print(f"هیچ هنرمندی با نام {artist_name} یافت نشد.")

def get_youtube_track_url(song_name,cid):
    try:
        # جستجو در YouTube
        videos_search = VideosSearch(song_name, limit = 1)
        results = videos_search.result()

        # چک کردن آیا نتیجه وجود دارد یا خیر
        if results['result']:
            # گرفتن لینک اولین ویدئو
            video_url = results['result'][0]['link']
            video_do(video_url,cid,song_name)
        else:
            return None
    except Exception as e:
        print(f"خطا در دریافت لینک از YouTube: {e}")


def video_do(url,cid,song_name):
    yt = YouTube(url)
    try:
        # print("P")
        video = yt.streaming_data
        # print(video["formats"])
        # print(video["formats"][0]["url"])
        # print("_"*20)
        voice= yt.streaming_data
        # pprint(voice["adaptiveFormats"])
        for i in voice["adaptiveFormats"]:
            # print(i["mimeType"])
            if i["mimeType"].startswith('audio/mp4; codecs="mp4a.40.2"'):
                # print(i["url"])
                download_video(i["url"],cid,f"{song_name}.mp3")
        #     elif i["mimeType"].startswith('audio/webm; codecs="opus"'):
        #         print(i["url"])
        #         download_video(i["url"],"alliiik2.mp3")
        #         break

        # print(voice["adaptiveFormats"][12]["url"])
        # download_video(voice["adaptiveFormats"][12]["url"],cid,"hoooooooooooy.mp3")

    except:
        print("noo")



def download_video(url,cid, output_path='videooooooo.mp4'):
    try:
        download_file(url,filename=output_path)
        # درخواست GET برای دریافت داده‌های ویدئو
        # response = requests.get(url, stream=True)
        # response.raise_for_status()
        bot.send_message(cid,"در حال ارسال آهنگ")
        # bot.send_audio(cid,response.content)

       # باز کردن یک فایل برای ذخیره ویدئو
        # with open(output_path, 'wb') as video_file:
        #     for chunk in response.iter_content(chunk_size=8192):
        #         if chunk:
        #             video_file.write(chunk)
        # bot.send_message(cid,"ذخیره شد")
        with open(output_path,'rb') as vois:
            bot.send_audio(cid,vois)

        print(f"ویدئو با موفقیت در {output_path} ذخیره شد.")

    except requests.exceptions.HTTPError as errh:
        print ("خطا HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("خطا اتصال:", errc)
    except requests.exceptions.Timeout as errt:
        print ("خطا Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print ("خطای نامشخص:", err)



def download_chunk(url, start_byte, end_byte, temp_filename):
    headers = {'Range': f'bytes={start_byte}-{end_byte}'}
    response = requests.get(url, headers=headers, stream=True)
    with open(temp_filename, 'ab') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def download_file(url, num_chunks=1, filename='adadadadaad.mp3'):
    temp_filename = filename + '.temp'
    response = requests.head(url)
    file_size = int(response.headers.get('content-length', 0))
    chunk_size = file_size // num_chunks

    with ThreadPoolExecutor(max_workers=num_chunks) as executor:
        futures = []

        for i in range(num_chunks):
            start_byte = i * chunk_size
            end_byte = (i + 1) * chunk_size - 1 if i < num_chunks - 1 else file_size - 1
            futures.append(executor.submit(download_chunk, url, start_byte, end_byte, temp_filename))

        for future in futures:
            future.result()

    os.rename(temp_filename, filename)
    print('آهنگ با موفقیت ذخیره شد.')


@bot.callback_query_handler(func=lambda call: call.data.startswith("chois"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data=call.data.split("_")[-1]
    tracks=sp.album_tracks(data,limit=10)
    markup=InlineKeyboardMarkup()
    for track in tracks['items']:
        markup.add(InlineKeyboardButton(track['name'],callback_data=f"select_{track['name']}"))
        print(track['name'])
    if len(tracks['items'])==10:
        markup.add(InlineKeyboardButton("آهنگ های بیشتر",callback_data=f"add_10_track_{data}"))
    
    bot.send_message(cid,"لطفا آهنگ مورد نظر خود را انتخاب کنید",reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith("send"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data=call.data.split("_")[-1]
    if data=="name":
        bot.send_message(cid,"اسم خواننده مورد نظر را ارسال کنید")
        userStep[cid]=1
    elif data=="song":
        bot.send_message(cid,"اسم آهنگ مورد نظر را ارسال کنید")
        userStep[cid]=2    

@bot.callback_query_handler(func=lambda call: call.data.startswith("aadd"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    song_name=call.data.split("_")[-1]
    offset_=int(call.data.split("_")[1])
    data=call.data.split("_")[2]   
    results = sp.search(q=song_name, type='track',limit=10,offset=offset_)
    offset_+=10
    if results["tracks"]["items"]:
        id=results['tracks']['items'][0]['id']
        markup=InlineKeyboardMarkup()
        for track in results["tracks"]["items"]:
            markup.add(InlineKeyboardButton(track['name'],callback_data=f"select_{track['name']}"))
        if len(results["tracks"]["items"])==10:
            markup.add(InlineKeyboardButton("آهنگ های بیشتر",callback_data=f"aadd_{offset_}_track_{song_name}"))
        elif len(results["tracks"]["items"])==0:
            markup.add(InlineKeyboardButton("آهنگ دیگری وجود ندارد"))
        bot.send_message(cid,"لطفا آهنگ مورد نظر خود را انتخاب کنید",reply_markup=markup)
    else:
        bot.send_message(cid,"هیچ نتیجه ای یافت نشد")


@bot.callback_query_handler(func=lambda call: call.data.startswith("add"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    id=call.data.split("_")[-1]
    offset_=int(call.data.split("_")[1])
    data=call.data.split("_")[2]
    if data=="album":
        markup=InlineKeyboardMarkup()
        album_list=sp.artist_albums(id,album_type="album",limit=5,offset=offset_)
        offset_+=5
        for album in album_list['items']:
            markup.add(InlineKeyboardButton(album["name"],callback_data=f"chois_{album["id"]}"))
            # for track in ttrack['items']:
            #     markup.add(InlineKeyboardButton(track['name'],callback_data=f"select_{track['name']}"))
            #     print(track['name'])
        if len(album_list['items'])==5:
            markup.add(InlineKeyboardButton("آهنگ های بیشتر",callback_data=f"add_{offset_}_album_{id}"))
        elif len(album_list['items'])==0:
            markup.add(InlineKeyboardButton("آهنگ دیگری وجود ندارد"))
        
        bot.send_message(cid,"لطفا آلبوم مورد نظر خود را انتخاب کنید",reply_markup=markup)

    elif data=="track":
        tracks=sp.album_tracks(id,limit=10,offset=offset_)
        markup=InlineKeyboardMarkup()
        offset_+=10
        for track in tracks['items']:
            markup.add(InlineKeyboardButton(track['name'],callback_data=f"select_{track['name']}"))
            print(track['name'])
        if len(tracks['items'])==10:
            markup.add(InlineKeyboardButton("آهنگ های بیشتر",callback_data=f"add_{offset_}_track_{id}"))
        elif len(tracks['items'])==0:
            markup.add(InlineKeyboardButton("آهنگ دیگری وجود ندارد"))
        
        bot.send_message(cid,"لطفا آهنگ مورد نظر خود را انتخاب کنید",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("select"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data=call.data.split("_")[-1]
    get_youtube_track_url(data,cid)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ارسال نام خواننده",callback_data="send_name"))
    markup.add(InlineKeyboardButton("ارسال نام آهنگ",callback_data="send_song"))
    markup.add(InlineKeyboardButton("ارسال بخشی از متن آهنگ",callback_data="send_song"))
    bot.copy_message(cid,chanel_id,2,reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1)
def send_music(m):
    cid=m.chat.id
    download_artist_tracks(m.text,cid)


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==2)
def send_music(m):
    cid=m.chat.id
    download_song(m.text,cid)

bot.infinity_polling()
# تست کد با نام هنرمند مورد نظر
# download_artist_tracks('greedy')