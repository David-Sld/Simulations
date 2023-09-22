from Filters.g_h_filter import g_h_filter
from numpy import array, pi as PI, sqrt, std, reshape, mean
import matplotlib.pyplot as plt
from scale import Scale
"""
This files simulate cointainer emptying.
The container is filled with water and as a circular gap with a 10 cm diameter
The container has a circular shape with à 1 m diameter and a 1 mter height.
The container is on a scale. The scale has a 10 kg standart deviation
The purpose of this script ios to estimate container mass while emptying.
Simulation uses Torricelli's equation to simulate container emptying.
"""


######## CONSTANTS DEFINITION #########
RHO_WATER = 1026 # (kg/m^3) water density
D = 1 # (m) container diameter
d = 0.1 # (m) gap diameter
H = 10 # (m) container height
g = 9.81 # (m.s^(-2), gravity
EMPTY_MASS = 10.0 # (kg), container water without water
SCALE_STD = 5.0 # (kg), scale standart deviation
SCALE_BIAS = 0.0 # (kg) scale bias
SCALE_SAM = 1.0 # Scalling and (mis)-Aligneme,nt Matrix 
dt = 0.1 #(s), sampling time
alpha = 0.1
beta = 0.1
#######################################

######### INITIAL CONDITION ###########
H0 = 1 # (m) initial water heigh
Mdot0 = -sqrt(2.0 * g * H0 / 2.0) * RHO_WATER * PI * (d/2) * (d/2)
M0 = EMPTY_MASS + RHO_WATER * H0 * PI * (D/2) ** 2.0

######### OBJECT DEFINITION ###########
scale = Scale(p_std = [SCALE_STD], p_bias = [SCALE_BIAS], p_SAM = [SCALE_SAM])
filter_1 = g_h_filter([M0, Mdot0], 0.04, 0.5)
filter_2 = g_h_filter([M0, Mdot0], 0.055, 0.6)
filter_3 = g_h_filter([M0, Mdot0], 0.06, 0.7)
filter_4 = g_h_filter([M0, Mdot0], 0.065, 0.8)
#######################################
0
############# SIMULATION ##############                                                             
time = 0
h = H0 # Current water height in the container
trueMass = M0
history_trueMass = [trueMass]
history_measuredMass = [ scale.GetMeasurement([trueMass])[0,0]]
history_estimatedMass1, history_estimatedMass2, history_estimatedMass3, \
                        history_estimatedMass4 = [M0], [M0], [M0], [M0]
history_time = [time]
history_measTime = [time]
history_massOut = []
history_h = [h]


it = 0
while trueMass>EMPTY_MASS:
    it += 1
    time = time + dt
    history_time.append(time)
    # Simulation of what happen in dt second    
    v = sqrt(2.0 * g * h) # (m/s) Torriceli's equation
    massOut = v * RHO_WATER * PI * (d/2) * (d/2) * dt# (kg) water getting out of container between t and t + dt
    trueMass = trueMass - massOut if (trueMass - massOut)>EMPTY_MASS else EMPTY_MASS
    estimatedMass1 = filter_1.Predict(dt)[0,0]
    estimatedMass2 = filter_2.Predict(dt)[0,0]
    estimatedMass3 = filter_3.Predict(dt)[0,0]
    estimatedMass4 = filter_4.Predict(dt)[0,0]
    h = (trueMass - EMPTY_MASS) / (RHO_WATER * PI * (D/2) ** 2.0)
    # Save values
    history_trueMass.append(trueMass)
    history_massOut.append(massOut)
    history_h.append(h)
    if (it % 10) == 0:
        measurement = scale.GetMeasurement([trueMass])[0,0]
        history_measuredMass.append(measurement)
        history_measTime.append(time)
        estimatedMass1 = filter_1.Update(measurement, dt)[0,0]
        estimatedMass2 = filter_2.Update(measurement, dt)[0,0]
        estimatedMass3 = filter_3.Update(measurement, dt)[0,0]
        estimatedMass4 = filter_4.Update(measurement, dt)[0,0]
    history_estimatedMass1.append(estimatedMass1)
    history_estimatedMass2.append(estimatedMass2)
    history_estimatedMass3.append(estimatedMass3)
    history_estimatedMass4.append(estimatedMass4)
    
history_measuredMass = array(history_measuredMass)
history_trueMass = array(history_trueMass)
history_estimatedMass1 = array(history_estimatedMass1)
history_estimatedMass2 = array(history_estimatedMass2)
history_estimatedMass3 = array(history_estimatedMass3)
history_estimatedMass4 = array(history_estimatedMass4)
plt.subplot(411)
plt.plot(history_time, history_estimatedMass1, 'r', label = 'filter1')
plt.plot(history_time, history_trueMass)
plt.scatter(history_measTime, history_measuredMass, c='k', alpha=0.5, marker="+")
plt.subplot(412)
plt.plot(history_time, history_estimatedMass2, 'g', label = 'filter2')
plt.plot(history_time, history_trueMass)
plt.scatter(history_measTime, history_measuredMass, c='k', alpha=0.5, marker="+")
plt.subplot(413)
plt.plot(history_time, history_estimatedMass3, 'b', label = 'filter3')
plt.plot(history_time, history_trueMass)
plt.scatter(history_measTime, history_measuredMass, c='k', alpha=0.5, marker="+")
plt.subplot(414)
plt.plot(history_time, history_estimatedMass4, 'c', label = 'filter4')
plt.plot(history_time, history_trueMass)
plt.scatter(history_measTime, history_measuredMass, c='k', alpha=0.5, marker="+")
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('mass (kg)')
deltaMass1 = history_trueMass - history_estimatedMass1
deltaMass2 = history_trueMass - history_estimatedMass2
deltaMass3 = history_trueMass - history_estimatedMass3
deltaMass4 = history_trueMass - history_estimatedMass4
print("Filter 1 : mean = " + str(mean(deltaMass1)) + " (kg) et std = " + str(std(deltaMass1))+ " (kg)")
print("Filter 2 : mean = " + str(mean(deltaMass2)) + " (kg) et std = " + str(std(deltaMass2))+ " (kg)")
print("Filter 3 : mean = " + str(mean(deltaMass3)) + " (kg) et std = " + str(std(deltaMass3))+ " (kg)")
print("Filter 4 : mean = " + str(mean(deltaMass4)) + " (kg) et std = " + str(std(deltaMass4))+ " (kg)")
plt.show()







