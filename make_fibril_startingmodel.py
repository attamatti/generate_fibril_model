#!/usr/bin/env python

#make a fibrilstarting model

import sys
import subprocess
import os

####### UPDATE PATHS HERE ##########
relion_HT_path='/fbs/emsoftware2/LINUX/fbscem/relion3/relion-3.0_beta/build/bin/relion_helix_toolbox'
pdb2mrc_path='/fbs/emsoftware2/LINUX/EMAN2.12/bin/e2pdb2mrc.py'
##################


###### no touchy touchy ##########

if os.path.isfile(relion_HT_path) ==False:
    sys.exit('relion_helix_toolbox not found at {0}: update the path in the script'.format(relion_HT_path))

if os.path.isfile(pdb2mrc_path) ==False:
    sys.exit('e2pdb2mrc.py not found at {0}: update the path in the script'.format(pdb2mrc_path))

if len(sys.argv) < 5:
    sys.exit('\nUSAGE: make _fibril_starting_model <width (A)> <thickness (A)> <x-over length (nm) <apix>')

width_thick = int(sys.argv[1])
width_thin = int(sys.argv[2])
crossoverlength = float(sys.argv[3])
apix = float(sys.argv[4])

twist = 180.0/((crossoverlength*10)/4.8)
if '-RH' not in sys.argv:
    twist = twist*-1
print('using twist of {0} degrees'.format(twist))
corners = ((0-width_thick,0-width_thin,0),(0-width_thick,0+width_thin,0),(0+width_thick,0+width_thin,0),(0+width_thick,0-width_thin,0))

corner1 = (0-width_thick,0-width_thin,0)
corner2 = (0-width_thick,0+width_thin,0)
corner3 = (0+width_thick,0+width_thin,0)
corner4 = (0+width_thick,0-width_thin,0)


vrows = range(corner1[0],corner4[0]+1,5)
hrows = range(corner1[1],corner2[1]+1,5)
rowpairs = []
for v in vrows:
    for h in hrows:
        rowpairs.append((v,h,0))

output = open('{}_{}_{}.pdb'.format(width_thick,width_thin,crossoverlength),'w')

n=0
for i in rowpairs:
    output.write('ATOM  {0:>5} C    ALA A{0:>4}    {1:>8}{2:>8}{3:>8}  1.00     0           C\n'.format(n,i[0],i[1],i[2]))
    n+=1
output.close()

subprocess.call('{4} --pdb_helix --i {0}_{1}_{2}.pdb --o fibrilmodel.pdb --cyl_outer_diameter 0 --rise 4.8 --twist {3} --nr_subunits 100'.format(width_thick,width_thin,crossoverlength,twist,relion_HT_path),shell=True)
subprocess.call('{4} fibrilmodel.pdb {0}_{1}_{2}.mrc --res 15 --apix {3}'.format(width_thick,width_thin,crossoverlength,apix,pdb2mrc_path),shell=True)
subprocess.call('rm {}_{}_{}.pdb'.format(width_thick,width_thin,crossoverlength),shell=True)
