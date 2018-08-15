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
            self.A.biodegrade(self.Influent.temp,self.Influent,self.E)
            self.B.biodegrade(self.Influent.temp,self.A)
            self.C.biodegrade(self.Influent.temp,self.B)
            self.D.biodegrade(self.Influent.temp,self.C)
            self.E.biodegrade(self.Influent.temp,self.D)
            self.Influent.time=self.Influent.time+1
            
     def control(op_para):
         #op_para=[KLa,outflow_side]
         self.E.set_KLa(op_para[0])
         self.E.set_outflow_side(op_para[1])
A=WWTP()
A.pipe_connect()
for t in range (5):
    A.run()

