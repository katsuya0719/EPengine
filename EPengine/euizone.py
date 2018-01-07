import pandas as pd


class Base():
    def __init__(self,csv,row):
        df=pd.read_csv(csv)
        temp=df[row]
        self.df=temp

class HVAC(Base):
    def read_energy(self,csv):
        df2=pd.read_csv(csv)
        temp = df2.iloc[:,0:3]

    def calc_coef(self):
        df=self.df
        df["Total"]=df.sum(axis=1)


if __name__ == '__main__':
    light = Base("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\Light.csv",["Zone","Consumption [kWh]"])
    cooling=HVAC("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\HeatBalance.csv",["Unnamed: 0","HVAC Zone Eq & Other Sensible Air Cooling [kWh]","HVAC Terminal Unit Sensible Air Cooling [kWh]","HVAC Input Cooled Surface Cooling [kWh]"])
    cooling.read_energy("C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\Energy.csv")
    cooling.calc_coef()