import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.markers import MarkerStyle
import matplotlib.ticker as mtick
import sys
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

def get_data(file, number, metrix):
    data = pd.read_csv(file)
    target_list = data[metrix]
    return target_list.values[number]

def get_mean_and_std(method, data_name, date, seed_list, metrix, number):
    path  = os.path.join(sys.path[-1], 'exp', method, data_name, date)
    vals = []
    if seed_list == "default":
        f = path + '/result_default.csv'
        vals.append(get_data(f, number, metrix))
    else:
        for i in seed_list:
            f = path + '/result_' + str(i) + '.csv'
            vals.append(get_data(f, number, metrix))
    return np.array(vals).mean(), np.array(vals).std()


def errorbar_plot_rmse(data_name_list, compare_method, date, metrix, seed_list):

    color_dic = {'fides':'#DC143C', 'dmfal':'#2ca02c', 'ifc':'#1f77b4', 'ar':'#ff7f0e', 'resgp':'#0033ff', 'gar':'#708090', 'cigp':'#17becf'}
    marker_dic = {'fides':"o", 'dmfal':"s", 'ifc':"^", 'ar':"v", 'resgp':"P", 'gar':"d", 'cigp':"h"}
    ls_dic = {'fides':'dashed', 'ifc':'solid', 'dmfal':'solid', 'ar':'solid', 'resgp':'solid', 'gar':'solid', 'cigp':'solid'}
    label_dic = {'fides':'Ours', 'dmfal':'MF-BNN', 'ifc':'IFC-GPT', 'ar':'AR', 'resgp':'resGP', 'gar':'fides_withbeta', 'cigp':'DC-I'}
    
    # if metrix == 'rmse' or metrix == 'time':
    #     method = ['dmfal', 'resgp', 'ar', 'fides']
    # else:
    #     method = ['resgp', 'ar', 'fides']
    
    method = compare_method

    for data_name in data_name_list:
        type = metrix
        plt.figure(figsize=(7,6), dpi=100)
        
        
        orders = [16, 32, 64, 128]
        for i in range(len(method)):
            vals = []
            vars = []
            for j in range(len(orders)): # j = 0, 1, 2, 3 -> 32, 64, 96, 128
                # method, data_name, date, seed_list, type, number
                m, s = get_mean_and_std(method[i], data_name, date, seed_list, type, j) # 修改指标
                vals.append(m)
                vars.append(s)

            plt.errorbar(orders, vals, yerr = vars, ls = ls_dic[method[i]], linewidth=3.5, color=color_dic[method[i]], label= label_dic[method[i]], marker=MarkerStyle(marker_dic[method[i]], fillstyle='full'), elinewidth = 3 ,capsize = 13, markersize = 17, alpha = 0.8)

        plt.xlabel("# Training Samples $N^{0}$", fontsize=25)
        if metrix == 'rmse':
            plt.ylabel("RMSE", fontsize = 25)
        elif metrix == 'nll':
            plt.ylabel("NLL", fontsize = 25)
        elif metrix == 'nrmse':
            plt.ylabel("nRMSE", fontsize = 25)

        ax = plt.gca()
        plt.gcf().subplots_adjust(top=0.93,
                                    bottom=0.2,
                                    left=0.18,
                                    right=0.95,
                                    hspace=0.2,
                                    wspace=0.2)

        if data_name == "Poisson_mfGent_v5" or data_name == "maolin6":
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%2d'))
        else:
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))

        plt.xticks(orders)
        plt.tick_params(axis='both', labelsize=25)

        legend_list = ['Heat_mfGent_v5', 'TopOP_mfGent_v6', 'plasmonic2_MF', "borehole", "maolin1"]
        if data_name in legend_list:
                if data_name == 'TopOP_mfGent_v6':
                    pass
                elif data_name == 'plasmonic2_MF':
                    pass
                else:
                    plt.legend(loc='upper right', fontsize=25)
        plt.grid()
        # plt.legend(loc='upper right', fontsize=20)

        folder_path = os.path.join(sys.path[-1], 'graphs', date, 'subset', str(metrix))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        fig_file = os.path.join(folder_path, data_name + '_subset'+ '.eps')
        plt.savefig(fig_file, bbox_inches = 'tight')

if __name__ == '__main__':
    errorbar_plot_rmse(data_name_list = ['toy_data'],
                       compare_method = ['fides'], # ['dmfal', 'resgp', 'ar', 'fides']
                       date = "2023-06-22",
                       metrix = 'rmse',
                       seed_list =  'default') #[1, 2]

        

