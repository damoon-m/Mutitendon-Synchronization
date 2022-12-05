# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:01:44 2021

@author: GOD_FUCKER
"""

import sys
#print(sys.path)

import matplotlib.pyplot as plt
import numpy as np
from snake import snake 

angles, transs, rots = np.load('m4.npy', allow_pickle=True, encoding='latin1')



transs=transs[0]
rots=rots[0]
angles=np.array(angles)
angles=-1*angles #activate/deactivate dependeing the polarity of the stepper cable
pi=np.pi

angle_sclr=3.65
m=5 # number of links in each section
l=40# link lenght
a=snake(1, m, l)

dists_1=[]
dists_2=[]
dists_3=[]
dists_4=[]
dists_5=[]

rots_1=[]
rots_2=[]
rots_3=[]
rots_4=[]
rots_5=[]

fig=plt.figure(figsize=(20,10))
ax= fig.add_subplot(1, 1, 1, aspect=1)
ax.set_xlim(0, 220)
ax.set_ylim(-200, 200)
ax.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)

fig2=plt.figure(figsize=(15,10))
ax2= fig2.add_subplot(1, 1, 1, aspect=1)
ax2.set_xlim(0, 6)
ax2.set_ylim(0, 12)
ax2.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)

for i in range(np.size(angles,0)):

    if np.mod(angles[i]/10, 2)==0:
        color='ro'
    else:
        color='ko'
    phi=angles[i]
   
    
    theta=(phi/angle_sclr)*m # arbitrary ratio selected during the pulley design
    a.set_theta([np.deg2rad(theta)])
    a.fw_kin()
    a.plot_snake(ax)
    
    mids=a.get_mid_pts()
    sim_xs=mids[:,0]
    sim_ys=mids[:,1]
    ax.plot(sim_xs, sim_ys, 'g+', lw=6)
    
    ys=-1000*transs[i][:,0]
    xs=1000*transs[i][:,1]
    ax.plot(xs, ys, color, lw=1)
    print(angles[i])
    
    dists=np.sqrt(np.sum([[np.square(xs-sim_xs[:,0])], [np.square(ys-sim_ys[:,0])]],
                 axis=0))
    
    dists=dists[0]
    ax2.plot(dists, 'ro')
    
    rots_1.append(np.rad2deg(rots[i][1,2]))
    rots_2.append(np.rad2deg(rots[i][2,2]))
    rots_3.append(np.rad2deg(rots[i][3,2]))
    rots_4.append(np.rad2deg(rots[i][4,2]))
    rots_5.append(np.rad2deg(rots[i][5,2]))
    
    if angles[i]>angles[i-1]:
        dists_1.append(dists[1])
        dists_2.append(dists[2])
        dists_3.append(dists[3])
        dists_4.append(dists[4])
        dists_5.append(dists[5])
    else:
        dists_1.append(-1*dists[1])
        dists_2.append(-1*dists[2])
        dists_3.append(-1*dists[3])
        dists_4.append(-1*dists[4])
        dists_5.append(-1*dists[5])


title='Hysteresis: Deviations from ideal position of link mid-points'
fig3=plt.figure(figsize=(10,6.66))
ax3= fig3.add_subplot(1, 1, 1)
ax3.set_title(title, fontsize=17, verticalalignment='bottom')
ax3.set_ylim(-11, 4.5)
ax3.set_ylabel('Distance Error [mm]',fontsize=15)
ax3.set_xlabel('Pulley Angle [°]',fontsize=15)
ax3.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)

markersize=6.66
ax3.plot(angles, dists_1, ':s', markersize=markersize)
ax3.plot(angles, dists_2, '--p', markersize=markersize)
ax3.plot(angles, dists_3, '-.*', markersize=markersize)
ax3.plot(angles, dists_4, ':x', markersize=markersize)
ax3.plot(angles, dists_5, '-d', markersize=markersize)

ax3.legend([ 'L_1', 'L_2','L_3','L_4','L_5'], fontsize=14, loc='lower left', bbox_to_anchor=(0, 0),
          fancybox=True, shadow=True, ncol=5)



title='Hysteresis Measurement: Rotation of indivisual links'
fig4=plt.figure(figsize=(10,10))
ax4= fig4.add_subplot(1, 1, 1)
ax4.set_title(title, fontsize=20, verticalalignment='bottom')
ax4.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)
ax4.set_xlabel('Pulley Angle [°]')
ax4.set_ylabel('Link Rotatoin [°]')
ax4.set_ylim(-120, 120)


ax4.plot(angles, rots_1, ':s', markersize=markersize)
ax4.plot(angles, rots_2, '--p', markersize=markersize)
ax4.plot(angles, rots_3, '-.*', markersize=markersize)
ax4.plot(angles, rots_4, ':x', markersize=markersize)
ax4.plot(angles, rots_5, '-d', markersize=markersize)
        
        
ax4.legend([ 'L_1', 'L_2','L_3','L_4','L_5'], fontsize=15, ncol=5)

rot_dists_1=rots_1-1*angles/angle_sclr
rot_dists_2=rots_2-2*angles/angle_sclr
rot_dists_3=rots_3-3*angles/angle_sclr
rot_dists_4=rots_4-4*angles/angle_sclr
rot_dists_5=rots_5-5*angles/angle_sclr
    

title='Hysteresis: Deviation from ideal rotation of indivisual links'
fig5=plt.figure(figsize=(10,6.66))
ax5= fig5.add_subplot(1, 1, 1)
ax5.set_title(title, fontsize=17, verticalalignment='bottom')
ax5.grid(linestyle="--", linewidth=0.5, color='0.25', zorder=-10)
ax5.set_xlabel('Pulley Angle [°]', fontsize=15)
ax5.set_ylabel('Link Rotatoin Deviation [°]', fontsize=15)
ax5.set_ylim(-2.5, 6)


ax5.plot(angles, rot_dists_1, ':s', markersize=markersize)
ax5.plot(angles, rot_dists_2, '--p', markersize=markersize)
ax5.plot(angles, rot_dists_3, '-.*', markersize=markersize)
ax5.plot(angles, rot_dists_4, ':x', markersize=markersize)
ax5.plot(angles, rot_dists_5, '-d', markersize=markersize)
        
        
ax5.legend([ 'L_1', 'L_2','L_3','L_4','L_5'], fontsize=14, loc='lower left', bbox_to_anchor=(0.2, 0),
          fancybox=True, shadow=True, ncol=5)


fig3.tight_layout()
fig3.savefig('position_hysteresis.png')


fig5.tight_layout()
fig5.savefig('orientation_hysteresis.png')
    
    
    
    
    
    
    
    