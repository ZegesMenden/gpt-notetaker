from pytube import YouTube 
import os
import sys

dl_path = os.getcwd()
link = sys.argv[1]

try: 
    # object creation using YouTube 
    yt = YouTube(link) 
except: 
    #to handle exception 
    print("Connection Error") 

mp3_streams = yt.streams.filter(file_extension='webm')

d_audio = mp3_streams[-1]

try: 
    # downloading the video 
    d_audio.download(output_path=dl_path)
    print('Video downloaded successfully!')
except: 
    print("Some Error!")
