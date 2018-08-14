class people():
    def __init__(self,height,age,sex):
        self.height=height
        self.age=age
        self.sex=sex
    def add(self,a,b=None):
        self.height=self.height+a
        if b!=None:
            self.age=self.age+b

    def get_information(self):
        return self.height,self.age,self.sex

Jack=people(175,24,'F')
Jack.add(2,1)
Jack.add(1.5)
print(Jack.get_information())
