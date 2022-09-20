# -*- coding: utf-8 -*-

#%% Import required libraries
import numpy as np
import numpy.ma as ma
import pandas as pd


#%% Definition of Python classes that constitute the model architecture
'''
The code is based on two concatenated python classes, namely 'User' and
'Appliance', which are used to define at the outer level the User classes and 
at the inner level all the available appliances within each user class, with 
their own characteristics. Within the Appliance class, some other functions are
created to define windows of use and, if needed, specific duty cycles
'''

#Define the outer python class that represents 'User classes'
class User():
    
    def __init__(self, name = "", n_users = 1):
        self.user_name = name
        self.num_users = n_users #specifies the number of users within the class
        self.App_list = [] #each instance of User (i.e. each user class) has its own list of Appliances

#Define the inner class for modelling user's appliances within the correspoding user class
    class Appliance():
    
        def __init__(self,user, n = 1, Par_power = [0, 0, 0], Battery_cap = 0, P_var = 0, w = 1, t_func = 0, d_tot = 0, r_d = 0, r_v = 0, d_min = 1, occasional_use = 1, wd_we_type = 3, P_series = False):
            self.user = user #user to which the appliance is bounded
            self.number = n #number of appliances of the specified kind
            self.num_windows = w #number of functioning windows to be considered
            self.dist_tot = d_tot #total distance the mobility appliance drives during the day [Km]
            self.r_d = r_d #percentage of total distance that is subject to random variability
            # self.vel = v #velocity at which the mobility appliance drives [Km/h]
            self.r_v = r_v #percentage of velocity that is subject to random variability
            # self.func_time = t #total time the appliance is on during the day
            self.func_dist = d_min #minimum distance the mobility appliance drives after switch-on event 
            self.func_cycle = t_func #minimum time the appliance is kept on after switch-on event 
            self.occasional_use = occasional_use #probability that the appliance is always (i.e. everyday) included in the mix of appliances that the user actually switches-on during the day
            self.P_var = P_var #allows to randomly variate the mobility App power within a precentage range
            self.wd_we = wd_we_type #defines if the App is associated with weekdays, saturday or sunday | 0 is wd, 1 is saturday, 2 is sunday, 3 all week
            self.Par_power = Par_power # List of 3 parameters to define the quadratic power-velocity relation
            self.POWER = ((Par_power[0] * 130**2 + Par_power[1] * 130 + Par_power[2]) * 12) * np.ones(365) #Maximum Power of the EV to scale the power curve [kW]
            self.Battery_cap = Battery_cap #Nominal Battery capacity of the EV [kWh]
            # if P_series == False and isinstance(P_max, pd.DataFrame) == False: #check if the user defined P as timeseries
            #     self.POWER = P_max*np.ones(365) #treat the power as single value for the entire year
            # else:
            #     self.POWER = P_max.values[:,0] #if a timeseries is given the power is treated as so    
            
        def windows(self, w1 = np.array([0,0]), w2 = np.array([0,0]),r_w = 0, w3 = np.array([0,0])):    
            self.window_1 = w1 #array of start and ending time for window of use #1
            self.window_2 = w2 #array of start and ending time for window of use #2
            self.window_3 = w3 #array of start and ending time for window of use #3
            self.random_var_w = r_w #percentage of variability in the start and ending times of the windows
            self.daily_use = np.zeros(1440) #create an empty daily use profile
            self.daily_use[w1[0]:(w1[1])] = np.full(np.diff(w1),0.001) #fills the daily use profile with infinitesimal values that are just used to identify the functioning windows
            self.daily_use[w2[0]:(w2[1])] = np.full(np.diff(w2),0.001) #same as above for window2
            self.daily_use[w3[0]:(w3[1])] = np.full(np.diff(w3),0.001) #same as above for window3
            self.daily_use_masked = np.zeros_like(ma.masked_not_equal(self.daily_use,0.001)) #apply a python mask to the daily_use array to make only functioning windows 'visibile'
            self.random_var_1 = int(r_w*np.diff(w1)) #calculate the random variability of window1, i.e. the maximum range of time they can be enlarged or shortened
            self.random_var_2 = int(r_w*np.diff(w2)) #same as above
            self.random_var_3 = int(r_w*np.diff(w3)) #same as above
            self.user.App_list.append(self) #automatically appends the appliance to the user's appliance list
            
        
            
