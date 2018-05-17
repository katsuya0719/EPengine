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
import esoreader


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

class ProcessESO():
    def __init__(self,path,freq):
        self.freq=freq
        self.read(path)

    def read(self,path):
        eso=esoreader.read_from_path(path)
        self.eso=eso
        self.getKeyword()


        #print (eso.dd.variables)
        #print(eso.find_variable(search,frequency=freq))

    def getKeyword(self):
        #print (eso.dd.index)
        index=self.eso.dd.index
        keywords=set()
        for key in index.keys():
            keywords.add(key[2])

        print ("possible keyword is")
        print (keywords)

    def setdf(self,search):
        df=self.eso.to_frame(search,frequency=self.freq)
        df=self.addTime(df)

        return df

    def addTime(self,df):
        "assuming the calculation is for whole year"
        if self.freq=='Hourly':
            hours_in_year=pd.date_range('2013-01-01', '2013-12-31 T23:00', freq='H')
            temp=df.iloc[-8760:,:]
            print(len(list(hours_in_year)))
            temp.index=hours_in_year
            return temp

def make_heatmap(df,colstr):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()

    def preprocess(df,colstr):
        #temp=pd.DataFrame(df[colstr])
        df["Hour"]=df.index.hour.astype(str)
        df["Date"]=df.index.date.astype(str)
        df["DateTime"]=df.index
        temp=df.drop_duplicates(subset='DateTime')
        temp=temp[["Hour","Date",colstr]]

        return temp

    # Load the example flights dataset and conver to long-form
    temp=preprocess(df,colstr)
    hour=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

    table = temp.pivot("Date", "Hour", colstr)
    table=table.ix[:,hour]
    #table=table.sort_values(['Hour'],ascending=True)

    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(20, 5))
    #sns.heatmap(table, annot=True, fmt="d", linewidths=.5, ax=ax)
    sns.heatmap(table, linewidths=0, ax=ax,cmap="coolwarm")
    plt.show()

def multipleScatter(x,y,xlabel,ylabel,xrange=(0,1),yrange=(0,8),alpha=1,fig=(10,7),size=1):
    import matplotlib.cm as cm
    import math
    import numpy as np
    legends=[]
    for str in y.columns:
        temp=str.split(":")[0]
        legends.append(temp)

    fig=plt.figure(figsize=fig)
    ax1=fig.add_subplot(111)
    colors = cm.rainbow(np.linspace(0, 1, len(x.columns)))

    for row,color,legend in zip(range(len(x.columns)),colors,legends):

        ax1.scatter(x.iloc[:,row],y.iloc[:,row],c=color,label=legend,alpha=alpha,s=size)

    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    #in case xmax=no
    if xrange=='na':
        xmax=math.ceil(x.max().max())
        xmin=math.floor(x.min().min())
        xrange=(xmin,xmax)

    if yrange=='na':
        ymax=math.ceil(y.max().max())
        ymin=math.floor(y.min().min())
        yrange=(ymin,ymax)

    ax1.set_xlim(xrange)
    ax1.set_ylim(yrange)

    #legend=ax1.legend(loc='upper left')
    legend=ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def stackHist(df,bins,xlim=False,exclude=False,xlabel="COP"):
    """
    exclude:exclude value 0
    """
    import matplotlib.cm as cm
    from matplotlib.patches import Rectangle
    import numpy as np
    temp=[]
    colors = cm.rainbow(np.linspace(0, 1, len(df.columns)))
    labels=[]
    for col in df.columns:
        labels.append(col.split(":")[0])
        if exclude:
            temp.append(df[col][df[col]>0])
        else:
            temp.append(df[col])
    plt.hist(temp,bins=bins,stacked=True,color=colors)
    handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in colors]
    plt.legend(handles,labels,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(xlabel)
    if xlim:
        plt.xlim(xlim)
    plt.ylabel("operating hours[h]")

if __name__ == '__main__':
    #for esoreader
    #eso="C:\\Users\\obakatsu\\Dropbox\\LHS\\LEED_Submission\\Baseline\\case8\\case8exp.eso"
    eso="D:\\Projects\\Katsuya\\1701_NW_LukHopSt\\Analysis\\Energy\\result\\LEED_Submission\\Proposed\\case8\\case8.eso"
    key1="Fan"
    key2='VRF Heat Pump Cooling COP'
    key3='VRF Heat Pump Part Load Ratio'
    freq='Hourly'
    eso=ProcessESO(eso,freq)
    #fandf=eso.setdf(key1)
    copdf=eso.setdf(key2)
    plrdf=eso.setdf(key3)
    #print(fan.df)
    #make_heatmap(fandf,'SYS8 SYSTEM 12F SUPPLY FAN')
    multipleScatter(plrdf,copdf,"Part Load Ratio","COP",size=0.5)
    #stackHist(copdf,10,True)

    #for ProcessCSV
    """
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
    """