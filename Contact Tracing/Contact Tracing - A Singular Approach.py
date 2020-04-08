#!/usr/bin/env python
# coding: utf-8

# # Contract Tracing: A Singular Approach

# In[2]:


### Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


# In[4]:


### Defining Variables
#N = None # Total No. of Users
#N1 = None # Total entries of user being matched
#N2 = None # Total entries of all the users except the on being traced
#User_Match = [[0,0,0] for a in range(N1)]# Matrix of the user being matched. Information in columns is that of lattitude, longitude and Timestamp
#User_Complete = [[0,0,0,0] for b in range(N2)] # Matrix of location data of all other users except the user in User_Match . Information in columns is that of lattitude, longitude, Timestamp and Unique ID


# In[9]:


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
    User_Complete = np.array(User_Complete)
    
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


# In[10]:


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


# In[16]:


### Tracing Contact

def Trace_Contact(User_Match,User_Filtered,Distance_Threshold,Time_Threshold):
    
    """
    Function to return a list of UniqueID with whom entity in User_Match met with
    
    Inputs : 
    User_Match - Matrix of the user being matched. Information in columns is that of lattitude, longitude and Timestamp
    User_Filtered -  Matrix of only filtered entries for User_Match
    Distance_Threshold - Threshold of Maximum Spatial Seperation in Kms
    Time_Threshold - Threshold of Maximum Time Separation 
    
    Ouputs :
    User_Contacts - List of UniqueIDs of other users with whom entity in User_Match met
    
    """
    
    # Initializing User_Contacts and other lists as arrays
    User_Contacts = []
    User_Match = np.array(User_Match)
    
    # Defining Trace Contacts Function's Mechanism
    for i in range(np.array(User_Match).shape[0]):
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


# In[21]:


### Testing

# Defining 2-D List of dimensions (N1,(LAT,LONG,TIMESTAMP)) and (N2,(LAT,LONG,TIMESTAMP,INDEX)) for User_Match and User_Complete respectively : First filtering by backend database must be done
# Basically User_Match is the matrix(List) which is to be assigned for the User whoose contacts are being traced
# User_Complete is the matrix(List) which contains (LAT,LONG,TIMESTAMP,INDEX) info of all other except the user whoose contacts are being traced

User_Match = [[21.567,81.898,345],[21.7894,81.42242,360.99385],[21.42424,81.46676,380.7678]]
User_Complete = [[21.567,81.898,345,3],[21.985,81.9864,369,3],[21.44242,81.7832145,356.4625345,5],[21.613231,81.73133,340,6],[21.22,81.44,350,7]]

# Function for Filtering

User_Filtered = Filter(User_Match,User_Complete)

# Function for getting Output

Traced_Contacts = Trace_Contact(User_Match,User_Filtered,20,40)
print(Traced_Contacts)

# Note:-
# 1. One may merge Filter and Trace_Contacts Function
# 2. Date_Threshold and Time_Threshold are to be selected as per convinience

