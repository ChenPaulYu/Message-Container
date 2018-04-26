from flask import Flask,jsonify
from flask import request
from flask import send_file, send_from_directory
import youtube_dl
import time,random
import os
import signal,psutil
import pygame, sys
from pygame.locals import *
import threading
import serial
import time
import requests
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from socketIO_client_nexus import SocketIO, LoggingNamespace



pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
app = Flask(__name__)
port = "/dev/ttyACM0"

try: 
    serialFromArduino = serial.Serial(port,9600)
except:
    serialFromArduino = None


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/music", methods=['POST'])
def music():
    if request.json:
        url = request.json['url']
        r = requests.get(url)
        with open('./music/movie.mp3', 'wb') as f:
            f.write(r.content)
            global player
            player = OMXPlayer('./music/movie.mp3')
        return jsonify({'success':True})
    return jsonify({'success':False})

@app.route("/background", methods=['POST'])
def background():
    event = pygame.event.Event(pygame.USEREVENT, {'data': 'background'})
    pygame.event.post(event)
    return jsonify({'success':True})

@app.route("/image", methods=['POST'])
def image():
    if request.json:
        url = request.json['url']
        print(url)
        r = requests.get(url)
        with open('./image/img01.jpg', 'wb') as f:
            f.write(r.content)
            event = pygame.event.Event(pygame.USEREVENT, {'data': 'image'})
            pygame.event.post(event)
        return jsonify({'success':True})
    return jsonify({'success':False})

@app.route("/text", methods=['POST'])
def text():
    if request.json:
        global text 
        text = request.json['text']
        event = pygame.event.Event(pygame.USEREVENT, {'data': 'text'})
        pygame.event.post(event)
        return jsonify({'success':True})
    return jsonify({'success':False})
    
@app.route("/message",methods=['POST'])
def message():
    if request.json:
        message_trigger = request.json['message_trigger']
        communicateWithArduino(message_trigger)
        return jsonify({'success':True})
    return jsonify({'success':False})

@app.route("/video",methods=['POST'])
def video():
    if request.json:
        url = request.json['url']
        playYoutube(url)
        return jsonify({'success':True})
    return jsonify({'success':False})


@app.route("/quit",methods=['POST'])
def quit():
    player.quit()
    return jsonify({'success':True})


