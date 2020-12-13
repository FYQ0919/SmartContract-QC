#Punchlist
"""
3. Distributive collaboration
7. Need to get draw data from blockchain to trigger the next step, not via python

"""
#import csv file
import pandas
import random

import sqlite3
from sqlite3 import Error


steps = pandas.read_csv('steps_blockchain_dagum.csv')

#for blockchain

import hashlib #library for encryption/hash algorithms
import json #Javascript object notation - encoder/decoder

#JSON = JavaScript Object Notation - an open-standard file format that uses 
#human-readable text to transmit data objects consisting of attribute–value 5

#pairs and array data types (or any other serialisable value). 
#It is a very common data format used for asynchronous browser–server 
#communication

from time import time #import time() function from time module
from urllib.parse import urlparse #parse URL into 6 components - split URL 
#into 6 different components
from uuid import uuid4  
import requests

#Requests = licensed HTTP library
#Requests will allow you to send HTTP/1.1 requests using Python. 
#Add content like headers, form data, multipart files, and parameters 
#via simple Python libraries. It also allows you to access the response 
#data of Python in the same way.

from flask import Flask, jsonify, request
application = Flask(__name__)

#*****************************************************************************

#original parameters

#get number of iterations to perform
iterations = input("Enter number of parts to make ")
iterations = int(iterations)

repeats = input("Enter number of repeats to run ")
repeats = int(repeats)

cumulative_time = 0
cumulative_production_time = 0
cumulative_validation_time = 0

#to get total number of steps
count_row = steps.shape[0]

#row = current step
row = 0      # the index for the first workcell is 0

part_being_made = 0

repeats_performed = 0

part_quality = "Neutral"    #Poor/Good/Reject by 2QC

successful_step_count = 0

'''
Each post is mined as one block.
Alternatively, it's possible to post multiple chunk of data (add in), and mine them as one block. << but not used
There types of situation calling this mine_transaction: sequential transfer of workpiece // redistributed workpiece.
No matter pass or fail, the workcell will also mine a block. Due to many if-else conditions,
this mine_transaction is called multiple time.
'''
Post_Transaction = 'http://localhost:5000/transactions/new'
Mine_Transaction = 'http://localhost:5000/mine'


#*****************************************************************************

while repeats_performed < repeats:
    #print("restart")
    #Assumption: Once there's a defective part, start from step 0 again, with all previous spares used for manufacture of part wasted
    #current point of time, t
    time_stamp = 0
    row = 0
    part_being_made = 0
    steps = pandas.read_csv('steps_blockchain_dagum.csv')
    #*****************************************************************************
    
    #*****************************************************************************
    
    #calculate initial projected times
    
    while row < count_row:
        '''
        This while loop is
        1. to record the projected next production time
        '''
    
        if row == 0:
            
            steps.loc[row,"Projected_Next_Production_Time"] = 0
            
            #print("row86")
            
            row = row + 1   # going to the next workcell
            
        else:
            
            if steps.loc[row,"Existing_Quantity"] == 0:
            
                steps.loc[row,"Projected_Next_Production_Time"] = steps.loc[row-1,"Projected_Next_Production_Time"] + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                
                #print("row96")
                
                row = row + 1
                            
            else:
                
                steps.loc[row,"Projected_Next_Production_Time"] = time_stamp + 1
                
                #print("row104")
                
                row = row + 1
    
    #*****************************************************************************
    
    row = 0
    

    #iterations = number of parts to make
    #part_being_made = part number that is being made
    while part_being_made < iterations:
        '''
        This loop is
        1. to iterate the whole manufacturing process for each part
        '''
                
        while row <= count_row:
            '''
            This while loop is 
            1. to iterate the part_being_made from the previous outer while loop based on manufacturing success
            2. to determine which step that workcell will be doing in the current outer while loop
            '''
            
            #print("row122",row,count_row,)
