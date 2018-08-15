import influent as If
import reactor as Ra
import clarifier as Ca
import constant
import pandas as pd
import numpy as np

Influent=If.influent('influent',0,'data/bsm1LT.xlsx')
A=Ra.bioreactor('Reactor1',0,1000)
B=Ra.bioreactor('Reactor2',0,1000)
C=Ra.bioreactor('Reactor3',0,1333)
D=Ra.bioreactor('Reactor4',0,1333)
E=Ra.bioreactor('Reactor5',0,1333)
Clarifier=Ca.clarifier('Clarifier',0,1000,7000,12)
A.add_upstream(Influent,'Main')
B.add_upstream(A,'Main')
C.add_upstream(B,'Main')
D.add_upstream(C,'Main')
E.add_upstream(D,'Main')
E.set_outflow_side()
A.add_upstream(E,'Side')
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
    A.biodegrade()
    B.biodegrade()
    C.biodegrade()
    D.biodegrade()
    E.biodegrade()
    Clarifier.update_inflow1(E)
    Clarifier.update_outflow_main()
    a=np.array([])
    for i in range (0,constant.ComponentNumbers):
        a=np.append(a,np.array([Influent.time,A.get_comps()[i],B.get_comps()[i],C.get_comps()[i],D.get_comps()[i],E.get_comps()[i]]),axis=0)
    Influent.time=Influent.time+1
    print(a)
    
