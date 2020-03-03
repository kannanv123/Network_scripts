import sys
my_path ="C://Users//vignesh//Desktop//python"
sys.path.append(my_path)
import numpy as np
import math
import Rsl as Rs
EIRP_basestation = 57
EIRP_smallcell = 30 
height_Basestation = 50
height_smallcell = 10
height_mobile = 1.7
frequency = 1000
penetration_loss = -21
#dictionary to store the active user's details of Basestation 
dict1 ={}
#dictionary to store the active user's details of small cell
dict2 ={}
count = 0
#distance between basestation and smallcell
distance_BS = int(input("enter the distance between basestation and small cell"))
parkinglot_length = 100
mall_length = 200
Roadlength = distance_BS - parkinglot_length - mall_length
length_outside_mall = Roadlength + parkinglot_length
entry_way = 10
#shadowing values are stored in a array
shadowing = np.random.normal(0.0, 2,int(length_outside_mall/10)+1)
#Total No.of channel blocked because of channel unavailability in Basestation
channel_blocked_basestation = 0
#Total No.of channel blocked because of channel unavailability in Small cell
channel_blocked_smallcell = 0
#Successfully completed calls in the Basestation  
call_successfully_completed = 0
#Successfully completed calls in the small cell
call_successfully_completed_smallcell = 0
#call drop due to unavailabilty of channels in Basestation while Handoff 
call_drop_Basestation = 0
#call drop due to unavailabilty of channels in Basestation while Handoff 
call_drop_smallcell = 0
#Total no.of call handoff from Base_station to small cell small cell to Base station
call_handoff_basestation =0
#Total no.of call handoff from small cell to Base station
call_handoff_smallcell = 0
#No.of Attempted calls from basestation 
handoff_attempts_basestation =0
#NO.of Attempted calls from smallcell
handoff_attempts_smallcell =0
#No.of Handoff failures from smallcell to basestation
handoff_failure_smallcell = 0
#No.of Handoff failures from basestation to smallcell
handoff_failure_basestation =0
#No.of Call attempts from Basestation
call_attempts_basestation = 0
#No.of Call attempts from smallcell
call_attempts_smallcell =0
#No.of successful Call connection from Basestation
successful_connection_basestation=0
#No.of successful Call connection from small cell
successful_connection_smallcell =0
#Total No.of users
Total_users = 1000
#call block due to power in basestation
call_block_basestation_power = 0
#call block due to power in smallcell
call_block_smallcell_power  = 0

def properties(distance):
   global call_attempts_basestation,call_attempts_smallcell
   #list to store duration,distance and rsl
   list1 = []
   duration_b = np.random.exponential(scale=180)
   #append the duration of the call to the List
   list1.append(duration_b)
   #append the distance from the user to the List
   list1.append(distance)
   #if the user is outside the mall
   if(distance <= length_outside_mall):
     
     #converting to metres from kilometers and divided by 10 for getting the shadowing values
     shadow_dist = distance/10
     #Assigning "1" to the direction if it is from Basestation to small cell 
     direction = 1
     #rsl of basestation
     Rsl = Rs.Rsl(height_Basestation,distance,EIRP_basestation,shadowing[int(round(shadow_dist))])  
     #append the Rsl to the List
     list1.append(Rsl)
     #append the direction to the list
     list1.append(direction)
     return(list1)
   #if the user in mall  
   else:
     #distance from small cell
     dm = distance_BS - distance
     #Assigning "-1" to the direction if it is from small cell to Basestation
     direction = -1
     #check if the user is in the entry way. if yes, then the penetration loss is calculated using the formula
     if (distance > (entry_way+length_outside_mall)):
       #rsl of smallcell 
       Rsls = Rs.Rsl(height_smallcell,dm,EIRP_smallcell)
     else:
        #rsl of smallcell at the entry way 
       Rsls = Rs.Rsl(height_smallcell,dm,EIRP_smallcell) + penetration_loss*(entry_way+length_outside_mall- distance)/10

    #append the Rsl and direction to the List
     list1.append(Rsls)
     list1.append(direction)
     return(list1)
        
