import json
import urllib.request
import re
from pytube import YouTube
import os

def get_link(search_keyword):
    search_keyword = search_keyword.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword + "lyrics")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return ("https://www.youtube.com/watch?v=" + video_ids[0])

f = open ('data.json', "r")

# Reading from file
data = json.loads(f.read())

# Iterating through the json
# list
for i in data['items']:
    name = (i["track"]["name"])
    link = get_link(name)

    try:
        yt = YouTube(link)
    
        # extract only audio
        video = yt.streams.filter(only_audio=True).first()
        

        # replace destination with the path where you want to save the downloaded file
        destination = "/run/user/1000/gvfs/smb-share:server=10.147.18.233,share=media/Music"
        
        # download the file
        out_file = video.download(output_path=destination)
        
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        
        # result of success
        print(yt.title + " has been successfully downloaded.")
    except:
        print("Could not download: " + name)

# Closing file
f.close()
