from flask import Flask
from flask import request
import youtube_dl
import subprocess
import time
import os
import signal

pid = 0
job = []

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/video",methods=['POST'])
def video():
    if request.json:
        url = request.json['url']
        playYoutube(url)
        return url
        
    return "None"

@app.route("/quit")
def quit():
    # os.kill(pid,signal.SIGTERM)
    # print(job[0].poll())
    print(os.getpgid(pid))
    print(pid)
    print(job[0].kill())
    subprocess.Popen(['kill',str(pid)])
    subprocess.Popen(['ps','-a'])
    # os.killpg(pid,signal.SIGTERM)
    return str(pid)


def playYoutube(url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    with ydl:
        result = ydl.extract_info(
            url,
            download=False)
        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result
    video_url = video['formats'][-1]['url']
    print(video_url)
    # subprocess.call(['omxplayer','-b',video_url])
    proc = subprocess.Popen(['omxplayer','-b',video_url],stdout=subprocess.PIPE)
    job.append(proc)
    global pid
    pid = proc.pid
    print('proc :' + str(proc.pid))
    # proc.terminate()





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082,threaded=True)
    