import matplotlib.pyplot as plt
import math
import numpy as np
f =1000
hm = 1.7 
EIRP = 57
EIRP1 = 30
shadowing = np.random.normal(0.0, 2, 281)
h = 50
hs = 10
penetration_loss = -21
def loss(h,i,EIRP):
  d =  i/1000
  #okamara hata model
  ahm = (1.1*math.log10(f) - 0.7)*hm - (1.56*math.log10(f) - 0.8)    
  pl = 69.55 + 26.16*math.log10(f) - (13.82*math.log10(h)) + ((44.9 - (6.55*math.log10(h)))*math.log10(d)) - ahm
  #fading
  fading_a =  np.sort(np.random.rayleigh(1, 10)) 
  fadinga_db = 20*np.log10(fading_a[1])
  #path loss
  loss = EIRP - pl + fadinga_db 
  return(loss)
x = []
y =[]
for i in range(2999):
 #distance from small cell 
 d = 3000 - i    
 if(i <= 2800):
  #rsl of basestation in the road  
  path_loss = loss(h,(i+1),EIRP) + shadowing[int(round(i/10))]
  #rsl of smallcell in the road
  path_loss_s = loss(hs,d,EIRP1)+ penetration_loss + shadowing[int(round(i/10))]
  #append the rsl of basestation to the list
  x.append(path_loss)
  #append the rsl of smallcell to the list
  y.append(path_loss_s)
 elif(i > 2800 and i<= 2810):
   #rsl of basestation at the entry way
   path_loss = loss(h,(i+1),EIRP) + penetration_loss*((i-2800)/10)
   #rsl of smallcell at the entry way
   path_loss_s = loss(hs,d,EIRP1) + penetration_loss*((2810-i)/10)
   #append the rsl of basestation to the list
   x.append(path_loss)
   #append the rsl of smallcell to the list
   y.append(path_loss_s)
 else:
    #rsl of basestation in the mall
    path_loss = loss(h,(i+1),EIRP) + penetration_loss
     #rsl of smallcell in the mall
    path_loss_s = loss(hs,d,EIRP1)
    #append the rsl of basestation to the list
    x.append(path_loss)
    #append the rsl of smallcell to the list
    y.append(path_loss_s)
plt.plot(x,'b-',y,'r-')
plt.xlabel('distance')
plt.ylabel('Rsl')
plt.grid(linestyle='dotted')
plt.show()  
