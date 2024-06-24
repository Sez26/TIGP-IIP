### script to post process data
# plot strain against temperature
# calculate thermal expansion coeffecient

import numpy as np
import matplotlib.pyplot as plt

# load data
with open('/home/sez26/TIGP-IIP/HEA/Record_thermal_exp.txt', 'r') as lmps_file:
    lmps_data = lmps_file.readlines()

# print(lmps_data)

# create new array
lmps_table = np.empty((len(lmps_data)-1, 2))
for i in range(1,len(lmps_data)):
    before, sep, after = lmps_data[i].partition('\t')
    lmps_table[i-1, 0] = before
    before, sep, after = after.partition('\n')
    lmps_table[i-1, 1] = before

# print(lmps_table)
# plt.figure(figsize=(10, 6))

plt.plot(lmps_table[:,0], lmps_table[:,1])

plt.title('Thermal expansion of HEA')
plt.xlabel('Temperature (K)')
plt.ylabel('Strain')
plt.grid(True)
# plt.legend()

# Calculating thermal expansion coefficient
coefficients = np.polyfit(lmps_table[:,0], lmps_table[:,1], 1)  # 1 means linear fit
m, c = coefficients

# Add text annotation
text_x = 300
text_y = 0
plt.text(text_x, text_y, ['Thermal expansion coefficient is: ', m, 'K^-1'], fontsize=12, color='green')

# print('Thermal expansion coefficient is: ', m, 'K^-1')

# add text to figure

plt.show()