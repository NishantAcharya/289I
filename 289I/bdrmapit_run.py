#!/usr/bin/env python
# coding: utf-8

# In[1]:


from os import listdir
from os.path import isfile, join, isdir
import os
import shutil


# In[2]:


#Changing Directory
os.chdir(r"/Users/nishantacharya/Desktop/bdrmapit_updated/mapkit-traceroute-bdrmapit-pipeline")


# In[3]:


os.getcwd()


# In[4]:


#Helpers
def is_hidden(file):
    return file.startswith('.')


# In[5]:


#creates a folder and puts the files in the folder, for each file in a directory
def folder_creator(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:
        if is_hidden(file):
            continue
        
        newpath = path+'/'+file[:-5]
        filepath = path+'/'+file
        print(newpath)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        if os.path.exists(filepath):
            shutil.move(filepath,newpath)
            
def execute_python_file(file_path):
    try:
        with open(file_path, 'r') as file:
            python_code = file.read()
            exec(python_code)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        


# In[6]:


#Update Config file, takes the path to the config file and the traceroute file and the letter code(upper case) 
#for the country

#'outDir = baseDir + "Output/"' --> the line to update
#'ripeInput = "/Users/nishantacharya/Desktop/bdrmapit_updated/bdrmapit/bdrmapit/traceroutes/R/"' --> The input file
def config_updater(configPath,fileName,filePath,country_code):
    with open(configPath,'r') as f:
        code = [line.strip() for line in f.readlines()]
    
    if country_code == "" or fileName == "":
        outCode = ""
    else:
        outCode = "-"+country_code+"-"+fileName
    
    out_dir = 'outDir = baseDir + ' + '"Output' + outCode+'/"'
    ripe_Input = 'ripeInput = "'+filePath+'"'
    
    if filePath == "":
        ripe_Input = 'ripeInput = "/Users/nishantacharya/Desktop/bdrmapit_updated/bdrmapit/bdrmapit/traceroutes/R/"'
    
    #finding the indicies
    code[3] = out_dir
    code[55] = ripe_Input
    
    with open(configPath,'w') as f:
        f.writelines([f"{line}\n" for line in code])

#Run bdrmapit and then set the value of the config files to deafult as shown above
def run_bdrmapit(dataPath,configPath,sql_to_csv,create_json,country_code):
    #grab the driectory names in the data path
    directories = [f for f in listdir(dataPath) if isdir(join(dataPath, f))]
    
    #for each directory edit the config file, update config and then run the files needed, then reset the config file
    for dr in directories:
        fileName = dr
        filePath = dataPath + '/' + dr
        
        #updating config
        config_updater(configPath,fileName,filePath,country_code)
        
        #execuing bdrmapit files
        execute_python_file(create_json)
        execute_python_file(sql_to_csv)
        
        #resetting the config file
        config_updater(configPath,"","","")


# In[7]:


#Files to edit and run path
config = '/Users/nishantacharya/Desktop/bdrmapit_updated/mapkit-traceroute-bdrmapit-pipeline/config.py'
sql_to_csv = '/Users/nishantacharya/Desktop/bdrmapit_updated/mapkit-traceroute-bdrmapit-pipeline/convert-sql-to-csv.py'
create_json = '/Users/nishantacharya/Desktop/bdrmapit_updated/mapkit-traceroute-bdrmapit-pipeline/create-json-config-and-run-bdrmapit.py'


# In[8]:


#Data paths
#slovakia = '/Users/nishantacharya/Desktop/bdrmapit_updated/bdrmapit/bdrmapit/traceroutes/S/Slovakia'
#romania = '/Users/nishantacharya/Desktop/bdrmapit_updated/bdrmapit/bdrmapit/traceroutes/R/Romania'
turkey = '/Users/nishantacharya/Desktop/bdrmapit_updated/bdrmapit/bdrmapit/traceroutes/T/Turkey'


# In[9]:


#Moving files into a folder
folder_creator(turkey)
#folder_creator(romania)
#folder_creator(slovakia)


# In[10]:


#running bdrmapit
#run_bdrmapit(slovakia,config,sql_to_csv,create_json,'S')
#run_bdrmapit(romania,config,sql_to_csv,create_json,'R')
run_bdrmapit(turkey,config,sql_to_csv,create_json,'T')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




