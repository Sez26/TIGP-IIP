### script to post process data
# plot density against time step
# verify that density value settles

import numpy as np
import matplotlib.pyplot as plt
import statistics

DirPath = '/home/sez26/TIGP-IIP/Automation_Results/Small_3'

def LoadLAMMPSResTxt(filename, dim):
    # load data
    with open(filename, 'r') as lmps_file:
        lmps_data = lmps_file.readlines()

    # print(len(lmps_data))

    # setting dimensions
    [rows, columns] = dim

    # create new array for results
    lmps_table = np.empty((rows-1, columns))
    for i in range(1,rows):
        before, sep, after = lmps_data[i].partition(' ')
        lmps_table[i-1, 0] = before
        for j in range(1,columns-1):
            before, sep, after = after.partition(' ')
            lmps_table[i-1, j] = before
        lmps_table[i-1, -1] = after

    # print(lmps_table)
    # # create new nested list for titles
    # titles = [None] * columns
    # before, sep, after = lmps_data[0].partition('  ')
    # titles[0] = before
    # for j in range(1,columns-1):
    #     before, sep, after = after.partition('  ')
    #     titles[j] = before
    # before, sep, after = after.partition('  \n')
    # titles[-1] = before
    # print(titles)
    return lmps_table

# Loading all results
FilePathArr = ['/var1_npt.txt', '/var2_npt.txt', '/var3_npt.txt', '/var4_npt.txt', '/var5_npt.txt', '/var6_npt.txt', '/var7_npt.txt', '/var8_npt.txt', '/var9_npt.txt', '/var10_npt.txt']
numfile = 10
res_rows = 1002
res_columns = 8

Res_Read = np.empty((numfile, res_rows-1, res_columns)) # minus one to remove title rows
Res_Col_Titles = titles = [None] * numfile
for i in range(0, numfile):
    FilePath = DirPath + FilePathArr[i]
    Res_Read[i, :, :] = LoadLAMMPSResTxt(FilePath, [res_rows, res_columns])

# average last ~200 results to get settled density value
Density = np.empty((numfile, 1))
rho = '\u03C1'
legend_text = []
for i in range(0, numfile):
    Density[i] = statistics.mean(Res_Read[i,800:,4])
    legend_text.append(f'Var{i+1}, {rho} = {Density[i, 0]:.3f}')

# Using custom style
plt.style.use("/home/sez26/TIGP-IIP/Automation_Prep/sez26_package/scripts/post_processing/my_style.mplstyle")

# for temperature only
for i in range(0,numfile):
    plt.plot(Res_Read[i, :, 0], Res_Read[i, :, 4], 'o-')
plt.xlabel('Simulation step')
plt.ylabel('Density')
plt.legend(legend_text)
# # adding Young's Mod annotation
# label_text = f"""
# E_x={m[i,0,0]:.3e}
# """
# axs[i].text(text_x, text_y, label_text, fontsize=12)

# save figure

plt.savefig(DirPath + '/results_npt_denonly.png', format = 'png')

plt.show()

