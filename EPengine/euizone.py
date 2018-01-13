import pandas as pd
import numpy as np
from functools import reduce

class Base():
    """
    this can work only for electricity
    """
    def __init__(self,csv,row):
        df=pd.read_csv(csv)
        temp=df[row]
        temp.index=df[row[0]]
        del temp[row[0]]
        self.df=temp

class Chiller(Base):
    def read_energy(self,csv,key):
        df2=pd.read_csv(csv)
        temp = df2.iloc[:,0:3]
        temp2=temp[temp["Unnamed: 0"]==key]
        self.energy=float(temp2["Electricity [kWh]"])

    def calc_eui(self):
        df=self.df
        col=df.columns
        df["Total"]=df.sum(axis=1)
        df["coef"]=df["Total"]/df["Total"].sum()
        df["consumption[kWh]"]=pd.Series(df["coef"])*self.energy
        #df=df.drop(col,axis=1)
        df1=pd.DataFrame(df["consumption[kWh]"],index=df.index)
        return df1

class SP(Base):
    pass

class HVAC(Chiller):
    """
    This is rough calculation. Has to be elaborated more in detail.
    Include Fans,Pumps,Heat Rejection, Humidification, Heat Recovery
    """
    def read_energy(self,csv,key):
        df2=pd.read_csv(csv)
        df2=df2.replace(r'^\s+', np.nan, regex=True)
        df2=df2.fillna(method='pad')

        df2.index=df2["Unnamed: 0"]

        del df2["Unnamed: 0"]

        temp = df2.loc[key,["Subcategory","Electricity [kWh]"]]

        temp1=self.filter_sub(temp)
        self.energy=float(temp1["Electricity [kWh]"].sum())
        print (self.energy)

    def filter_sub(self,df):
        """
        Currently, the logic is very simple. This should be sophisticated.
        :return:
        """
        temp=df[df["Subcategory"]=="General"]
        return temp

def agg_df(dfList,prefix):
    dfList2=[]

    for i in range(0,len(dfList)):
        dfList2.append(dfList[i].add_prefix(prefix[i]))

    temp=reduce(lambda left,right:pd.merge(left,right,left_index=True,right_index=True,how='outer'),dfList2)
    df=temp.fillna(0)
    df["Total Consumption[kWh]"]=df.sum(axis=1)

    return df

def zone_eui(path):
    light = Base(path+"\\Light.csv", ["Zone", "Consumption [kWh]"])
    df_light = light.df
    area = Base(path+"\\Light.csv", ["Zone", "Zone Area [m2]"])
    df_area = area.df
    sp = SP(path+"\\HeatBalance.csv",["Unnamed: 0", "Equipment Sensible Heat Addition [kWh]"])
    df_sp = sp.df
    cooling = Chiller(path+"\\HeatBalance.csv",["Unnamed: 0", "HVAC Zone Eq & Other Sensible Air Cooling [kWh]","HVAC Terminal Unit Sensible Air Cooling [kWh]", "HVAC Input Cooled Surface Cooling [kWh]"])
    cooling.read_energy(path+"\\Energy.csv", "Cooling")
    df_cool = cooling.calc_eui()

    hvac = HVAC(path+"\\HeatBalance.csv",["Unnamed: 0", "HVAC Zone Eq & Other Sensible Air Cooling [kWh]","HVAC Terminal Unit Sensible Air Cooling [kWh]", "HVAC Input Cooled Surface Cooling [kWh]"])
    hvac.read_energy(path+"\\Energy.csv",["Fans", "Pumps", "Heat Rejection", "Humidification", "Heat Recovery"])
    df_hvac = hvac.calc_eui()

    df_energy = agg_df([df_cool, df_light, df_sp, df_hvac], ('Chiller_','Light_','Small Power_','HVAC_'))

    df=calc_eui(df_energy,df_area)

    return df

def calc_eui(energy,area):
    df=pd.merge(energy, area, left_index=True, right_index=True, how='outer')

    df["EUI [kWh/m2]"]=df["Total Consumption[kWh]"]/df["Zone Area [m2]"]
    df=df.fillna(0)
    df=df.sort_values(by=["EUI [kWh/m2]"],ascending=False)

    return df

if __name__ == '__main__':
    """
    light = Base("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\Light.csv",["Zone","Consumption [kWh]"])
    df_light=light.df
    area = Base("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\Light.csv", ["Zone", "Zone Area [m2]"])
    df_area = area.df
    sp = SP("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\HeatBalance.csv",["Unnamed: 0", "Equipment Sensible Heat Addition [kWh]"])
    df_sp = sp.df
    cooling=Chiller("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\HeatBalance.csv",["Unnamed: 0","HVAC Zone Eq & Other Sensible Air Cooling [kWh]","HVAC Terminal Unit Sensible Air Cooling [kWh]","HVAC Input Cooled Surface Cooling [kWh]"])
    cooling.read_energy("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\Energy.csv","Cooling")
    df_cool=cooling.calc_eui()

    hvac=HVAC("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\HeatBalance.csv",["Unnamed: 0","HVAC Zone Eq & Other Sensible Air Cooling [kWh]","HVAC Terminal Unit Sensible Air Cooling [kWh]","HVAC Input Cooled Surface Cooling [kWh]"])
    hvac.read_energy("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\Energy.csv", ["Fans","Pumps","Heat Rejection","Humidification","Heat Recovery"])
    df_hvac=hvac.calc_eui()

    df=agg_df([df_cool,df_light,df_sp,df_hvac],('Chiller_','Light_','Small Power_','HVAC_'))
    print (df)
    """

    df=zone_eui("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop")

    print (df)