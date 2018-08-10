ComponentNumbers=14
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
        self.outflow_main=self.inflow-self.outflow_side
        
    def update_inflow(self):
        self.inflow=self.feed['Q'][self.time]/96
        
class bioreactor():
    def __init__ (self,name,time,volumn):
        self.name=name
        self.time=time 
        self.volumn=volumn
        self.inlet={}
        self.outlet={}
        self.outflow_main=0
        self.outflow_side=0
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
    def react(self):
        for i in range (ComponentNumbers):
            temp=0
            for a in self.inlet():
                temp=self.inlet[a]*a.get_comps()[i]
            self.comps[i]=(self.comps[i]*self.volumn-self.comps[i]*(self.get_outflow_main()+self.get_outflow_side())+temp)/self.volumn
        
    def set_comps(self,a):
        #intilaizing the contaminants in the bioreactor
        for i in range(ComponentNumbers):
            self.comps[i]=a[i]
        
    def set_DO_point(self,point):
        #adjust the dissolved oxygen point in aerated bioreactor
        self.DO_point=point
        
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
    def update_inflow1(self,B):
        self.inlet[B.name]=B.get_outflow_main()
    def update_inflow(self,B,C):
        self.inlet[B.name]=B.get_outflow_main()
        self.inlet[C.name]=C.get_outflow_side()
    def update_inflow(self,B,C,D):
        self.inlet[B.name]=B.get_outflow_main()
        self.inlet[C.name]=C.get_outflow_side()
        self.inlet[D.name]=D.get_outflow_side()

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
        self.kin_paras=[0]*14
        #self.kin_paras[0]=Ks
        #self.kin_paras[1]=μH
        #self.kin_paras[2]=KNO
        #self.kin_paras[3]=KOH
        #self.kin_paras[4]=bH
        #self.kin_paras[5]=ηg
        #self.kin_paras[6]=ηk
        #self.kin_paras[7]=kh
        #self.kin_paras[8]=Kx
        #self.kin_paras[9]=μA
        #self.kin_paras[10]=KNH
        #self.kin_paras[11]=ka
        #self.kin_paras[12]=KOA
        #self.kin_paras[13]=bA
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
        
    def EQ(self):
        SNKj=self.eff_comps[9]+self.eff_comps[10]+self.sto_paras[2]*(self.eff_comps[4]+self.eff_comps[5])+self.sto_paras[4]*(self.eff_comps[6]+self.eff_comps[2])+self.eff_comps[11]
        

Influent=influent('influent',0,'data/bsm1LT.xlsx')
A=bioreactor('Reactor1',0,1000)
B=bioreactor('Reactor2',0,1000)
C=bioreactor('Reactor3',0,1333)
D=bioreactor('Reactor4',0,1333)
E=bioreactor('Reactor5',0,1333)
Clarifier=clarifier('Clarifier',0,1000,7000,12)
A.add_upstream(Influent,'Main')
B.add_upstream(A,'Main')
C.add_upstream(B,'Main')
D.add_upstream(C,'Main')
E.add_upstream(D,'Main')
Clarifier.add_upstream(E,'Main')
for t in range(20):
    Influent.update_inflow()
    Influent.update_outflow_main()
    A.update_inflow1(Influent)
    A.update_outflow_main()
    B.update_inflow1(A)
    B.update_outflow_main()
    C.update_inflow1(B)
    C.update_outflow_main()
    D.update_inflow1(C)
    D.update_outflow_main()
    E.update_inflow1(D)
    E.update_outflow_main()
    Clarifier.update_inflow1(E)
    Clarifier.update_outflow_main()
    Influent.time=Influent.time+1
    print(Clarifier.get_outflow_main())

    
    


            
