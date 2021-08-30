"""
Kinematic calculations for doppler shift adapted from Franks root/.C script :)

When you calibrate the gamma energies from states in light nuclei,
the gammas could be doppler shifter enough to be significant 
to the analysis dependent on the angle of the gamma detector it was detected in. 


All masses and energies are given in MeV.
"""

import numpy as np

""" Ex = gamma energy without any shift """
# Levels in 15N
#Ex = 0. # MeV
Ex = 5.283489 #average
#Ex = 1.868 #2k peak
#Ex = 6.32235
#Ex = 7.29892

# Levels in 16O
#Ex = 0. # MeV
#Ex = 6.12863#3-
#Ex = 6.9155#2+
    
#Levels in 12C
#Ex = 0. # MeV
#Ex = 4.43894#2+

# Levels in 19F
#Ex = 0. # MeV
#Ex = 1.34567
#Ex = 2.779849

# Theta angles of SiRi in radians:
# To calculate all different SiRi-angles, use an array:
#theta = np.pi*np.array([140., 138., 136., 134., 132, 130, 128, 126])[:]/180.
# To calculate an average:
theta = np.mean(np.pi*np.array([140., 138., 136., 134., 132, 130, 128, 126])[:]/180.)

# a is incoming particle, b is outgoing particle
Ta = 30. #alpha beam energy
ma = 3728.400916 #alpha particle mass
pa2 = Ta*Ta + 2*ma*Ta
mb = 938.7829706 #outgoing proton mass

# x is target nucleus, y is resulting nucleus
mx = 11177.928 #mass of 12C
#mx = 14899.167 #mass of 16O

my = 13972.51144+Ex #15N
#my = 14899.167+Ex #16O
#my = 11177.928+Ex #12C
#my = 17696.89856+Ex #19F

# Total Q-value
Q=mx+ma-my-mb

print("Q0: ", mx+ma-my-mb+Ex , " MeV")


Tb = ((np.cos(theta)*np.sqrt(ma*mb*Ta)+np.sqrt(ma*mb*Ta*(np.cos(theta))**2+(my+mb)*(my*Q+(my-ma)*Ta)))/(my+mb))**2

Ty = Q - Tb +Ta

# NaI angles, degrees.
NaI_angle = np.array([142.6, 116.6, 100.7, 79.3, 63.4, 37.4]) 


print("SiRi angle : ", theta*180/np.pi)
print("outgoing particle energy: ", Tb , " MeV")
print("recoil energy: ", Ty , " MeV")
print("Excitation energy: ", Ex , " MeV")
print("Q: ", Q , " MeV")
print("recoil velocity: ", 100*np.sqrt(2*Ty/my) , " %")
print("Beam energy (test): ", Ty + Tb - Q )
print("Doppler shift for the 5.2 MeV 15N line: ", 5283.489*(1+np.sqrt(2*Ty/my)*np.cos(np.pi*NaI_angle/180))-5283.489 , " keV")
print("Total shifted for the 5.2 MeV 15N line: ", 5283.489*(1+np.sqrt(2*Ty/my)*np.cos(np.pi*NaI_angle/180)), " keV")
print("Recoil angle : ", np.arcsin(np.sqrt(mb*Tb)*np.sin(theta)/np.sqrt(my*Ty))*180/np.pi)


print(" -------------------")
print("Ex = %.3f"%Ex)

print("""Doppler shifted gammas for NaI angles. Averaged over all SiRi-angles.
NaI deg. | shifted Ex """)
for j in NaI_angle:
    doppler_shifted = Ex*1000*(1+np.sqrt(2*Ty/my)*np.cos(np.pi*j/180))
    print("%5.1f, %.3f "%(j, np.mean(doppler_shifted)))
    
    
    
