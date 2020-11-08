import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

Boolean = pd.read_excel("Boolean_J_vals.xlsx",index_col = 0)
Boolean['mean'] = Boolean.mean(axis = 1)
Boolean['std'] = Boolean.std(axis = 1)

Racipe = pd.read_excel("RACIPE_J_Vals.xlsx",index_col = 0)
Racipe_mean = Racipe.mean(axis = 0)
Racipe_std = Racipe.std(axis = 0)
print(Boolean.loc[0,'mean'])
print(Boolean.loc[0,'std'])
print((241.0-32)/2)
print((162.5-32)/2)
print(np.mean(Boolean.loc[1:,'mean']))

sns.set_context("paper", font_scale=1.5)
with sns.axes_style("white"):
    plt.hist(Boolean['mean'], density=False, bins=50)
    plt.axvline(Boolean.loc[0,'mean'],c='red',ls='--')
    plt.axvline(float(Racipe_mean),c='blue',ls='--')
    plt.axvline((162.5-32)/2,c='black',ls='--') #73160
    plt.axvline((241.0-32)/2,c='green',ls='--') #CCLE
    plt.xlabel('J Metric')
    plt.ylabel('Occurences')
    plt.grid(axis='y', alpha=0.75)
    plt.suptitle("Occurences of Metric values (Discrete to Continuous)")
    plt.savefig("dis_to_conti.png",dpi = 300, bbox_inches = 'tight')
