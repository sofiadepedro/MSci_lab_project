# %%
import os
import statistics
import matplotlib.pyplot as plt 

from local_functions import (
    get_folder_path,
    CondShuffle,
    getSuccData,
    parseDeltasResponses,
    plot_linregression,
    textMakeUp,
    universalMakeUp,
    get_linregression
)

if __name__ == "__main__":

    #SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt12_cold_scale/data"
    scaling_data = "data_scaling_subj"
    staircase_data = "data_staircase1_subj"

    ## SHUFFLE CONDITIONS NAME
    n1, n2, c1, c2 = "1", "2", "#B59A48", "#0F4C81"       #"#477DBD", #"#794493"

    #PLOT STUFF
    s_size = 100
    s_mean = 400
    lwd = 10
    pad_size = 30
    lenD = 15
    mc = "black"
    lateral_wiggle = 0.2

    textMakeUp(mc)

    n1_means = []
    n2_means = []

    deltas_list = []


    ## GO THROUGH FOLDERS & LOOK FOR SCALING SCRIPT
    for foldername in os.listdir(path):
        if foldername.startswith("test_"):
            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv') and os.path.isfile(f'{folder_path}/{staircase_data}.csv'):

                # GETTING THE DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)
                # print(scaling_df_succ)

                scaling_touch_conds = {
                    n1 : {"color": c1, "name": "Cold"},
                    n2 : {"color": c2, "name": "Cold + touch"},
                }

                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)

                ## GETTING MEAN
                for ind, cond in enumerate(scaling_touch_conds.keys()):
                    scaling_touch_conds[cond]["scaling_means"] = []

                    for delta in deltas:
                        scaling_touch_conds[cond]["scaling_means"].append(
                                    statistics.mean(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])
                                )
                        if cond == n1:
                            n1_means.append(
                                         statistics.mean(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])
                                    )
                        if cond == n2:
                             n2_means.append(
                                        statistics.mean(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])
                                    )

                for delta in deltas:
                    deltas_list.append(delta)

    ## PLOT LINEAR REGRESSION ###
    path_figures = "/Users/sofia/Documents/masters_project/expt12_cold_scale/globalfigures"
    figure_name = f"all_means_blindcheck_test_{todaydate}"

    fig, ax = plt.subplots(1, 1, figsize=(25, 20))

  
    # PLOT ALL DATA
    for cond in scaling_touch_conds.keys():
        if cond == n1:
            print("deltas", deltas_list)
            plt.scatter(
                deltas_list, 
                n1_means, 
                c = scaling_touch_conds[cond]["color"],
                linewidths = 10,
                alpha = 0.5
            )
            plot_linregression(
                deltas_list, 
                n1_means, 
                scaling_touch_conds[cond]["color"], 
                lwd, 
                scaling_touch_conds[cond]["name"]
            )
            slope, intercept = get_linregression(deltas_list, n1_means, cond)
            print(f"Slope_{cond}", slope)
            print(f"Intercept_{cond}", intercept)
            print("color", scaling_touch_conds[cond]["color"])
        elif cond == n2:
            plt.scatter(
                deltas_list, 
                n2_means, 
                c = scaling_touch_conds[cond]["color"],
                linewidths = 10,
                alpha=0.5
            )
            plot_linregression(
                deltas_list, 
                n2_means, 
                scaling_touch_conds[cond]["color"], 
                lwd, 
                scaling_touch_conds[cond]["name"]
            )
            slope, intercept = get_linregression(deltas_list, n2_means, cond)
            print(f"Slope_{cond}", slope)
            print(f"Intercept_{cond}", intercept)
            print("color", scaling_touch_conds[cond]["color"])

    universalMakeUp(ax, lwd, pad_size, lenD)

    ax.set_xticks(deltas)

    ax.set_ylim(-10, 100)
    ax.set_xlabel(f'Change in Temperature\n(ΔT °C)', labelpad=pad_size, fontsize = 50)
                        # {degree_sign}
    ax.set_ylabel("Perceived intensity", labelpad=pad_size, fontsize = 50)
    # ax.set_title("Means of Cold and Cold+Touch", pad=60)

    plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)
                    
