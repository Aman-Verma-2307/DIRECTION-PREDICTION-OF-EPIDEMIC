#!/usr/bin/env python
# coding: utf-8

# # Contact Tracing

# In[27]:


### Importing Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


# In[28]:


### Defining Variables

n = 18 # Number of arcs
l = 360/n # Arc Degree
N = 15 # Total Number of People
max_movement = 2 # Maximum Number of location shifts in all users 
max_meet = 4 # Maximum Number of meets among all users

Movement = [[[0,0,0,0] for a in range(max_movement)] for b in range(N)] # 3-D Matrix of dimension (max_movement*4*N) with hth 2-D plane showing data about users all location changes ie (lattitude, longitude, timestamp, arc_index) and that to for max_movement. If the hth user doesn't change location then all the remaining rows will be similar to last row but with just changed time stamp.   
Meeting = [[[[0,0] for b in range(max_meet)] for d in range (N)] for e in range(N)] # 3-D Matrix of dimensions (max_meets*2*N*N). This matrix contains the data about meeting of person and for a certain no. of times and also in which arc along with time duration and this is for all N peoples.
Person = [0 for g in range(N)] # 1-D vector representing person_index of a person
Update_Matrix = [[[[0,0] for b in range(max_meet)] for d in range (N)] for e in range(N)] # 3-D Matix of dimensions (max_meets*2*N*N) for updating entries and removal of redundancy


# In[29]:


### Distance Calculator

def distance(origin, destination):
   
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))         * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


# In[33]:


### Defining Function Trace_Contact

# One must initialize Update_Matrix with all zeros before initializing this function

def Trace_Contact(Movement,Person,max_movement,max_meet,eta,dist_threshold,time_correspondence):
    
    """ 
     Function to trace the contacts.
     
     Inputs:-
     
     Movement - 3-D Matrix of dimension N*max_movement*4 containing data about lattiutde, longitude, timestamp, arc_index
     Person -  1-D vector representing person_index of a person
     max_movement - Maximum Number of location shifts in all users
     max_meet -  Maximum Number of meets among all users
     eta - Threshold for a genuine meeting
     dist_threshold - Threshold for distance measurment
     time_correspondence - Time of Meetinng if meeting is just for single instance  
     
     Outputs:-
     
     Meeting - 4-D Matrix of dimesnion N*N*max_meet*2 which containing the data about meeting intervels, meeting arc etc.
     Update_Matrix - 4-D Matrix of dimension N*N*max_meet*2 which contains data for updtaing entries
     
    """
    
    # Converting Lists in Matrices
    Movement = np.array(Movement)
    Person = np.array(Person)
    Meetings = np.array(Meeting)
    
    # Implementing the Function
    for entity_1 in range(N):
        for movement_1 in range(max_movement):
            for entity_2 in range(N):
                if(Movement[entity_1,0,0] != Movement[entity_2,0,0]):
                    for movement_2 in range(max_movement):
                        if(distance(Movement[entity_1,movement_1,0:1],Movement[entity_2,movement_2,0:1]) < dist_threshold):
                            movement_decided = movement_2
                            time_beginning_en1 = Movement[entity_1,movement_1,2]
                            time_beginning_en2 = Movement[entity_2,meet_decided,2]
                            if((time_beginnig_en1-time_beginning_en2)**2 < eta**2):
                                while((distance(Movement[entity_1,movement_1,0:1],Movement[entity_2,movement_decided,0:1]) and (time_beginnig_en1-time_beginning_en2)**2 < eta**2) or movement_decided == max_movement):
                                    time_beginning_en2 = Movement[entity_2,movement_decided,2]
                                    movement_decided = movement_decided + 1
                                if(time_beginnig_en1 > time_beginning_en2):
                                      time_of_meeting = time_beginnig_en1 - time_beginning_en2
                                elif(time_beginning_en2 > time_beginning_en1):
                                      time_of_meeting = time_beginning_en2 - time_beginning_en1
                                else:
                                      time_of_meeting = time_correspondence
                                Meetings[entity_1,entity_2,movement_1,0] = time_of_meeting
                                Meetings[entity_1,entity_2,movement_1,1] = Movement[entity_2,meeting_decided,Person[entity_2]]
    return Meetings

