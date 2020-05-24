import os
import tableExtractor

for name in os.listdir('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats'):
    try:
        tableExtractor.makeCSV(name, 'C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats\\')
        os.remove('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats\\' + name)
    except:
        os.remove('C:\Krish\Coding\Python Practice\Soccer Player Predictor\Data\Player Stats\\' + name)
        pass
    print('done')
