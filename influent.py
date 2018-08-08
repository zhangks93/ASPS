ComponentNumbers=9
class influent():
    def __init__(self,time=0,flow=0):
        self.time=time
        self.flow=flow
        self.comps = [0] * ComponentNumbers
    def set_comps(a):
        for i in range(ComponentNumbers):
            self.comps[i]=a[i]
    def add_downstream(self, receiver):
        ''' Set the mainstream unit that will receive effluent from the
            current unit
        '''
           self.main_outlet = receiver
           self.main_outlet_connected = True
           if receiver != None:
               receiver.add_upstream(self)
    def get_Xs(self):
        return self.Xs
    
    def get_TSS(self):
        ''' Return the Total Suspsended Solids (TSS) in the unit '''
        return self._TSS

    def get_VSS(self):
        ''' Return the Volatile Suspended Solids (VSS) in the unit '''
        return self._VSS

    def get_total_COD(self):
        ''' Return the Total COD (both soluable and particulate) in the unit'''
        return self._inf_comp[0] + self._inf_comp[1] + self._inf_comp[2] \
                + self._inf_comp[3] + self._inf_comp[4] + self._inf_comp[5] \
                + self._inf_comp[6]

    def get_soluble_COD(self):
        ''' Return the SOLUABLE COD in the unit '''
        return self._inf_comp[5] + self._inf_comp[6]

    def get_particulate_COD(self):
        ''' Return the PARTICULATE COD in the unit '''
        return self.get_total_COD() - self.get_soluble_COD()
    
    def get_TN(self):
        ''' Return the Total Nitrogen of the unit '''
        return self._inf_comp[8] + self._inf_comp[9] \
                + self._inf_comp[10] + self._inf_comp[11]

    def get_particulate_N(self):
        ''' Return organic nitrogen of the unit '''
        return self._inf_comp[11]

    def get_soluble_N(self):
        ''' Return soluable nitrogen of the unit '''
        return self.get_TN() - self.get_particulate_N()

    def get_organic_N(self):
        ''' Return organic nitrogen of the unit '''
        return self._inf_comp[10] + self._inf_comp[11]

    def get_inorganic_N(self):
        ''' Return inorganic nitrogen of the unit '''
        return self._inf_comp[8] + self._inf_comp[9] 
    

a=influent(1)
a.set_Xs(5)
print(a.time,a.get_Xs())
del a
    
