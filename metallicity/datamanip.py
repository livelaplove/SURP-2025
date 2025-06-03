import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics as stat


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

def readcsv(csv, x = None, xbin = None, xbinlabel = None, hue = None, huebin = None, huebinlabel = None):
    '''
    Reads csv with option for creating bins and subbins based on given intervals
    '''

    df = pd.read_csv(csv)

    if x == None:
        if hue != None:
            huebin = pd.cut(df[hue], huebin, labels=huebinlabel, include_lowest=True)

            df = df.drop(hue, axis=1)
            df = df.merge(huebin, how='inner', left_index=True, right_index=True)
        else:
            pass

        return df
        
    else: 
        xbins = pd.cut(df[x], xbin, labels=xbinlabel, include_lowest=True)
        huebins = pd.cut(df[hue], huebin, labels=huebinlabel, include_lowest=True)

        df = df.drop([x, hue], axis=1)
        df = df.merge(xbins, how='inner', left_index=True, right_index=True)
        df = df.merge(huebins, how='inner', left_index=True, right_index=True)

        return df

def readdf(df, x, hue, xbin, xbinlabel, huebin, huebinlabel):
    '''
    Pandas dataframe version of readcsv.
    '''

    xbins = pd.cut(df[x], xbin, labels=xbinlabel, include_lowest=True)
    huebins = pd.cut(df[hue], huebin, labels=huebinlabel, include_lowest=True)

    df = df.drop([x, hue], axis=1)
    df = df.merge(xbins, how='inner', left_index=True, right_index=True)
    df = df.merge(huebins, how='inner', left_index=True, right_index=True)

    return df

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

def findbincounts(df, bin, subbin=None):
    if subbin != None:
        return df.groupby(by=[subbin, bin]).size().reset_index(name='counts')
    else:
        return df.groupby(by=bin).size().reset_index(name='counts')

def calcvzdisp(df, mhbinlabels, x=None, xbinlabels=None):
    '''
    Finds sample standard deviation of vertical velocity dispersion based on metallicity and/or stellar property bin.
    '''

    mhbins = []
    samplesizes = []
    vzdisps = []
    means = []

    if xbinlabels == None:
        for mhbin in mhbinlabels:
            sample = df.loc[df['mh_xgboost'] == mhbin]
            if len(sample) < 2:
                continue
            else:
                vzdisp = round(stat.stdev(sample['vz']), 3)
                mean = round(stat.mean(sample['Prot']), 3)

                mhbins.append(mhbin)
                samplesizes.append(len(sample))
                vzdisps.append(vzdisp)
                means.append(mean)

        return pd.DataFrame({'mh_xgboost':mhbins, 'samplesize':samplesizes, 'vzdisp':vzdisps, 'meanprot':means})
            
    
    else:
        xbins = []
        for xbin in xbinlabels:
            for mhbin in mhbinlabels:

                sample = df.loc[df['mh_xgboost'] == mhbin]
                sample = sample.loc[df[x] == xbin]
                if len(sample) < 2:
                    continue
                
                else:
                    vzdisp = round(stat.stdev(sample['vz']), 3)
                    mean = round(stat.mean(sample['Prot']), 3)

                    xbins.append(xbin)
                    mhbins.append(mhbin)
                    samplesizes.append(len(sample))
                    vzdisps.append(vzdisp)
                    means.append(mean)

        return pd.DataFrame({x:xbins, 'mh_xgboost':mhbins, 'samplesize':samplesizes, 'vzdisp':vzdisps, 'meanprot':means})

def rescaleperiods(df, x, xbinlabels, mhbinlabels, refmhbin):
    '''
    Rescales periods of stars based on velocity dispersion per metallicity bin. 

    The age of stars that form under similar sconditions can be correlated to the variance in their vertical velocities. 
    Over time, external peturbations alter the motion of the star, changing this variance. Assuming a Skumanich relationship
    between rotation period and age, velocity dispersion and age can be described with a similar relationship such that 
    period and velocity disperion are directly proportional. Generally older stars are more metal poor. 

    Within a temperature bin, mass bin, etc., the roation periods of the more metal poor stars can be adjusted to get conditions of 
    the stars at roughly equal age. This point should be far enough into the lifecycle of a main-sequence star such that the 
    inital conditions have converged. This function places the reference at star sof solar metallicity.
    '''
    pass
