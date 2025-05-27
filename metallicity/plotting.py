import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import patches

px = 1/plt.rcParams['figure.dpi']

def plotparams():
    '''
    Holds plot parameters for legibility.
    '''

    plt.rcParams.keys()
    plt.rc('font', family='serif')
    params = {
    'axes.labelsize': 30,
    'axes.linewidth': 1.5,
    'legend.fontsize': 25,
    'legend.frameon': False,
    'lines.linewidth': 2,
    'xtick.direction': 'in',
    'xtick.labelsize': 20,
    'xtick.major.bottom': True,
    'xtick.major.pad': 10,
    'xtick.major.size': 10,
    'xtick.major.width': 1,
    'xtick.minor.bottom': True,
    'xtick.minor.pad': 3.5,
    'xtick.minor.size': 5,
    'xtick.minor.top': True,
    'xtick.minor.visible': True,
    'xtick.minor.width': 1,
    'xtick.top': True,
    'ytick.direction': 'in',
    'ytick.labelsize': 20,
    'ytick.major.pad': 10,
    'ytick.major.size': 10,
    'ytick.major.width': 1,
    'ytick.minor.pad': 3.5,
    'ytick.minor.size': 5,
    'ytick.minor.visible': True,
    'ytick.minor.width': 1,
    'ytick.right': True,
    'figure.figsize': [10,10], # instead of 4.5, 4.5
    'savefig.format': 'eps',
    }
    plt.rcParams.update(params)

def boxplotdf(df, x, y, hue, xorder, hueorder, palette, title, show=True, figsize=(800*px,1600*px), notch=False):
    '''
    Creates boxplot.
    '''

    plt.figure(figsize=figsize)
    ax = sns.boxplot(data=df, x=x, y=y, orient='v', order=xorder, hue=hue, 
                hue_order=hueorder, palette=palette, notch=notch)
    
    plt.title(title, fontsize=18)

    if show == True:
        plt.show()

    return ax

def addboxcounts(ax, bincounts, size='x-small', color='w'):
    plots = [obj.get_path().get_extents().bounds for obj in ax.get_children() if type(obj) == patches.PathPatch]
    counts = bincounts['counts']
    for plot, count in zip(plots, counts):
        ax.text(x=plot[0], y=plot[1] + 3 * plot[3] / 4, s=count, size=size, color=color)

    return None

def histogram(csv, x, hue=None, title=None, nbins='auto', figsize=(16,8), binrange=None):
    df = pd.read_csv(csv)

    plt.figure(figsize=figsize)
    ax = sns.histplot(data=df, x=x, hue=hue, bins=nbins, binrange=binrange)
    ax.set_title(title, fontsize=18)
    ax.minorticks_on()
    ax.grid()

    bins = np.histogram(df[x], bins=nbins, range=binrange)
    return ax, bins

def addhistcounts(ax, bincounts, size='small', color='w'):
    rects = [obj for obj in ax.get_children() if type (obj) == patches.Rectangle]
    for box, count in zip(rects, bincounts):
        ax.text(box.get_x() + box.get_width() / 4 ,box.get_y() + 3 * box.get_height() / 4, count)

    return None

def scatterplot(df, x, y, hue, hueorder, title, palette, show=False, figsize=(10,5)):
    plt.figure(figsize=figsize)
    ax = sns.scatterplot(data=df, x=x, y=y, hue=hue, hue_order=hueorder, size=3, palette=palette, alpha=0.5)
    ax.set_title(title, fontsize=18)

    if show == True:
        plt.show()

    return ax

def manyscatterplots():
    pass