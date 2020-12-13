'''
WE WON'T BE USING THIS THIS IS A CONTROL
'''
#import csv file
import pandas
import random
steps = pandas.read_csv('steps.csv')
#print(steps)

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
row = 0

part_being_made = 0

repeats_performed = 0

part_quality = "Neutral"

successful_step_count = 0

#Assumption: Once there's a defective part, start from step 0 again, with all previous spares used for manufacture of part wasted
#current point of time, t
time_stamp = 1
#time = 0

while repeats_performed < repeats:
    #print("restart")
    #Assumption: Once there's a defective part, start from step 0 again, with all previous spares used for manufacture of part wasted
    #current point of time, t
    time_stamp = 0
    row = 0
    part_being_made = 0
    steps = pandas.read_csv('steps.csv')





    
    #while iterations (number of parts to make) still greater than the parts already made

            
     #iterations = number of parts to make
    #part_being_made = part number that is being made
    while part_being_made < iterations:
                
            while row <= count_row:
                
                #print("row122",row,count_row,)
    #at last step                     
                if (row == count_row) and steps.at[row-1, "Existing_Quantity"] > 0:
                    
                    #print("row125")
                    #if status = successful
                    
                    if success > 0 and (part_quality == "Good" or part_quality == "Poor"):
        
                        #print("row130")
     
                        steps.at[row-1, "Existing_Quantity"] = steps.at[row-1, "Existing_Quantity"] - 1
                        part_being_made = part_being_made + 1
                        print("Part", (part_being_made), "started final step production at", time_stamp-1, "Quality",part_quality)
                        row = 0
                        part_quality = "Neutral"
                                          
                    else:
                        part_being_made = part_being_made
                        row = 0
                        part_quality = "Neutral"
                                                                           
                #if number of sueccessful attempts = 0
                else:
                    time_stamp = time_stamp + 1
                    row = count_row + 1 #to exit from while loop 
                    continue #exit current while loop
                
            #to reset/prep for next while loop
            successful_step_count = 0
            row = 0           
            
            
        
            while row < count_row:
                
                #need to see different rows being processed at the same time
                #print(time, row)
                
            #to determine time multiple for determining if number of attempts is up
            #determine if time is ripe for execution of any step at a particular point, t in time 
            #temp_Attempts needed for the zeroth try, else everything is a multiple
                if steps.loc[row,"Number_of_Previous_Attempts"] == 0:
                    temp_Attempts = 1
                else:
                    temp_Attempts = steps.loc[row,"Number_of_Previous_Attempts"]+1
                            
                if (((temp_Attempts == time_stamp/(steps.loc[row,"Production_Time"]+steps.loc[row,"Validation_Time"])) and temp_Attempts != 1)) or (time_stamp == 1 and temp_Attempts == 1 and (steps.at[row,'Projected_Next_Production_Time'] < time_stamp)) or (time_stamp >= temp_Attempts*(steps.loc[row,"Production_Time"]+steps.loc[row,"Validation_Time"])) and (steps.at[row,'Projected_Next_Production_Time'] < time_stamp):
                    
                    #print("validated")
                    
                    #if you have the spares for your step, proceed, else you wait for next multiple of t
                    if row == 0 or (steps.loc[row,"Existing_Quantity"] > 0):
                        
                        from random import *
                   
                        random = randint(1, 100)    # Pick a random number between 1 and 100
                                  
                        success = steps.loc[row,"Probability_of_Success"]*100 - random
                        
                        correctness = steps.loc[row,"Validation_Correctness"]*100 - random
                        
                        #if part_quality already poor, then it stays poor, else you it resets
                        
                        if part_quality == "Poor":
                            part_quality = "Poor"
                            
                        else:                
                            if  correctness >= 0:
                                part_quality = "Good"
                                                                 
                            if  correctness < 0:
                                part_quality = "Poor"
                        
                #end of determination of success of step
                        steps.loc[row,"Number_of_Previous_Attempts"] = steps.loc[row,"Number_of_Previous_Attempts"] + 1
                       
                
                #if negative number from previous part, step has failed, repeat step, else, step is a success, proceed to next step at the same time
                        if  success < 0:
                            #print("failed")
                            cumulative_time = cumulative_time + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                            steps.loc[row,"Cumulative_Production_Time"] = steps.loc[row,"Cumulative_Production_Time"] + steps.loc[row,"Production_Time"]
                            steps.loc[row,"Cumulative_Validation_Time"] = steps.loc[row,"Cumulative_Validation_Time"] + steps.loc[row,"Validation_Time"]
                            #if you fail, remain stagnant at this step? No, you repeat this step, but at a different time use your old spares to make new part
                            #spare for next step remains constant, spare for existing step decreases
                            if row != 0:
                                steps.at[row, 'Existing_Quantity'] = steps.at[row, 'Existing_Quantity']-1
                                #basically provide a baseline to show when part quantity changed, so that in future, you known when its next due to be changed
                                steps.at[row+1, 'Time_Spare_Changed'] = time_stamp
                            #end of spares adjustment
                            row = row + 1
                                                    
                            status = "Failed"
                            print("Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Step",row,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row - 1, 'Existing_Quantity'])
                            #print("repeat inner loop")
                            #if got spares, continue, else start from front again 
                            if row < count_row:
                                if steps.loc[row, 'Existing_Quantity'] > 0:
                                    row = row
                                    steps.at[(row - 1),'Number_of_Successful_Attempts'] = steps.at[row,'Number_of_Successful_Attempts'] + 1
                                    print("Spare used at step", row)
                                else:
                                    row = 0
                                    print("No spares")
                            else:
                                print("Restart")
                            
                        #part production successful scenario
                        
                        else:  
                            cumulative_time = cumulative_time + steps.loc[row,"Production_Time"] + steps.loc[row,"Validation_Time"]
                            steps.loc[row,"Cumulative_Production_Time"] = steps.loc[row,"Cumulative_Production_Time"] + steps.loc[row,"Production_Time"]
                            steps.loc[row,"Cumulative_Validation_Time"] = steps.loc[row,"Cumulative_Validation_Time"] + steps.loc[row,"Validation_Time"]
                            #acknowledge that step is successful - for part success counter - see lines below first while loop
                            steps.at[row,'Number_of_Successful_Attempts'] = steps.at[row,'Number_of_Successful_Attempts'] + 1                    
                            #minimum production time
                            steps.at[row,'Projected_Next_Production_Time'] = time_stamp + steps.at[row,'Production_Time'] + steps.at[row,'Validation_Time']  
                                                    
                            #spare for next step increases, spare for existing step decreases
                            
                            
                            if row != 0:
                                steps.at[row, 'Existing_Quantity'] = steps.at[row, 'Existing_Quantity']-1
                                #print(row)
                            #condition required for last row
                            
        #to prevent the 0 spares, once spares change at next t = 1 scenario, spare generated, introduce concept of Projected_Next_Production_Time - if t before Projected_Next_Production_Time, no spare production
    
                            
                            if (row) < (count_row):
                                steps.at[row+1, 'Time_Spare_Changed'] = time_stamp
                                steps.at[row+1, 'Existing_Quantity'] = steps.at[row+1, 'Existing_Quantity']+1
                                
                                #print("check", steps.at[row+1, 'Existing_Quantity'])
                            #else: #for last step, no need to add parts to next step
                                #continue    
                            #end of spares adjustment
                                                    
                            row = row + 1
                            
                            status = "Passed"
                                                        
                            # Need to make sure no simultaneous action when 0 then add 1 = all action/create at same time
                
                            #print (row,time)
                
                            #if (row != count_row) and (steps.at[row, 'Existing_Quantity']-1 == 0):
                            
                            print("Iteration", repeats_performed+1,"Status",status,"Part",part_being_made + 1,"Step",row,"Time_At_Point_Of_Step",time_stamp,"Part_Quality",part_quality, "Step_Spares_Left", steps.at[row - 1, 'Existing_Quantity'])
                            
                            if ((row) < (count_row) and (steps.at[row, 'Existing_Quantity'] == steps.loc[row,"Current_Time_Spares"] + 1)):
                                
                                #print("test", steps.at[row,'Projected_Next_Production_Time'], row)                            
                                #row = row + 1
                                steps.at[row,'Projected_Next_Production_Time'] = steps.at[row-1,'Projected_Next_Production_Time'] + 1
                                #print(steps.at[row,'Projected_Next_Production_Time'])
                                
                            #row-1 != 0 or
                            
                            
                            #else:
                                
                                #print(time_stamp,"else")
                                #steps.at[row,'Projected_Next_Production_Time'] = 0
                                
                                #continue
                                                                                        
                            #    continue                                                             
                            
                            
                        
                    else: #if row == 0 or (steps.loc[row,"Existing_Quantity"] > 0):
                        row = row + 1
                        continue
                        #execute step if time is ripe. use probability to determine if step is a success
                           
                else: #accompanies  if (time % (temp_Attempts*(steps.loc[row,"Production_Time"]+steps.loc[row,"Validation_Time"]))) == 0:
                    row = row + 1
                    continue
            
            #break
    repeats_performed = repeats_performed + 1          
    
        