import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dfonefold = pd.read_pickle(r"C:\Users\me424\Documents\nanopore\stExp23_06_07\01111_ecds\ints.pkl").dropna(axis='rows',subset = 'event_num')
dfthreefold = pd.read_pickle(r"C:\Users\me424\Documents\nanopore\stExp23_06_07\00111_ecds\ints.pkl").dropna(axis='rows',subset = 'event_num')

for i in set(dfonefold["event_num"]):
    subDf = dfonefold.query("event_num == @i")
    num = len(subDf)
    if num != 4:
        print(f"Dropping event {i}")
        dfonefold = pd.concat([dfonefold, subDf]).drop_duplicates(keep=False)

for i in set(dfthreefold["event_num"]):
    subDf = dfthreefold.query("event_num == @i")
    num = len(subDf)
    if num != 4:
        print(f"Dropping event {i}")
        dfthreefold = pd.concat([dfthreefold, subDf]).drop_duplicates(keep=False)

print(dfonefold[dfonefold.index.get_level_values('Integral Number') == 0])
print(np.array(dfonefold[dfonefold.index.get_level_values('Integral Number') == 0].Integral))

fig, ax = plt.subplots()
ax.boxplot([np.array(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 0].Integral),
            np.array(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 1].Integral),
            np.array(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 2].Integral),
            np.array(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 3].Integral)])

fig1, ax1 = plt.subplots()
ax1.violinplot([np.array(dfonefold[dfonefold.index.get_level_values('Integral Number') == 0].Integral.astype(float)),
            np.array(dfonefold[dfonefold.index.get_level_values('Integral Number') == 1].Integral.astype(float)),
            np.array(dfonefold[dfonefold.index.get_level_values('Integral Number') == 2].Integral.astype(float)),
            np.array(dfonefold[dfonefold.index.get_level_values('Integral Number') == 3].Integral.astype(float))],[1,4,7,10])
ax1.violinplot([np.array(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 0].Integral.astype(float)),
            np.array(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 1].Integral.astype(float)),
            np.array(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 2].Integral.astype(float)),
            np.array(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 3].Integral.astype(float))],[2,5,8,11])
ax1.set_xticks([1,2,4,5,7,8,10,11])
ax1.set_xticklabels(["1x,1OH", "3x,1OH","1x,2OH", "3x,2OH", "1x,4OH", "3x,4OH", "1x,6OH", "3x,6OH"])
ax1.set_ylabel("e.c.d")
            

plt.show()

stds = [np.std(dfonefold[dfonefold.index.get_level_values('Integral Number') == 0].Integral.astype(float)),
        np.std(dfonefold[dfonefold.index.get_level_values('Integral Number') == 1].Integral.astype(float)),
        np.std(dfonefold[dfonefold.index.get_level_values('Integral Number') == 2].Integral.astype(float)),
        np.std(dfonefold[dfonefold.index.get_level_values('Integral Number') == 3].Integral.astype(float)),
        np.std(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 0].Integral.astype(float)),
        np.std(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 1].Integral.astype(float)),
        np.std(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 2].Integral.astype(float)),
        np.std(dfthreefold[dfthreefold.index.get_level_values('Integral Number') == 3].Integral.astype(float))
        ]
print(stds)


