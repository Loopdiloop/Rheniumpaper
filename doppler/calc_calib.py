""" Script for calulating gains and shifts of peaks in NaI for 
1.868MeV and 5.270 MeV in 15N, with doppler shift (i.e. NaI angles). 
Output can be copied into the gainshift-file of the sorting usersort.
"""

import numpy as np 
import matplotlib.pyplot as plt
import sys

peaks_rings = np.zeros((8,26,2))

""" # IF gated on NaI crystal AND SiRi ring (not neccesary in my experiment)
for i in range(8): # For all rings of SiRi
	# cactus_gains_ring contains
	peaks = np.loadtxt('cactus_gains_ring%d.txt'%i, dtype=None)
	peaks_rings[i,:,0] = peaks[:,0]/5
	peaks_rings[i,:,1] = peaks[:,1]/5
"""

# Doppler shifted energies for NaI angles
# Ex = 5.283
# 142, 116, ... 37 deg
peak_5k_doppler = np.array([5113.736, 5187.810, 5243.815, 5323.163, 5379.168, 5453.242])

#Ex = 1.868
#142, 116, ... 37 deg 
peak_2k_doppler = np.array([1806.331, 1833.241, 1853.587, 1882.413, 1902.759, 1929.669])

# Load the setup to find which crystal in which angle
# Crystal no. Ring Theta Phi HV Supply

crystal_no = [] ; ring_no = []; theta = []; filenumber = []
Nai_file = open("NaI_positions.txt")
while len(crystal_no)<26:
	linje = Nai_file.readline()
	a = (linje.strip("\n")).split(",")
	crystal_no.append(int(a[0]))
	ring_no.append(int(a[1]))
	theta.append(float(a[2]))
	filenumber.append(int(a[3]))

crystal_no = np.array(crystal_no) ; ring_no = np.array(ring_no); theta = np.array(theta); filenumber = np.array(filenumber)

# The doppler shifter ideal
actual_5k = peak_5k_doppler[ring_no-1]
actual_2k = peak_2k_doppler[ring_no-1]
print(actual_5k, filenumber)
peaks_5k = np.zeros(26)
peaks_2k = np.zeros(26)

spread_5k = np.zeros((8,26))

for k in range(8):
	# The uncorrected peaks, for all siri rings
	peaks_5k += peaks_rings[k,:,1]
	peaks_2k += peaks_rings[k,:,0]
	spread_5k[k] = peaks_rings[k,:,1]
	#print("spread for NaI 2k: ", np.max(peaks_rings[k,:,0])-np.min(peaks_rings[k,:,0]))
	#print("spread for NaI 5k: ", np.max(peaks_rings[k,:,1])-np.min(peaks_rings[k,:,1]))

print("Min/max: ", np.max(spread_5k,axis=0) - np.min(spread_5k, axis=0))


#peaks_5k = peaks_rings[7,:,1]
#peaks_2k = peaks_rings[7,:,0]

peaks_5k = peaks_5k/8.
peaks_2k = peaks_2k/8.

gain = (actual_5k - actual_2k)/(peaks_5k - peaks_2k)
shift = actual_5k - peaks_5k*gain





N = 32 #no. channels, 0 -> 31
gain_formatted = np.ones(N)
shift_formatted = np.zeros(N)

for j in range(len(filenumber)):
	I = filenumber[j]
	gain_formatted[I] = gain[j]
	shift_formatted[I] = shift[j]

def print_lines(array):
	print("%s "%(str(array[:4]).strip("[]\n")),"%s "%(str(array[4:7]).strip("[]\n")))
	print("%s "%(str(array[7:10]).strip("[]\n")), "%s "%(str(array[10:14]).strip("[]\n")))
	print("%s "%(str(array[14:18]).strip("[]\n")), "%s "%(str(array[18:21]).strip("[]\n")))
	print("%s "%(str(array[21:25]).strip("[]\n")), "%s "%(str(array[25:28]).strip("[]\n")))
	print("%s "%(str(array[28:]).strip("[]\n")))

print("gain:")
print_lines(gain_formatted)

