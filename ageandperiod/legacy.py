import pandas as pd

legacy = pd.read_csv('legacyabridged.txt', delimiter='\s+')[['KIC', 'Age']]
mcquillan = pd.read_csv('mcquillanabridged.txt', header=None, delimiter='\s+')[[0,4]]
mcquillan.columns = ['KIC', 'Period']

y = pd.merge(mcquillan, legacy)
print(y)