#!/usr/bin/env python
# coding: utf-8

# # Contract Tracing: A Singular Approach

# In[1]:


### Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


# In[3]:


### Defining Variables
N = None # Total No. of Users
N1 = None # Total entries of user being matched
N2 = None # Total entries of all the users except the on being traced
User_Match = [[0,0,0] for a in range(N1)]# Matrix of the user being matched. Information in columns is that of lattitude, longitude and Timestamp
User_Complete = [[0,0,0,0] for b in range(N2)] # Matrix of location data of all other users except the user in User_Match . Information in columns is that of lattitude, longitude, Timestamp and Unique ID


# In[18]:


### Data Preprocessing : Filtering User_Complete Matrix

def Filter(User_Match,User_Complete):
    
    """
    Function to filter out nearby entries from User_Complete Matrix
    
    Inputs :
    User_Match - Matrix of the user being matched. Information in columns is that of lattitude, longitude and Timestamp
    User_Complete -  Matrix of location data of all other users except the user in User_Match . Information in columns is that of lattitude, longitude, Timestamp and Unique ID
    
    Returns :
    User_Filtered -  Matrix of only filtered entries for User_Match
    
    """
     # Array Conversion
    User_Match = np.array(User_Match)
    User_Completing = np.array(User_Complete)
    
    # Initializing List
    User_Filtered = []
    
    # Computing Bounding Box
    x_max = np.max(User_Match[:,0])
    x_min = np.min(User_Match[:,0])
    y_max = np.max(User_Match[:,1])
    y_min = np.min(User_Match[:,1])
    
    Bounding_Box = [x_max,x_min,y_max,y_min]
    
    # Filtering User_Complete
    for i in range(User_Complete.shape[0]):
        if(User_Complete[i,0] <= x_max and User_Complete[i,0] >= x_min and User_Complete[i,1] <= y_max and User_Complete[i,1] >= y_min):
            User_Filtered.append(User_Complete[i])
    
    # Forming Array and Returning User_Filtered
    User_Filtered = np.array(User_Filtered)
    return User_Filtered


# In[19]:


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


# In[29]:


### Tracing Contact

def Trace_Contact(User_Match,User_Filtered,Distance_Threshold,Time_Threshold):
    
    """
    Function to return a list of UniqueID with whom entity in User_Match met with
    
    Inputs : 
    User_Match - Matrix of the user being matched. Information in columns is that of lattitude, longitude and Timestamp
    User_Filtered -  Matrix of only filtered entries for User_Match
    Distance_Threshold - Threshold of Maximum Spatial Seperation
    Time_Threshold - Threshold of Maximum Time Separation
    
    Ouputs :
    User_Contacts - List of UniqueIDs of other users with whom entity in User_Match met
    
    """
    
    # Initializing User_Contacts
    User_Contacts = []
    
    # Defining Trace Contacts Function's Mechanism
    for i in range(User_Match.shape[0]):
        for j in range(User_Filtered.shape[0]):
            if(distance(User_Match[i,0:2],User_Filtered[j,0:2]) <= Distance_Threshold):
                if(User_Match[i,2]>User_Filtered[j,2]):
                    if((User_Match[i,2]-User_Filtered[j,2]) <= Time_Threshold):
                        User_Contacts.append(User_Filtered[j,3])
                elif(User_Match[i,2]<User_Filtered[j,2]):
                    if((User_Filtered[j,2]-User_Match[i,2]) <= Time_Threshold):
                        User_Contacts.append(User_Filtered[j,3])
                else:
                    User_Contacts.append(User_Filtered[j,3])
                    
    # Returning User_Contacts
    return User_Contacts           

