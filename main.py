from pytube import YouTube

# لینک یوتیوب را وارد کنید
youtube_link = "https://youtu.be/-dthTiyaPRw?si=J7pdnzEkY6gEqUKr"

# دانلود صدا با سرعت بالا
yt = YouTube(youtube_link)
audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
audio_stream.download(output_path='.', filename='audio')

# تغییر پسوند فایل به mp3
import os
os.rename("audio.mp4", "audio.mp3")