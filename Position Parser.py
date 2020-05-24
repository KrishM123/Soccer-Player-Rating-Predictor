import os
player_names = os.listdir('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats')
for names in player_names:
    try:
        file = open('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats\\' + names, 'r')
        file = file.read()
        file = file.split('<strong>Position:</strong>')[1]
        position = file.split('&')[0]
        try:
            position = file.split('\n')[0]
        except:
            pass
        try:
            position = position.split('(')[0]
        except:
            pass
        position = position.replace(' ', '')
        file = open('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Position\\' + names, 'w')
        file.write(position)
        print(position)
    except:
        pass
