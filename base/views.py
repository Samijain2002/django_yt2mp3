from django.shortcuts import render
from django.http import HttpResponse
from pytube import YouTube
import os
import math
def solve(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
ytlink = 0
def index(request):
    if request.method == 'POST':
        global ytlink
        ytlink = request.POST['ytlink']
        aud = request.POST.get('typeto', False)
        ext = "mp3" if aud == "1" else "mp4"
        yt = YouTube(str(ytlink))
        if ext == "mp3":
            video = yt.streams.filter(only_audio=True).first()
        else:
            video = yt.streams.filter(file_extension = ext).first()
        start = ytlink.index("=")
        if "&" in ytlink:
            end = ytlink.index("&")
            link = "https://www.youtube.com/embed/" + ytlink[start+1:end]
        else:
            link = "https://www.youtube.com/embed/" + ytlink[start+1:]
        if ext == "mp3":
            resolution = [st.abr for st in yt.streams.filter(type = "audio").all()]
            filesize = [solve(st.filesize) for st in yt.streams.filter(type = "audio").all()]
        else:
            resolution = [st.resolution for st in yt.streams.filter(progressive=True).all()]
            filesize = [solve(st.filesize) for st in yt.streams.filter(progressive=True).all()]
        arr = [[i,j] for i,j in zip(resolution, filesize)]
        arr.sort()
        data = {"url":ytlink, "embedlink":link, "tabledata":arr, "videotitle":video.title}
        return render(request, "index.html", data)
    link =  "https://www.youtube.com/embed/IlLFLAX3zEQ" 
    data = {"url":None, "embedlink":link}
    return render(request, "index.html", data)

def downloadfile(request, res = 0):
    if res != 0:
        global ytlink
        yt = YouTube(str(ytlink))
        ext = "mp3" if "kbps" in res else "mp4"
        print(ext, ytlink)
        if ext == "mp3":
            video = yt.streams.filter(abr=res).first()
        else:
            video = yt.streams.filter(res = res).first()
        print(video)
        try:
            homedir = os.path.expanduser("~")
            dest = homedir+"/Desktop"
            out_file = video.download(output_path=dest)
            base, ext = os.path.splitext(out_file)
            new_file = base + "."+ext
            os.rename(out_file, new_file)
        except:
            return HttpResponse("file exists")
        return HttpResponse("Download Done")

