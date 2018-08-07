 
import pandas as pd
data1= pd.read_table('dry.txt',index_col=0)
data2= pd.read_table('rain.txt',index_col=0)
data3= pd.read_table('storm.txt',index_col=0)
data4= pd.read_table('noise.txt',header=None)
data5= pd.read_table('bsm1LT.txt',sep=' ',header=None)
writer = pd.ExcelWriter('./bsm.xlsx')
data1.to_excel(writer,'dry')
data2.to_excel(writer,'rain')
data3.to_excel(writer,'storm')
data4.to_excel(writer,'noise')
data5.to_excel(writer,'bsm1LT')
writer.save()
print('success!')

