# %% 

import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

from local_functions import (
    CondShuffle,
    textMakeUp,
    get_folder_path,
    getSuccData,
    parseDeltasResponses,
    plot_alldata,
    plot_linregression,
    universalMakeUp
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

    n1_means = []
    n2_means = []

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
                    n1 : {"color": c1},
                    n2 : {"color": c2},
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

                print("n1", len(n1_normalized_responses))
                print("n2", len(n2_normalized_responses))

                n1_deltas = scaling_touch_conds[n1]["table"]["delta_stimulation"]
                n2_deltas = scaling_touch_conds[n2]["table"]["delta_stimulation"]


                ### PLOT MEAN DATA
                

                # ### PLOT NORMALITY HISTOGRAM
                # ### PLOT LINEAR REGRESSION ###
                # path_figures = "/Users/sofia/Documents/masters_project/expt12_cold_scale/globalfigures"
            

                # fig, ax = plt.subplots(1, 1, figsize=(20, 15))
                
                # for cond in scaling_touch_conds.keys():
                #     figure_name = f"normality_zscore_blindcheck_test_{todaydate}_{cond}"
                #     if cond == n1:
                #         plt.hist(n1_normalized_responses, color = scaling_touch_conds[cond]["color"])

                #         universalMakeUp(ax, lwd, pad_size, lenD)

                #         ax.set_xlim(-2, 2)
                #         ax.set_xlabel("response", labelpad=pad_size)
                #         ax.set_ylabel("Frequency")
                #         ax.set_title("Normality of data", pad=60)

                #         plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)

                #     elif cond == n2:
                #         plt.hist(n2_normalized_responses, color = scaling_touch_conds[cond]["color"])
                #         universalMakeUp(ax, lwd, pad_size, lenD)

            
                #         ax.set_xlim(-2, 2)
                #         ax.set_xlabel("response", labelpad=pad_size)
                #         ax.set_ylabel("Frequency")
                #         ax.set_title("Normality of data", pad=60)

                #         plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)

                    



                # ### PLOT Z-SCORE RAW DATA
                # ### PLOT LINEAR REGRESSION ###
                # path_figures = "/Users/sofia/Documents/masters_project/expt12_cold_scale/globalfigures"
                # figure_name = f"zscore_blindcheck_test_{todaydate}"

                # fig, ax = plt.subplots(1, 1, figsize=(20, 15))
                # # PLOT ALL DATA
                # for cond in scaling_touch_conds.keys():
                #     if cond == n1:
                #         print("delta", len(scaling_touch_conds[cond]["table"]["delta_stimulation"]))
                #         plt.scatter(
                #             scaling_touch_conds[cond]["table"]["delta_stimulation"], 
                #             n1_normalized_responses, 
                #             c = scaling_touch_conds[cond]["color"]
                #         )

                #         plot_linregression(
                #             scaling_touch_conds[cond]["table"]["delta_stimulation"], 
                #             n1_normalized_responses, 
                #             scaling_touch_conds[cond]["color"], 
                #             lwd, 
                #             scaling_touch_conds[cond]
                #         )
                #     if cond == n2:
                #         print("delta", len(scaling_touch_conds[cond]["table"]["delta_stimulation"]))
                #         plt.scatter(
                #             scaling_touch_conds[cond]["table"]["delta_stimulation"], 
                #             n2_normalized_responses, 
                #             c = scaling_touch_conds[cond]["color"],
                #         )

                #         plot_linregression(
                #             scaling_touch_conds[cond]["table"]["delta_stimulation"], 
                #             n2_normalized_responses, 
                #             scaling_touch_conds[cond]["color"], 
                #             lwd, 
                #             scaling_touch_conds[cond]
                #         )

                # universalMakeUp(ax, lwd, pad_size, lenD)

                # ax.set_xticks(deltas)

                # ax.set_ylim(-2, 2)
                # ax.set_xlabel("ΔT", labelpad=pad_size)
                # ax.set_ylabel("Perceived intensity")
                # ax.set_title("Z-score data of Cold and Cold+Touch", pad=60)

                # plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)
