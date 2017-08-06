from eppy import modeleditor
from eppy.modeleditor import IDF
from chiller import visBiquadratic

class parseIDF():
    def __init__(self,idf):
        #idd="data/EP/idd/Energy+V7_2_0.idd"
        idd = "data/EP/idd/Energy+V8_7_0.idd"
        IDF.setiddname(idd)
        self.idf = IDF(idf)

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

        return objList

   # def plot(self,objs):


if __name__ == '__main__':
    idf="data/EP/idf/AirCooledChiller.idf"
    #idf="data/EP/idf/smallidf.idf"
    objects=['Chiller:Electric:EIR','Curve:Biquadratic','Curve:Quadratic']
    attributes=["Name","Coefficient1_Constant","Coefficient2_x","Coefficient3_x2","Coefficient4_y","Coefficient5_y2","Coefficient6_xy"]
    #attributes = [Name, Coefficient1 Constant, Coefficient2 x, Coefficient3 x2, Coefficient4 y,Coefficient5 y2, Coefficient6 xy]
    parsed=parseIDF(idf)
    #print (parsed.idf.printidf())
    #print(parsed.idf.idfobjects['Chiller:Electric:EIR'.upper()])
    parsed.readobjs(objects)

    biquadratic=parsed.readattrs(1,attributes)
    #print (parsed.objects[0][0])
    #print(biquadratic)
    id = 125
    name=biquadratic[id][0]
    name1=name.split(" ")[3]
    cap=float(name1.split("/")[0][:-2])
    cop=float(name1.split("/")[1][:-3])
    print (cap,cop)
    #visualize result
    xrange = [4, 10]
    yrange = [24, 50]
    gsize = 0.1
    xlabel = "Chilled water leaving temperature"
    ylabel = "Entering Condenser fluid temperature"

    visBiquadratic(xrange, yrange, gsize, biquadratic[id][1:], xlabel, ylabel,name,"cop",cop)