while(count<14400):
 #Assigning Probability to all the users  
 user = np.random.uniform(0,1,size=Total_users)
 #probability of user making a call
 probablity_making_call = [x for x in user if x<= 1/3600]
 for user in probablity_making_call:
    #probability to check the user location
   probability = np.random.uniform(0,1)
   if(probability  > 0.5):
     call_attempts_smallcell +=1 
      #assigning the random distance in the mall
     distance= np.random.uniform(length_outside_mall,distance_BS) 
     #calling the function to get distance, duration and Rsl of small cell
     list1 = properties(distance)
     #if the user is outside the entry way then the -22 is added for the Rsl from basestation 
     if (distance > (entry_way+length_outside_mall)):
       Rsl = Rs.Rsl(height_Basestation,distance,EIRP_basestation)+ penetration_loss
     #if the user is at the entry way then the penetration loss is calculated by using the formula for the rsl  from basestation 
     else:
       Rsl = Rs.Rsl(height_Basestation,distance,EIRP_basestation)+ penetration_loss*(distance-length_outside_mall)/10
     #checking the RSl of small cell whether it is greater than threshold or not
     if(list1[2] >= -102):
      #checking the length of the smallcell channel  
      if(len(dict2) <=29):
        #increment the successfully connected call to the smallcell by 1  
        successful_connection_smallcell +=1
        #connect the user to the smallcell(by storing it in the smallcell dictionary)
        dict2[distance] = list1
        #decrement the total user by 1
        Total_users-=1
      else:
        #channel block of smallcell is incremented by 1  
        channel_blocked_smallcell +=1
     #checking the RSl of basestation whether it is greater than threshold or not  
     else:
      #call block for the small cell due to strength increment by 1 
      call_block_smallcell_power += 1  
      if(Rsl>= -102):
       call_attempts_basestation +=1
       #checking the length of the basestation channel
       if(len(dict1) <=29):
         #increment the successfully connected call to the basestation by 1  
         successful_connection_basestation +=1
         #connect the user to the basestation
         dict1[distance] = list1
          #decrement the total user by 1
         Total_users-=1
       else:
        #call drop in the smallcell
        call_drop_smallcell +=1  
     #else the call is blocked and the count increments by one    
      else:
       #call drop in the smallcell
       call_drop_smallcell +=1
   elif(probability  > 0.2 and probability  <= 0.5):
     call_attempts_basestation += 1
      #assigning the random distance in the parkinglot
     distance= np.random.uniform(Roadlength,length_outside_mall)
      #calling the function to get distance, duration and Rsl of basestation
     list1=properties(distance)
     #distnce from mobile station
     dm = distance_BS - distance
     #converting to metres from kilometers and divided by 10 for getting the shadowing values
     shadow_dist = distance/10
     #rsl of small cell and since the user is in the parking lot,the penetration loss is added
     Rsls = Rs.Rsl(height_smallcell,dm,EIRP_smallcell,shadowing[int(round(shadow_dist))])+penetration_loss
     #checking the RSl of basestation whether it is greater than threshold or not
     if(list1[2] >= -102):
        #checking the length of the basestation channel 
       if(len(dict1) <=29):
          #increment the successfully connected call to the basestation by 1 
         successful_connection_basestation +=1
         #connect the user to the basestation
         dict1[distance] = list1
         #decrement the total user by 1
         Total_users-=1
         #else the call is blocked and the count increments by one
       else:
          channel_blocked_basestation +=1
     else:
       
        #call block for the basestation due to strength increment by 1 
       call_block_basestation_power += 1
       if(Rsls >=-102):
        call_attempts_smallcell +=1
       #checking the length of the smallcell channel 
        if(len(dict2) <=29):
          #increment the successfully connected call to the smallcell by 1 
         successful_connection_smallcell +=1
         #connect the user to the smallcell
         dict2[distance] = list1
         #decrement the total user by 1
         Total_users-=1
        else:
           #else the call is blocked in the basestation and the count increments by one
         call_drop_Basestation +=1
       else:
         call_drop_Basestation +=1  
     
   else:
     call_attempts_basestation += 1
      #assigning the random distance in the road 
     distance= np.random.uniform(0,Roadlength)
      #calling the function to get distance, duration and Rsl of basestation
     list1 = properties(distance)
     #distnce from mobile station
     dm = distance_BS - distance
     #converting to metres from kilometers and divided by 10 for getting the shadowing values
     shadow_dist = distance/10
     #rsl of small cell and since the user is in the road,the penetration loss is added
     Rsls = Rs.Rsl(height_smallcell,dm,EIRP_smallcell,shadowing[int(round(shadow_dist))])+penetration_loss
     #checking the RSl of basestation whether it is greater than threshold or not
     if(list1[2] > -102):
         #checking the length of the basestation channel
       if(len(dict1) <=29):
         #increment the successfully connected call to the basestation by 1 
         successful_connection_basestation +=1
         #connect the user to the basestation
         dict1[distance] = list1
         #decrement the total user by 10
         Total_users-=1
      #else the call is blocked and the count increments by one
       else:
          channel_blocked_basestation +=1
   #checking the RSl of smallcell whether it is greater than threshold or not     
     else:
       #call block for the basestation due to strength increment by 1  
      call_block_basestation_power += 1  
      if(Rsls >= -102):
       call_attempts_smallcell +=1
       #checking the length of the smallcell channel
       if(len(dict2) <=29):
    #increment the successfully connected call to the smallcell by 1  
         successful_connection_smallcell +=1
         #connect the user to the basestation
         dict2[distance] = list1
         #decrement the total user by 1
         Total_users-=1
       else:
         #else the call is blocked in the basestation and the count increments by one 
         call_drop_Basestation +=1
     
      else:
       #else the call is blocked in the basestation and the count increments by one
       call_drop_Basestation +=1
 if(len(dict1) != 0):
  #create a copy of the dictionary   
   d = dict1.copy()
   for key,value in d.items():
     #decrementing the value of duration by one of each active users for every iteration 
      if(value[0] > 0):
        value[0] -=1  
     #if the time of duration completes then the call is consider as the successful call     
      else:
        #successfully completed call in the basestation 
         call_successfully_completed +=1
         #increment the user by 1
         Total_users+=1
         #remove the user from basestation
         del dict1[key]
         continue
       #Increments the distance by 15m if the user is on the road and the the direction is towards small cell 
      if(value[1] <= Roadlength  and value[3]==1 and value[1] >= 1):    
          value[1]+=15
     #Increments the distance by 1m if the user is in parking lot or in mall and the direction is towards small cell   
      elif(value[1] > Roadlength and value[1] <= (distance_BS-1)  and value[3]==1 ):    
         value[1]+= 1
     #Decrements the distance by 15metres if the if the user is on the road and the direction is towards Basestation     
      elif(value[1] <= Roadlength and value[3]==-1 and value[1]>=0):    
         value[1]-= 15
     #Decrements the distance by 1m if the user is in parking lot or in mall and the direction is towards Basestation        
      elif(value[1] > Roadlength and value[1] <= (distance_BS-1) and value[3]==-1 ):    
        value[1]-= 1 
      #distance from smallcell
      distance_from_smallcell = distance_BS - value[1]
      #if the user is outside the mall
      if(value[1] <= length_outside_mall and value[1]>= 1):
         #rsl of basestation
        value[2] = Rs.Rsl(height_Basestation,value[1],EIRP_basestation,shadowing[int(round(value[1]/10))])
        #rsl of smallcell , it includes penetration loss since the user is outside the mall
        Rsls = Rs.Rsl(height_smallcell,distance_from_smallcell,EIRP_smallcell,shadowing[int(round(value[1]/10))])+penetration_loss
      #if the user is outside the entry way and between small cell
      elif(value[1] > (length_outside_mall+entry_way) and value[1]<= (distance_BS-1)):
      #rsl of basestation , it includes penetration loss since the user is in mall  
        value[2] = Rs.Rsl(height_Basestation,value[1],EIRP_basestation)+ penetration_loss
       #rsl of smallcell
        Rsls = Rs.Rsl(height_smallcell,distance_from_smallcell,EIRP_smallcell)
      #if the user is at the entry way
      elif(value[1]> length_outside_mall and value[1] <= (length_outside_mall+entry_way)):
        #rsl of basestation, the penetration loss is calculated based on the formula
         value[2] = Rs.Rsl(height_Basestation,value[1],EIRP_basestation)+ (penetration_loss*((value[1]-length_outside_mall)/10))
         #rsl of smallcell, the penetration loss is calculated based on the formula
         Rsls = Rs.Rsl(height_smallcell,distance_from_smallcell,EIRP_smallcell) + (penetration_loss*((length_outside_mall+entry_way)-value[1])/10)
      else:
        #successfully completed call in the basestation 
        call_successfully_completed +=1
        #increment the user by 1
        Total_users+=1
        #remove the user from basestation
        del dict1[key]
        continue
      #if the RSl of Basestation goes below -102
      if(value[2] < -102.0):
        call_drop_Basestation +=1
        #increment the user by 1
        Total_users+=1
        #remove the user from basestation
        del dict1[key]
        continue
      else:
        #if the rsl of smallcell is greater than the rsl of basestation 
        if(Rsls > value[2]):  
          handoff_attempts_basestation +=1
          #checks whether the Rsl of smallcell is greater than -102
          #checks the no.of channels in the dictionary 
          if(len(dict2) <=29):
                 call_handoff_basestation += 1
                #increase in the handoff connection
                 dict2[key] = dict1[key]
                 #remove the user from basestation
                 del dict1[key]
                 
          #if the no.of channels is less than 30 than the handoff fails
          else:
               handoff_failure_basestation += 1
               channel_blocked_smallcell +=1 
               
