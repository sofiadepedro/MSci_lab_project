# %%
# IMPORT LIBRARIES
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics

from saving_data import(
    buildDict,
)
from local_functions import (
    universalMakeUp,
    getSuccData,
    get_linregression,
    plot_alldata,
    plot_linregression,
    getThreshold,
)

# %%
test_state = "test"
todaydate = "16122021_2"

subj = test_state + "_" + todaydate

# SAVING DATA
data_linreg = buildDict(
    "subject",
    "slope_touch",
    "slope_notouch",
    "intercept_touch",
    "intercept_notouch",
    "threshold",
    "perceived_threshold_intensity",
)

llaves = data_linreg.keys()

path = '/Users/sofia/Documents/masters_project/expt12_cold_scale/data'
filepath = os.path.join(path, 'linreg_file.csv')
if not os.path.exists(path):
    os.makedirs(path)
if not os.path.exists(filepath):
    file = open(filepath, "a")
    file_writer = csv.writer(file)
    file_writer.writerow(llaves)

data_linreg["subject"] = subj

# GETTING THE DATA
scaling_df_succ = getSuccData(test_state=test_state, subj=todaydate)
print(scaling_df_succ)

scaling_touch_conds = {
    "notouch": {"color": "#794493", "name": "Cold"},
    "touch": {"color": "#477DBD", "name": "Cold + Touch"},
}


for ind, cond in enumerate(scaling_touch_conds.keys()):
    scaling_touch_conds[cond]["table"] = scaling_df_succ.loc[
        scaling_df_succ["touch"] == ind
    ]
    deltas = scaling_touch_conds[cond]["table"]["delta_stimulation"].unique()
    deltas = np.sort(deltas)
    scaling_touch_conds[cond]["scaling_means"] = []

    for delta in deltas:
        key_delta = f"scaling_delta{delta}"
        scaling_touch_conds[cond][key_delta] = scaling_touch_conds[cond]["table"].loc[
            scaling_touch_conds[cond]["table"]["delta_stimulation"] == delta
        ]

        key_delta_list = f"scaling_delta{delta}_list"
        scaling_touch_conds[cond][key_delta_list] = list(
            scaling_touch_conds[cond][key_delta]["delta_stimulation"]
        )

        key_delta_response_list = f"scaling_delta{delta}_response_list"
        scaling_touch_conds[cond][key_delta_response_list] = list(
            scaling_touch_conds[cond][key_delta]["response"]
        )

        key_delta_mean = f"scaling_delta{delta}_mean"
        scaling_touch_conds[cond]["scaling_means"].append(
            statistics.mean(scaling_touch_conds[cond][key_delta_response_list])
        )

# %%
# GET LINEAR REGRESSION EQUATION, SLOPE & INTERCEPT
for cond in scaling_touch_conds.keys():
    x = deltas
    y = scaling_touch_conds[cond]["scaling_means"]
    data_linreg[f"slope_{cond}"], data_linreg[f"intercept_{cond}"] = get_linregression(x, y, cond)
    print(f"{cond}_slope is: {data_linreg[f'slope_{cond}']}")
    print(f"{cond}_intercept is: {data_linreg[f'intercept_{cond}']}")


# %%
### PLOT LINEAR REGRESSION ###
path_figures = "../globalfigures"
figure_name = f"linear_fit_{test_state}_{todaydate}"

s_size = 100
s_mean = 400
lwd = 10
pad_size = 20
lenD = 15
mc = "black"
lateral_wiggle = 0.2

plt.rcParams.update(
    {
        "font.size": 40,
        "axes.labelcolor": "{}".format(mc),
        "xtick.color": "{}".format(mc),
        "ytick.color": "{}".format(mc),
        "font.family": "sans-serif",
    }
)

fig, ax = plt.subplots(1, 1, figsize=(20, 15))
# PLOT ALL DATA (Do we want all data in this figure?)
for delta in deltas:
    for cond in scaling_touch_conds.keys():
        x = scaling_touch_conds[cond][f"scaling_delta{delta}_list"]
        y = scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"]
        c = scaling_touch_conds[cond]["color"]

        scaling_data = plot_alldata(x, y, c, lateral_wiggle, s_size)

# PLOT MEAN + LINEAR REGRESSION
for cond in scaling_touch_conds.keys():
    x = deltas
    y = scaling_touch_conds[cond]["scaling_means"]
    c = scaling_touch_conds[cond]["color"]
    label = scaling_touch_conds[cond]["name"]

    linear_func = plot_linregression(x, y, c, s_mean, lwd, label)

plt.legend(frameon=False, loc=2)

universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(deltas)

ax.set_ylim(-10, 110)
ax.set_xlabel("ΔT", labelpad=pad_size)
ax.set_ylabel("Perceived intensity")
ax.set_title("Means of Cold and Cold+Touch", pad=60)

plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)


# %%
#GET PERCEIVED INTENSITY OF THRESHOLD VALUE
data_linreg["threshold"] = getThreshold(test_state=test_state, subj=todaydate)

x = deltas
y = scaling_touch_conds["notouch"]["scaling_means"]

data_linreg["perceived_threshold_intensity"] = np.interp(data_linreg["threshold"], x, y)

print(data_linreg["perceived_threshold_intensity"])

# %%
#SAVING DATA
if os.path.getsize(filepath) == 0:
    file = open(filepath, "a")
    file_writer = csv.writer(file)
    file_writer.writerow(list(data_linreg.values()))
    file.close()

else:
    load_data = pd.read_csv(filepath, delimiter=',')

    df =  pd.DataFrame(load_data)
    print(df)

    if subj not in df.values:
        print("\nThis value does not exists in Dataframe")
        file = open(filepath, "a")
        file_writer = csv.writer(file)
        file_writer.writerow(list(data_linreg.values()))
        file.close()

    else:
        print("\nThis value exists in Dataframe")

        index = df.index
        condition = df["subject"] == subj
        subj_indices = index[condition]
        subj_index= subj_indices.tolist()
        

        for (columnName, columnData) in df.iteritems():
            df.at[subj_index, columnName] = data_linreg[columnName]

        print(df)
        
        df.to_csv(filepath, index= False)
