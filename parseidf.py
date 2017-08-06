from eppy import modeleditor
from eppy.modeleditor import IDF

class parseIDF():
    def __init__(self,idf):
        #idd="data/EP/idd/Energy+V7_2_0.idd"
        idd = "data/EP/idd/Energy+V8_7_0.idd"
        IDF.setiddname(idd)
        self.idf = IDF(idf)

    def readobjs(self,objs):
        """
        read specified objects from imported idf file and store in list
        :param objs:
        :return:
        """
        idf=self.idf
        objlist=[]
        for obj in objs:
            new=idf.idfobjects[obj.upper()]
            objlist.append(new)

        self.objects=objlist

if __name__ == '__main__':
    idf="data/EP/idf/AirCooledChiller.idf"
    #idf="data/EP/idf/smallidf.idf"
    objects=['Chiller:Electric:EIR','Curve:Biquadratic','Curve:Quadratic']
    parsed=parseIDF(idf)
    #print (parsed.idf.printidf())
    #print(parsed.idf.idfobjects['Chiller:Electric:EIR'.upper()])
    parsed.readobjs(objects)

    print(parsed.objects)


