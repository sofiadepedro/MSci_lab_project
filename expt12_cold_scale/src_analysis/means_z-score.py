# %% 
import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import statistics

from local_functions import (
    CondShuffle,
    textMakeUp,
    get_folder_path,
    getSuccData,
    parseDeltasResponses,
    plot_linregression,
    universalMakeUp,
    get_linregression
)

if __name__ == "__main__":

    #SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt12_cold_scale/data"
    scaling_data = "data_scaling_subj"
    staircase_data = "data_staircase1_subj"

    ## SHUFFLE CONDITIONS NAME
    n1, n2, c1, c2 = CondShuffle()

    #PLOT STUFF
    s_size = 100
    s_mean = 400
    lwd = 10
    pad_size = 20
    lenD = 15
    mc = "black"
    lateral_wiggle = 0.2

    textMakeUp(mc)

    n1_mean_list = []
    n2_mean_list = []

    deltas_list = []


    ## GO THROUGH FOLDERS & LOOK FOR SCALING SCRIPT
    for foldername in os.listdir(path):
        if foldername.startswith("test_"):
            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv') and os.path.isfile(f'{folder_path}/{staircase_data}.csv'):
                
                print("subject", subject)

                ### GET DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)

                scaling_touch_conds = {
                    n1 : {"color": c1, "name": "no touch"},
                    n2 : {"color": c2, "name": "touch"},
                }
                
                ### GET LIST OF ALL RESPONSES
                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)

            
                n1_response_list = list(scaling_touch_conds[n1]["table"]["response"])
                n2_response_list = list(scaling_touch_conds[n2]["table"]["response"])

                all_response_list = n1_response_list + n2_response_list

                ### DO Z-SCORE
                normalized_responses = stats.zscore(all_response_list)

                ### SEPARATE RESPONSES FOR EACH CONDITION
                n1_normalized_responses = normalized_responses[0:84]
                n2_normalized_responses = normalized_responses[84:168]

                # print("responses", all_response_list)
                # print("n1", n1_response_list)
                # print("normalized_responses", normalized_responses)
                
                # print("n1", len(n1_normalized_responses))
                # print("n2", len(n2_normalized_responses))

                n1_deltas = scaling_touch_conds[n1]["table"]["delta_stimulation"]
                n2_deltas = scaling_touch_conds[n2]["table"]["delta_stimulation"]

                for cond in scaling_touch_conds.keys():

                    zero_n1_list = []
                    seven_n1_list = []
                    fourteen_n1_list = []
                    twentyone_n1_list = []
                    twentyeight_n1_list = []
                    thirtyfive_n1_list = []

                    zero_n2_list = []
                    seven_n2_list = []
                    fourteen_n2_list = []
                    twentyone_n2_list = []
                    twentyeight_n2_list = []
                    thirtyfive_n2_list = []

                    for a,b in zip(n1_normalized_responses, n1_deltas):
                        # print("a", a, "b", b)
                        if b == 0.0:
                            zero_n1_list.append(a)
                        elif b == 0.7:
                            seven_n1_list.append(a)
                        elif b == 1.4:
                            fourteen_n1_list.append(a)
                        elif b == 2.1:
                            twentyone_n1_list.append(a)
                        elif b == 2.8:
                            twentyeight_n1_list.append(a)
                        elif b == 3.5:
                            thirtyfive_n1_list.append(a)
                        

                    print("n2", len(n2_normalized_responses))
                    for c,d in zip(n2_normalized_responses, n2_deltas):
                        # print("c", c, "d", d)
                        if d == 0.0:
                            zero_n2_list.append(c)
                        elif d == 0.7:
                            seven_n2_list.append(c)
                        elif d == 1.4:
                            fourteen_n2_list.append(c)
                        elif d == 2.1:
                            twentyone_n2_list.append(c)
                        elif d == 2.8:
                            twentyeight_n2_list.append(c)
                        elif d == 3.5:
                            thirtyfive_n2_list.append(c)
                    
    
                    
                    n1_mean_list.append(statistics.mean(zero_n1_list))
                    n1_mean_list.append(statistics.mean(seven_n1_list))
                    n1_mean_list.append(statistics.mean(fourteen_n1_list))
                    n1_mean_list.append(statistics.mean(twentyone_n1_list))
                    n1_mean_list.append(statistics.mean(twentyeight_n1_list))
                    n1_mean_list.append(statistics.mean(thirtyfive_n1_list))

                    n2_mean_list.append(statistics.mean(zero_n2_list))
                    n2_mean_list.append(statistics.mean(seven_n2_list))
                    n2_mean_list.append(statistics.mean(fourteen_n2_list))
                    n2_mean_list.append(statistics.mean(twentyone_n2_list))
                    n2_mean_list.append(statistics.mean(twentyeight_n2_list))
                    n2_mean_list.append(statistics.mean(thirtyfive_n2_list))

                    for delta in deltas:
                        deltas_list.append(delta)




     ## PLOT LINEAR REGRESSION ###
    path_figures = "/Users/sofia/Documents/masters_project/expt12_cold_scale/globalfigures"
    figure_name = f"z_score_all_means_blindcheck_test"

    fig, ax = plt.subplots(1, 1, figsize=(20, 15))

  
    # PLOT ALL DATA
    plt.scatter(
        deltas_list,
        n1_mean_list,
        c = scaling_touch_conds[n1]["color"]
    )
    plot_linregression(
        deltas_list, 
        n1_mean_list, 
        scaling_touch_conds[n1]["color"], 
        lwd, 
        scaling_touch_conds[n1]["name"]
    )

    plt.scatter(
        deltas_list,
        n2_mean_list,
        c = scaling_touch_conds[n2]["color"]
    )
    plot_linregression(
        deltas_list, 
        n2_mean_list, 
        scaling_touch_conds[n2]["color"], 
        lwd, 
        scaling_touch_conds[n2]["name"]
    )


    slopen1, interceptn1 = get_linregression(deltas_list, n1_mean_list, n1)
    print(f"Slope_n1", slopen1)
    print(f"Intercept_n1", interceptn1)

    slopen2, interceptn2 = get_linregression(deltas_list, n2_mean_list, n2)
    print(f"Slope_n2", slopen2)
    print(f"Intercept_2", interceptn2)

    universalMakeUp(ax, lwd, pad_size, lenD)

    ax.set_xticks(deltas)

    ax.set_ylim(-2, 2)
    ax.set_xlabel("ΔT", labelpad=pad_size)
    ax.set_ylabel("Perceived intensity")
    ax.set_title("z-score Means of Cold and Cold+Touch", pad=60)

    plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)

                    
                    
# %%
