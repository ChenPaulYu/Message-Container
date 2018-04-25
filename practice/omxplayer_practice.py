from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

VIDEO_PATH = Path("https://r2---sn-3cgv-un5y.googlevideo.com/videoplayback?itag=22&mn=sn-3cgv-un5y%2Csn-un57en7s&mm=31%2C29&signature=E125F5AA10822F2074710540F93E20D0725557D9.59BAF69769C497523B111588727070EAC7A82E62&c=WEB&pl=22&dur=69.334&ms=au%2Crdu&initcwndbps=1012500&mv=m&sparams=dur%2Cei%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cexpire&source=youtube&ratebypass=yes&lmt=1521805008018602&requiressl=yes&ip=118.233.153.127&ei=zLvdWorbHIymqAHj47SoDg&fexp=23724337&expire=1524502572&mime=video%2Fmp4&id=o-AJjqTnLGtcgsQoKycYo9JyWAvZrLUWJnqmV1mmdRn8m1&mt=1524480881&fvip=2&ipbits=0&key=yt6")

player = OMXPlayer(VIDEO_PATH)

# sleep(5)

# player.quit()



