# import datetime
from datetime import timedelta, datetime
import sys
import m3u8
# import /../StreamDownloader.twitch_basic as twitch
from os.path import dirname, join
import time
import re


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
            # print('Naiden start!')
            # print(seg.uri)
            lastdur = seg.duration
            break
    else:
        print('segment не найден')
    lastdur = lastdur - (ssum - sTotal)
    return seg.uri, lastdur


def WriteConfigFile(startSeg, addDurStart, lastSeg, addDurLast, momentCount, lowPrior=False):
    lp = ' LowPrior' if lowPrior else ''
    with open('ConfigFileForFFMPEG_505944491.txt', 'a', encoding='utf8') as f:
        f.write(f'{momentCount}: {startSeg}(+{addDurStart}sec) - {lastSeg}(+{addDurLast}sec){lp}\n')


def find_all(finding_str, s):
    # print(f'ищем {finding_str} в {s}')
    occurences_count = 0
    k = -1
    while True:  # if s.find(finding_str, k) == -1:
        k = s.find(finding_str, k+1)
        if k != -1:
            occurences_count += 1
        else:
            break
    # print(occurences_count)
    return occurences_count


re_smiles = r'^\d{2}:\d{2}:\d{2}\s\(\+\d*\)\s\S*\s(.*)'
folderToSaveTS = 'F:\\moments\\'
batfile = join(folderToSaveTS, '505944491', 'create_moments_505944491.bat')
configFile = 'ConfigFileForFFMPEG_505944491.txt'
momentsFileName = 'blackufa_2019-11-09_10-59_505944491_moments.txt'
momentsFileNameNew = 'blackufa_2019-11-09_10-59_505944491_moments_NEW.txt'

# --- Очищаем файлы: конфиг для FFMPEG, батник для FFMPEG
# Конфиг-файл - это файл, где указываются сегменты и смещение по времени для каждого "момента"
# батник - это файл, в котором указываются команды FFMPEG для стряпания одного видео файла из ts-сегментов
f = open(configFile, 'w', encoding='utf8')
f.write('')
f.close()
f = open(batfile, 'w')
f.write('')
f.close()

# сколько добавлять секунд в начале
secondsToPass = 10

# плейлист стрима
playlistFilename = '505944491.m3u8'
pl = m3u8.load(playlistFilename)
plUrl = dirname('https://vod-secure.twitch.tv/bc99f95b046d797d7b1b_blackufa_144049985_9052011/chunked/index-dvr.m3u8') + '/'

# for test
fff = open(momentsFileNameNew, 'w', encoding='utf8')

