### script to post process data
# plot strain against temperature
# calculate thermal expansion coeffecient

import numpy as np
import matplotlib.pyplot as plt

DirPath = './HEA_compression/LMP_Files/Var2/'

def LoadLAMMPSResTxt(filename, dim):
    # load data
    with open(filename, 'r') as lmps_file:
        lmps_data = lmps_file.readlines()

    # print(lmps_data)

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
    # create new nested list for titles
    titles = [None] * columns
    before, sep, after = lmps_data[0].partition('  ')
    titles[0] = before
    for j in range(1,columns-1):
        before, sep, after = after.partition('  ')
        titles[j] = before
    before, sep, after = after.partition('  \n')
    titles[-1] = before
    # print(titles)
    return lmps_table, titles

# Loading all results
FilePathArr = ['100/SS_Curve_100.txt', '110/SS_Curve_110.txt', '111/SS_Curve_111.txt']
Figure_Titles = ['SS_curve_100', 'SS_curve_110', 'SS_curve_111']
numfile = 3
res_rows = 22
res_columns = 4

Res_Read = np.empty((numfile, res_rows-1, res_columns)) # minus one to remove title rows
Res_Col_Titles = titles = [None] * numfile
for i in range(0, numfile):
    FilePath = DirPath + FilePathArr[i]
    Res_Read[i, :, :], Res_Col_Titles[i] = LoadLAMMPSResTxt(FilePath, [res_rows, res_columns])

# getting Young's modulus (gradient)
m = np.empty((numfile, 1, res_columns-1))
c = np.empty((numfile, 1, res_columns-1))
print(m.shape)
for i in range(0, numfile):
    for j in range(1,numfile):
        m[i,0,j-1], c[i,0,j-1] = np.polyfit(Res_Read[i, :, 0], Res_Read[i,:,j], 1)  # 1 means linear fit

print('m: ',m)
print('c: ',c)

# Create a figure with a numfilex1 grid of subplots
fig, axs = plt.subplots(numfile, 1, figsize=(10, 8), gridspec_kw={'wspace': 0.5, 'hspace': 0.5})

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

# literature values
lit_val_HEA_E = np.array([96, 92, 92]) # GPa
# uncertainty values (+/- xGPa)
lit_val_HEA_Eu = np.array([1, 3, 2])


# for stress x only
for i in range(0, numfile):
    axs[i].plot(Res_Read[i, :, 0], Res_Read[i, :, 1])
    # plot literature values
    axs[i].plot(Res_Read[i, :, 0], Res_Read[i, :, 0]*lit_val_HEA_E[i],'r')
    # add shaded uncertainty region
    axs[i].fill_between(Res_Read[i, :, 0], Res_Read[i, :, 0]*(lit_val_HEA_E[i] - lit_val_HEA_Eu[i]), Res_Read[i, :, 0]*(lit_val_HEA_E[i] + lit_val_HEA_Eu[i]), color = 'r', alpha=0.2)
    # figure titles and axes labels
    axs[i].set_title(Figure_Titles[i])
    axs[i].set_xlabel('Strain')
    axs[i].set_ylabel('Stress')
    axs[i].legend(['Modelled', 'Literature'])
    # adding Young's Mod annotation
    label_text = f"""
    E_x={m[i,0,0]:.3e}
    """
    axs[i].text(text_x, text_y, label_text, fontsize=12)


# save figure

plt.savefig(DirPath + 'results_Var2_Eu.png', format = 'png')

plt.show()

