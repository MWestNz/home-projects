from matplotlib import pyplot as plt
import numpy as np

reach = [31,16,44,127,94,28,66,166,895,1063,128,138,42,395,0,369,38,215,650, \
    119,0,273,277,61,91,173,161,50,50,63,543,62,340,419,77,15,241,83,71,153,167,11,92,82,322]
likes = [1,0,5,9,3,0,0,8,16,40,4,8,0,17,0,18,2,7,22,3,0,5,5,5,7,2,12,0,0, \
    1,14,0,14,11,1,11,6,3,1,1,2,0,0,0,14]

ziplist = zip(likes,reach)
ziplist.sort()
likes, reach = zip(*ziplist)

plt.plot(likes,reach,'o')
plt.show()