print("shift:")
print_lines(shift_formatted)

print(filenumber)

sys.exit()













#beta = 0.04

#theta_SiRi = np.array([140., 138., 136., 134., 132., 130., 128., 126.])
#shifted_NaI_15N = np.array([5456.3,  5455.7, 5455.1, 5454.5, 5453.9, 5453.2, 5452.5, 5451.8]) #5.2MeV 15N
#shifted_NaI_15N_recoil_vel = np.array([4.09567289, 4.08245307, 4.06852226, 4.05387241, 4.03849543, 4.02238328, 4.005528,   3.98792176]) # % ? v2/c2 ?
#beta = shifted_NaI_15N_recoil_vel

for k in range(8):
	#plt.plot(range(26), peaks_rings[k, :, 0])
	plt.plot(range(26), peaks_rings[k, :, 1])

#plt.show()

"""
$ python3 frank.py 
Q0:  -4.965494599999292  MeV
SiRi angle :  [140. 138. 136. 134. 132. 130. 128. 126.]
outgoing particle energy:  [8.02746492 8.1030242  8.18238291 8.26554512 8.35251226 8.44328272
 8.5378514  8.63620934]  MeV
recoil energy:  [11.72355148 11.6479922  11.56863349 11.48547128 11.39850414 11.30773368
 11.213165   11.11480706]  MeV
Excitation energy:  5.283489  MeV
Q:  -10.248983599999292  MeV
recoil velocity:  [4.09567289 4.08245307 4.06852226 4.05387241 4.03849543 4.02238328
 4.005528   3.98792176]  %
Beam energy (test):  [30. 30. 30. 30. 30. 30. 30. 30.]
Doppler shift for the 5.2 MeV 15N line:  [172.8202731  172.26245216 171.67463029 171.05646774 170.40762364
 169.72775832 169.01653576 168.27362621]  keV
 Total shifted for the 5.2 MeV 15N line:  [5456.3092731  5455.75145216 5455.16363029 5454.54546774 5453.89662364
 5453.21675832 5452.50553576 5451.76262621]  keV
Recoil angle :  [ 7.92315304  8.31612023  8.7082196   9.09931009  9.48923537  9.87782277
 10.26488232 10.65020561]
"""

#actual_5k = 5270.*(1+beta*np.cos(np.deg2rad(theta_angles_NaI[positions])))
#actual_2k = 2582. # From experimentation
#actual_2k = 1868.*(1+beta*np.cos(np.deg2rad(theta_angles_NaI[positions])))

gain = (actual_5k - actual_2k)/(peaks_5k - peaks_2k)
shift = actual_5k - peaks_5k*gain

print("\nmin / max!!!")
print("max: %d, OG: %d, min: %d" %(np.max(actual_5k), 5270., np.min(actual_5k)))
print("diff: ", np.max(actual_5k)-np.min(actual_5k)) 
print("\n")


#print('i: ', i)
#print('gain: ', gain)
#print('shift: ', shift)

# Formatting for missing channels not in array i:

N = 32 #no. channels, 0 -> 31
gain_formatted = np.zeros(N)
shift_formatted = np.zeros(N)

for j in range(len(i)):
	I = int(i[j])
	gain_formatted[I] = gain[j]
	shift_formatted[I] = shift[j]

print('gain formatted: ', gain_formatted)
print('shift formatted: ', shift_formatted)


#import matplotlib.pyplot as plt



#plt.plot(i, peaks_5k)# gain)
#plt.show()
#plt.clf()

#plt.plot(i, shift)
#plt.show()


"""
# Plot each ring of detector to see possible systematics!

#peaks_rings[0,:,2] # for ring 0 in SiRi, take all NaI angles :, for the 5.3MeV peak
colour=["r", "g", "b", "y", "p", "c", "m", "o"]
for l in range(8):
	for k in range(26):
		x = ring_no[np.argmin(abs(filenumber-k))]
		y = peaks_rings[l,k,1]
		plt.plot(x, y, "*", color=colour[l])
		print(x,y)

plt.show()
sys.exit()
"""