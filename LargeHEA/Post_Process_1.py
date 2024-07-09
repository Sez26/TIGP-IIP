### script to post process data
# plot strain against temperature
# calculate thermal expansion coeffecient

import numpy as np
import matplotlib.pyplot as plt

def LoadLAMMPSResTxt(filename):
    # load data
    with open(filename, 'r') as lmps_file:
        lmps_data = lmps_file.readlines()

    # print(lmps_data)

    # create new array
    lmps_table = np.empty((len(lmps_data)-1, 2))
    for i in range(1,len(lmps_data)):
        before, sep, after = lmps_data[i].partition('\t')
        lmps_table[i-1, 0] = before
        before, sep, after = after.partition('\n')
        lmps_table[i-1, 1] = before
    return lmps_table

# Loading all results
Var1_HEA_II_therm_exp = LoadLAMMPSResTxt('./LargeHEA/Var1_HEA_II_Res.txt')
Var2_HEA_II_therm_exp = LoadLAMMPSResTxt('./LargeHEA/Var2_HEA_II_Res.txt')

# Using custom style
plt.style.use("/home/sez26/TIGP-IIP/Learning/my_style.mplstyle")

plt.plot(Var1_HEA_II_therm_exp[:,0], Var1_HEA_II_therm_exp[:,1])
plt.plot(Var2_HEA_II_therm_exp[:,0], Var2_HEA_II_therm_exp[:,1])

plt.title('Thermal expansion of HEA')
plt.xlabel('Temperature (K)')
plt.ylabel('Strain')
plt.grid(True)
legend_text = ['Var1', 'Var2']
plt.legend(legend_text)

# Calculating thermal expansion coefficient
coefficients_I = np.polyfit(Var1_HEA_II_therm_exp[:,0], Var1_HEA_II_therm_exp[:,1], 1)  # 1 means linear fit
m_I, c_I = coefficients_I
coefficients_II = np.polyfit(Var2_HEA_II_therm_exp[:,0], Var2_HEA_II_therm_exp[:,1], 1)  # 1 means linear fit
m_II, c_II = coefficients_II

# Add text annotation
text_x = 800
text_y = 0
text_y = 0
# unicode stuff
alpha = '\u03B1'
# subscripts
sub_i = '\u1D62'
label_text = f"""
{alpha}{sub_i}={m_I:.3e}
{alpha}{sub_i}{sub_i}={m_II:.3e}
"""
plt.text(text_x, text_y, label_text, fontsize=12)

# save figure

plt.savefig('./LargeHEA/results_fig.png', format = 'png')

plt.show()

