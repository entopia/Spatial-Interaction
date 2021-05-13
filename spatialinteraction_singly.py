'''
Created on Mar 13, 2015

@author: o
'''
from scripting import *
import math
# get a CityEngine instance
ce = CE()

'''get objects from scene and store them in list''' 
#allobjects=ce.getObjectsFrom(ce.scene)
#selection=ce.getObjectsFrom(ce.selection)
#blocksSel=ce.getObjectsFrom(ce.selection,ce.withName("block"))


blocks=ce.getObjectsFrom(ce.scene,ce.withName("blocks"))
LandUse=[ce.getAttribute(blocks[x],'landuse') for x in range (len(blocks))]
Pop=[ce.getAttribute(blocks[x],'Pop') for x in range (len(blocks))]

''' get FID of blocks and LandUse'''
#FID=len(blocks)
Apo = [blocks[i] for i in range (len(blocks)) if LandUse[i]=='Industrial']
Pros =  [blocks[i] for i in range (len(blocks)) if LandUse[i]=='resi']

'''GENERIC SPATIAL INTERACTION SINGLY CONSTRAINED FUNCTION'''
def SpatialInt(I, J, O):
    
    '''get x-y location of blocks/ calculate area'''
    I_X=[ce.getPosition(I[i])[0] for i in range (len(I))] # pinakas olon ton x
    I_Y=[ce.getPosition(I[i])[2] for i in range (len(I))]
    J_X=[ce.getPosition(J[i])[0] for i in range (len(J))] # pinakas olon ton x
    J_Y=[ce.getPosition(J[i])[2] for i in range (len(J))]
    Pop=[ce.getAttribute(I[i],O) for i in range (len(I))]
    
    '''Oi*ei Population income'''
    Oi=[]   
    for i in range (len(I)):
        Oi_each= Pop[i]*5
        Oi.append(Oi_each)        

    '''calculating coefficient Ai for Ai= 1/SiWiexp(-bcij)'''
    Ai=[]
    bres = 0.01 #bb=0.00125  # factor pou kanonizei to concetration (oso pio megalo toso pio dinati i elxi. polis kosmos sigkentronetai giro apo ta kentra.)
    for i in range (len(I)): 
        denominator=0
        for j in range(len(J)): # j '''the different centers'''
            distance2= math.sqrt((math.pow(I_X[i]-J_X[j],2))+math.pow(I_Y[i]-J_Y[j],2))
            denominator=denominator+(math.exp(-bres*distance2)) #''' the Sum of dist i--> j
        Ai.append(denominator)
    
    '''MAIN SPATIAL INTERACTION EQUATION''' 
    '''creation of empty 2dimentional array to store all flows'''
    Sij =[[0 for x in range (len(J))] for y in range (len(I))] 
    
    '''Spatial Interaction (singly constrained) Sij= BiOiWjexp(-bcij) Calculation of Flows from I to J'''
    for j in range (len(J)):
        for i in range (len(I)):
            distance= math.sqrt((math.pow(I_X[i]-J_X[j],2))+math.pow(I_Y[i]-J_Y[j],2))
            Sij[i][j]=  (Oi[i]*math.exp(-bres*distance))/Ai[i]


    '''creating obj attr for each industry (automatic creation-generation of no of attr according to no of industries)  '''
    #ce.setAttribute(blocks[y], 'pop'+str(x), pop_each[x][y]) NEEDED TO SET EACH POP INDIVIDUALLY.     

    '''Sums: Sums of flows to each zone J (how many people go to each retail).  of all pop to check if the pop distributed is the same as the pop in the industries.'''
    sum_all=0
    poptotal=[]
    for j in range (len(J)):
        sum_each_p=0 # midenizei ti metabliti meta apo kathe iteration gia na min prosthetei olous tous plithismous mazi. 
        for i in range (len(I)):
            #sum_all = sum_all+pop_each[g][b] # kanei sum olon ton plithismon se mia metavliti
            sum_each_p = sum_each_p+Sij[i][j] # apothikeuei ton sinoliko plithismo gia kathe block xexorista. 
        poptotal.append(sum_each_p) #  vazi to kathe athrisma se ena keli tis array.
        #to set attributes for each zone J: 
        #ce.setAttribute(J[j], 'flow', poptotal[j]) # vazei ton sinoliko plithismo tis kathe zonis 
        
    print ("model pop:", sum(poptotal), "no of units:", len(poptotal))
    print ("finished spatial interaction")
    # returns flows for each retail center J. (residence in lowry). 
    return poptotal



''' Run Spatial interaction with inputs I,J'''
a= SpatialInt (Apo,Pros, Pop)
print a


