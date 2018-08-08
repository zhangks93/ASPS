 
import pandas as pd
data1= pd.read_table('dry.txt',index_col=0)
data2= pd.read_table('rain.txt',index_col=0)
data3= pd.read_table('storm.txt',index_col=0)
data4= pd.read_table('noise.txt',sep=' ',header=None)
data5= pd.read_table('bsm1LT.txt',sep='  ',header=None)
print(data4)

