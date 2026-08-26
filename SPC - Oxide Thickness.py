# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 15:11:52 2026

@author: tamog
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.stats import norm

#--------------------------------------------------------------------------------------------------------

"""
Target thickness = 100nm
LSL and USL = +-5nm
number of lots = 150
Wafers per lot = 5
Std = 1.25
"""
Trgt_th = 100
USL = 100+5
LSL = 100-5
n = 150
k = 5

#--------------------------------------------------------------------------------------------------------


# Simulating normally distributed data to work on

data1 = np.random.normal(100,1.25,100*k)
data2 = np.random.normal(100,1.25,25*k)
data3 = np.random.normal(100,1.25,25*k)

data = np.concatenate((data1,data2,data3))

df_dict = {'Lot_no.':np.repeat(np.arange(1,n+1),k),'Serial_no.' : np.arange(1,n*k+1),'Thickness' : data}
df = pd.DataFrame(df_dict)
df.to_csv(r'C:\Users\tamog\OneDrive\Documents\Chip Fab\project_data.csv',index = False)

#--------------------------------------------------------------------------------------------------------

#Calculating mean and range for each subgroup

##calculate mean
def df_mean_calc(df): 
    mean = []
    s = 0
    m = 0
    for i in df.loc[:,'Thickness'] :
        if m==k: 
            mean.append(s/m)
            m = 1
            s = i
        else:
            s += i
            m += 1
    mean.append(s/m)
    return mean

#--------------------------------------------------------------------------------------------------------

##Calculating range
def df_range_calc(df):
    rng = []
    ma = 0
    mi = 0
    m = 0
    for i in df['Thickness']:
        if m==k: 
            rng.append(ma- mi)
            m,ma,mi = 1,i,i
        elif m == 0:
            m,ma,mi = 1,i,i
        else:
            if ma<i :
                ma = i
            if mi>i :
                mi = i
            m += 1
    rng.append(ma-mi)
    return rng

#--------------------------------------------------------------------------------------------------------

subgroups_dict = {'Lot': df.loc[0:n*k:k,'Lot_no.'],'Mean' : df_mean_calc(df),'Range' : df_range_calc(df)}
subgroups = pd.DataFrame(subgroups_dict)

#Grand mean and range mean
Grand_mean = subgroups['Mean'].mean()
rng_mean = subgroups['Range'].mean()

'''Instead of deriving complicated probability equations every time, statisticians already calculated constants.
        For X-bar chart -
            UCL = X-bar + A2*R-bar
            LCL = X-bar - A2*R-bar
            
        For R-bar char -
            UCL = D4*R-bar
            LCL = D3*R-bar
            
        For sigma - 
            Sigma = R-bar/d2
'''
#For n = 5
A2 = 0.577
D4 = 2.114
D3 = 0.000
d2 = 2.326

#calculating limits
UCL_xbar = Grand_mean + (A2*rng_mean)
LCL_xbar = Grand_mean - (A2*rng_mean)

UCL_rbar = rng_mean*D4
LCL_rbar = rng_mean*D3

sigma = rng_mean/d2/math.sqrt(k)
overall_sigma = rng_mean/d2

print('UCL xbar:',UCL_xbar)
print('LCL xbar:',LCL_xbar)
print('UCL rbar:',UCL_rbar) 
print('LCL rbar:',LCL_rbar) 
print('Sigma:',overall_sigma)
print('Xbar_mean',Grand_mean)
print('Range Mean :',rng_mean)

#--------------------------------------------------------------------------------------------------------

#X Control Chart
plt.plot(subgroups['Lot'],subgroups['Mean'])
plt.axhline(y = UCL_xbar, color= 'r', linestyle = '--',label = 'UCL')
plt.axhline(y = LCL_xbar, color= 'r', linestyle = '--',label = 'LCL')
plt.axhline(y = Grand_mean, color= 'g', linestyle = '--',label = 'Mean')
plt.axhline(y = USL, color= (0.4,0.5,0.8), linestyle = ':',label = 'USL')
plt.axhline(y = LSL, color= (0.4,0.5,0.8), linestyle = ':',label = 'LSL')
plt.fill_between((0,n),y1 = Grand_mean+sigma, y2= Grand_mean-sigma,color = (0,1,0,0.4))
plt.fill_between((0,n),y1 = Grand_mean+2*sigma, y2= Grand_mean+sigma,color = (0,0.6,0,0.4))
plt.fill_between((0,n),y1 = Grand_mean-2*sigma, y2= Grand_mean-sigma,color = (0,0.6,0,0.4))
plt.fill_between((0,n),y1 = Grand_mean+3*sigma, y2= Grand_mean+2*sigma,color = (0,0.4,0,0.4))
plt.fill_between((0,n),y1 = Grand_mean-3*sigma, y2= Grand_mean-2*sigma,color = (0,0.4,0,0.4))

