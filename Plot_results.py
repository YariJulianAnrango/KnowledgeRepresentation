import copy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

jwos = pd.read_csv('./endrunresultsJWOS.csv', sep = ',')
jwos = jwos[jwos.heuristic == 'JW']
ranmoms = pd.read_csv('./endrunresults Random + Moms.csv', sep = ',',header = None)
dlcs = pd.read_csv('./endrunresults_DLCS.csv', sep = ',',header = None)
dlis = pd.read_csv('./endrunresults_DLIS.csv', sep = ',',header = None)

cols = ranmoms.iloc[0,:]

for file in [ranmoms,dlcs,dlis, jwos]:
    file.columns = cols

df_old = pd.concat([ranmoms,dlcs,dlis])
df_old = df_old[df_old.heuristic != 'JW']
df = pd.concat([df_old, jwos], axis = 0)

rem = df[(df.Result == 'False') | (df.Result == False)]
df = df[(df.Result == 'True') | (df.Result == True)]
df.time = df.time.apply(lambda x: float(x))
df.n_backtracks = df.n_backtracks.apply(lambda x: int(x))
df = df.reset_index(drop = True)

# Get statistics
methods = ['random','MOMs','JW','DLCS','DLIS']
def statistics(df, methods):
    for met in methods:
        n = len(df[df.heuristic == met])
        print(met)
        print('n =',n)
        mean_b = np.mean(df[df.heuristic == met].n_backtracks)
        mean_t = np.mean(df[df.heuristic == met].time)
        print('mean of backtracks is',mean_b)
        print('mean of runtime is',mean_t)
        std_b = np.std(df[df.heuristic == met].n_backtracks)
        std_t = np.std(df[df.heuristic == met].time)
        print('standard deviation of backtracks is',std_b)
        print('standard deviation of runtime is',std_t)
        print()

def scatter(data):
    fig, ax = plt.subplots(2,3)
    cor_ran = round(np.corrcoef(data.n_backtracks[data.heuristic == 'random'], data.time[data.heuristic == 'random'])[0][1], 2)
    title_ran = 'Random splitting, r = '
    title_ran = title_ran + str(cor_ran)
    ax[0, 0].scatter(data.n_backtracks[data.heuristic == 'random'], data.time[data.heuristic == 'random'], c = 'b')
    ax[0, 0].set_title(title_ran, fontsize = 12)
    ax[0, 0].set_xlabel('N backtracks', fontsize = 8)
    ax[0, 0].set_ylabel('Runtime in seconds', fontsize = 8)

    cor_mom = round(np.corrcoef(data.n_backtracks[data.heuristic == 'MOMs'], data.time[data.heuristic == 'MOMs'])[0][1], 2)
    title_mom = 'MOMS heuristic splitting, r = '
    title_mom = title_mom + str(cor_mom)
    ax[0, 1].scatter(data.n_backtracks[data.heuristic == 'MOMs'], data.time[data.heuristic == 'MOMs'], c='r')
    ax[0, 1].set_title(title_mom, fontsize = 12)
    ax[0, 1].set_xlabel('N backtracks', fontsize = 8)
    ax[0, 1].set_ylabel('Runtime in seconds', fontsize = 8)

    cor_dlcs = round(np.corrcoef(data.n_backtracks[data.heuristic == 'DLCS'], data.time[data.heuristic == 'DLCS'])[0][1], 2)
    title_dlcs = 'DLCS heuristic splitting, r = '
    title_dlcs = title_dlcs + str(cor_dlcs)
    ax[1, 0].scatter(data.n_backtracks[data.heuristic == 'DLCS'], data.time[data.heuristic == 'DLCS'], c='g')
    ax[1, 0].set_title(title_dlcs, fontsize = 12)
    ax[1, 0].set_xlabel('N backtracks', fontsize = 8)
    ax[1, 0].set_ylabel('Runtime in seconds', fontsize = 8)

    cor_dlis = round(np.corrcoef(data.n_backtracks[data.heuristic == 'DLIS'], data.time[data.heuristic == 'DLIS'])[0][1], 2)
    title_dlis = 'DLIS heuristic splitting, r = '
    title_dlis = title_dlis + str(cor_dlis)
    ax[1, 1].scatter(data.n_backtracks[data.heuristic == 'DLIS'], data.time[data.heuristic == 'DLIS'], c='y')
    ax[1, 1].set_title(title_dlis, fontsize = 12)
    ax[1, 1].set_xlabel('N backtracks', fontsize = 8)
    ax[1, 1].set_ylabel('Runtime in seconds', fontsize = 8)

    cor_jwos = round(np.corrcoef(data.n_backtracks[data.heuristic == 'JW'], data.time[data.heuristic == 'JW'])[0][1], 2)
    title_jwos = 'JWOS heurstic splitting, r = '
    title_jwos = title_jwos + str(cor_jwos)
    ax[0, 2].scatter(data.n_backtracks[data.heuristic == 'JW'], data.time[data.heuristic == 'JW'], c='orange')
    ax[0, 2].set_title(title_jwos, fontsize=12)
    ax[0, 2].set_xlabel('N backtracks', fontsize=8)
    ax[0, 2].set_ylabel('Runtime in seconds', fontsize=8)

    ax[1,2].axis('off')
    fig.tight_layout()
    plt.show()


def boxplot_backtracks(data):
    ran = data[data.heuristic == 'random'].n_backtracks
    mom = data[data.heuristic == 'MOMs'].n_backtracks
    jw = data[data.heuristic == 'JW'].n_backtracks
    dlcs = data[data.heuristic == 'DLCS'].n_backtracks
    dlis = data[data.heuristic == 'DLIS'].n_backtracks

    res = [ran, mom, dlcs, dlis, jw]
    plt.boxplot(res)
    plt.xticks([1, 2, 3, 4, 5], ['Random', 'MOMS', 'DLCS','DLIS', 'JWOS'])
    plt.xlabel('Splitting method')
    plt.ylabel('N backtracks')
    plt.title('Boxplot of the amount of backtracks per splitting method')


def boxplot_runtime(data):
    ran = data[data.heuristic == 'random'].time
    mom = data[data.heuristic == 'MOMs'].time
    jw = data[data.heuristic == 'JW'].time
    dlcs = data[data.heuristic == 'DLCS'].time
    dlis = data[data.heuristic == 'DLIS'].time
    res = [ran, mom, dlcs, dlis, jw]
    plt.boxplot(res)
    plt.xticks([1, 2, 3, 4, 5], ['Random', 'MOMS', 'DLCS','DLIS', 'JWOS'])
    plt.xlabel('Splitting method')
    plt.ylabel('Runtime in seconds')
    #plt.ylim(bottom=0)
    plt.title('Boxplot of the runtime per splitting method')
    plt.yscale('log')


#boxplot_runtime(df)
#boxplot_backtracks(df)
scatter(df)
#plt.boxplot(df.n_backtracks[df.heuristic == 'DLIS'])
