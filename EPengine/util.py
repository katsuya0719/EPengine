#from eppy.useful_scripts import doc_images
import pandas as pd
import numpy as np

def combine_csv(csv1,csv2,col1,ix):
    df1=pd.read_csv(csv1,usecols=col1)
    df2=pd.read_csv(csv2)
    df1=fillempty(df1,1)

    df1=change_index(df1,ix)
    #change data format
    df1[col1[1]]=df1[col1[1]].astype('float')
    print (df1)
    df2=change_index(df2,ix)
    #print (df1)

    df=pd.merge(df2, df1, left_index=True, right_index=True, how='left')
    print (df)
    return df

def fillempty(df,num):
    df=df.replace(r'^\s+', np.nan, regex=True)
    df=df.fillna(num)
    return df

def change_index(df,col):
    df.index=df[col]
    del df[col]

    return df

def div_multiplier(path,data,col2):
    csv1=path+data[0]
    csv2=path+data[1]
    col1 = ["Unnamed: 0", "Multipliers"]
    index = "Unnamed: 0"
    df = combine_csv(csv1, csv2, col1, index)
    new_col=col2+"_floor"
    df[new_col]=df[col2]/df["Multipliers"]
    return df

if __name__ == '__main__':
    #path1="C:\\Users\\obakatsu\\Dropbox\\JS\\csv\kls\\Zone.csv"
    #path2 = "C:\\Users\\obakatsu\\Dropbox\\JS\\csv\kls\\HeatBalance.csv"
    path="E:\\Reference\\Programming\\Python\\DjangoEP-master\\data\\html\\KingLamSt_Proposed15\\"
    data=["Zone.csv","HeatBalance.csv"]
    col2='Window Heat Addition [kWh]'
    df=div_multiplier(path,data,col2)

    df.to_csv("HeatBalance.csv")