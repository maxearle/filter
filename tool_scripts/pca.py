from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plot = False

df_fname = r"E:\nanopores\2023_02_20\ch1\pore2\data3\f1.pkl"
root = os.path.dirname(df_fname)
name,ext = os.path.splitext(os.path.basename(df_fname))

df = pd.read_pickle(df_fname)

dfInfToNan = df.replace([np.inf, -np.inf], np.nan, inplace=False)
noNan = dfInfToNan.copy().dropna()
conditionedDf = noNan.iloc[:,1:]
array = conditionedDf.to_numpy()

print(f"All values finite: {np.isfinite(array).all()}")

pca = PCA(n_components = 2)
pca.fit(array)
new = pca.transform(array)

if plot:
    fig, ax = plt.subplots()
    ax.scatter(new[:,0],new[:,1], alpha = 0.1)
    plt.show()

noNan['pc_1'] = new[:,0]
noNan['pc_2'] = new[:,1]

noNan.to_pickle(os.path.join(root,f"{name}_PCA.pkl"))

names = list(conditionedDf.columns)
pc1 = dict(zip(names,pca.components_[0]))
pc2 = dict(zip(names,pca.components_[1]))
print(f"PC1: {pc1}")
print(f"PC2: {pc2}")