def playYoutube(url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    with ydl:
        result = ydl.extract_info(url,download=False)
        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result
    video_url = video['formats'][-1]['url']
    global player
    player = OMXPlayer(video_url)

def communicateWithArduino(message_trigger):
    if serialFromArduino == None:
        return
    else :
        serialFromArduino.flushInput()

    if message_trigger == 'True':
        print("send1")
        serialFromArduino.write('1')
    else:
        print("send0")
        serialFromArduino.write('0')

def readData():
    if serialFromArduino == None:
        return
    else :
        serialFromArduino.flushInput()
    while True:
        if(serialFromArduino.isOpen()>0):
            input = serialFromArduino.read(1)
            print("read:",ord(input))

def fade_in_element(element,rect,state,state_time,FADE_IN_TIME):
    FADE_IN_EASING = lambda x: x
    if state == True:
        if state_time >= FADE_IN_TIME:
            state = False
    if state == True:
        global alpha
        alpha = FADE_IN_EASING(1.0 * state_time / FADE_IN_TIME)

    element_rect = rect
    element_surf = pygame.surface.Surface((element_rect.width, element_rect.height))
    element_surf.set_alpha(255 * alpha)

    return element_surf,state,element

def backgroundDsiplay():
    display_first = True
    display = pygame.image.load('bridge.jpg')
    x = 0
    y = 0
    position = [x,y]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                display_first = False
                print(event.data)
                tmp = event.data
                if(tmp == "image"):
                    print('image')
                    last_state_change = time.time()
                    state = True
                    image = pygame.image.load('./image/img01.jpg')
                    size = image.get_rect()
                    picture_rect = image.get_rect(center = screen.get_rect().center)
                    # image = pygame.transform.scale(display, (600, 800))
                    x = picture_rect.center[0]-(size[2]/2)
                    y = picture_rect.center[1]-((size[3]/2))
                    position = [x,y]

                    while(state):
                        state_time = time.time() - last_state_change
                        surf,state,element = fade_in_element(image,size,state,state_time,1)
                        screen.fill((0, 0, 0))
                        surf.blit(element, (0, 0))
                        screen.blit(surf, position)
                        pygame.display.flip()

                elif(tmp == "background"):
                    screen.fill((0,0,0))
                    display = pygame.image.load('bridge.jpg')
                    x = 0
                    y = 0
                    position = [x,y]
                    screen.blit(display,position)

                elif(tmp == "text"):
                    color = pygame.Color(44,130,155)
                    state = True    
                    text_list = text.replace(u'\uff0c', ",").split(",")  
                    x = 200
                    y = 200
                    fontsize = 70
                    screen.fill(color)                   
                    for text_temp in text_list:
                        last_state_change = time.time()
                        print(text_temp)
                        state = True  
                        Text,Rect = showText(text_temp,fontsize)
                        y += (fontsize+20) 
                        while(state):
                            state_time = time.time() - last_state_change                            
                            surf,state,element = fade_in_element(Text,Rect,state,state_time,2)
                            surf.fill((44,130,155))
                            surf.blit(Text, (0, 0))
                            position = [x,y]
                            screen.blit(surf, position)
                            pygame.display.flip()

        if display_first:
            screen.blit(display,position)
        pygame.display.flip()


# def get_data(*args):
#     socketIO.emit('res',args[0]["message"])
#     print(args[0]["message"])

# def video_socket(*args):
#     url = args[0]["url"]
#     print("url:",url)
#     playYoutube(url)
#     socketIO.emit('video',jsonify({'success':True}))

# def message_socket(*args):
#     socketIO.emit('res',args[0]["message"])
#     # print(args[0]["message"])

# def music_socket(*args):
#     # socketIO.emit('res',args[0]["message"])
#     # print(args[0]["message"])

# def image_socket(*args):
#     # socketIO.emit('res',args[0]["message"])
#     # print(args[0]["message"])

# def background_socket(*args):
#     # socketIO.emit('res',args[0]["message"])
#     # print(args[0]["message"])

# def text_socket(*args):
#     # socketIO.emit('res',args[0]["message"])
#     # print(args[0]["message"])


def serverStart():
    app.run(host='0.0.0.0', port=8080,threaded=True)


def showText(tmp,fontsize):
    font = pygame.font.Font('./font/genyo-font/TW/GenYoMinTW-Medium.ttf', fontsize)
    color = pygame.Color(48, 48, 48)
    Text = font.render(tmp, True, color)
    Rect = Text.get_rect()
    print(Rect)
    return Text,Rect


def socketStart():
    global socketIO
    target_url = '192.168.31.123'
    socketIO = SocketIO( target_url, 3000, LoggingNamespace)
    print('Started')

    socketIO.emit('test','test')
    socketIO.on('test', get_data)

    socketIO.on('video', video_socket)
    socketIO.on('quit', quit_socket)
    socketIO.on('message', message_socket)
    socketIO.on('music', music_socket)
    socketIO.on('image', image_socket)
    socketIO.on('background', background_socket)
    socketIO.on('text', text_socket)

    socketIO.wait()



if __name__ == "__main__":
    
    thread_server = threading.Thread(target=serverStart)
    thread_server.daemon = True
    thread_server.start()

    # thread_read   = threading.Thread(target=readData)
    # thread_read.daemon = True
    # thread_read.start()

    thread_backgroud = threading.Thread(target=backgroundDsiplay)
    thread_backgroud.daemon = True
    thread_backgroud.start()
    
    # thread_socket = threading.Thread(target=socketStart)
    # thread_socket.daemon = True
    # thread_socket.start()

    while True:
        time.sleep(1)
