# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from globals import(
    conditions,
    part_to_use,
)

from plotting import (
    plotParams,
    pad_size_label,
    pad_size_ticks,
    width_lines,
    length_ticks,
    scatter_size,
    nt_color,
    t_color,
    alpha_partici,
    width_participants
)

plotParams()

path_globalfigures = "../globalfigures/"

def plot_pretty(x_label, y_label, number_x_ticks, number_y_ticks):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.yaxis.set_tick_params(width=width_lines, length=length_ticks)
    ax.xaxis.set_tick_params(width=width_lines, length=length_ticks)

    ax.tick_params(axis="y", which="major", pad=10)
    ax.tick_params(axis="x", which="major", pad=10)

    ax.spines["left"].set_linewidth(width_lines)
    ax.spines["bottom"].set_linewidth(width_lines)

    ax.set_ylabel(y_label, labelpad=25)
    ax.set_ylim([number_y_ticks[0], number_y_ticks[-1]])

    ax.set_xlim(-0.35)

    ax.set_xticks(number_x_ticks)
    ax.set_yticks(number_y_ticks)
    labels = [item.get_text() for item in ax.get_xticklabels()]

    for i, dist in enumerate(x_label):
        labels[i] = distance_label[i]

    ax.set_xticklabels(labels)

# %%
sdt_df = pd.read_csv("../data/sdt.csv")
# sdt_df = old_sdt_df.drop(index= [3, 4, 5])

rawsdt_df = pd.read_csv("../data/raw_data.csv")



# %%
### D-PRIME
plot_name = f"d_prime_ianet_plot_skinD"


distance_label = ["No touch", "0-s", "1-s", "2-s", "3-s"]

fig, ax = plt.subplots(1, 1, figsize=(20, 10))

d_prime_data = {}

for i in range(0, 5):
    d_prime_data[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"]

for i in range(0, 5):
    if i == 0:
        new_color = t_color
        scatter_label = "Cold"
        mean_label = "Cold Mean"
    else:
        new_color = nt_color
        scatter_label = "Cold + Touch"
        mean_label = "Cold + Touch Mean"
    ax.scatter(
        np.repeat((i), len(sdt_df[f"d-{conditions[i]['name']}"])),
        sdt_df[f"d-{conditions[i]['name']}"],
        s=scatter_size,
        color=new_color,
        # label = scatter_label, 
        alpha = 0.5
    )

    ax.scatter([i], sdt_df[f"d-{conditions[i]['name']}"].mean(), lw=60, color=new_color, marker = "|", s = 100)
    # label = mean_label


ax.plot(list(d_prime_data.values()), color = "k", alpha = 0.5)

plot_pretty(x_label = distance_label, y_label = "Sensitivity (d')", number_x_ticks = list(range(0, 5)), number_y_ticks = [0, 1, 2, 3, 4])

from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], color=t_color, lw=10),
                Line2D([0], [0], color=nt_color, lw=10),]

