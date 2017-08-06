import time,datetime
import numpy as np
# noinspection PyUnresolvedReferences
import pandas as pd
# noinspection PyUnresolvedReferences
import csv
# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt
import os
from eppy.results import readhtml
import json
from datetime import  timedelta
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class ProcessHtml():
    def __init__(self,folder):
        self.folder=folder
        self.setfolder()

    def setfolder(self):
        """
        set folder and set html file
        :return:
        """
        files=os.listdir(self.folder)
        for file in files:
            print(file)
            if file.endswith('Table.html'):
                html = open((str(self.folder)+'/'+file),'r').read()
                self.htables=readhtml.titletable(html)
                name=file[0:-10]+'.csv'

    def extract_html(self):
        htables=self.htables
        if len(htables)==1:
            self.extract_comf()
        else:
            self.extract_basic()

    def extract_comf(self):
        htables=self.htables

        comf=self.convert_df(htables[0][1])
        value=[comf]
        k=["comfortable"]
        self.db=dict(zip(k,value))
        print(self.db)

    def extract_basic(self):
        """
        extract required parameter from html file
        :return:
        """
        htables=self.htables
        print(len(htables))

        for i,html in enumerate(htables):
           print (i,html[0])

        EUI=self.convert_df(htables[0][1])
        Area=self.convert_df(htables[2][1])
        Energy=self.convert_df(htables[4][1])
        Unmet=self.convert_df(htables[11][1])
        WWR=self.convert_df(htables[13][1])
        WWRcon=self.convert_df(htables[14][1])
        ZoneSummary=self.convert_df(htables[16][1])
        ElUIcon=self.convert_df(htables[20][1])
        ElUI=self.convert_df(htables[21][1])
        Opaque=self.convert_df(htables[24][1])
        Glazing=self.convert_df(htables[25][1])
        InLight=self.convert_df(htables[30][1])
        Fan=self.convert_df(htables[39][1])
        Pump=self.convert_df(htables[40][1])
        HW=self.convert_df(htables[41][1])
        Cooling=self.convert_df(htables[42][1])
        Heating=self.convert_df(htables[43][1])
        UnmetDetail=self.convert_df(htables[49][1])
        OAaverage=self.convert_df(htables[50][1])
        OAmin=self.convert_df(htables[51][1])
        HVAC=self.convert_df(htables[53][1])


        self.HeatBalance=self.convert_df(htables[63][1])

        value=[EUI,Area,Energy,Unmet,WWR,WWRcon,ZoneSummary,ElUIcon,ElUI,Opaque,Glazing,InLight,Fan,Pump,HW,Cooling,Heating,UnmetDetail,OAaverage,OAmin,HVAC,self.HeatBalance]
        k=["EUI","Area","Energy","Unmet","WWR","WWRcon","Zone","ElUIcon","ElUI","Opaque","Glass","Light","Fan","Pump","HW","Cooling","Heating","UnmetDetail","OAaverage","OAmin","HVAC","HeatBalance"]
        self.db=dict(zip(k,value))

    def convert_df(self,html):
        col=html[0]
        df=pd.DataFrame(list(html))
        ix=df.iloc[:,0]
        df.columns=col
        #print (df.columns)
        df.index=ix
        #df.drop('',axis=1)
        return df

    def export_csv(self,arr):
        #Zone=self.ZoneSummary
        #HB=self.HeatBalance)

        df=pd.concat(arr,axis=1,join='inner')
        #print (df)
        return df

    def extract_col(self,df,keys):
        col=df.columns
        ix=df.index
        #print (ix)
        new=[]
        for str in col:
            for key in keys:
                if str.count(key):
                    new.append(str)
                    break
        df1=df[new]

        room=pd.DataFrame(ix,index=ix)
        #print(room)
        df1.index=ix
        df2=pd.concat([room,df1],axis=1)
        df2.iloc[0,0]="room"
        return df2

    def export_json(self,file):
        Area=self.Area
        WWR=self.WWR
        Opaque=self.Opaque


        dict_area=self.convert_dict2(Area,[1,2],0)
        dict_wwr=self.convert_dict2(WWR,[4,5],0)
        #dict_opaque=self.convert_dict2(Opaque,[0:])

        dict_area.update(dict_wwr)

        f=open(file,"w")
        json.dump(dict_area,f,indent=2)

    def convert_dict1(self,eppy,parent,child):
        c_key=[]
        c_value=[]
        for i in child:
            c_key.append(eppy[i][0])
            c_value.append(eppy[i][1:])
        c_dict=dict(zip(c_key,c_value))
        print (c_dict)
        p_key=eppy[parent][1:]

        result=dict(zip(p_key,c_dict))
        return result

    def convert_dict2(self,eppy,ix,col):
        p_key=[]
        c_value=[]
        for i in ix:
            p_key.append(eppy[i][0])
            c_value.append(eppy[i][1:])

        c_key=eppy[col][1:]
        #print (c_key)
        #print (c_value)
        c_dict=[]
        for value in c_value:
            new=dict(zip(c_key,value))
            c_dict.append(new)

        #print (c_dict)
        result=dict(zip(p_key,c_dict))
        return result

    #def convert_set(self,df,key,value):


if __name__ == '__main__':
    root="C:\\Users\\obakatsu\\Documents\\Python_scripts\\EnergyPlus\\PostprocessEP\\data\\"
    #loc="Macdo\\fail\\"
    #loc="2ndPA\\T3\\"
    #loc="KingsRoad\\"
    #loc="LukHopSt\\Design\\case1\\"
    #loc="Nantou\\Design\\151221_ReviseWWR\\"
    #loc="Mitaka\\"
    #loc="LukHopSt\\BEAM\\case1\\"
    loc="LukHopSt\\1st_submission\\proposed\\case6\\"
    folder=root+loc
    strFile="output.csv"

    dest="C:\\Users\\obakatsu\\Documents\\JavaScript\\EnergyPlus\\static\csv\\"
    keyword=["Air Heating","Heat Addition"]
    #export=["Energy","Zone","Opaque","Glass"]

    case=ProcessHtml(folder)
    case.extract_html()

    if os.path.exists(dest+loc):
        pass
    else:
        os.makedirs(dest+loc)
    """This is to export heat gain for each room
    each_room=case.export_csv([case.HeatBalance])
    each_room=case.extract_col(each_room,keyword)
    each_room.to_csv(dest+loc+'heatgain.csv', encoding='utf-8',index=False,header=False)
    """

    for k,v in case.db.items():
        print(v)
        v.to_csv(dest+loc+k+'.csv', encoding='utf-8',index=False,header=False)
    """
    for k,v in case.db.items():
        for key in export:
            if k==key:
                v.to_csv(dest+loc+k+'.csv', encoding='utf-8',index=False,header=False)
    """
    #f_json="general.json"
    #files.export_json(f_json)

    print ("Finished!!!")
