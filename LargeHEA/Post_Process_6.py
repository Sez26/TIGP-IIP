### script to post process data
# plot density against time step
# verify that density value settles

import numpy as np
import matplotlib.pyplot as plt
import statistics

DirPath = '/home/sez26/TIGP-IIP/LargeHEA/'

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
FilePathArr = ['Var1_HEA_II_NPT.txt', 'Var2_HEA_II_NPT.txt']
numfile = 2
res_rows = 1002
res_columns = 8

Res_Read = np.empty((numfile, res_rows-1, res_columns)) # minus one to remove title rows
Res_Col_Titles = titles = [None] * numfile
for i in range(0, numfile):
    FilePath = DirPath + FilePathArr[i]
    Res_Read[i, :, :] = LoadLAMMPSResTxt(FilePath, [res_rows, res_columns])

# average last ~200 results to get settled density value
Density = np.empty((numfile, 1))
for i in range(0, numfile):
    Density[i] = statistics.mean(Res_Read[i,800:,4])

# Using custom style
plt.style.use("/home/sez26/TIGP-IIP/Learning/my_style.mplstyle")

# Create a figure with a numfilex1 grid of subplots
# fig, axs = plt.subplots(1, 1, figsize=(10, 8), gridspec_kw={'wspace': 0.5, 'hspace': 0.5})

# looping the plotting
text_x = 0.015
text_y = 0.2
# subscripts
# for i in range(0, numfile):
#     axs[i].plot(Res_Read[i, :, 0], Res_Read[i, :, 1:])
#     axs[i].legend(Res_Col_Titles[i][1:])
#     # figure titles and axes labels
#     axs[i].set_title(Figure_Titles[i])
#     axs[i].set_xlabel('Strain')
#     axs[i].set_ylabel('Stress')
#     # adding Young's Mod annotation
#     label_text = f"""
#     E_x={m[i,0,0]:.3e}
#     E_y={m[i,0,1]:.3e}
#     E_z={m[i,0,2]:.3e}
#     """
#     axs[i].text(text_x, text_y, label_text, fontsize=12)

# # literature values
# lit_val_HEA_E = np.array([96, 92, 92]) # GPa
# # uncertainty values (+/- xGPa)
# lit_val_HEA_Eu = np.array([1, 3, 2])


# for temperature only
# temperature
# for i in range(0,numfile):
#     axs[0].plot(Res_Read[i, :, 0], Res_Read[i, :, 1], 'o-')
# axs[0].set_xlabel('Simulation step')
# axs[0].set_ylabel('Temperature')
# axs[0].legend(['HEA_II', 'HEA_II', 'HEA_III'])

# for temperature only
# temperature
for i in range(0,numfile):
    plt.plot(Res_Read[i, :, 0], Res_Read[i, :, 4], 'o-')
plt.xlabel('Simulation step')
plt.ylabel('Density')
plt.legend([f"Var1, density={Density[0]}", f"Var2, density={Density[1]}"], loc = 'upper right')
# # adding Young's Mod annotation
# label_text = f"""
# E_x={m[i,0,0]:.3e}
# """
# axs[i].text(text_x, text_y, label_text, fontsize=12)

# save figure

plt.savefig(DirPath + 'results_npt_denonly.png', format = 'png')

plt.show()