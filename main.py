import spotipy
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from youtubesearchpython import VideosSearch
from pprint import pprint
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


TOKEN = '6317356905:AAGQ2p8Lo0Kc4mkChTmE7ZbI2p1bzw9cIO8'
# تنظیمات API Spotify
client_id = 'c4821cf4363c4c438110e04b0d50f59b'
client_secret = 'd8eac638fd604aa8849f6f929ef8b538'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
bot = telebot.TeleBot(TOKEN)


userStep = {}

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0
    
def download_artist_tracks(artist_name,cid):
    # جستجوی هنرمند بر اساس نام
    results = sp.search(q=artist_name, type='artist')

    if results['artists']['items']:
        artist_id = results['artists']['items'][0]['id']

        # دریافت تمام آهنگ‌های هنرمند
        tracks = sp.artist_top_tracks(artist_id)
        markup=InlineKeyboardMarkup()
        # دانلود تمام آهنگ‌ها
        for track in tracks['tracks']:
            track_name = track['name']
            print(track_name)
            markup.add(InlineKeyboardButton(track_name,callback_data=f"select_{track_name}"))
            # get_youtube_track_url(track_name,cid)
            break
            # track_id = track['id']
            # download_track(track_id, f"{artist_name} - {track_name}")
        bot.send_message(cid,"لطفا آهنگ مورد نظر را انتخاب کنید",reply_markup=markup)
    else:
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
            video_do(video_url,cid)
        else:
            return None
    except Exception as e:
        print(f"خطا در دریافت لینک از YouTube: {e}")


def video_do(url,cid):
    yt = YouTube(url)
    try:
        # print("P")
        video = yt.streaming_data
        # print(video["formats"])
        # print(video["formats"][0]["url"])
        # print("_"*20)
        voice= yt.streaming_data
        pprint(voice["adaptiveFormats"])
        for i in voice["adaptiveFormats"]:
            print(i["mimeType"])
            if i["mimeType"].startswith('audio/mp4; codecs="mp4a.40.2"'):
                print(i["url"])
                download_video(i["url"],cid,"adadadadaad.mp3")
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
        download_file(url)
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

import requests
from concurrent.futures import ThreadPoolExecutor
import os

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




@bot.callback_query_handler(func=lambda call: call.data.startswith("select"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data=call.data.split("_")[-1]
    get_youtube_track_url(data,cid)
    
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid,"لطفا اسم آهنگ مورد نظر خود را ارسال کنید")
    userStep[cid]=1

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1)
def send_music(m):
    cid=m.chat.id
    download_artist_tracks(m.text,cid)

bot.infinity_polling()
# تست کد با نام هنرمند مورد نظر
# download_artist_tracks('greedy')
