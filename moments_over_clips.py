import datetime
import sys
import m3u8
from StreamDownloader.twitch_basic import *
import os
import time


def GetClipV5(clipslug):
    # https://clips.twitch.tv/PowerfulEnergeticSnoodSwiftRage
    V5header = {STR_ACCEPT: HEADER_AcceptV5, STR_CLIENT: CID_streamDownloader}
    method = f'https://api.twitch.tv/kraken/clips/{clipslug}'
    j = sendRequest(method, V5header)
    # print(j)
    if 'error' in j:
        return None
    return j
    


def GetClipNew(clipslug):
    # https://clips.twitch.tv/PowerfulEnergeticSnoodSwiftRage
    VNewHeader = {STR_CLIENT: CID_streamDownloader}
    method = f'https://api.twitch.tv/helix/clips?id={clipslug}'
    j = sendRequest(method, VNewHeader)
    print(j)


def GetClipsNew(channelid, dt, cursor):
    # https://clips.twitch.tv/PowerfulEnergeticSnoodSwiftRage
    VNewHeader = {STR_CLIENT: CID_streamDownloader}
    # if cursor:
    #     cur = f'&after={cursor}'
    # else:
    #     cur = ''
    cur = f'&after={cursor}' if cursor else ''
    print('cur:', cur)
    method = f'https://api.twitch.tv/helix/clips?broadcaster_id={channelid}&first=100&started_at={dt}{cur}'
    j = sendRequest(method, VNewHeader)
    if 'error' in j:
        print(j)
    return j



vid = '505944491'
ArturID = 98742675
DSid = '494364'

# дальше по идее узнаем дату начала стрима-видоса, но мы просто подставим
startDates = '2019-11-09T10:59:14Z'
startDatedt = datetime.datetime(2019, 11, 9, 10, 59, 14)

clips = []
cursor = ''
while 1:
    j = GetClipsNew(ArturID, startDates, cursor)
    if 'data' in j:
        print('скачано', len(j['data']), 'клипов')
        clips.extend(j['data'])
    else:
        break

    if 'pagination' in j:
        if 'cursor' in j['pagination']:
            cursor = j['pagination']['cursor']
        else:
            break
print('Вышли')

print('всего клипов:', len(clips))

# выудим видосы, из которых делались все клипы в списке 
#  (чтобы потом одним запросом взять информацию о видео
#   (чтобы узнать, равянется ли название клипа = названию видео))
usedChannelVideos = []
for clip in clips:
    if clip['game_id'] == DSid:
        usedChannelVideos.append(clip['video_id'])
setVideos = set(usedChannelVideos)
print('used channel videos:', len(setVideos))
for v in setVideos:
    print(v)

print()
try:
    setVideos.remove('')
except:
    pass
try:
    setVideos.remove('\n')
except:
    pass

videosTitles = []
videosTitles.append('Профи-грузчик рейтинга "ASS" | DEATH STRANDING Марафон [HARD] ')
videosTitles.append("I'm a little ГРУЗЧИК, you know | DEATH STRANDING Марафон [HARD]") #DEATH STRANDING 100% RUN | Марафон 
videosTitles.append("DEATH STRANDING 100% RUN | Марафон ") #DEATH STRANDING 100% RUN | Марафон 
videosTitles.append("Вся игра целиком | DEATH STRANDING Марафон [HARD]") #DEATH STRANDING 100% RUN | Марафон 
videosTitles.append("[Финал] | DEATH STRANDING Марафон [HARD] ") #DEATH STRANDING 100% RUN | Марафон 
for video_id in setVideos:
    (dump, dump, videoDate, videoTitle, game, dump) = GetInfoAboutVideo(video_id)
    videosTitles.append(videoTitle)

print('videosTitles count = ', len(videosTitles))
for title in videosTitles:
    print(title)
print()

cTotal = 0
cNotOriginalName = 0
lPassedClipsByName = []
totalDur = 0

# just for test
# for clip in clips:
#     cTotal += 1
#     s = f"{cTotal}) - {clip['url']} - {clip['creator_name']} - {clip['title']} ({clip['view_count']} просмотров) - vod: {clip['video_id']} создано: {clip['created_at']}"
#     print(s)
# print('============================================')

for clip in clips:
    if clip['game_id'] == DSid and clip['video_id'] == vid:
        if clip['title'] in videosTitles:
            cNotOriginalName += 1
            lPassedClipsByName.append(clip['id'])
            continue
        cTotal += 1
        clipinfoV5 = GetClipV5(clip['id'])
        totalDur += clipinfoV5['duration']
        s = f"{cTotal}) {clipinfoV5['duration']} сек. - {clip['url']} - {clip['creator_name']} - {clip['title']} ({clip['view_count']} просмотров) - vod: {clipinfoV5['vod']['url']}"  # - создано: {clip['created_at']}
        print(s)
print('total Duration:', totalDur)
print('-------')
print()
print('кол-во пропущенных (с одинаковым названием):', cNotOriginalName)
for cl in lPassedClipsByName:
    # clipinfo = GetClipV5(cl)
    # if clipinfo['duration'] 
    # ['url'] ['offset'] ['duration']
    # print(f"пропущен клип {cl} (длит.: {clipinfo['duration']})")
    print(f"пропущен клип {cl}")



# ------------------------
# GetClipV5('PowerfulEnergeticSnoodSwiftRage')
# print('----\n')
# GetClipNew('PowerfulEnergeticSnoodSwiftRage')