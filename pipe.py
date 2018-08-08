 
class pipe():
    def __init__(self,time=0):
        self.time=time
        self.eff_comps= [0] * ComponentNumbers
        # _inlet store the upstream units and their flow contribution
        # in the format of {unit, Flow}
        self.inlet={}
        self.inlet_main = 0
        self.inlet_side = 0

        # a SINGLE unit that receives all the flows from the
        # current unit
        self.outlet={}
        self.outlet_mian = 0
        self.outlet_side = 0#By default this is the MAIN OUTLET.
        
        # a Boolean flag to indicate whether there are upstream units
        self.upstream_connected = False

        # Boolean flag to indicate whether there are units in MAIN downstream
        self.downstream_connected = False

        # the Total Inflow, which is the same as the outflow for a pipe obj.
        self.total_flow = 0      
    def set_comps(a):
        for i in range(ComponentNumbers):
            self.comps[i]=a[i]
    def add_upstream(self, discharger, branch='Main'): 
            '''Add a single upstream unit to the current unit'''
            if discharger not in self.inlet:
                self.inlet[discharger] = 0.0
                self.upstream_connected = True
            if branch == 'Main':
                discharger.set_downstream_main_unit(self)
            elif branch == 'Side':
                discharger.set_downstream_side_unit(self)

    

    def add_downstream(self, receiver):
        ''' Set the mainstream unit that will receive effluent from the
            current unit
        '''
           self.main_outlet = receiver
           self.main_outlet_connected = True
           if receiver != None:
               receiver.add_upstream(self)
    def totalize_flow(self):
        ''' Totalize all the flows entering the current unit.
            Return type: NO Return
        '''
        self.total_flow = 0.0
        for unit in self.inlet:
            self.total_flow += self.inlet[unit]
   
    def get_outlet_flow(self):
        return self._total_flow
    
    def get_outlet_concs(self):
        return self.eff_comps
    
    def update():
        for index in range(ComponentNumbers):
                temp = 0.0
                for unit in self.inlet:
                    temp += unit.get_outlet_concs()[index] * unit.get_outlet_flow()
                self.eff_comps[index] = temp / self.total_flow

    