#at last step                     
            if (row == count_row) and steps.at[row-1, "Existing_Quantity"] > 0:
                
                #print("row125")
                #if status = successful

                # manufacturing correctly part quality can be removed v
                if success > 0 and (part_quality == "Good" or part_quality == "Poor"):
    
                    #print("row130")
 
                    steps.at[row-1, "Existing_Quantity"] = steps.at[row-1, "Existing_Quantity"] - 1
                    part_being_made = part_being_made + 1
                    # for debugging v, to see when going to finish that part
                    print("Part", (part_being_made), "started final step production at", time_stamp-1, "Quality",part_quality)
                    row = 0
                    part_quality = "Neutral"    #just for debugging
                                      
                else:
                    part_being_made = part_being_made    
                    row = 0
                    part_quality = "Neutral"    #just for debugging
                                                                       
            #if number of sueccessful attempts = 0
            else:
                time_stamp = time_stamp + 1
                row = count_row + 1 #to exit from while loop 
                continue #exit current while loop
            
        #to reset/prep for next while loop
        successful_step_count = 0
        
        row = 0
        temp_row = row   
        #*************************************************************************
            
        while row < count_row:
            '''
            *** ONLY CHANGE THIS PORTION IF WANT TO IMPLEMENT THE CODE FOR OTHER USAGE ***
            This loop is for each workcell
            1. to carry out one manufacturing step of the part
            2. to validate that workpiece (done using that step) by one primary validator
            3. to validate that workpiece by 4 secondary validators (no. of validators can be changed)
            4. to compile all validation results to determine part quality
            5. to restart fabricating failed workpiece/part
            6. to send data to blockchain
            7. to perform the distributive function
            '''
            
            #step_that_is_helping portion is for distribution of task
            
                #For distributive             
            
            #continue with original processing
            #row = temp_row
                                  
            if row == 0:    # because there is no spare in the first workcell # the index for the first workcell is 0

                if time_stamp >= steps.loc[row,"Projected_Next_Production_Time"]:   # means workcell is NOT occupied
                    '''
                    This if-else is
                    1. to check if that workcell (row) is occupied
                    if not occupied then only carry manufacturing process
                    '''
                    #*****************************************************************************
                    from random import *
                    
                    random0 = randint(1, 100)    # Pick a random number between 1 and 100
                              
                    success = steps.loc[row,"Probability_of_Success"]*100 - random0
                    
                    random1 = randint(1, 100)    # Pick a random number between 1 and 100
                    
                    correctness = steps.loc[row,"Validation_Correctness"]*100 - random1
                    
                    #secondary validation 1. Add time for correctness check
                    
                    random2 = randint(1, 100)    # Pick a random number between 1 and 100
                
                #secondary validation
                #*****************************************************************************
                                
                    secondary_validation_row_1 = steps.loc[row,"Secondary_Validation_1"] - 1
                    
                    if secondary_validation_row_1 == steps.loc[row,"Step"]:
                        
                        correctness_1 = 1
                    else:
                        correctness_1 = steps.loc[secondary_validation_row_1,"Validation_Correctness"]*100 - random2
                                            
                    #for now...human validation means human drops manufacturing step and works on task on hand immediately
                    #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                        if steps.loc[secondary_validation_row_1,"Validation_Type"] == "Human":
                            
                            steps.loc[secondary_validation_row_1,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_1,"Pending_Validation_Count"] + 1
                            #in case projected next prodution time is way behind current time, normalise current projected time
                            if  steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] < time_stamp:
    
                                 steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] = time_stamp
                                   
                            #else next projection time follows completion of step
                            else:
    
                                steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_1,"Validation_Time"]
         
                    #secondary validation 2
                    
                    random3 = randint(1, 100)    # Pick a random number between 1 and 100
                    
                    secondary_validation_row_2 = steps.loc[row,"Secondary_Validation_2"] - 1
                
                    #if NA = no secondary validation
                    if secondary_validation_row_2 == steps.loc[row,"Step"]:
                        correctness_2 = 1
                    else:
                        correctness_2 = steps.loc[secondary_validation_row_2,"Validation_Correctness"]*100 - random3            
                
                    #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                        if steps.loc[secondary_validation_row_2,"Validation_Type"] == "Human":
                            steps.loc[secondary_validation_row_2,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_2,"Pending_Validation_Count"] + 1
                            #in case projected next prodution time is way behind current time, normalise current projected time
                            if  steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] < time_stamp:
    
                                 steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] = time_stamp 
        
                            #else next projection time follows completion of step
                            else:
    
                                steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_2,"Validation_Time"]
           
                    #secondary validation 3
                    
                    random4 = randint(1, 100)    # Pick a random number between 1 and 100
                    
                    secondary_validation_row_3 = steps.loc[row,"Secondary_Validation_3"] - 1
                   
                    if secondary_validation_row_3 == steps.loc[row,"Step"]:
                        correctness_3 = 1
                    else:
                        correctness_3 = steps.loc[secondary_validation_row_3,"Validation_Correctness"]*100 - random4              
                    
                    #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                        if steps.loc[secondary_validation_row_3,"Validation_Type"] == "Human":
                            steps.loc[secondary_validation_row_3,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_3,"Pending_Validation_Count"] + 1
                            #in case projected next prodution time is way behind current time, normalise current projected time
                            if  steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] < time_stamp:
                                 steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] = time_stamp 
                            #else next projection time follows completion of step
                            else:
                                steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_3,"Validation_Time"]
                 
                    #secondary validation 4
                    
                    random5 = randint(1, 100)    # Pick a random number between 1 and 100
                    
                    secondary_validation_row_4 = steps.loc[row,"Secondary_Validation_4"] - 1
                    
                    if secondary_validation_row_4 == steps.loc[row,"Step"]:
                        correctness_4 = 1
                    else:
                        correctness_4 = steps.loc[secondary_validation_row_4,"Validation_Correctness"]*100 - random5                    
                
                    #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously/instantaneously
                        if steps.loc[secondary_validation_row_4,"Validation_Type"] == "Human":
                            steps.loc[secondary_validation_row_4,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_4,"Pending_Validation_Count"] + 1
                            #in case projected next prodution time is way behind current time, normalise current projected time
                            if  steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] < time_stamp:
                                 steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] = time_stamp 
                            #else next projection time follows completion of step
                            else:
                                steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_4,"Validation_Time"]

                    # part QC classification
                    # Overall part check
                    # >0 is correct validation
                    # <=0 is wrong validation
                    # todo: change part quality to validation
                    if  correctness >=0 and correctness_1 >= 0 and correctness_2 >= 0 and correctness_3 >= 0 and correctness_4 >= 0:
                        part_quality = "Good"
                    
                    else:                                     
                    
                        if  correctness < 0 and correctness_1 < 0 and correctness_2 < 0 and correctness_3 < 0 and correctness_4 < 0:
                            part_quality = "Poor"
                    
                        #if secondary validation catches poor product quality, part is rejected
                        if (correctness_1 >= 0 or correctness_2 >= 0 or correctness_3 >= 0 or correctness_4 >= 0) and correctness <= 0:
                            success = -1
                            part_quality = "Rejected by Secondary QC"            
                        
                    #to track number of previous attempts
                    steps.loc[row,"Number_of_Previous_Attempts"] = steps.loc[row,"Number_of_Previous_Attempts"] + 1
                                    
                    #determination of validation time for purpose of showing final time
                    steps.loc[row,"Total_Validation_Time"] == steps.loc[row,"Validation_Time"]
                
                    if steps.loc[secondary_validation_row_1,"Validation_Type"] == "Human":
                        
                        steps.loc[row,"Total_Validation_Time"] = max(steps.loc[row,"Validation_Time"], steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"])
                        
                    if steps.loc[secondary_validation_row_2,"Validation_Type"] == "Human":
                        
                       steps.loc[row,"Total_Validation_Time"] = max(steps.loc[row,"Validation_Time"], steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"]) 
                    
                    if steps.loc[secondary_validation_row_3,"Validation_Type"] == "Human":
                        
                       steps.loc[row,"Total_Validation_Time"] = max(steps.loc[row,"Validation_Time"], steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"]) 
                    
                    if steps.loc[secondary_validation_row_4,"Validation_Type"] == "Human":
                        
                       steps.loc[row,"Total_Validation_Time"] = max(steps.loc[row,"Validation_Time"], steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"]) 
                    
                #*****************************************************************************
                    
                    #*****************************************************************************
                                   
            #if negative number from previous part, step has failed, repeat step, else, step is a success, proceed to next step at the same time
                    if  success < 0:
                        '''
                        This if-else is for workpiece/part completed successfully or failed
                        1. to prepare the data to be sent to blockchain
                        2. send data to blockchain (post-transaction and then mine-transaction)
                        '''
                        # manufacturing success line
                        cumulative_time = cumulative_time + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                        steps.loc[row,"Cumulative_Production_Time"] = steps.loc[row,"Cumulative_Production_Time"] + steps.loc[row,"Production_Time"]
                        steps.loc[row,"Cumulative_Validation_Time"] = steps.loc[row,"Cumulative_Validation_Time"] + steps.loc[row,"Validation_Time"]                                     
                        steps.at[row,'Projected_Next_Production_Time'] = time_stamp + steps.at[row,'Production_Time'] + steps.at[row,'Validation_Time']                          
        
                        # make sure don't restart the time when redo the failed part, make sure that it's at the next time step
                        #to make sure no simultaneous production
                        if steps.at[row+1,'Projected_Next_Production_Time'] <= time_stamp:
                            steps.at[row+1,'Projected_Next_Production_Time'] = time_stamp + 1   
    
                        
                        #end of spares adjustment
                        
        #prepare data to send to blockchain*******************************************                        
                        
                        status = "Failed"
                        text_temp = "Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Row",row,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row, "Existing_Quantity"]
                        transaction_temp = "Step",steps.at[row,'Step']+1, "Production_Time",steps.at[row, 'Production_Time'],"Validation_Time",steps.at[row, 'Validation_Time'],"Validation_Type",steps.at[row, 'Validation_Type'],"Probability_of_Success",steps.at[row, 'Probability_of_Success'],"Validation_Correctness",steps.at[row, 'Validation_Correctness'],"Existing_Quantity",steps.at[row, "Existing_Quantity"],"Number_of_Previous_Attempts",steps.at[row, 'Number_of_Previous_Attempts'],"Number_of_Successful_Attempts",steps.at[row, 'Number_of_Successful_Attempts'],"Cumulative_Production_Time",steps.at[row, 'Cumulative_Production_Time'],"Cumulative_Validation_Time",steps.at[row, 'Cumulative_Validation_Time'],"Current_Time_Spares",steps.at[row, 'Current_Time_Spares'],"Time_Spare_Changed", steps.at[row, 'Time_Spare_Changed'],"Projected_Next_Production_Time",steps.at[row, 'Projected_Next_Production_Time'],"Secondary_Validation_1",steps.at[row, 'Secondary_Validation_1'],"Secondary_Validation_1_Count",steps.at[row, 'Secondary_Validation_1_Count'],"Secondary_Validation_2",steps.at[row, 'Secondary_Validation_2'],"Secondary_Validation_2_Count",steps.at[row, 'Secondary_Validation_2_Count'],"Secondary_Validation_3",steps.at[row, 'Secondary_Validation_3'],"Secondary_Validation_3_Count",steps.at[row, 'Secondary_Validation_3_Count'],"Secondary_Validation_4",steps.at[row, 'Secondary_Validation_4'],"Secondary_Validation_4_Count",steps.at[row, 'Secondary_Validation_4_Count'],"Pending_Validation_Count",steps.at[row, 'Pending_Validation_Count'],"Total_Validation_Time",steps.at[row, 'Total_Validation_Time'],"Dagum",steps.at[row, 'Dagum']
                                                
                        text = str(text_temp)
                        transaction = str(transaction_temp)
                        status_text = str(status)
                        part_text = str(part_being_made + 1)
                        step_text = str(row)
                        time_stamp_text = str(time_stamp)
                        part_quality_text = str(part_quality)
                        step_spares_text = str(steps.at[row, "Existing_Quantity"])                                                                   
                        
                        #print("row400")
                        
                        print("Status",status,"Iteration", repeats_performed+1,"Part",part_being_made + 1,"Step",steps.at[row, "Step"],"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row, "Existing_Quantity"])
                      
            #send data to blockchain ****************************************************
                      
                        payload = "{\n    \"history\":\""+text+"\",\"transaction\":\""+transaction+"\", \"status\":\""+status_text+"\", \"part\":\""+part_text+"\", \"step\":\""+step_text+"\", \"time\":\""+time_stamp_text+"\", \"quality\":\""+part_quality_text+"\", \"spares\":\""+step_spares_text+"\"}"
                        
                        headers = {
                            'Content-Type': "application/json",
                            }
                        
                        response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
                        
                        print(response.text)
                        
                        h = requests.get(url = Mine_Transaction) 
                            
        #**************************************************************************** 
        
                        #print("row418")
        
                        row = row + 1         
                    #part production successful scenario
                    
                    else:   # if the workpiece/part completed successful
                        
                        #print("389",steps.at[row, "Step"])
                        
                        cumulative_time = cumulative_time + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                        steps.at[row,'Projected_Next_Production_Time'] = max(time_stamp,steps.at[row,'Projected_Next_Production_Time']) + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                                            
                        #to make sure no simultaneous production
                        if steps.at[row+1,'Projected_Next_Production_Time'] <= time_stamp:  
                            steps.at[row+1,'Projected_Next_Production_Time'] = time_stamp + 1   
                                                               
                        
                        steps.loc[row,"Cumulative_Production_Time"] = steps.loc[row,"Cumulative_Production_Time"] + steps.loc[row,"Production_Time"]
                        steps.loc[row,"Cumulative_Validation_Time"] = steps.loc[row,"Cumulative_Validation_Time"] + steps.loc[row,"Validation_Time"]
                        #acknowledge that step is successful - for part success counter - see lines below first while loop
                        steps.at[row,'Number_of_Successful_Attempts'] = steps.at[row,'Number_of_Successful_Attempts'] + 1                    
                        #spare for step increases, spare for previous step decreases
                        steps.at[row, "Existing_Quantity"] = steps.at[row, "Existing_Quantity"]+1

                        if row != 0:
                            steps.at[row-1, "Existing_Quantity"] = steps.at[row-1, "Existing_Quantity"]-1
                                                                                  
                        #condition required for last row
                        
        #to prevent the 0 spares, once spares change at next t = 1 scenario, spare generated, introduce concept of Projected_Next_Production_Time - if t before Projected_Next_Production_Time, no spare production                    
                        steps.at[row, 'Time_Spare_Changed'] = time_stamp + steps.loc[row,"Production_Time"]
        
                        #else: #for last step, no need to add parts to next step
                            #continue    
                        #end of spares adjustment
           
                                               
                        status = "Passed"
                        
                        text_temp = "Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Row",row,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row, "Existing_Quantity"]                      
                        
                        transaction_temp = "Step",steps.at[row, "Existing_Quantity"],"Production_Time",steps.at[row, 'Production_Time'],"Validation_Time",steps.at[row, 'Validation_Time'],"Validation_Type",steps.at[row, 'Validation_Type'],"Probability_of_Success",steps.at[row, 'Probability_of_Success'],"Validation_Correctness",steps.at[row, 'Validation_Correctness'],"Existing_Quantity",steps.at[row, "Existing_Quantity"],"Number_of_Previous_Attempts",steps.at[row, 'Number_of_Previous_Attempts'],"Number_of_Successful_Attempts",steps.at[row, 'Number_of_Successful_Attempts'],"Cumulative_Production_Time",steps.at[row, 'Cumulative_Production_Time'],"Cumulative_Validation_Time",steps.at[row, 'Cumulative_Validation_Time'],"Current_Time_Spares",steps.at[row, 'Current_Time_Spares'],"Time_Spare_Changed", steps.at[row, 'Time_Spare_Changed'],"Projected_Next_Production_Time",steps.at[row, 'Projected_Next_Production_Time'],"Secondary_Validation_1",steps.at[row, 'Secondary_Validation_1'],"Secondary_Validation_1_Count",steps.at[row, 'Secondary_Validation_1_Count'],"Secondary_Validation_2",steps.at[row, 'Secondary_Validation_2'],"Secondary_Validation_2_Count",steps.at[row, 'Secondary_Validation_2_Count'],"Secondary_Validation_3",steps.at[row, 'Secondary_Validation_3'],"Secondary_Validation_3_Count",steps.at[row, 'Secondary_Validation_3_Count'],"Secondary_Validation_4",steps.at[row, 'Secondary_Validation_4'],"Secondary_Validation_4_Count",steps.at[row, 'Secondary_Validation_4_Count'],"Pending_Validation_Count",steps.at[row, 'Pending_Validation_Count'],"Total_Validation_Time",steps.at[row, 'Total_Validation_Time'],"Dagum",steps.at[row, 'Dagum']
                            
                        # Need to make sure no simultaneous action when 0 then add 1 = all action/create at same time
            
                        status = "Passed"
                                   
                        text = str(text_temp)
                        transaction = str(transaction_temp)
                        status_text = str(status)
                        part_text = str(part_being_made + 1)
                        step_text = str(row)
                        time_stamp_text = str(time_stamp)
                        part_quality_text = str(part_quality)
                        step_spares_text = str(steps.at[row, "Existing_Quantity"])
                                                                       
                        #print("row473")
                        
                        print("Status",status,"Iteration", repeats_performed+1,"Part",part_being_made + 1,"Step",steps.at[row, "Step"],"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row, "Existing_Quantity"])
                        
         #send data to blockchain ****************************************************
        
                        payload = "{\n    \"history\":\""+text+"\",\"transaction\":\""+transaction+"\", \"status\":\""+status_text+"\", \"part\":\""+part_text+"\", \"step\":\""+step_text+"\", \"time\":\""+time_stamp_text+"\", \"quality\":\""+part_quality_text+"\", \"spares\":\""+step_spares_text+"\"}"
                        
                        headers = {
                            'Content-Type': "application/json",
                            }
                        
                        response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
                        
                        print(response.text)
                        
                        h = requests.get(url = Mine_Transaction) 
                                                         
         #***************************************************************************** 
    
                        #print("row489",row)
               
                        row = row + 1
                        
                else:   # if time_stamp is less than projected next production time # means workcell is occupied
                    
                    #print("row495", row)
                    
                    row = row + 1
                    

            else:    # for rows > 0 (the rest of the workcells, not the first)
                
                #print("row455",row,time_stamp,steps.loc[row,"Projected_Next_Production_Time"])
                
                if time_stamp >= steps.loc[row,"Projected_Next_Production_Time"]:
                    '''
                    *** REPLACE THIS CHECKING OCCUPACY METHOD FOR EXPERIMENT ***
                    This if-else is
                    1. to check if that workcell (row) is occupied
                    if not occupied then only carry manufacturing process
                    '''
                #check if previous step spares > 0, if it is larger than 0, carry on
                    # ^ this line doesn't apply to the first workcell (row=0)
                    if steps.loc[row-1, "Existing_Quantity"] > 0:
                        
                        #print("spares479")
        
                        if time_stamp >= steps.loc[row,"Projected_Next_Production_Time"]:
                            #*****************************************************************************
                            # from here onward exactly the same as the first workcell
                            from random import *
                           
                            random0 = randint(1, 100)    # Pick a random number between 1 and 100
                                      
                            success = steps.loc[row,"Probability_of_Success"]*100 - random0
                            
                            random1 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            correctness = steps.loc[row,"Validation_Correctness"]*100 - random1
                            
                            #secondary validation 1. Add time for correctness check
                            
                            random2 = randint(1, 100)    # Pick a random number between 1 and 100
                        
                        #secondary validation
                        #*****************************************************************************
                                        
                            secondary_validation_row_1 = steps.loc[row,"Secondary_Validation_1"] - 1
                            
                            if secondary_validation_row_1 == steps.loc[row,"Step"]:
                                correctness_1 = 1
                            else:
                                correctness_1 = steps.loc[secondary_validation_row_1,"Validation_Correctness"]*100 - random2
                                                    
                            #for now...human validation means human drops manufacturing step and works on task on hand immediately
                            #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                if steps.loc[secondary_validation_row_1,"Validation_Type"] == "Human":
                                    steps.loc[secondary_validation_row_1,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_1,"Pending_Validation_Count"] + 1
                                    #in case projected next prodution time is way behind current time, normalise current projected time
                                    if  steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] < time_stamp:
                                        steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] = time_stamp
                                           
                                    #else next projection time follows completion of step
                                    else:
                                        steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_1,"Validation_Time"]
                 
                            #secondary validation 2
                            
                            random3 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            secondary_validation_row_2 = steps.loc[row,"Secondary_Validation_2"] - 1
                        
                            #if NA = no secondary validation
                            if secondary_validation_row_2 == steps.loc[row,"Step"]:
                                correctness_2 = 1
                            else:
                                correctness_2 = steps.loc[secondary_validation_row_2,"Validation_Correctness"]*100 - random3            
                        
                            #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                if steps.loc[secondary_validation_row_2,"Validation_Type"] == "Human":
                                    steps.loc[secondary_validation_row_2,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_2,"Pending_Validation_Count"] + 1
                                    #in case projected next prodution time is way behind current time, normalise current projected time
                                    if  steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] < time_stamp: 
                                        steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] = time_stamp
                
                                    #else next projection time follows completion of step
                                    else:
                                        steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_2,"Validation_Time"]
                 
                  
                            #secondary validation 3
                            
                            random4 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            secondary_validation_row_3 = steps.loc[row,"Secondary_Validation_3"] - 1
                           
                            if secondary_validation_row_3 == steps.loc[row,"Step"]:
                                correctness_3 = 1
                            else:
                                correctness_3 = steps.loc[secondary_validation_row_3,"Validation_Correctness"]*100 - random4              
                            
                            #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                if steps.loc[secondary_validation_row_3,"Validation_Type"] == "Human":
                                    steps.loc[secondary_validation_row_3,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_3,"Pending_Validation_Count"] + 1
                                    #in case projected next prodution time is way behind current time, normalise current projected time
                                    if  steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] < time_stamp:
                                        steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] = time_stamp
                                    #else next projection time follows completion of step
                                    else:
                                        steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_3,"Validation_Time"]
                         
                            #secondary validation 4
                            
                            random5 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            secondary_validation_row_4 = steps.loc[row,"Secondary_Validation_4"] - 1
                            
                            if secondary_validation_row_4 == steps.loc[row,"Step"]:
                                correctness_4 = 1
                            else:
                                correctness_4 = steps.loc[secondary_validation_row_4,"Validation_Correctness"]*100 - random5                    
                        
                            #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously/instantaneously
                                if steps.loc[secondary_validation_row_4,"Validation_Type"] == "Human":
                                    steps.loc[secondary_validation_row_4,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_4,"Pending_Validation_Count"] + 1
                                    #in case projected next prodution time is way behind current time, normalise current projected time
                                    if  steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] < time_stamp:
                                        steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] = time_stamp
                                    #else next projection time follows completion of step
                                    else:
                                        steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_4,"Validation_Time"]
                                                                                                       
                            #part QC classification
                            if  correctness >=0 and correctness_1 >= 0 and correctness_2 >= 0 and correctness_3 >= 0 and correctness_4 >= 0:
                                part_quality = "Good"
                            
                            else:                                     
                            
                                if  correctness < 0 and correctness_1 < 0 and correctness_2 < 0 and correctness_3 < 0 and correctness_4 < 0:
                                    part_quality = "Poor"
                            
                                #if secondary validation catches poor product quality, part is rejected
                                if (correctness_1 >= 0 or correctness_2 >= 0 or correctness_3 >= 0 or correctness_4 >= 0) and correctness >= 0:
                                    success = -1
                                    part_quality = "Rejected by Secondary QC"            
                                
                            #to track number of previous attempts
                            steps.loc[row,"Number_of_Previous_Attempts"] = steps.loc[row,"Number_of_Previous_Attempts"] + 1
                                            
                            #determination of validation time for purpose of showing final time
                            steps.loc[row,"Total_Validation_Time"] == steps.loc[row,"Validation_Time"]
                        
                            if steps.loc[secondary_validation_row_1,"Validation_Type"] == "Human":
                                
                                steps.loc[row,"Total_Validation_Time"] = max(steps.loc[row,"Validation_Time"], steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"])
                                
                            if steps.loc[secondary_validation_row_2,"Validation_Type"] == "Human":
                                
                               steps.loc[row,"Total_Validation_Time"] = max(steps.loc[row,"Validation_Time"], steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"]) 
                            
                            if steps.loc[secondary_validation_row_3,"Validation_Type"] == "Human":
                                
                               steps.loc[row,"Total_Validation_Time"] = max(steps.loc[row,"Validation_Time"], steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"]) 
                            
                            if steps.loc[secondary_validation_row_4,"Validation_Type"] == "Human":
                                
                               steps.loc[row,"Total_Validation_Time"] = max(steps.loc[row,"Validation_Time"], steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"]) 
                            
                        #*****************************************************************************
                            
                            #*****************************************************************************
                                           
                    #if negative number from previous part, step has failed, repeat step, else, step is a success, proceed to next step at the same time
                            if  success < 0:                      
                                cumulative_time = cumulative_time + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                                steps.loc[row,"Cumulative_Production_Time"] = steps.loc[row,"Cumulative_Production_Time"] + steps.loc[row,"Production_Time"]
                                steps.loc[row,"Cumulative_Validation_Time"] = steps.loc[row,"Cumulative_Validation_Time"] + steps.loc[row,"Validation_Time"]
                                                     
                                #if you fail, remain stagnant at this step? No, you repeat this step, but at a different time use your old spares to make new part
                                if row != 0:
                                    steps.at[row,'Projected_Next_Production_Time'] = time_stamp + steps.at[row,'Production_Time'] + steps.at[row,'Validation_Time']                          
                                    steps.at[row-1, "Existing_Quantity"] = steps.at[row-1, "Existing_Quantity"]-1
            
                                
                                if row + 1 < count_row:
                                
                                    #to make sure no simultaneous production
                                    if steps.at[row+1,'Projected_Next_Production_Time'] <= time_stamp:  
                                        steps.at[row+1,'Projected_Next_Production_Time'] = time_stamp + 1   
                                                                                        
                                if row == 0:
                                    steps.at[row,'Projected_Next_Production_Time'] = time_stamp + steps.at[row,'Production_Time'] + steps.at[row,'Validation_Time']                          
            
                                #end of spares adjustment
                                
            #prepare data to send to blockchain*******************************************                        
                                
                                status = "Failed"
                                text_temp = "Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Row",row,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row, "Existing_Quantity"]
                                transaction_temp = "Step",steps.at[row,'Step']+1,"Production_Time",steps.at[row, 'Production_Time'],"Validation_Time",steps.at[row, 'Validation_Time'],"Validation_Type",steps.at[row, 'Validation_Type'],"Probability_of_Success",steps.at[row, 'Probability_of_Success'],"Validation_Correctness",steps.at[row, 'Validation_Correctness'],"Existing_Quantity",steps.at[row, "Existing_Quantity"],"Number_of_Previous_Attempts",steps.at[row, 'Number_of_Previous_Attempts'],"Number_of_Successful_Attempts",steps.at[row, 'Number_of_Successful_Attempts'],"Cumulative_Production_Time",steps.at[row, 'Cumulative_Production_Time'],"Cumulative_Validation_Time",steps.at[row, 'Cumulative_Validation_Time'],"Current_Time_Spares",steps.at[row, 'Current_Time_Spares'],"Time_Spare_Changed", steps.at[row, 'Time_Spare_Changed'],"Projected_Next_Production_Time",steps.at[row, 'Projected_Next_Production_Time'],"Secondary_Validation_1",steps.at[row, 'Secondary_Validation_1'],"Secondary_Validation_1_Count",steps.at[row, 'Secondary_Validation_1_Count'],"Secondary_Validation_2",steps.at[row, 'Secondary_Validation_2'],"Secondary_Validation_2_Count",steps.at[row, 'Secondary_Validation_2_Count'],"Secondary_Validation_3",steps.at[row, 'Secondary_Validation_3'],"Secondary_Validation_3_Count",steps.at[row, 'Secondary_Validation_3_Count'],"Secondary_Validation_4",steps.at[row, 'Secondary_Validation_4'],"Secondary_Validation_4_Count",steps.at[row, 'Secondary_Validation_4_Count'],"Pending_Validation_Count",steps.at[row, 'Pending_Validation_Count'],"Total_Validation_Time",steps.at[row, 'Total_Validation_Time'],"Dagum",steps.at[row, 'Dagum']
                                                        
                                text = str(text_temp)
                                transaction = str(transaction_temp)
                                status_text = str(status)
                                part_text = str(part_being_made + 1)
                                step_text = str(row)
                                time_stamp_text = str(time_stamp)
                                part_quality_text = str(part_quality)
                                step_spares_text = str(steps.at[row - 1, "Existing_Quantity"])                                                                   
                                
                                #print("700")
                                
                                print("Status",status,"Iteration", repeats_performed+1,"Part",part_being_made + 1,"Step",steps.at[row, "Step"],"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row, "Existing_Quantity"])
                              
            #send data to blockchain ****************************************************
                              
                                payload = "{\n    \"history\":\""+text+"\",\"transaction\":\""+transaction+"\", \"status\":\""+status_text+"\", \"part\":\""+part_text+"\", \"step\":\""+step_text+"\", \"time\":\""+time_stamp_text+"\", \"quality\":\""+part_quality_text+"\", \"spares\":\""+step_spares_text+"\"}"
                                
                                headers = {
                                    'Content-Type': "application/json",
                                    }
                                
                                response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
                                
                                print(response.text)
                                
                                h = requests.get(url = Mine_Transaction)
                                                         
            #****************************************************************************                                                
            
            #if got spares (workpiece from previous workcell), continue, else start from front again
                                if row < count_row:
                                    if steps.loc[row, "Existing_Quantity"] > 0:
                                        row = row
                                        steps.loc[row, "Existing_Quantity"] = steps.loc[row, "Existing_Quantity"] - 1
                                        print("Spare used at step ", steps.loc[row, "Step"])
                                    else:
                                        row = 0
                                        print("No spares at step ", steps.loc[row, "Step"])
                                else:
                                    row = 0
                                    print("Restart. Last step failed, no spares")
                                    
            #**************************************************************************** 
                                     
                            #part production successful scenario
                            
                            else:  
                                
                                cumulative_time = cumulative_time + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                                steps.at[row,'Projected_Next_Production_Time'] = max(time_stamp, steps.at[row,'Projected_Next_Production_Time']) + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                                
                                if row + 1 < count_row:
                                    #to make sure no simultaneous production
                                    if steps.at[row+1,'Projected_Next_Production_Time'] <= time_stamp:  
                                        steps.at[row+1,'Projected_Next_Production_Time'] = time_stamp + 1                           
                                
                                steps.loc[row,"Cumulative_Production_Time"] = steps.loc[row,"Cumulative_Production_Time"] + steps.loc[row,"Production_Time"]
                                steps.loc[row,"Cumulative_Validation_Time"] = steps.loc[row,"Cumulative_Validation_Time"] + steps.loc[row,"Validation_Time"]
                                #acknowledge that step is successful - for part success counter - see lines below first while loop
                                steps.at[row,'Number_of_Successful_Attempts'] = steps.at[row,'Number_of_Successful_Attempts'] + 1                    
                                #spare for next step increases, spare for existing step decreases
                                steps.at[row, "Existing_Quantity"] = steps.at[row, "Existing_Quantity"]+1
                                
                               
                                
                                
                                if row != 0:
                                    steps.at[row-1, "Existing_Quantity"] = steps.at[row-1, "Existing_Quantity"]-1
                                                               
                                if row+1 < count_row:
                                    if steps.at[row+1, "Existing_Quantity"] == 0:
                                        steps.at[row+1,'Projected_Next_Production_Time'] = steps.at[row+1,'Projected_Next_Production_Time'] + 1
                                                                                        
                                #condition required for last row
                                
            #to prevent the 0 spares, once spares change at next t = 1 scenario, spare generated, introduce concept of Projected_Next_Production_Time - if t before Projected_Next_Production_Time, no spare production                    
                                steps.at[row, 'Time_Spare_Changed'] = time_stamp + steps.loc[row,"Production_Time"]
            
                                #else: #for last step, no need to add parts to next step
                                    #continue    
                                #end of spares adjustment
                                if row + 1 < count_row:
                                    
                                    #print("row767")
                                    
                                    row = row + 1
                                                                                   
                                status = "Passed" # pass means completed successfully
                                
                                text_temp = "Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Row",row-1,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row-1, "Existing_Quantity"]                      
                                
                                transaction_temp = "Step",steps.at[row-1,"Step"],"Production_Time",steps.at[row-1, 'Production_Time'],"Validation_Time",steps.at[row-1, 'Validation_Time'],"Validation_Type",steps.at[row-1, 'Validation_Type'],"Probability_of_Success",steps.at[row-1, 'Probability_of_Success'],"Validation_Correctness",steps.at[row-1, 'Validation_Correctness'],"Existing_Quantity",steps.at[row-1, "Existing_Quantity"],"Number_of_Previous_Attempts",steps.at[row-1, 'Number_of_Previous_Attempts'],"Number_of_Successful_Attempts",steps.at[row-1, 'Number_of_Successful_Attempts'],"Cumulative_Production_Time",steps.at[row-1, 'Cumulative_Production_Time'],"Cumulative_Validation_Time",steps.at[row-1, 'Cumulative_Validation_Time'],"Current_Time_Spares",steps.at[row-1, 'Current_Time_Spares'],"Time_Spare_Changed", steps.at[row-1, 'Time_Spare_Changed'],"Projected_Next_Production_Time",steps.at[row-1, 'Projected_Next_Production_Time'],"Secondary_Validation_1",steps.at[row-1, 'Secondary_Validation_1'],"Secondary_Validation_1_Count",steps.at[row-1, 'Secondary_Validation_1_Count'],"Secondary_Validation_2",steps.at[row-1, 'Secondary_Validation_2'],"Secondary_Validation_2_Count",steps.at[row-1, 'Secondary_Validation_2_Count'],"Secondary_Validation_3",steps.at[row-1, 'Secondary_Validation_3'],"Secondary_Validation_3_Count",steps.at[row-1, 'Secondary_Validation_3_Count'],"Secondary_Validation_4",steps.at[row-1, 'Secondary_Validation_4'],"Secondary_Validation_4_Count",steps.at[row-1, 'Secondary_Validation_4_Count'],"Pending_Validation_Count",steps.at[row-1, 'Pending_Validation_Count'],"Total_Validation_Time",steps.at[row-1, 'Total_Validation_Time'],"Dagum",steps.at[row-1, 'Dagum']
                                    
                                # Need to make sure no simultaneous action when 0 then add 1 = all action/create at same time
                    
                                status = "Passed"
                                           
                                text = str(text_temp)
                                transaction = str(transaction_temp)
                                status_text = str(status)
                                part_text = str(part_being_made + 1)
                                step_text = str(row)
                                time_stamp_text = str(time_stamp)
                                part_quality_text = str(part_quality)
                                step_spares_text = str(steps.at[row - 1, "Existing_Quantity"])
                                                                               
                                #print("row760")
                                
                                print("Status",status,"Iteration", repeats_performed+1,"Part",part_being_made + 1,"Step",steps.at[row-1, "Step"],"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row-1, "Existing_Quantity"])
                                
             #send data to blockchain ****************************************************
            
                                payload = "{\n    \"history\":\""+text+"\",\"transaction\":\""+transaction+"\", \"status\":\""+status_text+"\", \"part\":\""+part_text+"\", \"step\":\""+step_text+"\", \"time\":\""+time_stamp_text+"\", \"quality\":\""+part_quality_text+"\", \"spares\":\""+step_spares_text+"\"}"
                                
                                headers = {
                                    'Content-Type': "application/json",
                                    }
                                
                                response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
                                
                                print(response.text)
                                
                                h = requests.get(url = Mine_Transaction) 
                                                                 
             #*****************************************************************************
                        #if time_stamp <= steps.loc[row,"Projected_Next_Production_Time"] in other words, time not up yet
                        else:
                            
                            #print("row810")
                            
                            row = row + 1   
                    
                    #if step spares = 0, go to next step    
                    else:
                   
                        #print("row769")
                        
                        row = row + 1
                        continue      
                
          
                else:
                                   
                    row = row + 1
                    
                    #print("row781",row)

                    # todo: exactly the same ends here
    
                    continue
            
    ###############################################################################################################################################################        
            #for distributive collaboration
    ###############################################################################################################################################################
            '''
            *** THIS PART NEED TO REPLACE THE OCCUPANCY PORTION FOR EXPERIMENT ***
            This is to redistribute workcell with most work to the workcell with the least work
            '''
            #*************************************************************************
            temp_row = row
            
            #print("Zero793", row)
            
            row = 0
        
            counter = 0        
    
            #temp_row needed to store row number whilst Dagum is being calculated at every t
        
            while row < count_row:
                '''
                This loop is to
                #calculate Dagum
                #prepardness Z taken to be 1
                #need if statement else those with 0 cumulative times get wrong Dagum values
                #need to plus prod and validation times because time_stamp = time at point of step
                '''

                Gini = (steps.loc[row,'Cumulative_Production_Time']+steps.loc[row,'Cumulative_Validation_Time'])/(steps['Cumulative_Production_Time'].sum()+steps['Cumulative_Validation_Time'].sum())
                
                
                #initial Dagum values taken to be 1 - max inequality
                if Gini != 1:
                    
                    steps.loc[row,'Dagum'] = (1- Gini)/(1 + Gini)
                #steps.loc[row,'Dagum'] = ((1-((steps.loc[row,'Cumulative_Production_Time']+steps.loc[row,'Cumulative_Validation_Time'])/time_stamp)) )
                
                else:
                    
                    steps.loc[row,'Dagum'] = 0
                
                #print("row807",row)
                #row = row + 1    
            
            #identify highest Dagum and lowest Dagum
            
                #print("837",row, steps.loc[row,'Dagum'], Gini)
            
                row_highest_Dagum = steps['Dagum'].idxmax(0)    # job in this workcell will be taken away
                
                row_lowest_Dagum = steps['Dagum'].idxmin(0)     # this workcell will be given the job
        
                #row = temp_row
                
                #need to add condition that previous step must not have step spares that are 0 so that guy has things to work on for subsequent steps
                    
                if row_highest_Dagum !=  0 :    # need to consider spare
                    
                    #print("row822",row)
    
                    if steps.loc[row_highest_Dagum - 1,'Existing_Quantity'] == 0:
                        
                        #print("row837",row)
                        
                        #if step before has no spares, recursively go back steps until step has spares
                        while steps.loc[row_highest_Dagum - 1,'Existing_Quantity'] == 0 and row_highest_Dagum - 1 != 0 :
                            
                            #print("row842", row_highest_Dagum)
                            
                            row_highest_Dagum = row_highest_Dagum - 1
                            
                    else:
                        
                        
                        row_highest_Dagum = row_highest_Dagum
                        
                        
                    if steps.loc[row_lowest_Dagum ,'Projected_Next_Production_Time'] > time_stamp:
                        '''
                        *** REPLACE THIS CHECKING OCCUPACY METHOD FOR EXPERIMENT ***
                        This if-else is to check occupancy of that workcell and have spares before it
                        '''
                        #repeat max number of while loop below for as many times as there are steps
                        repeat_counter = 0
                        
                        #print("row837",row)
                                                #if step before has no spares, recursively go back steps until step has spares
                        while steps.loc[row_lowest_Dagum ,'Projected_Next_Production_Time'] > time_stamp and repeat_counter != count_row :
                            
                            #change the row's dagum to get 2nd lowest /nth lowest dagum
                            
                            steps.loc[row,'Dagum'] = 9999999
                            
                            row_lowest_Dagum = steps['Dagum'].idxmin(0)
                            
                            repeat_counter = repeat_counter + 1
                            
                    else:
                        
                        row_lowest_Dagum = row_lowest_Dagum                        
                        

                else: #for row 0, because don't need to consider spares
                    
                    #print("row839",row)

                    row_highest_Dagum = row_highest_Dagum
                                   
                #redistribute highest Dagum to lowest Dagum - dynamically...at every t, this is analysed
                #with lowest Dagum being assigned jobs from highest Dagum
                #in the event of conflict (e.g. >1 step have same Dagum), lowest numbering
                #step will get redistributed.
                
                #redistribution will only occur when Dagum is too much
                
                
                if steps.loc[row_highest_Dagum,'Dagum'] > 0 :
                    #step with smallest Dagum takes on production task of step with largest Dagum
                    #step with smallest Dagum will have added projected time due to additional manufacturing task
                    
                    #print("row855",row, steps.loc[row,'Dagum'], Gini)
    
                    step_for_redistribution = row_highest_Dagum
                    step_that_is_helping = row_lowest_Dagum                    
                    
                    #if step_for_redistribution's previous step got no spares, go back one more step
                    
                    if step_for_redistribution != 0:
                    
                        if steps.loc[step_for_redistribution-1, "Existing_Quantity"] == 0:
                            
                            step_for_redistribution = step_for_redistribution - 1
                    
                    
                    else:
                        
                        step_for_redistribution = 0
                    
                    
                    
                    if step_for_redistribution == 0:
                        
                         #print("row864",row)
                                          
                      
                         # todo: repeat line 528 but different variables, be careful (row >> step_for_redistribution)
                         if time_stamp >= steps.loc[step_that_is_helping ,"Projected_Next_Production_Time"]:
                            #*****************************************************************************
                            
                            #print("HELP889",row)                        
                            
                            from random import *
                           
                            random0 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            #success of part creation still dependent on the original step's probability of success
                            #not the helping step/station's probability of success
                                      
                            success = steps.loc[step_for_redistribution,"Probability_of_Success"]*100 - random0
                            
                            random1 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            correctness = steps.loc[step_for_redistribution,"Validation_Correctness"]*100 - random1
                            
                            #secondary validation 1. Add time for correctness check
                            
                            random2 = randint(1, 100)    # Pick a random number between 1 and 100
                        
                        #secondary validation - in redistributed work, validation will still be done by the individual
                        #stations and the stations designated to be secondary reviewers
                        
                        #*****************************************************************************
                                        
                            secondary_validation_row_1 = steps.loc[step_for_redistribution,"Secondary_Validation_1"] - 1
                            
                            if secondary_validation_row_1 == steps.loc[step_for_redistribution,"Step"]:
                                correctness_1 = 1
                            else:
                                correctness_1 = steps.loc[secondary_validation_row_1,"Validation_Correctness"]*100 - random2
                                                    
                            #for now...human validation means human drops manufacturing step and works on task on hand immediately
                            #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                if steps.loc[secondary_validation_row_1,"Validation_Type"] == "Human":
                                    steps.loc[secondary_validation_row_1,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_1,"Pending_Validation_Count"] + 1
                                    #in case projected next prodution time is way behind current time, normalise current projected time
                                    if  steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] < time_stamp:
                                        steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] = time_stamp
                                           
                                    #else next projection time follows completion of step
                                    else:
                                        steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_1,"Validation_Time"]
                 
                            #secondary validation 2
                            
                            random3 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            secondary_validation_row_2 = steps.loc[step_for_redistribution,"Secondary_Validation_2"] - 1
                        
                            #if NA = no secondary validation
                            if secondary_validation_row_2 == steps.loc[step_for_redistribution,"Step"]:
                                correctness_2 = 1
                            else:
                                correctness_2 = steps.loc[secondary_validation_row_2,"Validation_Correctness"]*100 - random3            
                        
                            #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                if steps.loc[secondary_validation_row_2,"Validation_Type"] == "Human":
                                    steps.loc[secondary_validation_row_2,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_2,"Pending_Validation_Count"] + 1
                                    #in case projected next prodution time is way behind current time, normalise current projected time
                                    if  steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] < time_stamp: 
                                        steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] = time_stamp
                
                                    #else next projection time follows completion of step
                                    else:
                                        steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_2,"Validation_Time"]
                 
                  
                            #secondary validation 3
                            
                            random4 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            secondary_validation_row_3 = steps.loc[step_for_redistribution,"Secondary_Validation_3"] - 1
                           
                            if secondary_validation_row_3 == steps.loc[step_for_redistribution,"Step"]:
                                correctness_3 = 1
                            else:
                                correctness_3 = steps.loc[secondary_validation_row_3,"Validation_Correctness"]*100 - random4              
                            
                            #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                if steps.loc[secondary_validation_row_3,"Validation_Type"] == "Human":
                                    steps.loc[secondary_validation_row_3,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_3,"Pending_Validation_Count"] + 1
                                    #in case projected next prodution time is way behind current time, normalise current projected time
                                    if  steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] < time_stamp:
                                        steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] = time_stamp
                                    #else next projection time follows completion of step
                                    else:
                                        steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_3,"Validation_Time"]
                         
                            #secondary validation 4
                            
                            random5 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            secondary_validation_row_4 = steps.loc[step_for_redistribution,"Secondary_Validation_4"] - 1
                            
                            if secondary_validation_row_4 == steps.loc[step_for_redistribution,"Step"]:
                                correctness_4 = 1
                            else:
                                correctness_4 = steps.loc[secondary_validation_row_4,"Validation_Correctness"]*100 - random5                    
                        
                            #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously/instantaneously
                                if steps.loc[secondary_validation_row_4,"Validation_Type"] == "Human":
                                    steps.loc[secondary_validation_row_4,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_4,"Pending_Validation_Count"] + 1
                                    #in case projected next prodution time is way behind current time, normalise current projected time
                                    if  steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] < time_stamp:
                                        steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] = time_stamp
                                    #else next projection time follows completion of step
                                    else:
                                        steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_4,"Validation_Time"]
                                                                                                       
                            #part QC classification
                            if  correctness >=0 and correctness_1 >= 0 and correctness_2 >= 0 and correctness_3 >= 0 and correctness_4 >= 0:
                                part_quality = "Good"
                            
                            else:                                     
                            
                                if  correctness < 0 and correctness_1 < 0 and correctness_2 < 0 and correctness_3 < 0 and correctness_4 < 0:
                                    part_quality = "Poor"
                            
                                #if secondary validation catches poor product quality, part is rejected
                                if (correctness_1 >= 0 or correctness_2 >= 0 or correctness_3 >= 0 or correctness_4 >= 0) and correctness >= 0:
                                    success = -1
                                    part_quality = "Rejected by Secondary QC"            
                                
                            #to track number of previous attempts
                            steps.loc[step_for_redistribution,"Number_of_Previous_Attempts"] = steps.loc[step_for_redistribution,"Number_of_Previous_Attempts"] + 1
                                            
                            #determination of validation time for purpose of showing final time
                            steps.loc[step_for_redistribution,"Total_Validation_Time"] == steps.loc[step_for_redistribution,"Validation_Time"]
                        
                            if steps.loc[secondary_validation_row_1,"Validation_Type"] == "Human":
                                
                                steps.loc[step_for_redistribution,"Total_Validation_Time"] = max(steps.loc[step_for_redistribution,"Validation_Time"], steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"])
                                
                            if steps.loc[secondary_validation_row_2,"Validation_Type"] == "Human":
                                
                               steps.loc[step_for_redistribution,"Total_Validation_Time"] = max(steps.loc[step_for_redistribution,"Validation_Time"], steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"]) 
                            
                            if steps.loc[secondary_validation_row_3,"Validation_Type"] == "Human":
                                
                               steps.loc[step_for_redistribution,"Total_Validation_Time"] = max(steps.loc[step_for_redistribution,"Validation_Time"], steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"]) 
                            
                            if steps.loc[secondary_validation_row_4,"Validation_Type"] == "Human":
                                
                               steps.loc[step_for_redistribution,"Total_Validation_Time"] = max(steps.loc[step_for_redistribution,"Validation_Time"], steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"]) 
                            
                        #*****************************************************************************
                            
                            #*****************************************************************************
                                           
                    #if negative number from previous part, step has failed, repeat step, else, step is a success, proceed to next step at the same time
                            if  success < 0:                      
                                cumulative_time = cumulative_time + steps.loc[step_for_redistribution,"Production_Time"] + steps.loc[step_for_redistribution,"Validation_Time"]
                                steps.loc[step_for_redistribution,"Cumulative_Production_Time"] = steps.loc[step_for_redistribution,"Cumulative_Production_Time"] + steps.loc[step_for_redistribution,"Production_Time"]
                                steps.loc[step_for_redistribution,"Cumulative_Validation_Time"] = steps.loc[step_for_redistribution,"Cumulative_Validation_Time"] + steps.loc[step_for_redistribution,"Validation_Time"]
                                                     
                                #if you fail, remain stagnant at this step? No, you repeat this step, but at a different time use your old spares to make new part
                                if step_for_redistribution != 0:
                                    #any projected next time incurred by manufacturing must go to the helping step
                                    #but any projected time for validation goes to original step
                                    steps.at[step_for_redistribution,'Projected_Next_Production_Time'] =  steps.at[step_for_redistribution,'Projected_Next_Production_Time'] + steps.at[step_for_redistribution,'Validation_Time']                          
                                    steps.at[step_that_is_helping,'Projected_Next_Production_Time'] = steps.at[step_that_is_helping,'Projected_Next_Production_Time'] + steps.at[step_that_is_helping,'Production_Time']                          
                                    steps.at[step_for_redistribution-1, "Existing_Quantity"] = steps.at[step_for_redistribution-1, "Existing_Quantity"]-1
            
                                
                                if step_that_is_helping + 1 < count_row:
                                
                                    #to make sure no simultaneous production
                                    if steps.at[step_that_is_helping+1,'Projected_Next_Production_Time'] <= time_stamp:  
                                        steps.at[step_that_is_helping+1,'Projected_Next_Production_Time'] = time_stamp + 1   
                                                                                        
                                if step_for_redistribution == 0:
                                    steps.at[step_that_is_helping,'Projected_Next_Production_Time'] = steps.at[step_for_redistribution,'Production_Time'] + steps.at[step_that_is_helping,'Projected_Next_Production_Time']                      
                                    steps.at[step_for_redistribution,'Projected_Next_Production_Time'] = steps.at[step_for_redistribution,'Projected_Next_Production_Time'] + steps.at[step_for_redistribution,'Validation_Time']                          
            
            
                                #end of spares adjustment
                                
            #prepare data to send to blockchain*******************************************                        
                                
                                status = "Collaborative Effort Failed"
                                text_temp = "Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Row",row,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[step_for_redistribution, "Existing_Quantity"]
                                transaction_temp = "Step",steps.at[step_for_redistribution,'Step']+1,"Production_Time",steps.at[step_for_redistribution, 'Production_Time'],"Validation_Time",steps.at[step_for_redistribution, 'Validation_Time'],"Validation_Type",steps.at[step_for_redistribution, 'Validation_Type'],"Probability_of_Success",steps.at[step_for_redistribution, 'Probability_of_Success'],"Validation_Correctness",steps.at[step_for_redistribution, 'Validation_Correctness'],"Existing_Quantity",steps.at[row, "Existing_Quantity"],"Number_of_Previous_Attempts",steps.at[step_for_redistribution, 'Number_of_Previous_Attempts'],"Number_of_Successful_Attempts",steps.at[step_for_redistribution, 'Number_of_Successful_Attempts'],"Cumulative_Production_Time",steps.at[step_for_redistribution, 'Cumulative_Production_Time'],"Cumulative_Validation_Time",steps.at[step_for_redistribution, 'Cumulative_Validation_Time'],"Current_Time_Spares",steps.at[step_for_redistribution, 'Current_Time_Spares'],"Time_Spare_Changed", steps.at[step_for_redistribution, 'Time_Spare_Changed'],"Projected_Next_Production_Time",steps.at[step_for_redistribution, 'Projected_Next_Production_Time'],"Secondary_Validation_1",steps.at[step_for_redistribution, 'Secondary_Validation_1'],"Secondary_Validation_1_Count",steps.at[step_for_redistribution, 'Secondary_Validation_1_Count'],"Secondary_Validation_2",steps.at[step_for_redistribution, 'Secondary_Validation_2'],"Secondary_Validation_2_Count",steps.at[step_for_redistribution, 'Secondary_Validation_2_Count'],"Secondary_Validation_3",steps.at[step_for_redistribution, 'Secondary_Validation_3'],"Secondary_Validation_3_Count",steps.at[step_for_redistribution, 'Secondary_Validation_3_Count'],"Secondary_Validation_4",steps.at[step_for_redistribution, 'Secondary_Validation_4'],"Secondary_Validation_4_Count",steps.at[step_for_redistribution, 'Secondary_Validation_4_Count'],"Pending_Validation_Count",steps.at[step_for_redistribution, 'Pending_Validation_Count'],"Total_Validation_Time",steps.at[step_for_redistribution, 'Total_Validation_Time'],"Dagum",steps.at[step_for_redistribution, 'Dagum'],"Step Assisting",step_that_is_helping+1                                                            
                                text = str(text_temp)
                                transaction = str(transaction_temp)
                                status_text = str(status)
                                part_text = str(part_being_made + 1)
                                step_text = str(row)
                                time_stamp_text = str(time_stamp)
                                part_quality_text = str(part_quality)
                                step_spares_text = str(steps.at[step_for_redistribution, "Existing_Quantity"])                                                                   
                                
                                #print("row1028")
                                
                                print("Status",status,"Iteration", repeats_performed+1,"Part",part_being_made + 1,"Step",step_for_redistribution+1,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row, "Existing_Quantity"])
                              
            #send data to blockchain ****************************************************
                              
                                payload = "{\n    \"history\":\""+text+"\",\"transaction\":\""+transaction+"\", \"status\":\""+status_text+"\", \"part\":\""+part_text+"\", \"step\":\""+step_text+"\", \"time\":\""+time_stamp_text+"\", \"quality\":\""+part_quality_text+"\", \"spares\":\""+step_spares_text+"\"}"
                                
                                headers = {
                                    'Content-Type': "application/json",
                                    }
                                
                                response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
                                
                                print(response.text)
                                
                                h = requests.get(url = Mine_Transaction) 
                                                         
            #****************************************************************************                                                
            
                                    
            #**************************************************************************** 
                                     
                            #collaborative part production successful scenario
                            
                            else:  
                                
                                cumulative_time = cumulative_time + steps.loc[step_for_redistribution,"Production_Time"] + steps.loc[step_for_redistribution,"Validation_Time"]
                                steps.at[step_for_redistribution,'Projected_Next_Production_Time'] = max(time_stamp, steps.at[step_for_redistribution,'Projected_Next_Production_Time']) + steps.loc[step_for_redistribution,"Validation_Time"]
                                steps.at[step_that_is_helping,'Projected_Next_Production_Time'] = max(time_stamp, steps.at[step_that_is_helping,'Projected_Next_Production_Time']) + steps.loc[step_that_is_helping,"Production_Time"]
                                
                                if step_for_redistribution + 1 < count_row:
                                    #to make sure no simultaneous production
                                    if steps.at[step_that_is_helping,'Projected_Next_Production_Time'] <= time_stamp:  
                                        steps.at[step_that_is_helping,'Projected_Next_Production_Time'] = time_stamp + 1                           
                                
                                #even though helping, still count under original station's production time
                                steps.loc[step_for_redistribution,"Cumulative_Production_Time"] = steps.loc[step_for_redistribution,"Cumulative_Production_Time"] + steps.loc[step_for_redistribution,"Production_Time"]
                                steps.loc[step_for_redistribution,"Cumulative_Validation_Time"] = steps.loc[step_for_redistribution,"Cumulative_Validation_Time"] + steps.loc[step_for_redistribution,"Validation_Time"]
                                
                                #acknowledge that step is successful - for part success counter - see lines below first while loop
                                steps.at[step_for_redistribution,'Number_of_Successful_Attempts'] = steps.at[step_for_redistribution,'Number_of_Successful_Attempts'] + 1                    
                                
                                #spare for next step increases, spare for existing step decreases
                                steps.at[step_for_redistribution, "Existing_Quantity"] = steps.at[step_for_redistribution, "Existing_Quantity"]+1
                                                                                               
                               #to prevent when step_for_redistribution = 0, index error occurs
                                if step_for_redistribution > 0:
                                    steps.at[step_for_redistribution-1, "Existing_Quantity"] = steps.at[step_for_redistribution-1, "Existing_Quantity"]-1
                                                               
                                if step_for_redistribution+1 < count_row:
                                    if steps.at[step_for_redistribution+1, "Existing_Quantity"] == 0:
                                        steps.at[step_for_redistribution+1,'Projected_Next_Production_Time'] = steps.at[step_for_redistribution+1,'Projected_Next_Production_Time'] + 1
                                                                                        
                                #condition required for last row
                                
            #to prevent the 0 spares, once spares change at next t = 1 scenario, spare generated, introduce concept of Projected_Next_Production_Time - if t before Projected_Next_Production_Time, no spare production                    
                                steps.at[step_for_redistribution, 'Time_Spare_Changed'] = time_stamp + steps.loc[step_for_redistribution,"Production_Time"]
            
                                #else: #for last step, no need to add parts to next step
                                    #continue    
                                #end of spares adjustment

                                                                                   
                                status = "Collaborative Effort Passed"
                                
                                text_temp = "Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Row",step_for_redistribution,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[step_for_redistribution, "Existing_Quantity"]                      
                                
                                transaction_temp = "Step",steps.at[step_for_redistribution,"Step"],"Production_Time",steps.at[step_for_redistribution, 'Production_Time'],"Validation_Time",steps.at[step_for_redistribution, 'Validation_Time'],"Validation_Type",steps.at[step_for_redistribution, 'Validation_Type'],"Probability_of_Success",steps.at[step_for_redistribution, 'Probability_of_Success'],"Validation_Correctness",steps.at[step_for_redistribution, 'Validation_Correctness'],"Existing_Quantity",steps.at[step_for_redistribution, "Existing_Quantity"],"Number_of_Previous_Attempts",steps.at[step_for_redistribution, 'Number_of_Previous_Attempts'],"Number_of_Successful_Attempts",steps.at[step_for_redistribution, 'Number_of_Successful_Attempts'],"Cumulative_Production_Time",steps.at[step_for_redistribution, 'Cumulative_Production_Time'],"Cumulative_Validation_Time",steps.at[step_for_redistribution, 'Cumulative_Validation_Time'],"Current_Time_Spares",steps.at[step_for_redistribution, 'Current_Time_Spares'],"Time_Spare_Changed", steps.at[step_for_redistribution, 'Time_Spare_Changed'],"Projected_Next_Production_Time",steps.at[step_for_redistribution, 'Projected_Next_Production_Time'],"Secondary_Validation_1",steps.at[step_for_redistribution, 'Secondary_Validation_1'],"Secondary_Validation_1_Count",steps.at[step_for_redistribution, 'Secondary_Validation_1_Count'],"Secondary_Validation_2",steps.at[step_for_redistribution, 'Secondary_Validation_2'],"Secondary_Validation_2_Count",steps.at[step_for_redistribution, 'Secondary_Validation_2_Count'],"Secondary_Validation_3",steps.at[step_for_redistribution, 'Secondary_Validation_3'],"Secondary_Validation_3_Count",steps.at[step_for_redistribution, 'Secondary_Validation_3_Count'],"Secondary_Validation_4",steps.at[step_for_redistribution, 'Secondary_Validation_4'],"Secondary_Validation_4_Count",steps.at[step_for_redistribution, 'Secondary_Validation_4_Count'],"Pending_Validation_Count",steps.at[step_for_redistribution, 'Pending_Validation_Count'],"Total_Validation_Time",steps.at[step_for_redistribution, 'Total_Validation_Time'], "Dagum",steps.at[step_for_redistribution, 'Dagum'],"Step Assisting",step_that_is_helping+1
                                    
                                # Need to make sure no simultaneous action when 0 then add 1 = all action/create at same time
                    
                                #status = "Passed"
                                           
                                text = str(text_temp)
                                transaction = str(transaction_temp)
                                status_text = str(status)
                                part_text = str(part_being_made + 1)
                                step_text = str(row)
                                time_stamp_text = str(time_stamp)
                                part_quality_text = str(part_quality)
                                step_spares_text = str(steps.at[step_for_redistribution, "Existing_Quantity"])
                                                                               
                                #print("row1116", row)
                                
                                print("Status",status,"Iteration", repeats_performed+1,"Part",part_being_made + 1,"Step",step_for_redistribution+1,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[step_for_redistribution, "Existing_Quantity"])
                                
             #send data to blockchain ****************************************************
            
                                payload = "{\n    \"history\":\""+text+"\",\"transaction\":\""+transaction+"\", \"status\":\""+status_text+"\", \"part\":\""+part_text+"\", \"step\":\""+step_text+"\", \"time\":\""+time_stamp_text+"\", \"quality\":\""+part_quality_text+"\", \"spares\":\""+step_spares_text+"\"}"
                                
                                headers = {
                                    'Content-Type': "application/json",
                                    }
                                
                                response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
                                
                                print(response.text)
                                
                                h = requests.get(url = Mine_Transaction)
                                
                         else:
                             row = row + 1
                         #print("row1174",row)
                                    
                        
                #if step_for_redistribution == 0:
                    else: 
                       
                        #print("row1171",row, steps.loc[step_for_redistribution-1, "Existing_Quantity"], steps.loc[step_that_is_helping ,"Projected_Next_Production_Time"], time_stamp, step_that_is_helping)
                
                            #check if previous step spares > 0, if it is larger than 0, carry on
                        if steps.loc[step_for_redistribution-1, "Existing_Quantity"] > 0:
                                                    
                            if time_stamp >= steps.loc[step_that_is_helping ,"Projected_Next_Production_Time"]:
                                #*****************************************************************************
                                
                                #print("HELP1166",row)                        
                                
                                from random import *
                               
                                random0 = randint(1, 100)    # Pick a random number between 1 and 100
                                
                                #success of part creation still dependent on the original step's probability of success
                                #not the helping step/station's probability of success
                                          
                                success = steps.loc[step_for_redistribution,"Probability_of_Success"]*100 - random0
                                
                                random1 = randint(1, 100)    # Pick a random number between 1 and 100
                                
                                correctness = steps.loc[step_for_redistribution,"Validation_Correctness"]*100 - random1
                                
                                #secondary validation 1. Add time for correctness check
                                
                                random2 = randint(1, 100)    # Pick a random number between 1 and 100
                            
                            #secondary validation - in redistributed work, validation will still be done by the individual
                            #stations and the stations designated to be secondary reviewers
                            
                            #*****************************************************************************
                                            
                                secondary_validation_row_1 = steps.loc[step_for_redistribution,"Secondary_Validation_1"] - 1
                                
                                if secondary_validation_row_1 == steps.loc[step_for_redistribution,"Step"]:
                                    correctness_1 = 1
                                else:
                                    correctness_1 = steps.loc[secondary_validation_row_1,"Validation_Correctness"]*100 - random2
                                                        
                                #for now...human validation means human drops manufacturing step and works on task on hand immediately
                                #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                    if steps.loc[secondary_validation_row_1,"Validation_Type"] == "Human":
                                        steps.loc[secondary_validation_row_1,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_1,"Pending_Validation_Count"] + 1
                                        #in case projected next prodution time is way behind current time, normalise current projected time
                                        if  steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] < time_stamp:
                                            steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] = time_stamp
                                               
                                        #else next projection time follows completion of step
                                        else:
                                            steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_1,"Validation_Time"]
                     
                                #secondary validation 2
                                
                                random3 = randint(1, 100)    # Pick a random number between 1 and 100
                                
                                secondary_validation_row_2 = steps.loc[step_for_redistribution,"Secondary_Validation_2"] - 1
                            
                                #if NA = no secondary validation
                                if secondary_validation_row_2 == steps.loc[step_for_redistribution,"Step"]:
                                    correctness_2 = 1
                                else:
                                    correctness_2 = steps.loc[secondary_validation_row_2,"Validation_Correctness"]*100 - random3            
                            
                                #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                    if steps.loc[secondary_validation_row_2,"Validation_Type"] == "Human":
                                        steps.loc[secondary_validation_row_2,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_2,"Pending_Validation_Count"] + 1
                                        #in case projected next prodution time is way behind current time, normalise current projected time
                                        if  steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] < time_stamp: 
                                            steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] = time_stamp
                    
                                        #else next projection time follows completion of step
                                        else:
                                            steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_2,"Validation_Time"]
                     
                      
                                #secondary validation 3
                                
                                random4 = randint(1, 100)    # Pick a random number between 1 and 100
                                
                                secondary_validation_row_3 = steps.loc[step_for_redistribution,"Secondary_Validation_3"] - 1
                               
                                if secondary_validation_row_3 == steps.loc[step_for_redistribution,"Step"]:
                                    correctness_3 = 1
                                else:
                                    correctness_3 = steps.loc[secondary_validation_row_3,"Validation_Correctness"]*100 - random4              
                                
                                #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously
                                    if steps.loc[secondary_validation_row_3,"Validation_Type"] == "Human":
                                        steps.loc[secondary_validation_row_3,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_3,"Pending_Validation_Count"] + 1
                                        #in case projected next prodution time is way behind current time, normalise current projected time
                                        if  steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] < time_stamp:
                                            steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] = time_stamp
                                        #else next projection time follows completion of step
                                        else:
                                            steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_3,"Validation_Time"]
                             
                                #secondary validation 4
                                
                                random5 = randint(1, 100)    # Pick a random number between 1 and 100
                                
                                secondary_validation_row_4 = steps.loc[step_for_redistribution,"Secondary_Validation_4"] - 1
                                
                                if secondary_validation_row_4 == steps.loc[step_for_redistribution,"Step"]:
                                    correctness_4 = 1
                                else:
                                    correctness_4 = steps.loc[secondary_validation_row_4,"Validation_Correctness"]*100 - random5                    
                            
                                #only human will need to do consequtively...manufacture then validate. AI does validation simultaneously/instantaneously
                                    if steps.loc[secondary_validation_row_4,"Validation_Type"] == "Human":
                                        steps.loc[secondary_validation_row_4,"Pending_Validation_Count"] = steps.loc[secondary_validation_row_4,"Pending_Validation_Count"] + 1
                                        #in case projected next prodution time is way behind current time, normalise current projected time
                                        if  steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] < time_stamp:
                                            steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] = time_stamp
                                        #else next projection time follows completion of step
                                        else:
                                            steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] = steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"] + steps.loc[secondary_validation_row_4,"Validation_Time"]
                                                                                                           
                                #part QC classification
                                if  correctness >=0 and correctness_1 >= 0 and correctness_2 >= 0 and correctness_3 >= 0 and correctness_4 >= 0:
                                    part_quality = "Good"
                                
                                else:                                     
                                
                                    if  correctness < 0 and correctness_1 < 0 and correctness_2 < 0 and correctness_3 < 0 and correctness_4 < 0:
                                        part_quality = "Poor"
                                
                                    #if secondary validation catches poor product quality, part is rejected
                                    if (correctness_1 >= 0 or correctness_2 >= 0 or correctness_3 >= 0 or correctness_4 >= 0) and correctness >= 0:
                                        success = -1
                                        part_quality = "Rejected by Secondary QC"            
                                    
                                #to track number of previous attempts
                                steps.loc[step_for_redistribution,"Number_of_Previous_Attempts"] = steps.loc[step_for_redistribution,"Number_of_Previous_Attempts"] + 1
                                                
                                #determination of validation time for purpose of showing final time
                                steps.loc[step_for_redistribution,"Total_Validation_Time"] == steps.loc[step_for_redistribution,"Validation_Time"]
                            
                                if steps.loc[secondary_validation_row_1,"Validation_Type"] == "Human":
                                    
                                    steps.loc[step_for_redistribution,"Total_Validation_Time"] = max(steps.loc[step_for_redistribution,"Validation_Time"], steps.loc[secondary_validation_row_1,"Projected_Next_Production_Time"])
                                    
                                if steps.loc[secondary_validation_row_2,"Validation_Type"] == "Human":
                                    
                                   steps.loc[step_for_redistribution,"Total_Validation_Time"] = max(steps.loc[step_for_redistribution,"Validation_Time"], steps.loc[secondary_validation_row_2,"Projected_Next_Production_Time"]) 
                                
                                if steps.loc[secondary_validation_row_3,"Validation_Type"] == "Human":
                                    
                                   steps.loc[step_for_redistribution,"Total_Validation_Time"] = max(steps.loc[step_for_redistribution,"Validation_Time"], steps.loc[secondary_validation_row_3,"Projected_Next_Production_Time"]) 
                                
                                if steps.loc[secondary_validation_row_4,"Validation_Type"] == "Human":
                                    
                                   steps.loc[step_for_redistribution,"Total_Validation_Time"] = max(steps.loc[step_for_redistribution,"Validation_Time"], steps.loc[secondary_validation_row_4,"Projected_Next_Production_Time"]) 
                                
                            #*****************************************************************************
                                
                                #*****************************************************************************
                                               
                        #if negative number from previous part, step has failed, repeat step, else, step is a success, proceed to next step at the same time
                                if  success < 0:                      
                                    cumulative_time = cumulative_time + steps.loc[step_for_redistribution,"Production_Time"] + steps.loc[step_for_redistribution,"Validation_Time"]
                                    steps.loc[step_for_redistribution,"Cumulative_Production_Time"] = steps.loc[step_for_redistribution,"Cumulative_Production_Time"] + steps.loc[step_for_redistribution,"Production_Time"]
                                    steps.loc[step_for_redistribution,"Cumulative_Validation_Time"] = steps.loc[step_for_redistribution,"Cumulative_Validation_Time"] + steps.loc[step_for_redistribution,"Validation_Time"]
                                                         
                                    #if you fail, remain stagnant at this step? No, you repeat this step, but at a different time use your old spares to make new part
                                    if step_for_redistribution != 0:
                                        #any projected next time incurred by manufacturing must go to the helping step
                                        #but any projected time for validation goes to original step
                                        steps.at[step_for_redistribution,'Projected_Next_Production_Time'] = steps.at[step_for_redistribution,'Projected_Next_Production_Time'] + steps.at[step_for_redistribution,'Validation_Time']                          
                                        steps.at[step_that_is_helping,'Projected_Next_Production_Time'] = steps.at[step_that_is_helping,'Projected_Next_Production_Time'] + steps.at[step_that_is_helping,'Production_Time']                          
                                        steps.at[step_for_redistribution-1, "Existing_Quantity"] = steps.at[step_for_redistribution-1, "Existing_Quantity"]-1
                
                                    
                                    if step_that_is_helping+1 < count_row:
                                    
                                        #to make sure no simultaneous production
                                        if steps.at[step_that_is_helping+1,'Projected_Next_Production_Time'] <= time_stamp:  
                                            steps.at[step_that_is_helping+1,'Projected_Next_Production_Time'] = time_stamp + 1   
                                                                                            
                                    if step_for_redistribution == 0:
                                        steps.at[step_that_is_helping,'Projected_Next_Production_Time'] = steps.at[step_that_is_helping,'Projected_Next_Production_Time'] + steps.at[step_that_is_helping,'Production_Time']                          
                                        steps.at[step_for_redistribution,'Projected_Next_Production_Time'] = steps.at[step_for_redistribution,'Projected_Next_Production_Time']  + steps.at[step_for_redistribution,'Validation_Time']                          
                
                
                                    #end of spares adjustment
                                    
                #prepare data to send to blockchain*******************************************                        
                                    
                                    status = "Collaborative Effort Failed"
                                    text_temp = "Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Row",row,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row, "Existing_Quantity"]
                                    transaction_temp = "Step",steps.at[step_for_redistribution,'Step']+1,"Production_Time",steps.at[step_for_redistribution, 'Production_Time'],"Validation_Time",steps.at[step_for_redistribution, 'Validation_Time'],"Validation_Type",steps.at[step_for_redistribution, 'Validation_Type'],"Probability_of_Success",steps.at[step_for_redistribution, 'Probability_of_Success'],"Validation_Correctness",steps.at[step_for_redistribution, 'Validation_Correctness'],"Existing_Quantity",steps.at[step_for_redistribution, "Existing_Quantity"],"Number_of_Previous_Attempts",steps.at[step_for_redistribution, 'Number_of_Previous_Attempts'],"Number_of_Successful_Attempts",steps.at[step_for_redistribution, 'Number_of_Successful_Attempts'],"Cumulative_Production_Time",steps.at[step_for_redistribution, 'Cumulative_Production_Time'],"Cumulative_Validation_Time",steps.at[step_for_redistribution, 'Cumulative_Validation_Time'],"Current_Time_Spares",steps.at[step_for_redistribution, 'Current_Time_Spares'],"Time_Spare_Changed", steps.at[step_for_redistribution, 'Time_Spare_Changed'],"Projected_Next_Production_Time",steps.at[step_for_redistribution, 'Projected_Next_Production_Time'],"Secondary_Validation_1",steps.at[step_for_redistribution, 'Secondary_Validation_1'],"Secondary_Validation_1_Count",steps.at[step_for_redistribution, 'Secondary_Validation_1_Count'],"Secondary_Validation_2",steps.at[step_for_redistribution, 'Secondary_Validation_2'],"Secondary_Validation_2_Count",steps.at[step_for_redistribution, 'Secondary_Validation_2_Count'],"Secondary_Validation_3",steps.at[step_for_redistribution, 'Secondary_Validation_3'],"Secondary_Validation_3_Count",steps.at[step_for_redistribution, 'Secondary_Validation_3_Count'],"Secondary_Validation_4",steps.at[step_for_redistribution, 'Secondary_Validation_4'],"Secondary_Validation_4_Count",steps.at[step_for_redistribution, 'Secondary_Validation_4_Count'],"Pending_Validation_Count",steps.at[step_for_redistribution, 'Pending_Validation_Count'],"Total_Validation_Time",steps.at[step_for_redistribution, 'Total_Validation_Time'],"Dagum",steps.at[step_for_redistribution, 'Dagum'],"Step Assisting",step_that_is_helping+1
                                                            
                                    text = str(text_temp)
                                    transaction = str(transaction_temp)
                                    status_text = str(status)
                                    part_text = str(part_being_made + 1)
                                    step_text = str(step_for_redistribution)
                                    time_stamp_text = str(time_stamp)
                                    part_quality_text = str(part_quality)
                                    step_spares_text = str(steps.at[step_for_redistribution, "Existing_Quantity"])                                                                   
                                    
                                    #print("row1028")
                                    
                                    print("Status",status,"Iteration", repeats_performed+1,"Part",part_being_made + 1,"Step",step_for_redistribution+1,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[step_for_redistribution, "Existing_Quantity"])
                                  
                #send data to blockchain ****************************************************
                                  
                                    payload = "{\n    \"history\":\""+text+"\",\"transaction\":\""+transaction+"\", \"status\":\""+status_text+"\", \"part\":\""+part_text+"\", \"step\":\""+step_text+"\", \"time\":\""+time_stamp_text+"\", \"quality\":\""+part_quality_text+"\", \"spares\":\""+step_spares_text+"\"}"
                                    
                                    headers = {
                                        'Content-Type': "application/json",
                                        }
                                    
                                    response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
                                    
                                    print(response.text)
                                    
                                    h = requests.get(url = Mine_Transaction) 
                                                             
                #****************************************************************************                                                
                
                                        
                #**************************************************************************** 
                                         
                                #collaborative part production successful scenario
                                
                                else:  
                                    
                                    cumulative_time = cumulative_time + steps.loc[step_for_redistribution,"Production_Time"] + steps.loc[step_for_redistribution,"Validation_Time"]
                                    steps.at[step_for_redistribution,'Projected_Next_Production_Time'] = max(time_stamp, steps.at[step_for_redistribution,'Projected_Next_Production_Time']) + steps.loc[step_for_redistribution,"Validation_Time"]
                                    steps.at[step_that_is_helping,'Projected_Next_Production_Time'] = max(time_stamp, steps.at[step_that_is_helping,'Projected_Next_Production_Time']) + steps.loc[step_that_is_helping,"Production_Time"]
                                    
                                    if step_for_redistribution + 1 < count_row:
                                        #to make sure no simultaneous production
                                        if steps.at[step_that_is_helping,'Projected_Next_Production_Time'] <= time_stamp:  
                                            steps.at[step_that_is_helping,'Projected_Next_Production_Time'] = time_stamp + 1                           
                                    
                                    #even though helping, still count under original station's production time
                                    steps.loc[step_for_redistribution,"Cumulative_Production_Time"] = steps.loc[step_for_redistribution,"Cumulative_Production_Time"] + steps.loc[step_for_redistribution,"Production_Time"]
                                    steps.loc[step_for_redistribution,"Cumulative_Validation_Time"] = steps.loc[step_for_redistribution,"Cumulative_Validation_Time"] + steps.loc[step_for_redistribution,"Validation_Time"]
                                    
                                    #acknowledge that step is successful - for part success counter - see lines below first while loop
                                    steps.at[step_for_redistribution,'Number_of_Successful_Attempts'] = steps.at[step_for_redistribution,'Number_of_Successful_Attempts'] + 1                    
                                    
                                    #spare for next step increases, spare for existing step decreases
                                    steps.at[step_for_redistribution, "Existing_Quantity"] = steps.at[step_for_redistribution, "Existing_Quantity"]+1
                                   
                                    
                                    
                                    if step_for_redistribution != 0:
                                        steps.at[step_for_redistribution-1, "Existing_Quantity"] = steps.at[step_for_redistribution-1, "Existing_Quantity"]-1
                                                                   
                                    if step_for_redistribution+1 < count_row:
                                        if steps.at[step_for_redistribution+1, "Existing_Quantity"] == 0:
                                            steps.at[step_for_redistribution+1,'Projected_Next_Production_Time'] = steps.at[step_for_redistribution+1,'Projected_Next_Production_Time'] + 1
                                                                                            
                                    #condition required for last row
                                    
                #to prevent the 0 spares, once spares change at next t = 1 scenario, spare generated, introduce concept of Projected_Next_Production_Time - if t before Projected_Next_Production_Time, no spare production                    
                                    steps.at[step_for_redistribution, 'Time_Spare_Changed'] = time_stamp + steps.loc[step_for_redistribution,"Production_Time"]
                
                                    #else: #for last step, no need to add parts to next step
                                        #continue    
                                    #end of spares adjustment
                                    #if step_for_redistribution < count_row:
                                        
                                        #print("row1083")
                                        
                                        #row = row + 1
                                                                                       
                                    status = "Collaborative Effort Passed"
                                    
                                    text_temp = "Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Row",step_for_redistribution,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[step_for_redistribution, "Existing_Quantity"]                      
                                    
                                    transaction_temp = "Step",steps.at[step_for_redistribution,"Step"],"Production_Time",steps.at[step_for_redistribution, 'Production_Time'],"Validation_Time",steps.at[step_for_redistribution, 'Validation_Time'],"Validation_Type",steps.at[step_for_redistribution, 'Validation_Type'],"Probability_of_Success",steps.at[step_for_redistribution, 'Probability_of_Success'],"Validation_Correctness",steps.at[step_for_redistribution, 'Validation_Correctness'],"Existing_Quantity",steps.at[step_for_redistribution, "Existing_Quantity"],"Number_of_Previous_Attempts",steps.at[step_for_redistribution, 'Number_of_Previous_Attempts'],"Number_of_Successful_Attempts",steps.at[step_for_redistribution, 'Number_of_Successful_Attempts'],"Cumulative_Production_Time",steps.at[step_for_redistribution, 'Cumulative_Production_Time'],"Cumulative_Validation_Time",steps.at[step_for_redistribution, 'Cumulative_Validation_Time'],"Current_Time_Spares",steps.at[step_for_redistribution, 'Current_Time_Spares'],"Time_Spare_Changed", steps.at[step_for_redistribution, 'Time_Spare_Changed'],"Projected_Next_Production_Time",steps.at[step_for_redistribution, 'Projected_Next_Production_Time'],"Secondary_Validation_1",steps.at[step_for_redistribution, 'Secondary_Validation_1'],"Secondary_Validation_1_Count",steps.at[step_for_redistribution, 'Secondary_Validation_1_Count'],"Secondary_Validation_2",steps.at[step_for_redistribution, 'Secondary_Validation_2'],"Secondary_Validation_2_Count",steps.at[step_for_redistribution, 'Secondary_Validation_2_Count'],"Secondary_Validation_3",steps.at[step_for_redistribution, 'Secondary_Validation_3'],"Secondary_Validation_3_Count",steps.at[step_for_redistribution, 'Secondary_Validation_3_Count'],"Secondary_Validation_4",steps.at[step_for_redistribution, 'Secondary_Validation_4'],"Secondary_Validation_4_Count",steps.at[step_for_redistribution, 'Secondary_Validation_4_Count'],"Pending_Validation_Count",steps.at[step_for_redistribution, 'Pending_Validation_Count'],"Total_Validation_Time",steps.at[step_for_redistribution, 'Total_Validation_Time'], "Dagum",steps.at[step_for_redistribution, 'Dagum'],"Step Assisting",step_that_is_helping+1
                                        
                                    # Need to make sure no simultaneous action when 0 then add 1 = all action/create at same time
                        
                                    #status = "Collaborative Effort Passed"
                                               
                                    text = str(text_temp)
                                    transaction = str(transaction_temp)
                                    status_text = str(status)
                                    part_text = str(part_being_made + 1)
                                    step_text = str(step_for_redistribution)
                                    time_stamp_text = str(time_stamp)
                                    part_quality_text = str(part_quality)
                                    step_spares_text = str(steps.at[step_for_redistribution, "Existing_Quantity"])
                                                                                   
                                    #print("row1116")
                                    
                                    print("Status",status,"Iteration", repeats_performed+1,"Part",part_being_made + 1,"Step",step_for_redistribution+1,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[step_for_redistribution-1, "Existing_Quantity"])
                                    
                 #send data to blockchain ****************************************************
                
                                    payload = "{\n    \"history\":\""+text+"\",\"transaction\":\""+transaction+"\", \"status\":\""+status_text+"\", \"part\":\""+part_text+"\", \"step\":\""+step_text+"\", \"time\":\""+time_stamp_text+"\", \"quality\":\""+part_quality_text+"\", \"spares\":\""+step_spares_text+"\"}"
                                    
                                    headers = {
                                        'Content-Type': "application/json",
                                        }
                                    
                                    response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
                                    
                                    print(response.text)
                                    
                                    h = requests.get(url = Mine_Transaction) 
                                                         
     #*****************************************************************************
                            else:
                        
                                #print("row1476")
                                
                                row = row + 1
                                continue
    
    
                        #if time_stamp <= steps.loc[row,"Projected_Next_Production_Time"] in other words, time not up yet
                        else:
                            
                                    #continue with original processing                    
                            #print("row1502", row, time_stamp)
                                    
                            row = row + 1
                else:
            
                    #print("row1476")
                    
                    row = row + 1
                    break
                
                
    
            #print("row1517")
            row = temp_row

    repeats_performed = repeats_performed + 1