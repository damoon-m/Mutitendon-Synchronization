# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:01:44 2021

@author: LetC000
"""

import sys
#print(sys.path)

import matplotlib.pyplot as plt
import numpy as np
from snake import snake 
import matplotlib.patches as mpatches

m=5 # number of links in each section
a=40# link lenght
snk=snake(1, m, a)

angle_sclr=3.65


# fig=plt.figure(figsize=(40,20))
# ax= fig.add_subplot(1, 1, 1, aspect=1)
# ax.set_xlim(0, 220)
# ax.set_ylim(-200, 200)
# ax.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)
# plt.xlabel('Y-axis')
# plt.ylabel('X-axis')

# fig2=plt.figure(figsize=(40,20))
# ax2= fig2.add_subplot(1, 1, 1, aspect=1)
# ax2.set_xlim(0, 6)
# ax2.set_ylim(0, 10)
# ax2.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)

fig3=plt.figure(figsize=(10,6.66))
ax3= fig3.add_subplot(1, 1, 1)
ax3.set_xlim(0.5, 5.5)
ax3.set_ylim(0, 6.66)
ax3.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)

ax3.set_xticks([1, 2 , 3 , 4,  5])
ax3.set_xticklabels(['L_1', 'L_2', 'L_3', 'L_4', 'L_5'], fontsize=20)

ax3.set_title('Links\' average deviation from the ideal positions', fontsize=20)
ax3.set_ylabel('Deviation(error)[mm]',fontsize=20)

title='Links\' average deviation from the ideal orientations'
fig5=plt.figure(figsize=(10,6.66))
ax5= fig5.add_subplot(1, 1, 1)
ax5.set_xlim(0.5, 5.5)
ax5.set_ylim(0, 3.5)
ax5.set_title(title, fontsize=20, verticalalignment='bottom')
ax5.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)

ax5.set_xticks([1, 2 , 3 , 4,  5])
ax5.set_xticklabels(['L_1', 'L_2', 'L_3', 'L_4', 'L_5'], fontsize=20)

ax5.set_ylabel('Link Rotatoin Deviation [°]', fontsize=20)



files=['m1.npy','m2.npy','m3.npy','m4.npy',]

width=0.15

for f in range(4):
    angles, transs, rots = np.load(files[f], allow_pickle=True, encoding='latin1')
    
    transs=transs[0]
    rots=rots[0]
    dists1=[0,0,0,0,0,0]
    rot_dists1=[0,0,0,0,0,0]
    angles=np.array(angles)
    # angles=-1*angles #activate/deactivate dependeing the polarity of the stepper cable
    pi=np.pi
    
    # for j in range(np.size(angles,0)):
    for j in range(7):
        if np.mod(angles[j]/10, 2)==0:
            color='ro'
        else:
            color='ko'
        
        phi=angles[j] # because :/
        theta=np.deg2rad(phi/angle_sclr) # arbitrary ratio selected during the pulley design
               
        theta_i=[i*theta for i in range(m+1)]
        
        if theta !=0:
            calc_mids=[-np.sign(theta_i)*a*(1-np.cos(theta_i))/(2*np.abs(np.tan(theta/2))), np.sign(theta_i)*a*np.sin(theta_i)/(2*np.abs(np.tan(theta/2)))]
        else:
            calc_mids=[i*a for i in range(6)]
            calc_mids=np.vstack([np.zeros(6),calc_mids])
            
        ys=-1*1000*transs[j][:,0]
        xs=1000*transs[j][:,1]

        print(angles[j])
        
        dists=np.sqrt(np.sum([[np.square(xs-calc_mids[1])], [np.square(ys-calc_mids[0])]],
                     axis=0))
        
        dists1=np.vstack([dists1, dists])
        
        
        calc_rots=[-i*theta for i in range(6)]
        rot_dists=np.abs(np.rad2deg(rots[j][:,2]-calc_rots))
        
        rot_dists1=np.vstack([rot_dists1, rot_dists])
        
    dists1=dists1[1:,:] # geting rid of the first 0 column
    dist_means=np.mean(dists1, axis=0)
    dist_std=np.std(dists1, axis=0)
    
    xxx=[i+(f-2)*width for i in range(6)]
    barr=ax3.bar(xxx, dist_means, yerr=dist_std, capsize=6,width=width)
    
    
    
    rot_dists1=rot_dists1[1:,:] # geting rid of the first 0 column
    rot_dist_means=np.mean(rot_dists1, axis=0)
    rot_dist_std=np.std(rot_dists1, axis=0)
    
    barrr=ax5.bar(xxx, rot_dist_means, yerr=rot_dist_std, capsize=6,width=width)


ax3.legend(['Measurement 1','Measurement 2','Measurement 3','Measurement 4','Measurement 5'], loc='upper left',
           fontsize=20)

ax5.legend(['Measurement 1','Measurement 2','Measurement 3','Measurement 4','Measurement 5'], loc='upper left',
           fontsize=20)


fig3.tight_layout()
fig3.savefig('position_error_bar.png')


fig5.tight_layout()
fig5.savefig('orientation_error_bar.png')

    
    

    

    

    

    

    

    

    

    

    

    

    

    

    
