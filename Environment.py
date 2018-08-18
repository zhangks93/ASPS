import influent as If
import reactor as Ra
import clarifier as Ca
import constant
import pandas as pd
import numpy as np

class WWTP():
     def __init__(self):
         self.Influent=If.influent('influent',0,'data/bsm1LT.xlsx')
         self.A=Ra.bioreactor('Reactor1',0,1000)
         self.B=Ra.bioreactor('Reactor2',0,1000)
         self.C=Ra.bioreactor('Reactor3',0,1333)
         self.D=Ra.bioreactor('Reactor4',0,1333)
         self.E=Ra.bioreactor('Reactor5',0,1333)
         self.A.set_comps([30,2.81,1149,82.1,2552,148,449,0.0043,5.37,7.92,1.22,5.28,4.93,3285])
         self.B.set_comps([30,1.46,1149,76.4,2553,148,450,0.0000631,3.66,8.34,0.882,5.03,5.08,3282])
         self.C.set_comps([30,1.15,1149,64.9,2557,149,450,1.72,6.54,5.55,0.829,4.39,4.67,3278])
         self.D.set_comps([30,0.995,1149,55.7,2559,150,451,2.43,9.3,2.97,0.767,3.88,4.29,3274])
         self.E.set_comps([30,0.889,1149,49.3,2559,150,452,0.491,10.4,1.73,0.688,3.53,4.13,3270])
         self.log_A=pd.DataFrame(columns=['Si','Ss','Xi','Xs','Xbh','Xba','Xp','So','Sno','Snh','Snd','Xnd','Salk','TSS','KLa','Ks','μH','KNO','KOH','bH','ηg','ηh','kh','Kx','μA','KNH','ka','KOA','bA','out_flow_main','out_flow_side'])
         self.log_B=pd.DataFrame(columns=['Si','Ss','Xi','Xs','Xbh','Xba','Xp','So','Sno','Snh','Snd','Xnd','Salk','TSS','KLa','Ks','μH','KNO','KOH','bH','ηg','ηh','kh','Kx','μA','KNH','ka','KOA','bA','out_flow_main','out_flow_side'])
         self.log_C=pd.DataFrame(columns=['Si','Ss','Xi','Xs','Xbh','Xba','Xp','So','Sno','Snh','Snd','Xnd','Salk','TSS','KLa','Ks','μH','KNO','KOH','bH','ηg','ηh','kh','Kx','μA','KNH','ka','KOA','bA','out_flow_main','out_flow_side'])
         self.log_D=pd.DataFrame(columns=['Si','Ss','Xi','Xs','Xbh','Xba','Xp','So','Sno','Snh','Snd','Xnd','Salk','TSS','KLa','Ks','μH','KNO','KOH','bH','ηg','ηh','kh','Kx','μA','KNH','ka','KOA','bA','out_flow_main','out_flow_side'])
         self.log_E=pd.DataFrame(columns=['Si','Ss','Xi','Xs','Xbh','Xba','Xp','So','Sno','Snh','Snd','Xnd','Salk','TSS','KLa','Ks','μH','KNO','KOH','bH','ηg','ηh','kh','Kx','μA','KNH','ka','KOA','bA','out_flow_main','out_flow_side'])
     def pipe_connect(self):
         self.A.add_upstream(self.Influent,'Main')
         self.B.add_upstream(self.A,'Main')
         self.C.add_upstream(self.B,'Main')
         self.D.add_upstream(self.C,'Main')
         self.E.add_upstream(self.D,'Main')
         self.E.set_outflow_side(10)
         self.A.add_upstream(self.E,'Side')
         
     def run(self):
            self.Influent.update_inflow()
            self.Influent.update_comps()
            self.Influent.update_outflow_main()
            self.A.update_inflow(self.Influent)
            self.A.update_outflow_main()
            self.B.update_inflow(self.A)
            self.B.update_outflow_main()
            self.C.update_inflow(self.B)
            self.C.update_outflow_main()
            self.D.update_inflow(self.C)
            self.D.update_outflow_main()
            self.E.update_inflow(self.D)
            self.E.update_outflow_main()
            self.log_A.loc[self.A.time,0:14]=self.A.get_comps()
            self.log_A.loc[self.A.time,14:15]=self.A.KLa
            self.log_A.loc[self.A.time,15:29]=self.A.kin_paras
            self.log_A.loc[self.A.time,29:30]=self.A.outflow_main
            self.log_A.loc[self.A.time,30:31]=self.A.outflow_side
            self.A.biodegrade(self.Influent.temp,self.Influent,self.E)
            self.log_B.loc[self.B.time,0:14]=self.B.get_comps()
            self.log_B.loc[self.B.time,14:15]=self.B.KLa
            self.log_B.loc[self.B.time,15:29]=self.B.kin_paras
            self.log_B.loc[self.B.time,29:30]=self.B.outflow_main
            self.log_B.loc[self.B.time,30:31]=self.B.outflow_side
            self.B.biodegrade(self.Influent.temp,self.A)
            self.log_C.loc[self.C.time,0:14]=self.C.get_comps()
            self.log_C.loc[self.C.time,14:15]=self.C.KLa
            self.log_C.loc[self.C.time,15:29]=self.C.kin_paras
            self.log_C.loc[self.C.time,29:30]=self.C.outflow_main
            self.log_C.loc[self.C.time,30:31]=self.C.outflow_side
            self.C.biodegrade(self.Influent.temp,self.B)
            self.log_D.loc[self.D.time,0:14]=self.D.get_comps()
            self.log_D.loc[self.D.time,14:15]=self.D.KLa
            self.log_D.loc[self.D.time,15:29]=self.D.kin_paras
            self.log_D.loc[self.D.time,29:30]=self.D.outflow_main
            self.log_D.loc[self.D.time,30:31]=self.D.outflow_side
            self.D.biodegrade(self.Influent.temp,self.C)
            self.log_E.loc[self.E.time,0:14]=self.E.get_comps()
            self.log_E.loc[self.E.time,14:15]=self.E.KLa
            self.log_E.loc[self.E.time,15:29]=self.E.kin_paras
            self.log_E.loc[self.E.time,29:30]=self.E.outflow_main
            self.log_E.loc[self.E.time,30:31]=self.E.outflow_side
            self.E.biodegrade(self.Influent.temp,self.D)
            self.Influent.time=self.Influent.time+1
            
     def control(op_para):
         #op_para=[KLa,outflow_side]
         self.E.set_KLa(op_para[0])
         self.E.set_outflow_side(op_para[1])
A=WWTP()
A.pipe_connect()
for t in range (700):
    A.run()
writer = pd.ExcelWriter('log.xlsx')
A.log_A.to_excel(writer,'log_A')
A.log_B.to_excel(writer,'log_B')
A.log_C.to_excel(writer,'log_C')
A.log_D.to_excel(writer,'log_D')
A.log_E.to_excel(writer,'log_E')
writer.save()

