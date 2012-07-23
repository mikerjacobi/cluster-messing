import os
import random

name='junk.'+str(int(random.random()*10000))
os.system('cp big.iso '+name)
os.system('rm '+name)
