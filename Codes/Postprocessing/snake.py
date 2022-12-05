# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 16:57:02 2020

@author: mohamadi
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance


class snake:
    def __init__(self, sct_qty, sgms_pr_sct, sgm_lgth):
        self.sct_qty=sct_qty
        self.sgms_pr_sct=sgms_pr_sct
        self.sgm_lgth=sgm_lgth
        self.configs={'sct_qty':sct_qty, 'sgms_pr_sct':sgms_pr_sct,
                      'sgm_lgth':sgm_lgth}
        self.slider_loc=0
        
        # segment 0 is the base (this +1 here eliminated the need for many +1s)
        self.sgm_qty=sct_qty*sgms_pr_sct+1
        self.length=sct_qty*sgms_pr_sct*sgm_lgth
        #Section and Segment bending Angles
        
        self.sct_theta=np.zeros(self.sct_qty)
        
        #segment 0 is reserved for base
        self.sgm_theta=np.zeros(self.sgm_qty)
        self.Tf=np.zeros((self.sgm_qty,4,4))
        
        #xy coordinates of the segment ends
        self.sgm_ends_xyz=np.zeros((self.sgm_qty,4,1))
        self.sgm_mids_xyz=np.zeros((self.sgm_qty,4,1))
        self.fw_kin()
        
    def fw_kin(self):
        #the snake starts at the beginning of segment 1 (not the base)
        self.Tf[0]=[[1, 0, 0, self.slider_loc-self.sgm_lgth/2],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]]
        
        #1st temporary transgform is trnasformation to base
        T_temp=np.eye(4,4)
        
        for i in range(1,self.sgm_qty):
            self.Tf[i]=self.mdh_tr(0, self.sgm_lgth, 0, self.sgm_theta[i])
        
        for i in range(self.sgm_qty):
            T_temp=np.matmul(T_temp, self.Tf[i])
            self.sgm_ends_xyz[i]=np.matmul(T_temp, [[self.sgm_lgth], [0], [0] ,[1]])
            self.sgm_mids_xyz[i]=np.matmul(T_temp, [[self.sgm_lgth/2], [0], [0] ,[1]])
    
    #input is thetas for sections startinf from 1
    def set_theta(self, sct_theta):
       
        self.sct_theta=sct_theta
        
        for i in range(self.sct_qty):
            for j in range(1, self.sgms_pr_sct+1):
                ii=i*self.sgms_pr_sct+j
                self.sgm_theta[ii]=self.sct_theta[i]/self.sgms_pr_sct
   
    def set_slider_loc(self, slider_loc):
        self.slider_loc=slider_loc        
    
    def get_xyz_pts(self):
        self.fw_kin()
        return self.sgm_ends_xyz
    
    def get_mid_pts(self):
        self.fw_kin()
        return self.sgm_mids_xyz
        
    def mdh_tr(self, alpha, a, d, theta):
        #alpha(i-1) , a(i-1), d(i), theta(i)
        tf=[
            [np.cos(theta), -np.sin(theta), 0, a],
            
            [np.sin(theta)*np.cos(alpha), np.cos(theta)*np.cos(alpha),
             -np.sin(alpha), -np.sin(alpha)*d],
            
            [np.sin(theta)*np.sin(alpha), np.cos(theta)*np.sin(alpha), 
             np.cos(alpha), np.cos(alpha)*d],
            [0, 0, 0, 1]
            ]
        return tf
    
    def plot_snake(self,ax):
        sgm_ends_xyz=self.get_xyz_pts()
    
        ax.plot(sgm_ends_xyz[:,0],sgm_ends_xyz[:,1])
        ax.scatter(sgm_ends_xyz[:,0],sgm_ends_xyz[:,1],s=10)
        ax.scatter(sgm_ends_xyz[::self.sgms_pr_sct,0],sgm_ends_xyz[::self.sgms_pr_sct,1],s=20,c='r')

    def set_path(self, path):
        self.path=path
    
    def deviation(self):     
        
        devs_sum, devs=self.part_dev(0, self.sct_qty)
        
        return devs_sum, devs


    def part_dev(self,start_sct, length):     
        devs=[]
        devs_sum=[]
        
        for i in range(start_sct, start_sct+length):
            tmp_devs=self.single_sct_dev(i)
            devs.append(tmp_devs)
            
        devs_sum=np.sum(devs)

        return devs_sum, devs
    
    def single_sct_dev(self,sct_no):
        
        devs=[]
        devs_sum=[]
               
        sgm_ends_xyz=self.get_xyz_pts()
        
        
        start_sgm=sct_no*self.sgms_pr_sct+1
        end_sgm=start_sgm + self.sgms_pr_sct
        
        for i in range(start_sgm, end_sgm):
                       
            #tmp=i%self.sgms_pr_sct
           
            #if (tmp==2) or (tmp==2) or (tmp==0):
            if True:
                sgm_end_xy=sgm_ends_xyz[i,0:2]
                #idx=(np.abs(self.path[0,:] -sgm_ends_xyz[i,0])).argmin()
                
                dev= self.min_dist(sgm_end_xy)
                #dev=np.abs(self.path[1,idx]-sgm_ends_xyz[i,1])
                devs.append(dev)
                #if i==end_sgm-1:
                    #devs.append(dev)
                            
        return devs 
    
    def min_dist(self, sgm_end_xy):
        
        path=np.asarray(self.path)
        path=path.transpose()
        sgm_end_xy=np.asarray(sgm_end_xy)
        sgm_end_xy=sgm_end_xy.transpose()
        
        dists=np.sqrt(np.sum((path-sgm_end_xy)**2, axis=1))
               
        return np.min(dists)
    
    
    
    
    
"""        
    def min_dist(self, sgm_end_xy):
        path_idx=(np.abs(self.path[0,:] -sgm_end_xy[0])).argmin()
        radius=10
        dists=[]
        for i in range(path_idx-radius,path_idx+radius):
            path_point=self.path[:, i]
            dists.append(distance.euclidean(path_point,sgm_end_xy))
            
        return np.min(dists)

"""




      
                
"""
    def part_dev(self,start_sct, length):     
        path=self.path
        
        devs=[]
        end_devs=[]
        
        sgm_ends_xyz=self.get_xyz_pts()
        
        
        start_sgm=start_sct*self.sgms_pr_sct+1
        end_sgm=start_sgm + length*self.sgms_pr_sct
        
        for i in range(start_sgm, end_sgm):
            idx=(np.abs(path[0,:] -sgm_ends_xyz[i,0])).argmin()
            
            tmp=i%self.sgms_pr_sct
           
            if (tmp==0) or (tmp==2)or (tmp==3):
                    
                dev=np.abs(path[1,idx]-sgm_ends_xyz[i,1])
                end_devs=np.append(end_devs, dev)
                    
            #devs=np.append(devs,dev)
        
        devs_sum=np.sum(end_devs)
        #np.sum(devs)+
        return devs_sum, devs 
"""
        
        
        
        
        
        
        
        
        
        