class Check():
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def alass(self):
        return ('he is %s ,age:%s, It\'s very good !'%(self.name,self.age))

#tim=Check('jx','22')
#tim.alass()

class No_class(Check):
    pass


tim=No_class('jx','22')
print(tim.alass())