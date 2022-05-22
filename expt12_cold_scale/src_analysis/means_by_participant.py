import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics

from saving_data import(
    buildDict,
)

from local_functions import (
    getSuccData,
    parseDeltasResponses,
    get_folder_path,
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
    mean_by_participant_blind = buildDict(
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

    llaves = mean_by_participant_blind.keys()

    filepath = os.path.join(path, 'mean_by_participant_blind.csv')
    
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
                mean_by_participant_blind["subject"] = subject
                
                ## GETTING DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)

                scaling_touch_conds = {
                    n1 : {"color": c1},
                    n2 : {"color": c2},
                }

                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)
                
                ## GETTING MEANS
                for ind, cond in enumerate(scaling_touch_conds.keys()):
                    for delta in deltas:
                        mean_by_participant_blind[f"min_value_{cond}"] = statistics.mean(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])

                        print(f"means_{delta}_{cond}", statistics.mean(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"]))
                
                ## SAVING DATA
                save_all_data(filepath, mean_by_participant_blind, subject)

                mean_by_participant_blind.clear()