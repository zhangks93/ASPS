import constant 

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
        self.sto_paras=[0]*5
        #self.sto_paras[0]=YA
        #self.sto_paras[1]=YH
        #self.sto_paras[2]=iXB
        #self.sto_paras[3]=fp
        #self.sto_paras[4]=iXP
        
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
            
    def update_inflow1(self,B):
        self.inlet[B.name]=B.get_outflow_main()
        
    def EQI(self):
        SNKj=self.eff_comps[9]+self.eff_comps[10]+self.sto_paras[2]*(self.eff_comps[4]+self.eff_comps[5])+self.sto_paras[4]*(self.eff_comps[6]+self.eff_comps[2])+self.eff_comps[11]
        TSS=0.75*(self.eff_comps[2]+self.eff_comps[3]+self.eff_comps[4]+self.eff_comps[5]+self.eff_comps[6])
        BOD=0.25*(self.eff_comps[1]+self.eff_comps[3]+(1-self.sto_paras[3])*(elf.eff_comps[4]+elf.eff_comps[5])
        COD=self.eff_comps[0]+self.eff_comps[1]+self.eff_comps[2]+self.eff_comps[3]+self.eff_comps[4]+self.eff_comps[5]+self.eff_comps[6]
        EQI=(2*TSS+COD+30*SNKj+10*self.eff_comps[8]+2*BOD)*self.get_outflow_main()
        

            

