import datetime
import m3u8
from os.path import join
import subprocess

playlistFilename = '505944491.m3u8'
pl = m3u8.load(playlistFilename)


def getSegmentByTime(dt):
    '''Получаем нужный сегмент из плейлиста и времени dt'''
    h = dt.hour
    m = dt.minute
    s = dt.second
    sTotal = (h * 60 + m) * 60 + s

    ssum = 0
    for seg in pl.segments:
        ssum = ssum + seg.duration
        if ssum > sTotal:
            lastdur = seg.duration
            break
    else:
        print('segment не найден')
    lastdur = lastdur - (ssum - sTotal)
    return seg.uri, lastdur



t = '02:56:22'
t = datetime.datetime.strptime(t, '%H:%M:%S')
res = getSegmentByTime(t)
print(res)

# open
dirf = 'F:\\moments\\505944491'
cmd = '"' + join(dirf, res[0]) + '"'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = proc.stdout.readlines()
