# read the dyno csv data and generate relevant graphs
# Rebecca McCabe
# Created 1-28-19
# Last updated 2-1-19

import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv

file = 'dynoCSVs//dynodata_Wed_Jan_30_14_41_10_2019.csv'

############## import the csv file ##########################
testV = []
loadV = []
RPM = []
torque = []
time = []
motVol = []
motCur = []
batVol = []
batCur = []
#TODO - make these originally numpy arrays instead of python lists that I change to numpy later

with open(file, 'rt') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	next(reader) # no data is in the first row so skip it
	for row in reader:
		if len(row) > 0:
			testV.append(float(row[0]))
			loadV.append(float(row[1]))
			RPM.append(float(row[2]))
			torque.append(float(row[3]))
			time.append(float(row[4]))
			motVol.append(float(row[5]))
			motCur.append(float(row[6]))
			batVol.append(float(row[7]))
			batCur.append(float(row[8]))

################## convert to numpy and do calcs #############

testV = np.asarray(testV)
loadV = np.asarray(loadV)
RPM = np.asarray(RPM)
torque = np.asarray(torque)
time = np.asarray(time)
motVol = np.asarray(motVol) / 1000
motCur = np.asarray(motCur)
batVol = np.asarray(batVol)
batCur = np.asarray(batCur)

# power and eff calcs
pMech = torque * RPM * 2 * np.pi / 60 	# Watts
pElec = batVol * batCur	/ 1000			# Watts
eff = pMech / pElec

################## make graphs #################################

# no load speed vs voltage
#TODO: plot only data points where there's no torque 
plt.figure(1)
plt.scatter(testV, RPM, label='Commanded')
plt.scatter(motVol, RPM, label='Measured')
plt.xlabel('Motor Voltage (V)')
plt.ylabel('No-Load Speed (RPM)')
plt.legend()


# torque speed curve colored by voltage
plt.figure(2)
uniqueVoltages, idxs = np.unique(testV, return_inverse=True)
normVs = uniqueVoltages / max(uniqueVoltages)
colors = [ mpl.cm.jet(x) for x in normVs ]

for v, uniqueVoltage in enumerate(uniqueVoltages):
	idxsOfUniqueV = [i for i, e in enumerate(testV) if e == uniqueVoltage]
	rpmsAtThisV = np.asarray([RPM[i] for i in idxsOfUniqueV])
	torquesAtThisV = np.asarray([torque[i] for i in idxsOfUniqueV])
	plt.scatter(rpmsAtThisV, torquesAtThisV, color=colors[v], label='voltage='+ str(round(uniqueVoltage,2)))
	plt.plot(np.sort(rpmsAtThisV), torquesAtThisV[np.argsort(rpmsAtThisV)], '--')
plt.xlabel('Speed (RPM)')
plt.ylabel('Torque (Nm)') 
plt.legend()


# torque speed curve colored by efficiency
plt.figure(3)
cmap = mpl.cm.jet
plt.scatter(RPM, torque, c=eff, cmap=cmap)

# make colorbar using method described here
# https://stackoverflow.com/questions/30779712/show-matplotlib-colorbar-instead-of-legend-for-multiple-plots-with-gradually-cha
smap = mpl.cm.ScalarMappable(cmap = cmap)
smap.set_array(eff)
cbar = plt.colorbar(smap)
cbar.set_label('Efficiency')

plt.xlabel('Speed (RPM)')
plt.ylabel('Torque (Nm)')
plt.show()