ax.legend(custom_lines, ['Cold', 'Cold + Touch'], frameon=False, bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.savefig(f"{path_globalfigures}/{plot_name}.png", transparent=True)





# %%
#PLOT D-PRIME DIFFERENCES 
plot_name = f"difference_d_prime_ianet_plot_skinD"

diff_data = {}

distance_label = ["0-s", "1-s", "2-s", "3-s"]

fig, ax = plt.subplots(1, 1, figsize=(15, 10))

counter = 0
while counter < len(part_to_use):
    for i in range(1, 5):
        diff_data[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"] = sdt_df[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"]

    counter += 1

for i in range(1, 5):
    if i == 0:
        new_color = t_color
    else:
        new_color = nt_color
    ax.scatter(
        np.repeat((i - 1), len(sdt_df[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"])),
        sdt_df[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"],
        s=scatter_size,
        color=new_color,
        alpha = 0.5
    )

    ax.scatter([i - 1], sdt_df[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"].mean(), lw=60, color=new_color, marker = "|", s=100)
plt.axhline(y=0, color='black', linestyle='--')

ax.plot(list(diff_data.values()), color = "k", alpha = 0.5)

plot_pretty(x_label = distance_label, y_label = "[(d')Cold+Touch] - [(d')Cold]", number_x_ticks = list(range(0, 4)), number_y_ticks = [-1, 0, 1, 2])

plt.tight_layout()
plt.savefig(f"{path_globalfigures}/{plot_name}.png", transparent=True)








# %%
### RESPONSE BIAS
plot_name = f"response_bias_ianet_plot_skinD"

c_data = {}

distance_label = ["No touch", "0-s", "1-s", "2-s", "3-s"]

fig, ax = plt.subplots(1, 1, figsize=(20, 10))

for i in range(0, 5):
    c_data[f"c-{conditions[i]['name']}"] = sdt_df[f"c-{conditions[i]['name']}"]

for i in range(0, 5):
    if i == 0:
        new_color = t_color
    else:
        new_color = nt_color
    ax.scatter(
        np.repeat((i), len(sdt_df[f"c-{conditions[i]['name']}"])),
        sdt_df[f"c-{conditions[i]['name']}"],
        s=scatter_size,
        color=new_color,
        alpha=0.5
    )

    ax.scatter([i], sdt_df[f"c-{conditions[i]['name']}"].mean(), lw=50, color=new_color, marker = "|", s=100)

ax.plot(list(c_data.values()), color = "k", alpha = 0.5)
plt.axhline(y=0, color='black', linestyle='--')

custom_lines = [Line2D([0], [0], color=t_color, lw=10),
                Line2D([0], [0], color=nt_color, lw=10),]

ax.legend(custom_lines, ['Cold', 'Cold + Touch'], frameon=False, bbox_to_anchor=(1, 1))

plot_pretty(x_label = distance_label, y_label = "Response bias (c)", number_x_ticks = list(range(0, 5)), number_y_ticks = [-1.5, -1, -0.5, 0, 0.5, 1])

plt.tight_layout()
plt.savefig(f"{path_globalfigures}/{plot_name}.png", transparent=True)





# %%
### CORRECT RESPONSES
plot_name = f"correct_resp_ianet_plot_skinD"

correctTrials_data = {}

distance_label = ["No touch", "0-s", "1-s", "2-s", "3-s"]

fig, ax = plt.subplots(1, 1, figsize=(20, 10))

counter = 0

while counter < len(part_to_use):
    for i in range(0, 5):
        correctTrials_data[f"correctTrials-{conditions[i]['name']}"] = rawsdt_df[f"correctTrials-{conditions[i]['name']}"]
    counter += 1


for i in range(0, 5):
    if i == 0:
        new_color = t_color
    else:
        new_color = nt_color
    ax.scatter(
        np.repeat((i), len(rawsdt_df[f"correctTrials-{conditions[i]['name']}"])),
        rawsdt_df[f"correctTrials-{conditions[i]['name']}"],
        s=scatter_size,
        color=new_color,
        alpha=0.5
    )

    ax.scatter([i], rawsdt_df[f"correctTrials-{conditions[i]['name']}"].mean(), lw=50, color=new_color, marker = "|", s=100)

ax.plot(list(correctTrials_data.values()), color = "k", alpha = 0.5)

custom_lines = [Line2D([0], [0], color=t_color, lw=10),
                Line2D([0], [0], color=nt_color, lw=10),]

ax.legend(custom_lines, ['Cold', 'Cold + Touch'], frameon=False, bbox_to_anchor=(1, 1))

plot_pretty(x_label = distance_label, y_label = "Correct responses", number_x_ticks = list(range(0, 5)), number_y_ticks = [0.5, 0.75, 1])

plt.tight_layout()
plt.savefig(f"{path_globalfigures}/{plot_name}.png", transparent=True)