import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from matplotlib.pyplot import cm

def analysis_data(dataframe):
    
    row_define = str(input('what row is that?: '))
    numb_exp = int(input('how many experiments in one row in triplicate?: '))
    cols_test = input('input colnames separated by a space: ') 
    cols = cols_test.split()
    if len(cols) != numb_exp:
        raise ValueError('number of experiments does not match the number of colnames!')
        
    exp_cols_iter = []
    for i in cols:
        for j in range(3):
            exp_cols_iter.append(i)

    dataframe = dataframe.set_index('Unnamed: 0')
    dataframe = dataframe.dropna()
    dataframe = dataframe.T
    
    for i in dataframe.columns:
        if i != row_define:
            dataframe = dataframe.drop(i, axis=1)
            
    dataframe = dataframe.rename(columns={row_define: "values"})
    dataframe = dataframe.iloc[1:(numb_exp*3)+1] #triplicates
    dataframe['condition'] = exp_cols_iter
    dataframe = dataframe.reset_index(drop=True)
    avg_pos_ctrl = dataframe.loc[3:5, 'values'].mean()
    dataframe['values'] = 100*(dataframe['values']/avg_pos_ctrl)
    
    return dataframe

def plot_figure(arg):
    
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(style="ticks", rc=custom_params)
    plt.figure(figsize=(8,5))
    plot_T = sns.barplot(data=arg, x='condition', y='values', 
                ci='sd', capsize=0.1, errwidth=1.5, linewidth=1.5, edgecolor=".05", color="lightsteelblue")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xticks(rotation=70)
    plt.ylabel('Intensity [%]', fontsize=14)
    plt.xlabel('', fontsize=12)
    # plt.legend(bbox_to_anchor=(1.0, 1), borderaxespad=0, loc='upper left', fontsize='medium')
    plt.savefig('folder', 
           dpi = 500, bbox_inches='tight')
    #palette="Blues"
    plt.show()
