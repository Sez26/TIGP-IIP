### script to post process data
# plot strain against temperature
# calculate thermal expansion coeffecient

import numpy as np
import matplotlib.pyplot as plt

DirPath = './HEA_compression/LMP_Files/'

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

    print(lmps_table)
    # create new nested list for titles
    titles = [None] * columns
    before, sep, after = lmps_data[0].partition('  ')
    titles[0] = before
    for j in range(1,columns-1):
        before, sep, after = after.partition('  ')
        titles[j] = before
    before, sep, after = after.partition('  \n')
    titles[-1] = before
    print(titles)
    return lmps_table, titles

# Loading all results
FilePathArr = ['100/SS_curve_100.txt', '110/SS_curve_110.txt', '111/SS_curve_111.txt']
numfile = 3
res_rows = 22
res_columns = 4

Res_Read = np.empty((numfile, res_rows-1, res_columns)) # minus one to remove title rows
Res_Col_Titles = titles = [None] * numfile
for i in range(0, numfile):
    FilePath = DirPath + FilePathArr[i]
    Res_Read[i, :, :], Res_Col_Titles[i] = LoadLAMMPSResTxt(FilePath, [res_rows, res_columns])

# Create a figure with a numfilex1 grid of subplots
fig, axs = plt.subplots(numfile, 1, figsize=(10, 8))

# looping the plotting
for i in range(0, numfile):
    axs[i].plot(Res_Read[i, :, 0], Res_Read[i, :, 1:-1])
    axs[i].legend(Res_Col_Titles[i+1:-1][:])

# plt.title('Thermal expansion of HEA')
# plt.xlabel('Temperature (K)')
# plt.ylabel('Strain')
# plt.grid(True)
# legend_text = ['HEA I', 'HEA II', 'HEA_III']
# plt.legend(legend_text)

# Add text annotation
# text_x = 800
# text_y = 0
# text_y = 0
# # unicode stuff
# alpha = '\u03B1'
# # subscripts
# sub_i = '\u1D62'
# label_text = f"""
# {alpha}{sub_i}={m_I:.3e}
# {alpha}{sub_i}{sub_i}={m_II:.3e}
# {alpha}{sub_i}{sub_i}{sub_i}={m_III:.3e}
# """
# plt.text(text_x, text_y, label_text, fontsize=12)

# save figure

# plt.savefig('./HEA/Therm_Exp_Res/results_fig.png', format = 'png')

plt.show()

