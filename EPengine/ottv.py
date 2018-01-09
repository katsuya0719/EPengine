import pandas as pd

class Base():
    def __init__(self,csv):
        df=pd.read_csv(csv,encoding='utf8')
        self.df=df

    def group(self,agg_method):
        df=self.df
        grouped=df.groupby(['Tilt [deg]', 'Azimuth [deg]'],as_index=False)
        groupdf=grouped.agg(agg_method)
        groupdf=groupdf[pd.to_numeric(groupdf['Azimuth [deg]'], errors='coerce').notnull()]

        self.group=groupdf

    def addDirection(self):
        group=self.group
        group['component'] = group['Tilt [deg]'].apply(checkTilt)
        group['direction']=group['Azimuth [deg]'].apply(getDirection)
        self.group=group

    def finalize(self,agg_method):
        group=self.group
        wall = group[group['component'] == "Wall"]
        roof = group[group['component'] == "Roof"]
        wall = wall.groupby(['direction'], as_index=False)
        wall=wall.agg(agg_method)
        roof = roof.agg(agg_method)
        roof=pd.DataFrame(roof).T
        roof["direction"]="Roof"
        #change NaN to 0
        roof=roof.fillna(0)
        return wall,roof

class Glass(Base):
    def temp(self):
        pass

class Opaque(Base):
    def group(self,agg_method):
        df=self.df

        df.iloc[:,2:8] = df.iloc[:,2:8].apply(pd.to_numeric, errors='coerce')
        grouped=df.groupby(['Tilt [deg]', 'Azimuth [deg]'],as_index=False)
        groupdf=grouped.agg(agg_method)

        self.group=groupdf

"""
    def finalize(self,agg_method):
        group=self.group
        #divide into two group
        wall=group[group['component']=="Wall"]
        floor=group[group['component']=="Floor"]
        roof=group[group['component']=="Roof"]

        wall=wall.groupby(['direction'],as_index=False)
        wall = wall.agg(agg_method)
        floor = floor.agg(agg_method)
        roof = roof.agg(agg_method)

        return wall,roof,floor
"""

def checkTilt(str):
    angle=float(str)
    if angle<30:
        return "Roof"
    elif angle >160:
        return "Floor"
    else:
        return "Wall"

def getDirection(str):
    #print(str)
    angle=float(str)
    if angle<11.25 or angle>=348.75:
        return "N"
    elif angle<33.75 and angle>=11.25:
        return "NNE"
    elif angle<56.25 and angle>=33.75:
        return "NE"
    elif angle<78.75 and angle>=56.25:
        return "ENE"
    elif angle<101.25 and angle>=78.75:
        return "E"
    elif angle<123.75 and angle>=101.25:
        return "ESE"
    elif angle<146.25 and angle>=123.75:
        return "SE"
    elif angle<168.75 and angle>=146.25:
        return "SSE"
    elif angle<191.25 and angle>=168.75:
        return "S"
    elif angle<213.75 and angle>=191.25:
        return "SSW"
    elif angle<236.25 and angle>=213.75:
        return "SW"
    elif angle<258.75 and angle>=236.25:
        return "WSW"
    elif angle<281.25 and angle>=258.75:
        return "W"
    elif angle<303.75 and angle>=281.25:
        return "WNW"
    elif angle<326.25 and angle>=303.75:
        return "NW"
    elif angle<348.75 and angle>=326.25:
        return "NNW"

def tabulize(vertGlass,horiGlass,wall,roof):

    vertical=pd.merge(vertGlass,wall,on="direction")
    horizontal=pd.merge(horiGlass,roof,on="direction")

    df=vertical.append(horizontal)

    before_col=["direction","Area of Multiplied Openings [m2]","Glass SHGC","Glass U-Factor [W/m2-K]","Glass Visible Transmittance","Gross Area [m2]","U-Factor with Film [W/m2-K]","Reflectance","U-Factor no Film [W/m2-K]"]
    after_col=["Direction","Glass Area[m2]","Glass SC","Glass U-value[W/m2-K]","Glass VLT","Opaque Area[m2]","U-value with Film[W/m2-K]","Opaque Reflectance","U-value without Film[W/m2-K]"]
    for before,after in zip(before_col,after_col):
        df.rename(columns={before:after},inplace=True)
    df=SHGCtoSC(df)

    return df
    #print (df)


