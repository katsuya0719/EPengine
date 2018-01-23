#from eppy.useful_scripts import doc_images
import pandas as pd

def combine_csv(csv1,csv2,col1,ix):
    df1=pd.read_csv(csv1,usecols=col1)
    df2=pd.read_csv(csv2)
    df1=change_index(df1,ix)
    df2=change_index(df2,ix)
    #print (df1)

    df=pd.merge(df2, df1, left_index=True, right_index=True, how='left')
    print (df)
    return df

def change_index(df,col):
    df.index=df[col]
    del df[col]

    return df

if __name__ == '__main__':
    path1="C:\\Users\\obakatsu\\Dropbox\\JS\\csv\kls\\Zone.csv"
    col1=["Unnamed: 0","Multipliers"]
    index="Unnamed: 0"
    path2 = "C:\\Users\\obakatsu\\Dropbox\\JS\\csv\kls\\HeatBalance.csv"
    df=combine_csv(path1,path2,col1,index)
    df.to_csv("HeatBalance.csv")