d_rating = {}
# Читаем moment-файл
with open(momentsFileName, 'r', encoding='utf8') as momentsFile:
    t1 = time.time()
    momentCount = 0  # счётчик моментов
    while True:
        momentCount += 1
        momentStartTime = 0
        l = momentsFile.readline()  # номер момента
        try:
            moment_number = int(l)
        except:
            moment_number = ''
        fff.write(l)
        if not l:
            break
        if l == '\n' or ' = КЛИПЫ = ' in l or l == '':
            break

        l = momentsFile.readline()  # а тут уже первая строка с моментом
        try:
            fff.write(l)
        except:
            print('ашипка')
            fff.close()

        # Время начала
        momentStartTime = l[:8]
        momentStartTime = datetime.strptime(momentStartTime, '%H:%M:%S')
        totalSec = (momentStartTime.hour * 60 + momentStartTime.minute) * 60 + momentStartTime.second
        lastTime = momentStartTime

        # Отнимаем от первого сегмента некое кол-во секунд, чтобы запечатлеть собсно сам момент :)
        if totalSec > secondsToPass:
            startTime2 = momentStartTime - timedelta(minutes=0, seconds=10)
        else:
            startTime2 = datetime.strptime('00:00:00', '%H:%M:%S')

        msgsCountInMoment = 1
        LULMessages = 0
        POGMessages = 0
        RAGEMessages = 0
        MLGMessages = 0
        rating = 0
        smiles_count_rating = 0
        LULsmiles_count_rating = 0
        pogSmiles_count = 0
        ragesmiles_count_rating = 0
        MLGsmiles_count = 0

        # идём по сообщениям момента
        while True:
            # определяем тип сообщения
            m = re.search(re_smiles, l, re.IGNORECASE)
            msg = m.group(1).upper()
            # print('msg:', msg)

            # LUL
            m2 = re.search(r'LUL|LAUGH|:D|KEKW|BSUTROLLED|OMEGAROLL|^[АХ]{3,}\)*|^ХД*\)*[\s]*', msg, re.IGNORECASE)
            if m2:
                LULMessages += 1
                LULsmiles_count_rating += find_all('LUL', msg)
                LULsmiles_count_rating += find_all('LAUGH', msg)
                LULsmiles_count_rating += find_all('KEKW', msg)
                LULsmiles_count_rating += find_all('BSUTROLLED', msg)
                LULsmiles_count_rating += find_all(':D', msg)
                LULsmiles_count_rating += find_all('OMEGAROLL', msg)
                if 'АХ' in msg:
                    if len(msg) > 9:
                        LULsmiles_count_rating += 2
                    elif len(msg) > 15:
                        LULsmiles_count_rating += 3
                    else:
                        LULsmiles_count_rating += 1
                if "ХД" in msg:
                    LULsmiles_count_rating += 0.5

            # POG
            if 'POG' in msg:
                POGMessages += 1
                pogSmiles_count += find_all('POG', msg)

            # RAGE
            m2 = re.search(r'RAGE|WUTFACE', msg, re.IGNORECASE)
            if m2:
                # print('найдено')
                RAGEMessages += 1
                ragesmiles_count_rating += find_all('RAGE', msg)
                ragesmiles_count_rating += find_all('WUTFACE', msg)
            # else:
                # print(' NE найдено')

            # MLG
            m2 = re.search(r'SEEMSGOOD|МЛЖ|MLG|МЛГ', msg, re.IGNORECASE)
            if m2:
                MLGMessages += 1
                MLGsmiles_count += find_all('SEEMSGOOD', msg)
                MLGsmiles_count += find_all('MLG', msg)
                if 'МЛГ' in msg or 'МЛЖ' in msg:
                    MLGsmiles_count += 1

            # l2 = momentsFile.readline()
            l = momentsFile.readline()
            fff.write(l)
            # если "--------", то заканчиваем обработку сообщений момента ------
            if l.find('--------') != -1 or l == '\n':
                break
            msgsCountInMoment += 1

            sLastTime = l[:8]
            lastTime = datetime.strptime(sLastTime, '%H:%M:%S')

        smiles_count_rating += LULsmiles_count_rating
        smiles_count_rating += (pogSmiles_count * 0.75)
        smiles_count_rating += (ragesmiles_count_rating * 0.5)
        smiles_count_rating += (MLGsmiles_count * 0.75)

        lastTime = lastTime + timedelta(minutes=0, seconds=1.5)
        rating = smiles_count_rating / msgsCountInMoment + msgsCountInMoment

        d_rating[moment_number] = rating

        # FOR TEST
        fff.write(f'LUL:{LULsmiles_count_rating}; POG:{pogSmiles_count}*0.75; \
RAG:{ragesmiles_count_rating}*0.5; MLG:{MLGsmiles_count}*0.75;\n\
{smiles_count_rating}, {msgsCountInMoment}, {rating}')
        fff.write('\n-----\n')


        # fff.close()
        # sys.exit()

        # --- Вычисляем сегменты .ts из плейлиста по времени
        startSeg, addDurStart = getSegmentByTime(startTime2)
        lastSeg, addDurLast = getSegmentByTime(lastTime)
        startSegNumber = int(startSeg[:-3])
        lastSegNumber = int(lastSeg[:-3])
        # print(f'{startSegNumber}.ts(+{addDurStart}) -- {lastSegNumber}.ts(+{addDurLast})')

        # --- Качаем сегменты
        '''
        for i in range(startSegNumber, lastSegNumber + 1):
            downloadUrl = plUrl + str(i) + '.ts'
            saveFileName = join(folderToSaveTS, '505944491', str(i) + '.ts')
            twitch.DownloadFile(downloadUrl, saveFileName, False)
        '''

        # WriteConfigFile(startSeg, addDurStart, lastSeg, addDurLast, momentCount, msgsCountInMoment < 3)

        # TODO: доделать обработку низкоприоритетных моментов
        # if msgsCountInMoment < 3:
        #     pass
        #     # WriteBATFileLowPrior()
        # else:
        # WriteBATFile(startSegNumber, addDurStart, lastSegNumber, addDurLast, momentCount)

        if momentCount % 10 == 0:
            print(f'{momentCount / 579 * 100}%..')

        # if momentCount > 100:
        #     sys.exit()

    list_d = list(d_rating.items())
    list_d.sort(key=lambda i: i[1])
    for msgnum, rat in list_d:
        fff.write(f'({msgnum}) : {rat}\n')

    t2 = time.time()
    print(t2 - t1, 'секунд')
    fff.close()
