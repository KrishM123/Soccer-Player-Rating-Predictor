import urllib.request, urllib.error, urllib.parse
import os


def writeHTMLPage(link, path):
    response = urllib.request.urlopen(link)
    player_dir = response.read()
    f = open(path, 'wb')
    f.write(player_dir)
    f.close

def getHTMLPage(link):
    response = urllib.request.urlopen(link)
    player_dir = response.read()
    return str(player_dir)

def getDirectoryLinks():
    writeHTMLPage('https://fbref.com/en/players/', os.path.join(os.getcwd(), 'Links', 'tempPage.txt'))
    
    filepath = os.path.join(os.getcwd(), 'Links', 'tempPage.txt')
    directories = open(filepath).read().split('<ul class="page_index">')[1].split('</ul>')[0].split('</a>&nbsp;&#183')
    filepath = os.path.join(os.getcwd(), 'Links', 'Directories.txt')
    text = open(filepath, 'w')
    for pos in range(0, len(directories)):
        directories[pos] = directories[pos][-7:-5]
        
    text.write(str(directories[:-7]))
    os.remove(os.path.join(os.getcwd(), 'Links', 'tempPage.txt'))

def getPlayerLinks():
    filepath = os.path.join(os.getcwd(), 'Links', 'Directories.txt')
    directories = str(open(filepath).read()[2:-2]).split(', ')
    for pos in range(0, len(directories)):
        directories[pos] = directories[pos].replace("'", '')

    filepath = os.path.join(os.getcwd(), 'Links', 'Players.txt')
    playerText = open(filepath, 'w')
    
    for ele in directories:
        text = str(getHTMLPage('https://fbref.com/en/players/' + ele + '/'))
        text = text.split('<div class="section_content" id="div_')[1].split('</p>\\n\\t\\t\\n  ')[0].split('<a href="/en/players/')
        text = text[1:]
        
        players = []
        names = []
        for ele in text:
            players.append(ele.split('"')[0])
            name = ele.split('/')[1].split('"')[0]
            if '-' in name:
                letters = []
                for letter in name:
                    letters.append(letter)
                name = ''
                letters[letters.index('-')] = ' '
                for letter in letters:
                    name += letter
            names.append(name)
    
        for pos in range(0, len(players)):
            playerText.write(str(players[pos].split('/')[0]) + ', ' + names[pos] + '\n')
        
def getTables(name, link):
    text = getHTMLPage(link)
    tables = []
    for ele in text.split('</thead>')[1:]:
        if '<tbody>' in ele:
            tables.append(ele.split('</tbody>')[0].replace('\\n   <tbody>\\n', '').replace('\\n\\n   ', '').replace('\\n', ''))
    
    totalSeasons = len(tables[0].replace('<tr id="stats" style="line-height: 1.3em" >', '').split('</tr>')[:-1])
    seasonalStats = [[]] * totalSeasons
    
    for pos in range(0, len(tables)):
        table = tables[pos].replace('<tr id="stats" style="line-height: 1.3em" >', '').split('</tr>')[:-1]
        stats = [[]] * len(table)
        for season in range(0, len(table)):
            row = table[season].replace('th>', 'td>').split('</td>')[:-1]
            for number in row[:-1]:
                if '</a>' in number:
                    valueToAppend = number.split('</a>')[0].split('>')[-1].replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
                else:
                    valueToAppend = number.split('>')[-1].replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
                
                try:
                    if int(valueToAppend) == float(valueToAppend):
                        valueToAppend = int(valueToAppend)
                except:
                    try:
                        valueToAppend = float(valueToAppend)
                    except:
                        pass
                
                if stats[season] == []:
                    stats[season] = [valueToAppend]
                else:
                    stats[season].append(valueToAppend)
        
        stats = stats[abs(len(stats) - len(seasonalStats)):]
        
        for row in range(0, len(stats)):
            if seasonalStats[row] == []:
                seasonalStats[row] = [stats[row]]
            else:
                seasonalStats[row].append(stats[row])
        
    temp = []
    for pos in range(0, len(seasonalStats)):
        if seasonalStats[pos][0][0] != '':
            temp.append(seasonalStats[pos])
            
    seasonalStats = temp
    
    position = text.split('<strong>Position:</strong>')[1][1:3]
    for table in range(0, len(seasonalStats)):
        filepath = os.path.join(os.getcwd(), 'Player Stats', position, name + ' ' + seasonalStats[table][0][0] + '.txt')
        player = open(filepath, 'w')
        if seasonalStats[table - 1][0][0] == seasonalStats[table][0][0]:
            for row in seasonalStats[table - 1]:
                player.write(str(row))
                player.write('\n')
            player.write('\n')
            
        for row in seasonalStats[table]:
            player.write(str(row))
            player.write('\n')
    print(name)
                
