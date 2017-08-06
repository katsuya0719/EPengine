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
import json
from datetime import  timedelta
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class ProcessCSV():
    def __init__(self,folder,strCsv):
        self.folder=folder
        self.setfolder(strCsv)

    def setfolder(self,strCsv):
        files=os.listdir(self.folder)
        for file in files:
            if file==strCsv:
                df=pd.read_csv(str(self.folder)+'/'+file)
                df.index=self.eplustimestamp(df)
                self.raw=df

    def eplustimestamp(self,simdata):
        timestampdict={}
        for i,row in simdata.T.iteritems():
            timestamp = str(2013) + row['Date/Time']
            try:
                timestampdict[i] = datetime.datetime.strptime(timestamp,'%Y %m/%d  %H:%M:%S')
            except ValueError:
                tempts = timestamp.replace(' 24', ' 23')
                timestampdict[i] = datetime.datetime.strptime(tempts,'%Y %m/%d  %H:%M:%S')
                timestampdict[i] += timedelta(hours=1)
        timestampseries = pd.Series(timestampdict)
        return timestampseries

    def extract_series(self,cols,newcols):
        """
        This method is for imported csv file
        Parameters
        ----------
        rows

        Returns
        -------

        """
        df=self.raw
        arr=[]
        colList=df.columns
        #print (colList)
        for row in cols:
            new_list = list(colList[(colList.str.endswith(row))])
            #print (new_list)
            new_df=df[new_list]
            #new_df.to_csv(row+".csv", encoding='utf-8',index=True,header=True)
            arr.append(new_df)
            #print(arr)

        dfList=self.divide_df(arr,newcols)

        #print (dfList)
        return dfList

    def divide_df(self,dfList,newcols):
        arr=[]
        rowCount=[]
        size=len(dfList)
        for df in dfList:
            rowCount.append(np.shape(df)[1])


        for i in range(min(rowCount)):
            df=pd.concat([dfList[0][[i]],dfList[1][[i]]],axis=1)
            j=2
            while j<len(dfList):
                #print (j)
                df=pd.concat([df,dfList[j][[i]]],axis=1)
                j+=1
            df.columns=newcols
            arr.append(df)

        return arr

    def export_multi_csv(self,dfList,csv_name):
        for i,df in enumerate(dfList):
            df.to_csv(csv_name+str(i)+".csv")

    def plot3d(self,dfList,size):
        """
        fig=plt.figure()
        #ax=Axes3D(fig)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter3D(df.COT,df.PLR,df.COP,s=1,c='b')
        #surf=ax.plot_trisurf(df.COT,df.PLR,df.COP,cmap=cm.jet,linewidth=0.1,vmin=1)

        ax.set_xlabel("Condenser Outlet Temperature")
        ax.set_ylabel("Part Load Ratio")
        ax.set_zlabel("COP")
        #fig.colorbar(surf, shrink=0.5, aspect=5)
        fig.savefig("test3d",dpi=200)
        plt.show()
        """
        fig=plt.figure(figsize=size)
        row=1
        for df in dfList:
            ax=fig.add_subplot(int(len(dfList)/2)+1,2,row, projection='3d')
            surf=ax.plot_trisurf(df.EIT,df.PLR,df.COP,cmap=cm.jet,linewidth=0.1,vmin=1)
            ax.set_title("chiller"+str(row))
            ax.set_ylim((0,1))
            ax.set_zlim((0,10))
            ax.set_xlabel("Evaporator Inlet Temperature")
            ax.set_ylabel("Part Load Ratio")
            ax.set_zlabel("COP")
            row+=1

        plt.show()
        #fig,axarr = plt.subplots(len(dfList),1,figsize=figsize, projection='3d')

    def plotHist(self,dfList,size):
        print (len(dfList))
        fig,axarr = plt.subplots(len(dfList),1,figsize=figsize,sharex=True,sharey=True)
        row=0
        for df in dfList:
            axarr[row].hist(df.PLR,10)
            axarr[row].set_title("chiller"+str(row+1))
            axarr[row].set_xlabel("Part Load Ratio")
            axarr[row].set_ylabel("working hour")
            axarr[row].grid(True)
            axarr[row].set_xlim((0,1))
            row+=1
        plt.show()

if __name__ == '__main__':
    root="D:\\Reference\\Programming\\Python\\EnergyPlus\\PostProcessing\\PostprocessEP\\data\\"
    #loc="Nantou\\Design\\151221_ReviseWWR\\"
    #loc="2ndPA\\T3\\"
    loc="KingsRoad\\"
    folder=root+loc
    strFile="Eq_detail.csv"
    csvFile=ProcessCSV(folder,strFile)
    #cols=["VRF Heat Pump Cooling COP [](Hourly)","VRF Heat Pump Part Load Ratio [](Hourly)","VRF Heat Pump Condenser Inlet Temperature [C](Hourly)"]
    #cols1=["COP","PLR","Temp"]
    cols=["Part Load Ratio [](Hourly)","Evaporator Inlet Temperature [C](Hourly)","Evaporator Outlet Temperature [C](Hourly)","COP [W/W](Hourly)","Condenser Inlet Temperature [C](Hourly)","Condenser Outlet Temperature [C](Hourly)"]
    cols1=["PLR","EIT","EOT","COP","CIT","COT"]
    figsize=(10,30)
    dfList=csvFile.extract_series(cols,cols1)
    csv_name="chiller_performance"
    #csvFile.export_multi_csv(dfList,csv_name)
    #csvFile.plot3d(dfList,figsize)
    csvFile.plotHist(dfList,figsize)

    print ("Finished!!!")