import os
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
    getThreshold,
    extractAnchoringDataFrame,
    plot_alldata,
    plot_linregression,
    parseDeltasResponses,
    get_folder_path,
    get_percentage_correct,
    save_all_data,
    CondShuffle,
    CreateFile,
    textMakeUp
)

if __name__ == "__main__":
    ## SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt12_cold_scale/data"
    scaling_data = "data_scaling_subj"
    staircase_data = "data_staircase1_subj"
    anchoring_data = "data_anchoring"

    ## SAVING DATA
    raw_data_blind = buildDict(
        "subject",
        "slope_1",
        "intercept_1",
        "min_value_1",
        "max_value_1",
        "slope_2",
        "intercept_2",
        "min_value_2",
        "max_value_2",
        "threshold",
        "perceived_threshold_intensity_1",
        "perceived_threshold_intensity_2",
        "anch_zero_percentage_correct",
        "anch_hundred_percentage_correct"
    )

    llaves = raw_data_blind.keys()

    filepath = os.path.join(path, 'raw_data_blind.csv')
    
    CreateFile(path, filepath, llaves)

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

    ## GO THROUGH FOLDERS & LOOK FOR SCALING SCRIPT
    for foldername in os.listdir(path):
        if foldername.startswith("test_"):

            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv'):
                raw_data_blind["subject"] = subject
                
                ## GETTING DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)

                scaling_touch_conds = {
                    n1 : {"color": c1},
                    n2 : {"color": c2},
                }

                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)
                
                for cond in scaling_touch_conds.keys():
                    all_deltas_list = list(
                            scaling_touch_conds[cond]["table"]["delta_stimulation"]
                        )
                    all_response_list = list(
                        scaling_touch_conds[cond]["table"]["response"]
                    )
                
                ### PLOT LINEAR REGRESSION ###
                path_figures = "/Users/sofia/Documents/masters_project/expt12_cold_scale/globalfigures"
                figure_name = f"raw_data_blindcheck_test_{todaydate}"

                fig, ax = plt.subplots(1, 1, figsize=(20, 15))
                # PLOT ALL DATA + LINEAR REGRESSION
                for delta in deltas:
                    for cond in scaling_touch_conds.keys():
                        plot_alldata(
                            scaling_touch_conds[cond][f"scaling_delta{delta}_list"], 
                            scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"], 
                            scaling_touch_conds[cond]["color"], 
                            lateral_wiggle, 
                            s_size
                        )
                        
                       
                # PLOT MEAN + LINEAR REGRESSION
                for cond in scaling_touch_conds.keys():
                    plot_linregression(
                            list(scaling_touch_conds[cond]["table"]["delta_stimulation"]), 
                            list(scaling_touch_conds[cond]["table"]["response"]), 
                            scaling_touch_conds[cond]["color"], 
                            lwd, 
                            scaling_touch_conds[cond]
                        )

                universalMakeUp(ax, lwd, pad_size, lenD)

                ax.set_xticks(deltas)

                ax.set_ylim(-10, 110)
                ax.set_xlabel("ΔT", labelpad=pad_size)
                ax.set_ylabel("Perceived intensity")
                ax.set_title("Raw Data of Cold and Cold+Touch", pad=60)

                plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)


                ## GET SLOPE, INTERCEPT, MIN AND MAX VALUE
                for cond in scaling_touch_conds.keys():
                    raw_data_blind[f"slope_{cond}"], raw_data_blind[f"intercept_{cond}"] = get_linregression(list(scaling_touch_conds[cond]["table"]["delta_stimulation"]),list(scaling_touch_conds[cond]["table"]["response"]), cond)


                    raw_data_blind[f"min_value_{cond}"] = min(all_response_list)
                    raw_data_blind[f"max_value_{cond}"] = max(all_response_list)

        
                ## GET PERCEIVED INTENSITY OF THRESHOLD VALUE
                if os.path.isfile(f'{folder_path}/{staircase_data}.csv'):
                    raw_data_blind["threshold"] = getThreshold(test_state="test", subj=todaydate)

                    for cond in scaling_touch_conds.keys():
                        raw_data_blind[f"perceived_threshold_intensity_{cond}"] = np.interp(raw_data_blind["threshold"], list(scaling_touch_conds[cond]["table"]["delta_stimulation"]), list(scaling_touch_conds[cond]["table"]["response"]))
                else:
                    raw_data_blind["threshold"] = np.NaN
                    for cond in scaling_touch_conds.keys():
                        raw_data_blind[f"perceived_threshold_intensity_{cond}"] = np.NaN
                
                
                ## GET ANCHORING CORRECT %
                if os.path.isfile(f'{folder_path}/{anchoring_data}.csv'):
                    df = pd.read_csv(f"{folder_path}/{anchoring_data}.csv")
                    anch_df = extractAnchoringDataFrame(df)

                    anch_df_succ = anch_df.loc[anch_df["failed"] == "False"]

                    delta_zero = anch_df_succ.loc[anch_df_succ["delta_stimulation"] == "0.0"]
                    delta_trescinco = anch_df_succ.loc[anch_df_succ["delta_stimulation"] == "3.5"]

                    delta_zero_list = list(delta_zero["response"])
                    delta_trescinco_list = list(delta_trescinco["response"])

                    raw_data_blind[f"anch_zero_percentage_correct"] = get_percentage_correct(delta_zero_list, "0")
                    raw_data_blind[f"anch_hundred_percentage_correct"] = get_percentage_correct(delta_trescinco_list, "100")
                    
    

                ## SAVING DATA
                save_all_data(filepath, raw_data_blind, subject)

                raw_data_blind.clear()