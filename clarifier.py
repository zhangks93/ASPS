class clarifier():
    
    def __init__(self,name,time,volumn,total_volumn,SRT):
        self.name=name
        self.time=time 
        self.volumn=volumn
        self.outflow_main=0
        self.outflow_side=0
        self.SRT=SRT
        self.outflow_sludge=total_volumn/self.SRT/24/4
        self.inlet={}
        self.outlet={'discharge':self.outflow_main,'sludge':self.outflow_sludge}
        self.eff_comps= [0] * ComponentNumbers
        
    def add_upstream(self, discharger, branch='Main'):
            #Add a single upstream unit to the bioreactor
            if branch == 'Main':
                self.inlet.update({discharger.name: discharger.get_outflow_main()})

            elif branch == 'Side':
                self.inlet.update({discharger.name: discharger.get_outflow_side()})
    def add_downstream(self, receiver, branch='Main'):
             #Add a single downstream unit to the bioreactor
            if branch == 'Main':
                self.outlet.update({receiver.name: self.get_outflow_main})

            elif branch == 'Side':
                self.outlet.update({receiver.name: self.get_outflow_side})

    def set_SRT(self, SRT):
        self.SRT=SRT
        
    def get_outflow_main(self):
        #get the mian outflow
        return self.outflow_main
        
    def get_outflow_side(self):
        #get the side outflow
        return self.outflow_side
    
    def get_outflow_sludge(self):
        #get the side outflow
        return self.outflow_sludge
    
    def get_comps(self):
        return self.eff_comps
    
    def set_outflow_side(self,flow):
        self.outflow_side=flow
        
    def update_outflow_main(self):
        temp=0
        for a in self.inlet:
            temp=temp+self.inlet[a]
            self.outflow_main=temp-self.outflow_side-self.outflow_sludge
            


            

