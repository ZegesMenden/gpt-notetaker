from pytube import YouTube 
from pyffmpeg import FFmpeg
import os

def fetch_from_yt(link, oname):
    dl_path = os.getcwd()

    try: 
        # object creation using YouTube 
        yt = YouTube(link) 
    except: 
        raise Exception("Connection failed")

    d_audio = yt.streams.filter(file_extension="webm")[-1]

    if d_audio is None:
        raise Exception("Could not find audio sources")

    try: 
        d_audio.download(output_path=dl_path, filename=oname)        
    except: 
        raise Exception("Download failed")

# print("converting to mp3...", end="")

# inp = "_.webm"
# out = "out.mp3"

# if oname != "":
#     out = oname

# ff = FFmpeg(enable_log=False)

# try:
#     output_file = ff.convert(inp, out)
# except:
#     pass
    
# print("[OK]")

# os.remove(inp)
