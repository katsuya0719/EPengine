import pandas as pd
import json
import numpy as np
from collections import defaultdict

def processHVAC(path):
    IES=["Chiller heat rej fans/pumps energy","Boiler space cooling energy","Boiler DHW energy","Lights energy","Chiller energy",
     "Boiler space heating energy","DHW & solar heating pump energy","System auxiliary energy","Boiler energy","Boiler space cond'g energy"]
    Dict = json.load(open(path))
    energy=defaultdict(int)
    for k1 in Dict.keys():
        for k2 in Dict[k1].keys():
            energy[k2]+=sum(Dict[k1][k2])

    df=pd.DataFrame.from_dict(energy,orient='index')
    #convert to fit to energy.csv

def processArea(path):
    Dict = json.load(open(path))
    total=sum(Dict.values())
    print (total)

def processLoad(path):
    Dict = json.load(open(path))
    Load = defaultdict(int)
    for key in


if __name__ == '__main__':
    #hvac='C:\\Users\\obakatsu\\Dropbox\\webEP\\IES\\hvac.json'
    #processHVAC(hvac)
    #area='C:\\Users\\obakatsu\\Dropbox\\webEP\\IES\\area.json'
    #processArea(area)
    load='C:\\Users\\obakatsu\\Dropbox\\webEP\\IES\\load.json'
    processArea(load)