def splitPlayers(failed, totalDays):
    if failed == 'players':
        filepath = os.path.join(os.getcwd(), 'Links', 'Players.txt')
    elif failed == 'failed':
        filepath = os.path.join(os.getcwd(), 'Links', 'Failed Players.txt')
    players = open(filepath, 'r').readlines()
    totalPlayers = len(players)
    playersPerDay = int((totalPlayers - (totalPlayers % totalDays)) / totalDays)
    
    for day in range(1, totalDays + 1):
        if failed == 'players':
            filepath = os.path.join(os.getcwd(), 'Links', 'Day ' + str(day) + ' Players.txt')
        elif failed == 'failed':
            filepath = os.path.join(os.getcwd(), 'Links', 'Failed Day ' + str(day) + ' Players.txt')
        file = open(filepath, 'w')
        for player in range((day - 1) * playersPerDay, day * playersPerDay):
            file.write(players[player])
            
        if day == totalDays:
            playersLeft = totalPlayers - (playersPerDay * totalDays)
            for player in players[-playersLeft:]:
                file.write(player)
                
def getPlayerStats(failed, day):
    if failed == 'failed':
        failedFilepath = os.path.join(os.getcwd(), 'Links', 'Failed Day ' + str(day) + ' Players.txt')
        mainFailed = os.path.join(os.getcwd(), 'Links', 'Failed Players.txt')
        oldFailed = open(failedFilepath, 'r').readlines()
        if day == 1:
            open(mainFailed, 'w')
        for player in oldFailed:
            name = player.split(', ')[1].replace('\n', '')
            link = 'https://fbref.com/en/players/' + player.split(', ')[0] + '/' + name.replace(' ', '-')
            try:
                getTables(name, link)
            except:
                newFailed = open(mainFailed, 'a')
                newFailed.write(player)
                pass
    
    elif failed == 'player':
        failedFilepath = os.path.join(os.getcwd(), 'Links', 'Failed Players.txt')
        playersFilepath = os.path.join(os.getcwd(), 'Links', 'Day ' + str(day) + ' Players.txt')
        players = open(playersFilepath, 'r').readlines()
        if day == 1:
            open(failedFilepath, 'w')
        for player in players:
            name = player.split(', ')[1].replace('\n', '')
            link = 'https://fbref.com/en/players/' + player.split(', ')[0] + '/' + name.replace(' ', '-')
            try:
                getTables(name, link)
            except:
                newFailed = open(failedFilepath, 'a')
                newFailed.write(player)
                pass
            
def getRemaining():
    playersPath = os.path.join(os.getcwd(), 'Links', 'Players.txt')
    failedPath = os.path.join(os.getcwd(), 'Links', 'Failed Players.txt')
    
    players = open(playersPath, 'r').readlines()
    failed = open(failedPath, 'w')
    existing = []
    
    for folder in os.listdir(os.path.join(os.getcwd(), 'Player Stats')):
        for file in os.listdir(os.path.join(os.getcwd(), 'Player Stats', folder)):
            existing.append(file[:-14])
    
    failed = open(failedPath, 'a')
    for pos in range(0, len(players)):
        try:
            existing.index(players[pos].split(', ')[1].replace('\n', ''))
        except:
            failed.write(players[pos])
            
def fixStats():
    for folder in os.listdir(os.path.join(os.getcwd(), 'Player Stats')):
        for file in os.listdir(os.path.join(os.getcwd(), 'Player Stats', folder)):
            filePath = os.path.join(os.getcwd(), 'Player Stats', folder, file)
            playerStats = open(filePath, 'r').read().split('\n\n')
            try:
                if playerStats[0][4:5] == playerStats[1][4:5]:
                    playerStats = playerStats[0:1]
                else:
                    playerStats = playerStats[0]
                    
                playerFile = open(filePath, 'w+')
                for ele in playerStats:
                    playerFile.write(str(ele))
            except:
                pass
            print(file)
    