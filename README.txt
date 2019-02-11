USAGE: make _fibril_starting_model <width (A)> <thickness (A)> <x-over length (nm) <apix>

update the paths to relion_helixtoolbox and e2pdb2mrc.py in the top of teh script before using 

to use the models in relion clip them to the corect box size with e2proc3d.py

e2proc3d.py in_file.mrc outfile.mrc --clip=boxsize,boxsize,boxsize

and apply a 90% spherical mask with relion_helix_toolbox:
relion_helix_toolbox --spherical_mask --i in_file.mrc --o file_masked.mrc --sphere_percentage 0.9
