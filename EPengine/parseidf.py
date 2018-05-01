from eppy import modeleditor
from eppy.modeleditor import IDF
#from .chiller import visBiquadratic,visQuadratic
import json
from collections import OrderedDict
import os

class parseIDF():
    def __init__(self,idf):
        #idd="data/EP/idd/Energy+V7_2_0.idd"
        idd = "C:\\Users\\obakatsu\\Documents\\Python_scripts\\EnergyPlus\\PostprocessEP\\data\\EP\\idd\\Energy+V8_7_0.idd"
        IDF.setiddname(idd)
        self.idf = IDF(idf)

    def readidf(self,dict):
        """
        read idf file and extract requested object and attributes
        :param dict:
        :return:extracted object and attributes
        """
        idf=self.idf
        strobjs=list(dict.keys())
        attrs=list(dict.values())
        #print(strobjs)
        #print(attrs)
        self.readobjs(strobjs)
        result={}
        for i in range(0,len(strobjs)):
            attrList=self.readattrs(i,attrs[i])
            #print(strobjs[i])
            result[strobjs[i]]=attrList

        return result

    def readobjs(self,objs):
        """
        read specified objects from imported idf file and store in list
        :param objs:specify objects user want to extract
        :return:
        """
        idf=self.idf
        objlist=[]
        for obj in objs:
            new=idf.idfobjects[obj.upper()]
            objlist.append(new)

        self.objects=objlist

    def readattrs(self,objid,attrs):
        objs=self.objects[objid]
        objList=[]
        for obj in objs:
            attrList=[]
            for attr in attrs:
                #print(obj,attr)
                attrList.append(obj[attr])

            objList.append(attrList)

        if dict==True:
            pass
        else:
            return objList

   # def plot(self,objs):

    def export(self,data,dest,strFile):
        """
        export all the data included in the class
        """
        if os.path.exists(dest):
            pass
        else:
            os.makedirs(dest)

        Json=json.dumps(data)
        f=open(dest+"\\"+strFile,"w")
        f.write(Json)
        f.close()

if __name__ == '__main__':
    #idf="data/EP/idf/AirCooledChiller.idf"
    #idf="data/EP/idf/smallidf.idf"
    #idf = "data\\Nantou\\Design\\151221_ReviseWWR\\output.idf"

    #extract material information
    """
    path="C:\\Users\\obakatsu\\Dropbox\\LHS\LEED_Submission\\case2\\case2exp.idf"
    attrConstruction = ["Name", "Outside_Layer", "Layer_2", "Layer_3","Layer_4", "Layer_5", "Layer_6", "Layer_7","Layer_8", "Layer_9","Layer_10"]
    attrMaterial = ["Name", "Roughness", "Thickness", "Conductivity", "Density",
                   "Specific_Heat", "Thermal_Absorptance", "Solar_Absorptance", "Visible_Absorptance",]
    attrWindowSimple = ["Name", "Solar_Heat_Gain_Coefficient", "Visible_Transmittance"]
    data = (
    ('Construction', attrConstruction), ('Material', attrMaterial), ('WindowMaterial:SimpleGlazingSystem', attrWindowSimple))
    objdict = OrderedDict(data)
    parsed = parseIDF(path)
    #print (parsed)
    json = parsed.readidf(objdict)
    print (json)
    #parsed.export(json, dest)
    #return parsed
    """

    #extract geometry information
    """
    #objects=['Zone','BuildingSurface:Detailed','FenestrationSurface:Detailed','Shading:Building:Detailed']
    attrZone = ["Name", "Multiplier", "Ceiling_Height", "Volume"]
    attrSurface=["Zone_Name","Construction_Name","Vertex_1_Xcoordinate","Vertex_1_Ycoordinate","Vertex_1_Zcoordinate","Vertex_2_Xcoordinate","Vertex_2_Ycoordinate","Vertex_2_Zcoordinate","Vertex_3_Xcoordinate","Vertex_3_Ycoordinate","Vertex_3_Zcoordinate","Vertex_4_Xcoordinate","Vertex_4_Ycoordinate","Vertex_4_Zcoordinate",]
    attrFenestration=attrSurface[1:]
    attrShading=attrSurface[2:]
    data = (('Zone',attrZone),('BuildingSurface:Detailed',attrSurface), ('FenestrationSurface:Detailed',attrFenestration), ('Shading:Building:Detailed',attrShading))
    objdict=OrderedDict(data)
    parsed=parseIDF(idf)
    test=parsed.readidf(objdict)
    print(test["Zone"])
    parsed.export(test)
    #parsed.readobjs(objects)
    #biquadratic = parsed.readattrs(1, attrbiquad)
    #parsed.export()
    """

    #reading chiller performance curve and visualize
    """
    idf = "data/EP/idf/AirCooledChiller.idf"
    objects=['Chiller:Electric:EIR','Curve:Biquadratic','Curve:Quadratic']
    attrbiquad=["Name","Coefficient1_Constant","Coefficient2_x","Coefficient3_x2","Coefficient4_y","Coefficient5_y2","Coefficient6_xy"]
    attrquad=["Name","Coefficient1_Constant","Coefficient2_x","Coefficient3_x2"]
    parsed=parseIDF(idf)
    parsed.readobjs(objects)

    biquadratic=parsed.readattrs(1,attrbiquad)
    quadratic=parsed.readattrs(2,attrquad)

    id = 160
    qid=80
    #name=biquadratic[id][0]
    name=quadratic[qid][0]
    name1=name.split(" ")[3]
    cap=float(name1.split("/")[0][:-2])
    cop=float(name1.split("/")[1][:-3])
    print (cap,cop)
    #visualize result
    #xrange = [4, 10]
    xr = [0.15, 1]
    yrange = [24, 50]
    gsize = 0.1
    xlabel = "Chilled water leaving temperature"
    ylabel = "Entering Condenser fluid temperature"
    xl = "Part Load Ratio"
    yl="EIR"

    #visBiquadratic(xrange, yrange, gsize, biquadratic[id][1:], xlabel, ylabel,name,"cap",cap)
    visQuadratic(xr,gsize,quadratic[qid][1:],xl,yl,name)
    """