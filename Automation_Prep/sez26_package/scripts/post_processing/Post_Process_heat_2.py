### script to post process data
# plot strain against temperature
# calculate thermal expansion coeffecient

import numpy as np
import matplotlib.pyplot as plt
import click

def LoadLAMMPSResTxt(filename):
    # load data
    with open(filename, 'r') as lmps_file:
        lmps_data = lmps_file.readlines()

    # print(lmps_data)

    # create new array
    lmps_table = np.empty((len(lmps_data)-1, 2))
    for i in range(1,len(lmps_data)): # skips title line
        before, sep, after = lmps_data[i].partition('    ')
        lmps_table[i-1, 0] = before
        before, sep, after = after.partition('\n')
        lmps_table[i-1, 1] = before
    return lmps_table

# @click.command()
# @click.option('--heat_results', multiple=True)
# @click.argument('run_steps', type=click.INT)
# @click.argument('wdir', type=click.Path(exists=True, dir_okay=True))
# @click.argument('save_directory', type=click.Path(exists=True, dir_okay=True))
def Post_Process_heat(heat_results, heat_loop, wdir, save_directory):
    numfile = len(heat_results)
    res_rows = heat_loop+2 # this might have to be parameterised
    res_columns = 2
    # Loading all results
    Res_Read = np.empty((numfile, res_rows-1, res_columns)) # minus one to remove title rows
    for i in range(0, numfile):
        FilePath = heat_results[i]
        Res_Read[i, :, :] = LoadLAMMPSResTxt(FilePath)

    # Using custom style
    plt.style.use(wdir+"/my_style.mplstyle")
    
    coefficients = np.empty((numfile, 2))
    legend_text = []
    alpha = '\u03B1'
    for i in range(0, numfile):
        plt.plot(Res_Read[i,:,0], Res_Read[i,:,1])
        # Calculating thermal expansion coefficient
        coefficients[i] = np.polyfit(Res_Read[i,:,0],Res_Read[i,:,1], 1)  # 1 means linear fit
        legend_text.append(f'Var{i+1}, {alpha} = {coefficients[i,0]:.3e}')

    plt.title('Thermal expansion of HEA')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Strain')
    plt.grid(True)
    plt.legend(legend_text)

    # save figure

    plt.savefig(save_directory+'/heat_results_fig.png', format = 'png')

    plt.show()

# # running function
# if __name__ == '__main__':
#     Post_Process_heat()

save_dir = '/home/sez26/TIGP-IIP/Automation_Results/Small_3'
heatResults = [save_dir+'/var1_therm_exp.txt', save_dir+'/var2_therm_exp.txt', save_dir+'/var3_therm_exp.txt', save_dir+'/var4_therm_exp.txt', save_dir+'/var5_therm_exp.txt', save_dir+'/var6_therm_exp.txt', save_dir+'/var7_therm_exp.txt', save_dir+'/var8_therm_exp.txt', save_dir+'/var9_therm_exp.txt', save_dir+'/var10_therm_exp.txt']
wDir = '/home/sez26/TIGP-IIP/Automation_Prep/sez26_package/scripts/post_processing'
heatLoop = 14

Post_Process_heat(heatResults, heatLoop, wDir, save_dir)