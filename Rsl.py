def Rsl(h,d,EIRP,shadowing = 0): 
     import math
     import numpy as np
     f = 1000
     hm = 1.7
     d = d/1000
     ahm = (1.1*math.log10(f) - 0.7)*hm - (1.56*math.log10(f) - 0.8)    
     pl = 69.55 + 26.16*math.log10(f) - (13.82*math.log10(h)) + ((44.9 - (6.55*math.log10(h)))*math.log10(d)) - ahm
     fading_a =  np.sort(np.random.rayleigh(1, 10))
     fadinga_db = 20*np.log10(fading_a[1])
     loss = EIRP - pl + fadinga_db + shadowing  
     return(loss)
     
