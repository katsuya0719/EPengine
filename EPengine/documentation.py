from parseidf import parseIDF
from collections import OrderedDict
import pandas as pd
import numpy as np

#for BEAM and LEED documentation
class Base():
    def __init__(self,idf):
        self.idf=idf

    def loadInfo(self):
        idf=self.idf
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
        objdict = OrderedDict(data)
        parsed = parseIDF(idf)
        # print (parsed)
        idfObj = parsed.readidf(objdict)
        #print(idfObj)
        tables=self.convertTable(idfObj,data)
        #print(tables)
        # parsed.export(json, dest)
        # return parsed

    def convertTable(self,obj,data):
        #print ("convert!")
        colDict=dict(data)
        tableDict={}
        for key in obj.keys():
            df1=pd.DataFrame(obj[key])
            df2=df1.replace(r'\s+', np.nan, regex=True)
            df2.columns=colDict[key]
            tableDict[key]=df2

        print (tableDict)

if __name__ == '__main__':
    # Extract Input information
    path = "C:\\Users\\obakatsu\\Dropbox\\LHS\LEED_Submission\\case2\\case2exp.idf"
    BEAM=Base(path)
    BEAM.loadInfo()