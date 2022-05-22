### BLINDCHECK OF SCALING PER PARTICIPANT 
import os
import numpy as np
import matplotlib.pyplot as plt
import random

from local_functions import (
    universalMakeUp,
    getSuccData,
    plot_alldata,
    plot_linregression,
    getThreshold,
    get_folder_path,
    textMakeUp,
    parseDeltasResponses
)

if __name__ == "__main__":

    path = "/Users/sofia/Documents/masters_project/expt12_cold_scale/data"
    scaling_data = "data_scaling_subj"

    color = ["#794493", "#477DBD"]
    random.shuffle(color)
    c1 = color.pop(0)
    c2 = color.pop(0)

    s_size = 100
    s_mean = 400
    lwd = 10
    pad_size = 20
    lenD = 15
    mc = "black"
    lateral_wiggle = 0.2

    textMakeUp(mc)

    for foldername in os.listdir(path):
        if foldername.startswith("test_"):
            folder_path, todaydate = get_folder_path(foldername)
            subject = "test" + "_" + todaydate

            print(foldername)

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv'):

                
                # GETTING THE DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)
                print(scaling_df_succ)

                scaling_touch_conds = {
                    "notouch": {"color": c1, "name": "Cold"},
                    "touch": {"color": c2, "name": "Cold + Touch"},
                }



                scaling_touch_conds, deltas = parseDeltasResponses(scaling_touch_conds)

                ### PLOT LINEAR REGRESSION ###
                path_figures = "/Users/sofia/Documents/masters_project/expt12_cold_scale/globalfigures"
                figure_name = f"blindcheck_test_{todaydate}"


                
                print("here")

                fig, ax = plt.subplots(1, 1, figsize=(20, 15))
                # PLOT ALL DATA
                for delta in deltas:
                    for cond in scaling_touch_conds.keys():
                        x = scaling_touch_conds[cond][f"scaling_delta{delta}_list"]
                        y = scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"]
                        c = scaling_touch_conds[cond]["color"]

                        plot_alldata(x, y, c, lateral_wiggle, s_size)

                # PLOT MEAN + LINEAR REGRESSION
                for cond in scaling_touch_conds.keys():
                    x = deltas
                    y = scaling_touch_conds[cond]["scaling_means"]
                    c = scaling_touch_conds[cond]["color"]
                    label = scaling_touch_conds[cond]["name"]

                    plot_linregression(x, y, c, s_mean, lwd, label)



                universalMakeUp(ax, lwd, pad_size, lenD)

                ax.set_xticks(deltas)

                ax.set_ylim(-10, 110)
                ax.set_xlabel("ΔT", labelpad=pad_size)
                ax.set_ylabel("Perceived intensity")
                ax.set_title("Means of Cold and Cold+Touch", pad=60)

                plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)