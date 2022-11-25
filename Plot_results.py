import copy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


files = ['./endrunresults Random + Moms.csv', './endrunresults_DLCS.csv','./endrunresults_DLIS.csv']
ranmoms = pd.read_csv('./endrunresults Random + Moms.csv', sep = ',',header = None)
dlcs = pd.read_csv('./endrunresults_DLCS.csv', sep = ',',header = None)
dlis = pd.read_csv('./endrunresults_DLIS.csv', sep = ',',header = None)

cols = ranmoms.iloc[0,:]

for file in [ranmoms,dlcs,dlis]:
    file.columns = cols

df = pd.concat([ranmoms,dlcs,dlis])

df = df[df.heuristic != 'JW']
rem = df[df.Result == 'False']
df = df[df.Result == 'True']
df.time = df.time.apply(lambda x: float(x))
df.n_backtracks = df.n_backtracks.apply(lambda x: int(x))


def scatter(data):
    fig, ax = plt.subplots(2,2)
    cor_ran = round(np.corrcoef(data.n_backtracks[data.heuristic == 'random'], data.time[data.heuristic == 'random'])[0][1], 2)
    title_ran = 'Random splitting, r = '
    title_ran = title_ran + str(cor_ran)
    ax[0, 0].scatter(data.n_backtracks[data.heuristic == 'random'], data.time[data.heuristic == 'random'], c = 'b')
    ax[0, 0].set_title(title_ran, fontsize = 12)
    ax[0, 0].set_xlabel('N backtracks', fontsize = 8)
    ax[0, 0].set_ylabel('Runtime in seconds', fontsize = 8)
    b, m = np.polyfit(data.n_backtracks[data.heuristic == 'random'], data.time[data.heuristic == 'random'], 1)
    ax[0, 0].plot(data.n_backtracks[data.heuristic == 'random'], b + m * data.n_backtracks[data.heuristic == 'random'], '-')

    cor_mom = round(np.corrcoef(data.n_backtracks[data.heuristic == 'MOMs'], data.time[data.heuristic == 'MOMs'])[0][1], 2)
    title_mom = 'Random splitting, r = '
    title_mom = title_mom + str(cor_mom)
    ax[0, 1].scatter(data.n_backtracks[data.heuristic == 'MOMs'], data.time[data.heuristic == 'MOMs'], c='r')
    ax[0, 1].set_title(title_mom, fontsize = 12)
    ax[0, 1].set_xlabel('N backtracks', fontsize = 8)
    ax[0, 1].set_ylabel('Runtime in seconds', fontsize = 8)

    cor_dlcs = round(np.corrcoef(data.n_backtracks[data.heuristic == 'DLCS'], data.time[data.heuristic == 'DLCS'])[0][1], 2)
    title_dlcs = 'Random splitting, r = '
    title_dlcs = title_dlcs + str(cor_dlcs)
    ax[1, 0].scatter(data.n_backtracks[data.heuristic == 'DLCS'], data.time[data.heuristic == 'DLCS'], c='g')
    ax[1, 0].set_title(title_dlcs, fontsize = 12)
    ax[1, 0].set_xlabel('N backtracks', fontsize = 8)
    ax[1, 0].set_ylabel('Runtime in seconds', fontsize = 8)

    cor_dlis = round(np.corrcoef(data.n_backtracks[data.heuristic == 'DLIS'], data.time[data.heuristic == 'DLIS'])[0][1], 2)
    title_dlis = 'Random splitting, r = '
    title_dlis = title_dlis + str(cor_dlis)
    ax[1, 1].scatter(data.n_backtracks[data.heuristic == 'DLIS'], data.time[data.heuristic == 'DLIS'], c='y')
    ax[1, 1].set_title(title_dlis, fontsize = 12)
    ax[1, 1].set_xlabel('N backtracks', fontsize = 8)
    ax[1, 1].set_ylabel('Runtime in seconds', fontsize = 8)

    fig.tight_layout()
    plt.show()

scatter(df)

'''
plt.hist(df.n_backtracks, bins=15)
plt.title('Amount of backtracks for DLCS')
plt.xlabel('Amount of backtracks')
plt.ylabel('Frequency')


ran = data[data.heuristic == 'random'].n_backtracks
mom = data[data.heuristic == 'MOMS'].n_backtracks
#jw = data[data.heuristic == 'JW'].n_backtracks
dlcs = data[data.heuristic == 'DLCS'].n_backtracks
dlis = data[data.heuristic == 'DLIS'].n_backtracks
'''

def boxplot_backtracks(data):
    ran = data[data.heuristic == 'random'].n_backtracks
    mom = data[data.heuristic == 'MOMs'].n_backtracks
    '''
    jw = data[data.heuristic == 'JW'].n_backtracks
    dlcs = data[data.heuristic == 'DLCS'].n_backtracks
    dlis = data[data.heuristic == 'DLIS'].n_backtracks
    '''
    res = [ran, mom]
    plt.boxplot(res)
    plt.xticks([1, 2], ['Random', 'MOMs'])
    plt.xlabel('Heuristic')
    plt.ylabel('N backtracks')
    #plt.ylim(bottom = 0)
    plt.yscale('log')
    plt.title('Boxplot of the amount of backtracks per heuristic')


def boxplot_runtime(data):
    ran = data[data.heuristic == 'random'].time
    mom = data[data.heuristic == 'MOMs'].time
    '''
    jw = data[data.heuristic == 'JW'].time
    dlcs = data[data.heuristic == 'DLCS'].time
    dlis = data[data.heuristic == 'DLIS'].time
    '''
    res = [ran, mom]
    plt.boxplot(res)
    plt.xticks([1, 2], ['Random', 'MOMs'])
    plt.xlabel('Heuristic')
    plt.ylabel('Runtime')
    #plt.ylim(bottom=0)
    plt.title('Boxplot of the runtime per heuristic')
    plt.yscale('log')

#boxplot_backtracks(data)

'''
plt.scatter(data.n_backtracks, data.time)
plt.xlabel('backtracks')
plt.ylabel('runtime')
'''