#if Rsl is less than -102 than handoff fails
           
               
 if(len(dict2) != 0):
  #I can't able to delete the dictionary while iterating. so, I copied the dictionary  
  d2 = dict2.copy()   
  for key,value in d2.items():
     #decrementing the value of duration by one of each active users for every iteration 
     if(value[0] > 0):
             value[0] -=1 
     else:
        #successfully completed call in the smallcell
         call_successfully_completed_smallcell +=1
          #call successfully completed in the small cell   
         Total_users+=1
           #increment the total number of users by 1
         del dict2[key]
         #remove the user the smallcell 
         continue         
     #if the time of duration completes then the call is consider as the successful call        
     #Decrements the distance by 1m if the user is  on the mall or on the parking lot  and the direction is towards Basestation  
     if(value[1] < distance_BS and value[1]>= Roadlength and value[3]==-1):    
        value[1]-=1
      #Decrements the distance by 15metres if the user is on the road and the direction is towards Basestation   
     elif(value[1] < Roadlength and value[1]>=0 and value[3]==-1):    
        value[1] -= 15
     #Increments the distance by 1m if the user is on the mall or on the parking lot and the direction is towards small cell   
     elif(value[1] < (distance_BS-1) and value[1]> Roadlength and value[3]==1):    
        value[1]+=1
     #Increments the distance by 1m if the user is on the roadlength and the direction is towards small cell    
     elif(value[1] <= Roadlength  and value[3]==1):    
        value[1] += 15     
     distance_from_smallcell = distance_BS - value[1]   
     #if the user is outside the mall
     if(value[1] <= length_outside_mall  and value[1]>=0):   
      #rsl of smallcell , it includes penetration loss since the user is outside the mall
       value[2] = Rs.Rsl(height_smallcell,distance_from_smallcell,EIRP_smallcell,shadowing[int(round(value[1]/10))])+penetration_loss
     #rsl of basestation    
       Rsl = Rs.Rsl(height_Basestation,value[1],EIRP_basestation,shadowing[int(round(value[1]/10))])
     #if the user is outside the entry way and between small cell
     elif(value[1] > (length_outside_mall+entry_way) and value[1]<distance_BS):
       #rsl of smallcell
       value[2] = Rs.Rsl(height_smallcell,distance_from_smallcell,EIRP_smallcell)
      #rsl of basestation , it includes penetration loss since the user is in mall  
       Rsl =   Rs.Rsl(height_Basestation,value[1],EIRP_basestation) + penetration_loss
     #if the user is at the entry way
     elif(value[1] > length_outside_mall and value[1]<=(length_outside_mall+entry_way)):
        #rsl of smallcell, the penetration loss is calculated based on the formula
         value[2] = Rs.Rsl(height_smallcell,distance_from_smallcell,EIRP_smallcell)+ (penetration_loss*((length_outside_mall+entry_way)-value[1])/10)
        #rsl of basestation, the penetration loss is calculated based on the formula
         Rsl =   Rs.Rsl(height_Basestation,value[1],EIRP_basestation) + (penetration_loss*(value[1]-length_outside_mall)/10)
     else:
     #call successfully completed in the small cell   
       call_successfully_completed_smallcell +=1
    #increment the total number of users by 1
       Total_users+=1
       #remove the user the smallcell 
       del dict2[key]
       continue
     #if the RSl of smallcell goes below -102
     if(value[2] < -102):
        #increment the call drop in the smallcell by 1
        call_drop_smallcell +=1
        #increment the total number of users by 1
        Total_users+=1
        #remove the user the smallcell 
        del dict2[key]
        continue
        
        
     else:
       #if the rsl of basestation is greater than the rsl of small cell 
       if(Rsl > value[2]):
          #hanoff attempts from smallcell
            handoff_attempts_smallcell +=1
            #checks the no.of traffic channels in the small cell
            if(len(dict1) <= 29):
               #increment the successfully connected handoff by 1
                 call_handoff_smallcell +=1
                 #swap the user from smallcell to basestation
                 dict1[key] = dict2[key]
                 #remove the user the smallcell 
                 del dict2[key]
                      
            #if the no.of channels is less than 30 than the handoff fails   
            else:
               handoff_failure_smallcell +=1
               channel_blocked_basestation+=1
               
              

 count+=1
