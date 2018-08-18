import constant
import pandas as pd
class influent():
    def __init__ (self,name,time,feed_doc):
        self.name=name
        self.time=time 
        self.outflow_main=0
        self.outflow_side=0
        self.inflow=0
        self.temp=15
        self.feed=pd.read_excel(feed_doc)
        self.eff_comps= [0]*constant.ComponentNumbers
        #self.eff_comps[0]=Si
        #self.eff_comps[1]=Ss
        #self.eff_comps[2]=Xi
        #self.eff_comps[3]=Xs
        #self.eff_comps[4]=Xbh
        #self.eff_comps[5]=Xba
        #self.eff_comps[6]=Xp
        #self.eff_comps[7]=So
        #self.eff_comps[8]=Sno
        #self.eff_comps[9]=Snh
        #self.eff_comps[10]=Snd
        #self.eff_comps[11]=Xnd
        #self.eff_comps[12]=Salk
        #self.eff_comps[13]=TSS
    def add_downstream(self, receiver, branch='Main'):
             #Add a single downstream unit to the bioreactor
            if branch == 'Main':
                self.outlet.update({receiver.name: self.get_outflow_main})

            elif branch == 'Side':
                self.outlet.update({receiver.name: self.get_outflow_side})
        
    def set_comps(self,a):
        #intilaizing the contaminants in the bioreactor
        for i in range(constant.ComponentNumbers):
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
        self.outflow_main=self.inflow-self.outflow_side
        
    def update_inflow(self):
        self.inflow=self.feed['Q'][self.time]/constant.time_index
    
    def update_comps(self):
        self.eff_comps=self.feed.iloc[self.time,1:15]
        self.temp=self.feed['Temp'][self.time]

    
