from eppy import modeleditor
from eppy.modeleditor import IDF
from chiller import visBiquadratic,visQuadratic
import json

class parseIDF():
    def __init__(self,idf):
        #idd="data/EP/idd/Energy+V7_2_0.idd"
        idd = "data/EP/idd/Energy+V8_7_0.idd"
        IDF.setiddname(idd)
        self.idf = IDF(idf)

    def readidf(self,dict):
        """
        read idf file and extract requested object and attributes
        :param dict:
        :return:
        """
        idf=self.idf
        strobjs=list(dict.keys())
        attrs=list(dict.values())
        #print(strobjs)
        #print(attrs)
        self.readobjs(strobjs)
        result={}
        for i in range(0,len(strobjs)):
            print(strobjs)
            attrList=self.readattrs(i,attrs[i])
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
                attrList.append(obj[attr])

            objList.append(attrList)

        if dict==True:
            pass
        else:
            return objList

   # def plot(self,objs):

    def export(self,format="json"):
        """
        export all the data included in the class
        """
        objs=self.objects
        #Json=json.dumps(objs)
        #f=open("test.json","w")
        #f.write(Json)
        #f.close()




if __name__ == '__main__':
    #idf="data/EP/idf/AirCooledChiller.idf"
    #idf="data/EP/idf/smallidf.idf"
    #extract geometry information
    idf="data\\Nantou\\Design\\151221_ReviseWWR\\output.idf"
    #objects=['Zone','BuildingSurface:Detailed','FenestrationSurface:Detailed','Shading:Building:Detailed']
    attrZone = ["Name", "Multiplier", "Ceiling_Height", "Volume"]
    attrSurface=["Construction_Name","Zone_Name","Vertex_1_Xcoordinate","Vertex_1_Ycoordinate","Vertex_1_Zcoordinate","Vertex_2_Xcoordinate","Vertex_2_Ycoordinate","Vertex_2_Zcoordinate","Vertex_3_Xcoordinate","Vertex_3_Ycoordinate","Vertex_3_Zcoordinate","Vertex_4_Xcoordinate","Vertex_4_Ycoordinate","Vertex_4_Zcoordinate",]
    attrShading=attrSurface[2:]
    objdict = {'Zone':attrZone,'BuildingSurface:Detailed':attrSurface, 'FenestrationSurface:Detailed':attrSurface, 'Shading:Building:Detailed':attrShading}
    parsed=parseIDF(idf)
    test=parsed.readidf(objdict)
    print(test)
    #parsed.readobjs(objects)
    #biquadratic = parsed.readattrs(1, attrbiquad)
    #parsed.export()


    #reading chiller performance curve and visualize
    """
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