print("total users left",Total_users)
print("No.of.calls currently in use in Basestation",len(dict1))
print("No.of.calls currently in use in smallcell",len(dict2))
print("call_successfully_completed_Basestation",call_successfully_completed)
print("call_successfully_completed_smallcell",call_successfully_completed_smallcell)
print("handoff_failure_smallcell",handoff_failure_smallcell)
print("handoff_failure_basestation",handoff_failure_basestation)
print("call_handoff_smallcell",call_handoff_smallcell)
print("call_handoff_basestation",call_handoff_basestation)
print("channel_blocked_smallcell",channel_blocked_smallcell) 
print("channel_blocked_basestation",channel_blocked_basestation)
print("handoff_attempts_smallcell",handoff_attempts_smallcell)
print("handoff_attempts_basestation",handoff_attempts_basestation)
print("call_attempts_smallcell",call_attempts_smallcell)
print("call_attempts_basestation",call_attempts_basestation)
print("successful_connection_smallcell",successful_connection_smallcell)
print("successful_connection_basestation",successful_connection_basestation)
print("call_drop_Basestation",call_drop_Basestation) 
print("call_drop_smallcell",call_drop_smallcell)
print('call_block_basestation_power',call_block_basestation_power)
print('call_block_smallcell_power',call_block_smallcell_power)

         
           
            



      

     
     