#--------------------------------------------------------------------------------------------------------

#Western electric rule
'''
Rule 1 -
         1 point falls outside the ±3σ control limits->The process has experienced a massive shift or a sudden, severe disruption
         
Rule 2 - 
        2 out of 3 consecutive points fall in Zone A or beyond -> There is an early warning of a moderate shift or trend away from the average
        
Rule 3 -
        4 out of 5 consecutive points fall in Zone B or beyond -> The process mean has likely shifted slightly, causing data to consistently cluster away from the center
        
Rule 4 -
        8 consecutive points fall on the same side of the center line (anywhere in Zones A, B, or C). ->  A sustained, minor shift in the process average has occurred, meaning the process is no longer balanced around the mean.
'''

#Rule check function
def check_R(df):
    lots = subgroups['Lot'].to_list()
    means = subgroups['Mean'].to_list()
    paired_matrix = [[lots[i], means[i]] for i in range(len(lots))]
    prv_mean = 0
    prv_lot = 0
    r4_counter = 1
    voilation_lots1 = []
    voilation_lots4 = []
    voil_dummy = []
    for (lot,mean) in paired_matrix:
        
        if mean>UCL_xbar or mean<LCL_xbar :
            print(f'Lot{lot} voilates rule 1')
            voilation_lots1.append(lot)
                
        if lot != 1:
            if (Grand_mean-mean)/abs(Grand_mean-mean) == (Grand_mean-prv_mean)/abs(Grand_mean-prv_mean):
                r4_counter += 1
                if not(prv_lot in voil_dummy):
                    voil_dummy.append(prv_lot)
                voil_dummy.append(lot)
            else:
                if r4_counter >= 8:
                    if Grand_mean-mean < 0:
                        print(f'There is a negative shift of consecutive {r4_counter} points from center line')
                    if Grand_mean - mean > 0:
                        print(f'There is a positive shift of consecutive {r4_counter} points from center line')
                    voilation_lots4.extend(voil_dummy)
                voil_dummy.clear()
                r4_counter = 1
        prv_mean = mean
        prv_lot = lot
    if r4_counter >= 8:
        if Grand_mean-mean < 0:
            print(f'There is a Positive shift of consecutive {r4_counter} points from center line')
        if Grand_mean - mean > 0:
            print(f'There is a negative shift of consecutive {r4_counter} points from center line')
        voilation_lots4.extend(voil_dummy)
    return voilation_lots1,voilation_lots4

#--------------------------------------------------------------------------------------------------------

voilation_lots1,voilation_lots4 = check_R(subgroups)
plt.scatter(voilation_lots1,subgroups.loc[subgroups['Lot'].isin(voilation_lots1), 'Mean'].to_list(),color = 'red', marker = 'D',label = 'Rule 1 voilation')
plt.scatter(voilation_lots4,subgroups.loc[subgroups['Lot'].isin(voilation_lots4), 'Mean'].to_list(),color = (1,1,0), marker = 'D',label = 'Rule 4 voilation')
plt.title('Xbar Chart', pad=55, fontsize=14, fontweight='bold')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=4, frameon=True)
plt.tight_layout()
plt.show()
#-------------------------------------------------------------------------------------------------------

#R chart
plt.plot(subgroups['Lot'],subgroups['Range'])
plt.axhline(y = UCL_rbar, color= 'r', linestyle = '--',label = 'UCL')
plt.axhline(y = LCL_rbar, color= 'r', linestyle = '--',label = 'LCL')
plt.axhline(y = rng_mean, color= 'g', linestyle = '--',label = 'Mean')
plt.title('R Chart', pad=35, fontsize=14, fontweight='bold')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=True)
plt.tight_layout()
plt.show()

#--------------------------------------------------------------------------------------------------------

#histogram
plt.hist(data,bins=n,density = True)
norm_x_axis = np.linspace(min(data),max(data),num = n)
norm_curve = norm.pdf(norm_x_axis,data.mean(),data.std())
plt.plot(norm_x_axis,norm_curve)
plt.axvline(LCL_xbar,linestyle = '--',color = (128/255,0,128/255))
plt.axvline(UCL_xbar,linestyle = '--', color = (128/255,0,128/255))
plt.title('Xbar Histogram',fontweight = 'bold')
plt.plot()

#--------------------------------------------------------------------------------------------------------

# Cp and Cpk
Cp = (USL - LSL)/6/overall_sigma
Cpk = min( ((USL-Grand_mean)/3/overall_sigma) , ((Grand_mean-LSL)/3/overall_sigma) )
print('Cp:',Cp,'Cpk:',Cpk)

#----------------------------------------------------------------------------------------------------------
