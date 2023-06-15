import pandas as pd
import h5py as h
import os

#Read in hdf5 and pkl of dataframe containing events for new file
hData = h.File(r"E:\nanopores\2023_06_07\ch2\pore5\data2\EVENTS.hdf5", 'r')
df = pd.read_pickle(r"E:\nanopores\2023_06_07\ch2\pore5\data2\propsE4R1.pkl")
cats = pd.read_pickle(r"C:\Users\me424\Documents\Python\nas\Scripts\nas\filter\filter\tool_scripts\output.hdf5.pkl")

#Define new output file
if os.path.exists(r"C:\Users\me424\Documents\Python\nas\Scripts\nas\filter\filter\tool_scripts\output.hdf5"):
    os.remove(r"C:\Users\me424\Documents\Python\nas\Scripts\nas\filter\filter\tool_scripts\output.hdf5")
hOut = h.File(r"C:\Users\me424\Documents\Python\nas\Scripts\nas\filter\filter\tool_scripts\output.hdf5", 'a')

hOut.create_group("current_data")
hOut["/current_data"].attrs["sample_rate"] = hData["/current_data"].attrs["sample_rate"]

from_props = False
cat_to_save = "00111"

if from_props:
    for name in df.name:
        hData.copy(hData[f"/current_data/{name}"], hOut[f"/current_data"], name)
else:
    for i, cat in enumerate(cats.event_type):
        if cat != cat_to_save:
            continue
        else:
            name = df.iloc[i,:]["name"]
            hData.copy(hData[f"/current_data/{name}"], hOut[f"/current_data"], name)
print(f"Datasets: {len(hOut['current_data'].keys())}")
hData.close()
hOut.close()

    