import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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

def writecsv(csv1, csv2, id1, id2, destination):
    '''
    Merges csvs to produce dataframe.
    '''

    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    df1 = df1.loc[df1[id1].isin(df2[id2])]

    df = pd.merge(df1, df2, left_on=id1, right_on=id2, how='inner')
    df.to_csv(destination)

    return

def findunique(csv1, csv2, id1, id2, destination):
    '''
    Compares two csvs and removes common rows based on value of columns
    '''

    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)

    df = df1.loc[~df1[id1].isin(df2[id2])]
    df.to_csv(destination)

    return df

def readcsv(csv, x, hue, xbin, xbinlabel, huebin, huebinlabel):
    '''
    Reads csv and creates bins and subbins for corresponding data columns.
    '''

    df = pd.read_csv(csv)

    xbins = pd.cut(df[x], xbin, labels=xbinlabel, include_lowest=True)
    huebins = pd.cut(df[hue], huebin, labels=huebinlabel, include_lowest=True)

    df = df.drop([x, hue], axis=1)
    df = df.merge(xbins, how='inner', left_index=True, right_index=True)
    df = df.merge(huebins, how='inner', left_index=True, right_index=True)

    return df

def boxplotdf(df, x, y, hue, xorder, hueorder, palette, figsize=(8,16)):
    '''
    Creates boxplot.
    '''

    plt.figure(figsize=figsize)
    ax = sns.boxplot(data=df, x=x, y=y, orient='v', order=xorder, hue=hue, 
                hue_order=hueorder, palette=palette, notch=False)

    return ax

def bprp_to_teff(bprp):
    """
    Calculate photometric Teff from Gaia color (use dereddened color!)
    Args:
        bprp (array): Gaia G_BP colour minus Gaia G_RP colour.
    Returns:
        teffs (array): Photometric effective temperatures.
    """

    coeffs = [8959.8112335205078, -4801.5566310882568, 1931.4756631851196,
            -2445.9980716705322, 2669.0248055458069, -1324.0671020746231,
            301.13205924630165, -25.923997443169355]
    """
    # Jason's updated parameters:
    coeffs = [-416.585, 39780.0, -84190.5, 85203.9, -48225.9, 15598.5,
              -2694.76, 192.865]
    """

    return np.polyval(coeffs[::-1], bprp)

def addteff(csv):
    '''
    Converts bp-rp to teff.
    '''

    df = pd.read_csv(csv)
    teff = pd.Series(bprp_to_teff(df['bp_rp']), name='teff')
    df = pd.merge(df, teff, left_index=True, right_index=True, how='inner')
    df.to_csv(csv)

    return df

def histogram(csv, x, nbins, title, figsize=(16,8)):
    df = pd.read_csv(csv)

    plt.figure(figsize=figsize)
    ax = sns.histplot(data=df, x=x, bins=nbins)
    ax.set_title(title, fontsize=18)
    
    bins = ax.hist(df[x], bins=nbins)
    return ax, bins