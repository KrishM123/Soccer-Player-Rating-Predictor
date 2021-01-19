import urllib.request, urllib.error, urllib.parse
import os


def getDir(link, path):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=link, headers=headers)
    player_dir = urllib.request.urlopen(req).read()

    f = open(path, 'wb')
    f.write(player_dir)
    f.close


def getRating(name):
    pname = name.split(' ')[0:-1]
    temp = ''
    for pos in range(0, len(pname)):
        temp += pname[pos]
        if pos == 0:
            temp += '+'
        else:
            temp += '-'
    pname = temp[:-1]
    year = 'fifa' + name[-6:-4]
    link = 'https://www.fifaindex.com/players/' + year + '/?name=' + pname
    print(link)
    getDir(link, 'C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\main.txt')
    main_file = open('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\main.txt', encoding="utf8").read()
    link = main_file.split('<td data-title="Name"><a href="')[1].split('"')[0]
    link = 'https://www.fifaindex.com/' + link
    getDir(link, 'C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\\new.txt')
    new = open('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\\new.txt', encoding="utf8").read()
    rating = \
    new.split(pname.replace('+', ' ') + '<span class="float-right"><span class="badge badge-dark rating r')[1].split(
        '<')[0][3:]
    return rating


folders = os.listdir('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats')
existing = os.listdir('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Ratings')
for folder in folders:
    player_names = os.listdir('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats\\' + folder)
    for name in player_names:
        try:
            if name not in existing and '-' in name:
                rating = getRating(name)
                if rating is not None:
                    file = open('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Ratings\\' + name, 'w')
                    file.write(rating)
                    file.close()
                else:
                    os.rename('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats\\' + folder + '\\' + name, 'C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Failed\\' + name)
        except:
            #os.rename(
            #    'C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats\\' + folder + '\\' + name,
            #    'C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Failed\\' + name)
            pass