from parseidf import parseIDF
from collections import OrderedDict
import pandas as pd
import numpy as np
import json

#for BEAM and LEED documentation
class Base():
    def __init__(self):
        self.setData()

    def setData(self):
        attrLight = ["Name", "Schedule_Name", "Design_Level_Calculation_Method", "Lighting_Level",
                     "Watts_per_Zone_Floor_Area", "Watts_per_Person"]
        attrSP = ["Name", "Schedule_Name", "Design_Level_Calculation_Method", "Design_Level",
                  "Watts_per_Zone_Floor_Area",
                  "Watts_per_Person"]
        attrPeople = ["Name", "Number_of_People_Schedule_Name", "Number_of_People_Calculation_Method",
                      "Number_of_People",
                      "People_per_Zone_Floor_Area",
                      "Zone_Floor_Area_per_Person"]
        attrDFR = ["Name", "Schedule_Name", "Design_Flow_Rate_Calculation_Method", "Design_Flow_Rate",
                   "Flow_Rate_per_Zone_Floor_Area", "Flow_Rate_per_Person",
                   "Air_Changes_per_Hour", "Ventilation_Type", "Fan_Pressure_Rise", "Fan_Total_Efficiency"]
        attrFuelEquipment = ["Name", "Fuel_Use_Type", "Schedule_Name", "Design_Level"]
        attrOA = ["Name", "Outdoor_Air_Method", "Outdoor_Air_Flow_per_Person", "Outdoor_Air_Flow_per_Zone_Floor_Area",
                  "Outdoor_Air_Flow_per_Zone", "Outdoor_Air_Flow_Air_Changes_per_Hour"]
        data = (
            ('Lights', attrLight), ('ElectricEquipment', attrSP),
            ('People', attrPeople), ('ZoneVentilation:DesignFlowRate', attrDFR),
            ('Exterior:FuelEquipment', attrFuelEquipment), ('DesignSpecification:OutdoorAir', attrOA))

        self.data=data

class Save(Base):
    def __init__(self,idf):
        super().__init__()
        self.idf=idf

    def loadInfo(self,dest,strFile):
        idf=self.idf
        data=self.data

        objdict = OrderedDict(data)
        parsed = parseIDF(idf)
        # print (parsed)
        json = parsed.readidf(objdict)
        #tables=self.convertTable(idfObj,data)
        #print(tables)
        parsed.export(json, dest,strFile)
        # return parsed


class Read(Base):
    def __init__(self):
        super().__init__()

    def hvacInfo(self,plantpath,pumppath,coilpath):
        plant=pd.read_csv(plantpath)
        pump = pd.read_csv(pumppath)
        coil = pd.read_csv(coilpath)

    def loadInfo(self,loadpath):
        print (open(loadpath))
        loadDict=json.load(open(loadpath))
        tableDict=self.convertTable(loadDict)
        print (tableDict)

    def convertTable(self,obj):
        data=self.data

        colDict=dict(data)
        tableDict={}
        for key in obj.keys():
            df1=pd.DataFrame(obj[key])
            df2=df1.replace(r'\s+', np.nan, regex=True)
            df2.columns=colDict[key]
            tableDict[key]=df2

        return tableDict

if __name__ == '__main__':
    # Extract Input information
    """
    path = "C:\\Users\\obakatsu\\Dropbox\\LHS\LEED_Submission\\case2\\case2exp.idf"
    dest="C:\\Users\\obakatsu\\Documents\\Python_scripts\\Django\\DjangoEP\\data\html\\LukHopSt_LEED_1st17"
    strFile="load.json"
    BEAM=Save(path)
    BEAM.loadInfo(dest,strFile)
    """

    #Read information for visualization
    plantpath="C:\\Users\\obakatsu\\Documents\\Python_scripts\\Django\\DjangoEP\\data\\html\\LukHopSt_LEED_1st17\\Plant.csv"
    pumppath = "C:\\Users\\obakatsu\\Documents\\Python_scripts\\Django\\DjangoEP\\data\\html\\LukHopSt_LEED_1st17\\Pump.csv"
    coilpath = "C:\\Users\\obakatsu\\Documents\\Python_scripts\\Django\\DjangoEP\\data\\html\\LukHopSt_LEED_1st17\\Coil.csv"
    loadpath="C:\\Users\\obakatsu\\Documents\\Python_scripts\\Django\\DjangoEP\\data\\html\\LukHopSt_LEED_1st17\\load.json"
    BEAM=Read()
    BEAM.loadInfo(loadpath)