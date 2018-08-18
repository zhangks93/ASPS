import constant
import pandas as pd

class bioreactor():
    def __init__ (self,name,time,volumn):
        self.name=name
        self.time=time 
        self.volumn=volumn
        self.inlet={}
        self.outlet={}
        self.outflow_main=0
        self.outflow_side=0
        self.KLa=1.5
        self.eff_comps= [0] * constant.ComponentNumbers
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
        self.kin_paras=[20,6.0,0.5,0.2,0.62,0.8,0.4,3,0.03,0.8,1,0.08,0.4,0.1]
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
        self.sto_paras=[0.24,0.67,0.086,0.08,0.06]
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
    def kin_paras_update(self,temp):
        #update kinetic parameters according to temperature
        self.kin_paras[1]=6*1.075**(temp-20)
        self.kin_paras[4]=0.62*1.075**(temp-20)
        self.kin_paras[7]=3*1.116**(temp-20)
        self.kin_paras[8]=0.03*1.116**(temp-20)
        self.kin_paras[9]=0.8*1.103**(temp-20)
        self.kin_paras[11]=0.08*1.072**(temp-20)
        self.kin_paras[13]=0.1*1.12**(temp-20)
        

    def biodegrade(self,temp,discharger1,discharger2=None,discharger3=None):
        #update all parameters concentration based on mass balance equations
        self.kin_paras_update(temp)
        #ρ1:Aerobic growth of heterotrophs
        ρ1=self.kin_paras[1]*self.eff_comps[1]/(self.eff_comps[1]+self.kin_paras[0])*self.eff_comps[7]/(self.eff_comps[7]+self.kin_paras[3])*self.eff_comps[4]
        #ρ2:Anoxic growth of hetertrophs
        ρ2=self.kin_paras[1]*self.eff_comps[1]/(self.eff_comps[1]+self.kin_paras[0])*self.kin_paras[3]/(self.eff_comps[7]+self.kin_paras[3])*self.eff_comps[8]/(self.eff_comps[8]+self.kin_paras[2])*self.kin_paras[5]*self.eff_comps[4]
        #ρ3:Aerobic growth of autotrophs
        ρ3=self.kin_paras[9]*self.eff_comps[9]/(self.eff_comps[9]+self.kin_paras[10])*self.eff_comps[7]/(self.eff_comps[7]+self.kin_paras[12])*self.eff_comps[5]
        #ρ4:Decay of heteroyrophs
        ρ4=self.kin_paras[4]*self.eff_comps[4]
        #ρ5:Decay of autotrophs
        ρ5=self.kin_paras[13]*self.eff_comps[5]
        #ρ6:Ammonification of soluable organic nitrogen
        ρ6=self.kin_paras[11]*self.eff_comps[10]*self.eff_comps[4]
        #ρ7:Hydrolysis of entrapped organics
        ρ7=self.kin_paras[7]*self.eff_comps[3]/self.eff_comps[4]/(self.kin_paras[8]+self.eff_comps[3]/self.eff_comps[4])*(self.eff_comps[7]/(self.eff_comps[7]+self.kin_paras[3])+self.kin_paras[6]*self.kin_paras[3]/(self.eff_comps[7]+self.kin_paras[3])*self.eff_comps[8]/(self.eff_comps[8]+self.kin_paras[2]))*self.eff_comps[4]
        #ρ8:Hydrolysis of entrapped organics nitrogen
        ρ8=ρ7*self.eff_comps[11]/self.eff_comps[3]
        print(ρ1,ρ2,ρ3,ρ4,ρ5,ρ6,ρ7,ρ8)
        #r:conversion rates
        r=[0]*constant.ComponentNumbers
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
        r[11]=(self.sto_paras[2]-self.sto_paras[3]*self.sto_paras[4])*(ρ4+ρ5)-ρ8
        r[12]=-self.sto_paras[2]*ρ1/14+((1-self.sto_paras[1])/(14*2.86*self.sto_paras[1])-self.sto_paras[2]/14)*ρ2-(self.sto_paras[2]/14+1/7/self.sto_paras[0])*ρ3+ρ6/14
        r[13]=0
        for i in range(constant.ComponentNumbers):
            r[i]=r[i]/constant.time_index
        
        if (discharger2==None and discharger3==None):
            for i in [0,1,2,3,4,5,6,8,9,10,11,12,13]:
                self.eff_comps[i]=self.eff_comps[i]+(discharger1.get_comps()[i]*discharger1.get_outflow_main()-self.eff_comps[i]*discharger1.get_outflow_main()+r[i]*self.volumn)/self.volumn
            self.eff_comps[7]=max(0.01,self.eff_comps[7]+((discharger1.get_comps()[7]*discharger1.get_outflow_main()-self.eff_comps[7]*discharger1.get_outflow_main())+r[7]*self.volumn+self.KLa*self.volumn*(8-self.eff_comps[7]))/self.volumn)
        elif (discharger3==None):
            for i in [0,1,2,3,4,5,6,8,9,10,11,12,13]:
                self.eff_comps[i]=self.eff_comps[i]+(discharger1.get_comps()[i]*discharger1.get_outflow_main()+discharger2.get_comps()[i]*discharger2.get_outflow_side()-self.eff_comps[i]*(discharger1.get_outflow_main()+discharger2.get_outflow_side())+r[i]*self.volumn)/self.volumn
            self.eff_comps[7]=max(0.01,self.eff_comps[7]+(discharger1.get_comps()[7]*discharger1.get_outflow_main()+discharger2.get_comps()[7]*discharger2.get_outflow_side()-self.eff_comps[7]*(discharger1.get_outflow_main()+discharger2.get_outflow_side())+r[7]*self.volumn+self.KLa*self.volumn*(8-self.eff_comps[7]))/self.volumn)
        else:
            for i in [0,1,2,3,4,5,6,8,9,10,11,12,13]:
                self.eff_comps[i]=self.eff_comps[i]+(discharger1.get_comps()[i]*discharger1.get_outflow_main()+discharger2.get_comps()[i]*discharger2.get_outflow_side()+discharger3.get_comps()[i]*discharger3.get_outflow_side()-self.get_comps[i]*(discharger1.get_outflow_main()+discharger2.get_outflow_side()+discharger3.get_outflow_side())+r[i]*self.volumn)/self.volumn
            self.eff_comps[7]=max(0.01,self.eff_comps[7]+(discharger1.get_comps()[7]*discharger1.get_outflow_main()+discharger2.get_comps()[7]*discharger2.get_outflow_side()+discharger3.get_comps()[7]*discharger3.get_outflow_side()-self.eff_comps[7]*(discharger1.get_outflow_main()+discharger2.get_outflow_side()+discharger3.get_outflow_side())+r[7]*self.volumn+self.KLa*self.volumn*(8-self.eff_comps[7]))/self.volumn)
        self.time=self.time+1
    
    def set_comps(self,a):
        #intilaizing the contaminants in the bioreactor
        for i in range(constant.ComponentNumbers):
            self.eff_comps[i]=a[i]
        
    def set_KLa(self,point):
        #adjust the dissolved oxygen point in aerated bioreactor
        self.KLa=point
        
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
        
    def update_inflow(self,discharger1,discharger2=None,discharger3=None):
        self.inlet[discharger1.name]=discharger1.get_outflow_main()
        if discharger2!=None:
            self.inlet[discharger2.name]=discharger2.get_outflow_side()
        if discharger3!=None:
            self.inlet[discharger3.name]=discharger3.get_outflow_side()

        

    
    


            
