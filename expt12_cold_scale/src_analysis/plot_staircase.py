# %%
from saving_data import rootToUser, saveIndvVar
from index_funcs import parsing_situation, getSubjNumDec, mkpaths
from failing import errorloc, recoverPickleRick
from staircases import Staircase
import matplotlib.pyplot as plt
from local_functions import universalMakeUp

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

# %%

plotParams()

test_state = "test"
todaydate = "15022022_2"

folder_name = test_state + "_" + todaydate

path_data = f"../data/{folder_name}/data/"

name_staircase_file = "online_back_up_staircases1"
staircase1 = recoverPickleRick(path_data, name_staircase_file)

staircase1.estimateValue()
print(staircase1.estimated_point)
saveIndvVar(path_data, staircase1.estimated_point, "temp_delta")
# staircase1.plotStaircase(
#     f"../data/{folder_name}/figures",
#     "Staircase",
#     "Delta",
#     [0, 3],
# )
# %%
mc = "black"

plt.rcParams.update(
    {
        "font.size": 40,
        "axes.labelcolor": "{}".format(mc),
        "xtick.color": "{}".format(mc),
        "ytick.color": "{}".format(mc),
        "font.family": "sans-serif",
    }
)

lwd = 10
pad_letters = 50
pad_numbers = 20
lenD = 20
s_size = 400

fig, ax = plt.subplots(1, 1, figsize=(30, 20))

ax.scatter(
    [x + 1 for x in staircase1.list_to_plot[1]["trial"]],
    staircase1.list_to_plot[1]["stimulation"],
    color="k",
    s=s_size,
    zorder=10,
    label = "Yes"
)

ax.scatter(
    [x + 1 for x in staircase1.list_to_plot[0]["trial"]],
    staircase1.list_to_plot[0]["stimulation"],
    color="red",
    s=s_size,
    zorder=10,
    label = "No"
)

# ax.plot(
#     list(range(1, len(staircase1.list_stimulations) + 1)),
#     staircase1.list_stimulations,
#     color="k",
#     linewidth=lwd,
#     zorder=5,
# )
# ax.plot(
#     list(range(1, len(staircase1.list_tracked_stimulations) + 1)),
#     staircase1.list_tracked_stimulations,
#     color="g",
#     linewidth=lwd,
#     zorder=5,
# )

ax.axhline(staircase1.estimated_point, color="k", linewidth=lwd, label = "Threshold", alpha = 0.5)

plt.legend(frameon=False, fontsize = 60)

# name = "Staircase"
# ax.set_title(f"{name}", pad=pad_letters)
ax.set_ylim([0, 2])
ax.set_ylabel("Change in Temperature\n(\u0394 T °C)", labelpad=pad_letters, fontsize = 65)
ax.set_xlabel("Trials", labelpad=pad_letters, fontsize = 65)

universalMakeUp(ax, lwd, pad_numbers, lenD)

plt.savefig(f"../data/{folder_name}/figures/staircase.png", transparent=True)

# %%
