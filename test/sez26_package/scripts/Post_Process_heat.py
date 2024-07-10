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
    for i in range(1,len(lmps_data)):
        before, sep, after = lmps_data[i].partition('\t')
        lmps_table[i-1, 0] = before
        before, sep, after = after.partition('\n')
        lmps_table[i-1, 1] = before
    return lmps_table

@click.command()
@click.option('--heat_results', multiple=True)
@click.argument('run_steps', type=click.INT)
@click.argument('wdir', type=click.Path(exists=True, dir_okay=True))
@click.argument('save_directory', type=click.Path(exists=True, dir_okay=True))
def Post_Process_heat(heat_results, run_steps, wdir, save_directory):
    numfile = len(heat_results)
    res_rows = run_steps//100 # this might have to be parameterised
    res_columns = 2
    # Loading all results
    Res_Read = np.empty((numfile, res_rows-1, res_columns)) # minus one to remove title rows
    for i in range(0, numfile):
        FilePath = heat_results[i]
        Res_Read[i, :, :] = LoadLAMMPSResTxt(FilePath)

    # Using custom style
    plt.style.use(wdir+"/my_style.mplstyle")

    for i in range(0, numfile):
        plt.plot(Res_Read[:,0], Res_Read[:,1], linewidth = 3)

    plt.title('Thermal expansion of HEA')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Strain')
    plt.grid(True)
    # legend_text = ['HEA I', 'HEA II', 'HEA III']
    # plt.legend(legend_text)

    # Calculating thermal expansion coefficient
    coefficients = np.empty((numfile, 2))
    for i in range(0, numfile):
        coefficients[i] = np.polyfit(Res_Read[:,0],Res_Read[:,1], 1)  # 1 means linear fit

    # Add text annotation
    text_x = 800
    text_y = 0
    text_y = 0
    # unicode stuff
    alpha = '\u03B1'
    # subscripts
    sub_i = '\u1D62'
    label_text = f"""
    {alpha}{sub_i}={coefficients[0,0]:.3e}
    {alpha}{sub_i}{sub_i}={coefficients[0,1]:.3e}
    """
    plt.text(text_x, text_y, label_text, fontsize=12)

    # save figure

    plt.savefig(save_directory+'/heat_results_fig.png', format = 'png')

# plt.show()

# running function
if __name__ == '__main__':
    Post_Process_heat()
