import os, sys
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import pearsonr
from scipy.stats import gaussian_kde
from misc_funcs import *
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import seaborn as sns;
nodes,intermat = Interaction('sclcnetwork', 'Ising')

DATA = pd.read_excel("run1_edge_perturb.xlsx", index_col = 0)

X = [] #change
Y = [] #del
for row in sorted(DATA.index):
    if row[-3:] == 'del':
        X.append(DATA.loc[row,'JSD'])
    elif row[-6:] == 'change':
        Y.append(DATA.loc[row,'JSD'])

x = np.array(X).astype(float)
y = np.array(Y).astype(float)

xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)
idx = z.argsort()
x, y, z = x[idx], y[idx], z[idx]

# Make the plot
plt.scatter(x, y,c='r',s=17)
#plt.colorbar()
sns.set_context("paper", font_scale=1.5)
plt.xlabel("Change of Sign of Edge (JSD)")
plt.ylabel("Deletion of Edge (JSD)")
plt.savefig("edge_perturb_out.png",bbox_inches='tight')
plt.close()

xless = x[x<0.09]
yless = y[y<0.09]
plt.scatter(xless, yless,s=7)
# # plt.ylim((0.0,0.0102))
# # plt.xlim((0.0,0.008))
# plt.show()
corre_less = pearsonr(xless,yless)
r2_less = r2_score(yless,xless)
print(corre_less,'\n',r2_less)

corre = pearsonr(x,y)
r2 = r2_score(y,x)
print(corre,'\n',r2)
# df = {'X':x, 'Y':y}
# df= pd.DataFrame(data = df)

# g = sns.lmplot(data = df,x='X',y='Y')
# plt.show()
