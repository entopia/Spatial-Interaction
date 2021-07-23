'''
Created on Mar 13, 2015

@author: o
'''
from scripting import *
import math
# get a CityEngine instance
ce = CE()

'''get objects from scene and store them in list''' 
#objects=ce.getObjectsFrom(ce.scene)
#objects2=ce.getObjectsFrom(ce.selection)
#blocksSel=ce.getObjectsFrom(ce.selection,ce.withName("block"))
blocks=ce.getObjectsFrom(ce.scene,ce.withName("blocks"))
LandUse=[ce.getAttribute(blocks[x],'landuse') for x in range (len(blocks))]
Pop= [ce.getAttribute(blocks[x],'Pop') for x in range (len(blocks))]

''' get FID of blocks and LandUse'''
#FID=len(blocks)

''' storing zones I,J per land use'''
I,J=[],[]
for i in range (len(blocks)):
    if LandUse[i]=='resi':
        I.append(blocks[i])
    if LandUse[i]=='retail': 
        J.append(blocks[i])

'''Generic Spatial Interaction function'''
def SpatialInt(I, J):
    
    '''get x-y location of blocks/ calculate area'''
    I_X=[ce.getPosition(I[i])[0] for i in range (len(I))] # pinakas olon ton x
    I_Y=[ce.getPosition(I[i])[2] for i in range (len(I))]
    J_X=[ce.getPosition(J[i])[0] for i in range (len(J))] # pinakas olon ton x
    J_Y=[ce.getPosition(J[i])[2] for i in range (len(J))]


    #bb=0.00125  # factor pou kanonizei to concetration (oso pio megalo toso pio dinati i elxi. polis kosmos sigkentronetai giro apo ta kentra.)
    '''calculation of total population produced by BE per zone'''
     #proportional factor for pop from employment
    Oi=[]
    Dj=[]
    Oite=[]
    
    '''Oi= SjTij'''
    for i in range (len(I)):
        Oi_each= Pop[i]*5
        Oi.append(Oi_each)
    '''Dj= SiTji'''
    for j in range (len (J)):
        Dj_each= Pop[i]*3
        Dj.append(Dj_each)
        

    '''calculating coefficient Bj for Bj=1/SiAiOiexp(-cij)but it cant have Ai in there so it is actually Bj= 1/SiWiexp(-bcij)'''
    Bj=[]
    bres = 0.01
    for j in range (len(J)): 
        paronomastis=0
        for i in range(len(I)): # j '''the different centers'''
            distance2= math.sqrt((math.pow(I_X[i]-J_X[j],2))+math.pow(I_Y[i]-J_Y[j],2))
            paronomastis=paronomastis+(math.exp(-bres*distance2)) #''' the Sum of dist i--> j
            #print c,": ",paronomastis
        Bj.append(paronomastis)
    
    '''calculating coefficient Ai for Ai=1/SjBjOjexp(-cij) actually: Ai= 1/SjWjexp(-bcij) '''
    Ai=[]
    bres1 = 0.01
    for i in range (len(I)): 
        paronomastis1=0
        for j in range(len(J)): # j '''the different centers'''
            distance1= math.sqrt((math.pow(I_X[i]-J_X[j],2))+math.pow(I_Y[i]-J_Y[j],2))
            paronomastis1=paronomastis1+(math.exp(-bres1*distance1)) #''' the Sum of dist i--> j
            #print c,": ",paronomastis
        Ai.append(paronomastis1)

    '''MAIN SPATIAL INTERACTION EQUATION''' 
    ''' pop= population from blocks to industry | creation of empty 2dimentional array to store'''
    Tij =[[0 for x in range (len(J))] for y in range (len(I))] 
    
    '''Spatial Interaction equation (singly constrained) for population in zones- allocation of Pop in all zones'''
    for j in range (len(J)):
        for i in range (len(I)):
            distance= math.sqrt((math.pow(I_X[i]-J_X[j],2))+math.pow(I_Y[i]-J_Y[j],2))
            Tij[i][j]=  (Oi[i]*math.exp(-bres*distance))/Bj[j]
        print (Tij[i][j])


    
    '''creating obj attr for each industry (automatic creation-generation of no of attr according to no of industries)  '''
    #ce.setAttribute(blocks[y], 'pop'+str(x), pop_each[x][y]) NEEDED TO SET EACH POP INDIVIDUALLY.     

    '''checking def. sums of all pop to check if the pop distributed is the same as the pop in the industries.'''
    sum_all=0
    poptotal=[]
    for j in range (len(J)):
        sum_each_p=0 # midenizei ti metabliti meta apo kathe iteration gia na min prosthetei olous tous plithismous mazi. 
        for i in range (len(I)):
            #sum_all = sum_all+pop_each[g][b] # kanei sum olon ton plithismon se mia metavliti
            sum_each_p = sum_each_p+pop_each[i][j] # apothikeuei ton sinoliko plithismo gia kathe block xexorista. 
        poptotal.append(sum_each_p) #  vazi to kathe athrisma se ena keli tis array.
        #pass
        ce.setAttribute(blocks[j], 'pop', poptotal[j]) # vazi ton sinoliko plithismo tis kathe zonis 

    #print pop_each [6][5]
    print ("model pop:", sum(pop), len(pop))
    print ("finished residential")

SpatialInt (I,J)