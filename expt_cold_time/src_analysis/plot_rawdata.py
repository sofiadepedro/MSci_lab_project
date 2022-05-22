# %%
import pandas as pd
import matplotlib.pyplot as plt
from globals import(
    conditions,
    part_to_use,
)
from local_functions import(
    universalMakeUp,
    textMakeUp
)
import numpy as np
import statistics

# %%
path_figures = "/Users/sofia/Documents/masters_project/expt_cold_time/globalfigures"

sdt_df = pd.read_csv("../data/raw_data.csv")

correctTrials_data = {}
mean_correct_data = {}
hits_data = {}
falseAlarm_data = {}
misses_data = {}
correctRejec_data = {}
hitRate_data = {}
falseRate_data = {}
print(sdt_df)

# %% 
## PLOTS
lwd = 10
pad_size = 20
lenD = 15
mc = "black"
lateral_wiggle = 0.2

textMakeUp(mc)

x_axis = [0, 1, 2, 3, 4]

# %%
## PARTICIPANTS
part_list = []
for i in part_to_use:
    part_list.append(part_to_use[i]["name"])


# %%
counter = 0

while counter < len(part_list):
    for i in range(0, 5):
        correctTrials_data[f"correctTrials-{conditions[i]['name']}"] = sdt_df[f"correctTrials-{conditions[i]['name']}"]
        mean_correct_data[f"correctTrials-{conditions[i]['name']}"] = sdt_df[f"correctTrials-{conditions[i]['name']}"].mean()
        hits_data[f"hits-{conditions[i]['name']}"] = sdt_df[f"hits-{conditions[i]['name']}"]
        falseAlarm_data[f"falseAlarm-{conditions[i]['name']}"] = sdt_df[f"falseAlarm-{conditions[i]['name']}"]
        misses_data[f"misses-{conditions[i]['name']}"] = sdt_df[f"misses-{conditions[i]['name']}"]
        correctRejec_data[f"correctRejec-{conditions[i]['name']}"] = sdt_df[f"correctRejec-{conditions[i]['name']}"]
        hitRate_data[f"misses-{conditions[i]['name']}"] = sdt_df[f"hitRate-{conditions[i]['name']}"]
        falseRate_data[f"correctRejec-{conditions[i]['name']}"] = sdt_df[f"falseRate-{conditions[i]['name']}"]


    counter += 1

# %%
#PLOT CORRECT TRIALS
figure_name = f"Correct trials"

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(mean_correct_data.values()), color='blue', linewidth='5')
ax.plot(list(correctTrials_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("Percentage of correct trials")
plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)

# %%
#PLOT HITS
figure_name = f"Hits"

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(hits_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("Hits")

plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)

# %%
#PLOT FALSE ALARM 
figure_name = f"False Alarm"

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(falseAlarm_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("False Alarm")

# %%
#PLOT MISSES

figure_name = f"Misses"

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(misses_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("Misses")

plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)

# %%
#PLOT CORRECT REJECTIONS
figure_name = f"Correct rejections"

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(correctRejec_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("Correct Rejections")

plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)

# %%
#PLOT HIT RATE
figure_name = f"Hit Rate"

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(hitRate_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("Hit Rate")

plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)

# %%
#PLOT FALSE ALARM RATE
figure_name = f"False Alarm Rate"

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(falseRate_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("False Alarm Rate")

plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)


# %%
figure_name = f"Hit vs False Alarm Rates"

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

plt.bar(0, 1, 3, 4, 6, 7)