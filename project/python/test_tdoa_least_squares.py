
import numpy as np
from TdoaLeastSquares import calcXY

bp=np.matrix([[2,0],[2,2],[0,1]])
tdoas=np.matrix(np.sqrt([26,10,17])-np.sqrt([26,26,26]))
tdoas=np.matrix([0,0,1-2*0.7])


xe=calcXY(bp,tdoas)

print('================================================================================')
print(xe)