def SHGCtoSC(df):
    df["Glass SC"]=df["Glass SC"]/0.87
    return df

def ottv(df,alpha=0.7):
    df["WWR[%]"]=df["Glass Area[m2]"]/(df["Glass Area[m2]"]+df["Opaque Area[m2]"])*100
    df["glass_numer"]=df["Glass Area[m2]"]*df["Glass SC"]*df["Direction"].apply(windowCoef)#will add esm later
    df["wall_numer"] = df["Opaque Area[m2]"] * df["U-value with Film[W/m2-K]"] * alpha*df["Direction"].apply(wallCoef)
    df["OTTV"]=(df["glass_numer"]+df["wall_numer"])/(df["Glass Area[m2]"]+df["Opaque Area[m2]"])
    df["Total_Area[m2]"]=df["Glass Area[m2]"]+df["Opaque Area[m2]"]
    numer=df["OTTV"]*df["Total_Area[m2]"]

    value=sum(numer)/sum(df["Total_Area[m2]"])

    df = tidydf(df)

    return value,df

def tidydf(df):
    df["Glass Area[m2]"]=df["Glass Area[m2]"].astype(float)
    df.index=df["Direction"]
    del df["Direction"]
    del df["glass_numer"]
    del df["wall_numer"]
    decimals=pd.Series([0,2,1,2,0,2,2,2,1,1,0], index=["Glass Area[m2]","Glass SC","Glass U-value[W/m2-K]","Glass VLT","Opaque Area[m2]","Opaque Reflectance","U-value without Film[W/m2-K]","U-value with Film[W/m2-K]","WWR[%]","OTTV","Total_Area[m2]"])
    temp=df.round(decimals)
    temp1=temp.ix[:,["WWR[%]","OTTV","Total_Area[m2]","Glass SC","Glass U-value[W/m2-K]","Glass VLT","Glass Area[m2]","U-value with Film[W/m2-K]","Opaque Reflectance","Opaque Area[m2]"]]
    return temp1

def wallCoef(direction):
    et={"N":2.72,"NNE":3.30,"NE":3.86,"ENE":4.44,"E":5.01,"ESE":4.65,"SE":4.3,"SSE":3.95,"S":3.6,"SSW":3.92,"SW":4.23,"WSW":4.29,"W":4.35,"WNW":3.94,"NW":3.54,"NNW":3.13,"Roof":13.37}
    return et[direction]


def windowCoef(direction):
    sf={"N":104,"NNE":121,"NE":138,"ENE":153,"E":168,"ESE":183,"SE":197,"SSE":194,"S":191,"SSW":197,"SW":202,"WSW":189,"W":175,"WNW":157,"NW":138,"NNW":121,"Roof":264}
    return sf[direction]

def main(glasspath,opaquepath):
    glass = Glass(glasspath)
    glass_agg = {'Glass Visible Transmittance': 'mean', 'Glass SHGC': 'mean', 'Glass U-Factor [W/m2-K]': 'mean',
                 'Area of Multiplied Openings [m2]': 'sum'}
    glass.group(glass_agg)
    glass.addDirection()
    vertGlass, HoriGlass = glass.finalize(glass_agg)

    opaque = Opaque(opaquepath)
    opaque_agg = {'Reflectance': 'mean', 'U-Factor with Film [W/m2-K]': 'mean', 'U-Factor no Film [W/m2-K]': 'mean',
                  'Gross Area [m2]': 'sum'}
    opaque.group(opaque_agg)
    opaque.addDirection()
    wall, roof = opaque.finalize(opaque_agg)

    table = tabulize(vertGlass, HoriGlass, wall, roof)

    value, df = ottv(table)

    return value,df

if __name__ == '__main__':
    glasspath="C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\Glass.csv"
    #glass=Glass("E:\\Reference\\Programming\\Python\\DjangoEP-master\\static\\csv\\lukhop\\Glass.csv")
    #wall=Wall("E:\\Reference\\Programming\\Python\\DjangoEP-master\\static\\csv\\lukhop\\Opaque.csv")
    opaquepath="C:\\Users\\obakatsu\\Dropbox\\JS\\csv\\lukhop\\Opaque.csv"

    value,df=main(glasspath,opaquepath)

    print(df)
    print(value)