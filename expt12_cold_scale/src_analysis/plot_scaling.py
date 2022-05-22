# %%
import pandas as pd
import statistics
import numpy as np
import matplotlib.pyplot as plt
from local_functions import universalMakeUp

# %%

path_data = "../data"
path_figures = "../globalfigures"

test_state = "test"
subj = "16122021_2"
file_name = "data_scaling_subj"

figure_name = f"scaling_{test_state}_{subj}"

scaling_df = pd.read_csv(f"{path_data}/{test_state}_{subj}/data/{file_name}.csv")
print(scaling_df)

# %%
scaling_df_succ = scaling_df.loc[scaling_df["failed"] == False]
print(scaling_df_succ)

# %%
scaling_touch_conds = {
    "notouch": {"color": "#794493", "name": "Cold"},
    "touch": {"color": "#477DBD", "name": "Cold+Touch"},
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
s_size = 300
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
for delta in deltas:
    x = scaling_touch_conds["touch"][f"scaling_delta{delta}_list"]
    y = scaling_touch_conds["touch"][f"scaling_delta{delta}_response_list"]
    ax.scatter(
        np.random.uniform(
            (x[0] - lateral_wiggle), (x[0] + lateral_wiggle), size=len(x)
        ),
        y,
        c=scaling_touch_conds["touch"]["color"],
        alpha=0.5,
        s=s_size,
    )

    x = scaling_touch_conds["notouch"][f"scaling_delta{delta}_list"]
    y = scaling_touch_conds["notouch"][f"scaling_delta{delta}_response_list"]
    ax.scatter(
        np.random.uniform(
            (x[0] - lateral_wiggle), (x[0] + lateral_wiggle), size=len(x)
        ),
        y,
        c=scaling_touch_conds["notouch"]["color"],
        alpha=0.5,
        s=s_size,
    )


for cond in scaling_touch_conds.keys():

    ax.plot(
        deltas,
        scaling_touch_conds[cond]["scaling_means"],
        c=scaling_touch_conds[cond]["color"],
        label=scaling_touch_conds[cond]["name"],
        lw=lwd,
    )


plt.legend(frameon=False)


universalMakeUp(ax, lwd, pad_size, lenD)

ax.set_xticks(deltas)

ax.set_ylim(-10, 110)
ax.set_xlabel("ΔT", labelpad=pad_size)
ax.set_ylabel("Perceived intensity")
ax.set_title("Means of Cold and Cold+Touch", pad=80)

plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)
# %%

# %%
