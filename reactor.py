ComponentNumbers=14
time_index=4*24
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
        self.inflow=self.feed['Q'][self.time]/time_index
        
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
        self.kin_paras=[0]*14
        #self.kin_paras[0]=Ks
        #self.kin_paras[1]=μH
        #self.kin_paras[2]=KNO
        #self.kin_paras[3]=KOH
        #self.kin_paras[4]=bH
        #self.kin_paras[5]=ηg
        #self.kin_paras[6]=ηh
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
        
    def set_kin_paras(self,i,para):
        self.kin_paras[i]=para
        
    def set_sto_paras(self,i,para):
        self.sto_paras[i]=para
        
    def add_upstream(self, discharger, branch='Main'):
            #Add a single upstream unit to the bioreactor
            if branch == 'Main':
                self.inlet.update({discharger.name: discharger.get_outflow_main()})

            elif branch == 'Side':
                self.inlet.update({discharger.name: discharger.get_outflow_side()})
    def add_downstream(self, receiver, branch='Main'):
             #Add a single downstream unit to the bioreactor
            if branch == 'Main':
                self.outlet.update({receiver.name: self.get_outflow_main()})

            elif branch == 'Side':
                self.outlet.update({receiver.name: self.get_outflow_side()})
                
    def mix(self,discharger):
        # Mix up the contaminants
        flux=self.inlet[discharger.name]
        for i in range (ComponentNumbers):
            self.eff_comps[i]=(self.eff_comps[i]*(self.volumn-flux)+flux*discharger.eff_comps[i])/self.volumn
            
    def biodegrade(self):
        ρ1=self.kin_paras[1]*self.eff_comps[1]/(self.eff_comps[1]+self.kin_paras[0])*self.eff_comps[7]/(self.eff_comps[7]+self.kin_paras[3])*self.eff_comps[4]
        ρ2=self.kin_paras[1]*self.eff_comps[1]/(self.eff_comps[1]+self.kin_paras[0])*self.kin_paras[3]/(self.eff_comps[7]+self.kin_paras[3])*self.eff_comps[8]/(self.eff_comps[8]+self.kin_paras[2])*self.kin_paras[5]*self.eff_comps[4]
        ρ3=self.kin_paras[9]*self.eff_comps[9]/(self.eff_comps[9]+self.kin_paras[10])*self.eff_comps[7]/(self.eff_comps[7]+self.kin_paras[12])*self.eff_comps[5]
        ρ4=self.kin_paras[4]*self.eff_comps[4]
        ρ5=self.kin_paras[13]*self.eff_comps[5]
        ρ6=self.kin_paras[11]*self.eff_comps[10]*self.eff_comps[4]
        ρ7=self.kin_paras[7]*self.eff_comps[3]/self.eff_comps[4]/(self.kin_paras[8]+self.eff_comps[3]/self.eff_comps[4])*(self.eff_comps[7]/(self.eff_comps[7]+self.kin_paras[3])+self.kin_paras[6]*(self.kin_paras[3]/(self.eff_comps[7]+self.kin_paras[3])*self.eff_comps[8]/(self.eff_comps[8]+self.kin_paras[2]))*self.eff_comps[4]
        ρ8=ρ7*self.eff_comps[11]/self.eff_comps[3]
        r=[0]*ComponentNumbers
        r[0]=0
        r[1]=ρ7-ρ1/self.sto_paras[1]-ρ2/self.sto_paras[1]
        r[2]=0
        r[3]=(1-self.sto_paras[3])*(ρ4+ρ5)-ρ7
        r[4]=ρ1+ρ2-ρ4
        r[5]=ρ3-ρ5
        r[6]=self.sto_paras[3]*(ρ4+ρ5)
        r[7]=-(1-self.sto_paras[1])/self.sto_paras[1]*ρ1-(4.57-self.sto_paras[0])/self.sto_paras[0]*ρ3
        r[8]=-(1-self.sto_paras[1])/2.86/self.sto_paras[1]*ρ2+ρ3/self.sto_paras[0]
        r[9]=-self.sto_paras[2]*ρ1-self.sto_paras[2]*ρ2-(self.sto_paras[2]+1/self.sto_paras[0])*ρ3+ρ6
        r[10]=ρ8-ρ6
        r[11]=(self.sto_paras[2]-self.sto_paras[3]*self.sto_paras[4])(ρ4+ρ5)-ρ8
        r[12]=-self.sto_paras[2]*ρ1/14+((1-self.sto_paras[1])/(14*2.86*self.sto_paras[1])-self.sto_paras[2]/14)*ρ2-(self.sto_paras[2]/14+1/7/self.sto_paras[0])*ρ3+ρ6/14
        r[13]=0
        for i in range (ComponentNumbers):
            self.eff_comps[i]=self.eff_comps[i]+r[i]/time_index
        self.time=self.time+1
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
    A.mix()
    B.mix()
    C.mix()
    D.mix()
    E.mix()
    A.biodegrade()
    B.biodegrade()
    C.biodegrade()
    D.biodegrade()
    E.biodegrade()
    Clarifier.update_inflow1(E)
    Clarifier.update_outflow_main()
    Influent.time=Influent.time+1
    print(Clarifier.get_outflow_main())

    
    


            
