import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./results_all_heuristics/results_17:47:42_all_heuristics.csv')

ran = data[data.heuristic == 'random'].n_backtracks
mom = data[data.heuristic == 'MOMS'].n_backtracks
jw = data[data.heuristic == 'JW'].n_backtracks
dlcs = data[data.heuristic == 'DLCS'].n_backtracks
dlis = data[data.heuristic == 'DLIS'].n_backtracks


def boxplot_backtracks(data):
    ran = data[data.heuristic == 'random'].n_backtracks
    mom = data[data.heuristic == 'MOMS'].n_backtracks
    jw = data[data.heuristic == 'JW'].n_backtracks
    dlcs = data[data.heuristic == 'DLCS'].n_backtracks
    dlis = data[data.heuristic == 'DLIS'].n_backtracks

    res = [ran, mom, jw, dlcs, dlis]
    plt.boxplot(res)
    plt.xticks([1, 2, 3, 4, 5], ['Random', 'MOMs', 'JW','DLCS','DLIS'])
    plt.xlabel('Heuristic')
    plt.ylabel('N backtracks')
    plt.ylim(bottom = 0)
    plt.title('Boxplot of the amount of backtracks per heuristic')


def boxplot_runtime(data):
    ran = data[data.heuristic == 'random'].time
    mom = data[data.heuristic == 'MOMS'].time
    jw = data[data.heuristic == 'JW'].time
    dlcs = data[data.heuristic == 'DLCS'].time
    dlis = data[data.heuristic == 'DLIS'].time

    res = [ran, mom, jw, dlcs, dlis]
    plt.boxplot(res)
    plt.xticks([1, 2, 3, 4, 5], ['Random', 'MOMs', 'JW', 'DLCS', 'DLIS'])
    plt.xlabel('Heuristic')
    plt.ylabel('Runtime')
    plt.ylim(bottom=0)
    plt.title('Boxplot of the runtime per heuristic')





