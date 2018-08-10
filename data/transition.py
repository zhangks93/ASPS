 
import pandas as pd

data5= pd.read_table('bsm1LT.txt',sep='  ',header=None)
writer = pd.ExcelWriter('bsm1LT.xlsx')
data5.to_excel(writer,'bsm')
writer.save()
print(data5)

