import pandas  as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
data=pd.read_excel('bsm1LT.xlsx')
data.insert(17,'COD',data.iloc[:,1]+data.iloc[:,2]+data.iloc[:,3]+data.iloc[:,4]+data.iloc[:,5]+data.iloc[:,6]+data.iloc[:,7])
data.insert(18,'BOD',0.25*(data.iloc[:,2]+data.iloc[:,4]+(1-0.08)*(data.iloc[:,5]+data.iloc[:,6])))
data.insert(19,'Snkj',data.iloc[:,10]+data.iloc[:,11]+data.iloc[:,12]+0.08*(data.iloc[:,5]+data.iloc[:,6])+0.06*(data.iloc[:,3]+data.iloc[:,7]))
Clock=(['A']*24+['B']*24+['C']*24+['D']*24)*609+['D']
Season=['Autumn']*46*96+['Winter']*91*96+['Spring']*91*96+['Summer']*91*96+['Autumn']*91*96+['Winter']*91*96+['Spring']*91*96+['Summer']*17*96+['Summer']
data.insert(20,'Clock_6',Clock)
data.insert(21,'Season',Season)

print(data)
def LineChart(self):
    a=0
    for i in range(0,len(self.columns)):
        x=self.iloc[:,i]
        x.hist(bins=10,alpha=0.3,color='blue',normed=True)
        x.plot(kind='kde',style='r--',title="LineChart of %s"%self.columns[i])
        a=a+1
        plt.show()  
def Pairplot(self):
    sns.pairplot(self,vars=['COD','TSS','Snkj','Q','Temp'],hue='Clock_6',diag_kind='kde',plot_kws={'alpha':0.01,'s':1},size=12)
    plt.show()
def Scatterplot(self):
    cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
    sns.set()
    ax = sns.scatter(x="COD", y="TSS",
                     hue="Temp", size="Q",
                     palette=cmap, sizes=(10, 200),
                     data=self)
Pairplot(data)

