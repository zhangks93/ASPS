ComponentNumbers=9
import pandas as pd
class influent():
    def __init__ (self,name,time,feed_doc):
        self.name=name
        self.time=time 
        self.outflow_main=0
        self.outflow_side=0
        self.inflow=0
        self.feed=pd.read_excel(feed_doc)
        self.eff_comps= [0] * ComponentNumbers
    def add_downstream(self, receiver, branch='Main'):
             #Add a single downstream unit to the bioreactor
            if branch == 'Main':
                self.outlet.update({receiver.name: self.get_outflow_main})

            elif branch == 'Side':
                self.outlet.update({receiver.name: self.get_outflow_side})
        
    def set_comps(self,a):
        #intilaizing the contaminants in the bioreactor
        for i in range(ComponentNumbers):
            self.comps[i]=a[i]
        
    def get_outflow_main(self):
        #get the mian outflow
        return self.outflow_main
        
    def get_outflow_side(self):
        #get the side outflow
        return self.outflow_side
    
    def get_comps(self):
        return self.eff_comps
    
    def set_outflow_side(self,flow):
        self.outflow_side=flow
        
    def update_outflow_main(self):
        temp=0
        for a in self.inlet:
            temp=temp+self.inlet[a]
        self.outflow_main=temp-self.outflow_side
    def update_inflow(self):
        self.inflow=self.feed['Q'][self.time]
A=influent('influent',0,'data/bsm.xlsx')
print(A.feed['Q'][A.time])
        

    
