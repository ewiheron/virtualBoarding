

import numpy as np
from numpy.linalg import inv

#beaconPositions is a matrix
#each row corresponds to the x/y coordinates of one beacon
#beacons are numbered from 0 to N-1
#beacon 0 is at x=0; y=0
#beacon 1 is the first row in the matrix
#beacon i is the ith row
#beaconPositions=[[xpos1,ypos1],[xpos2,ypos2],...]

#tdoas is a column vector with the relative distance to beacon 0
#tdoas=[diff1,diff2,...,diffN-1]
#diff1=distanceTo0-distanceTo1
#diff2=distanceTo0-distanceTo2
def calcXY(beaconPositions,tdoas):
    A=np.concatenate((beaconPositions,tdoas.transpose()),axis=1)
    beaconSquared=np.power(beaconPositions,2)
    Theta1=np.sum(beaconSquared,axis=1)
    Theta2=np.power(tdoas,2)

    Theta=0.5*(Theta1-Theta2.transpose())

    Atran=A.transpose()
    
    ApseudoInverse=np.linalg.inv(np.matmul(Atran,A))
    Arect=np.matmul(ApseudoInverse,Atran)
    xEstimated=np.matmul(Arect,Theta)
    return xEstimated

