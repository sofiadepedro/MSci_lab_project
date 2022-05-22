import os
import csv
import numpy as np
import pandas as pd
import statistics
import random

from local_functions import (
    get_folder_path,
    CreateFile,
    CondShuffle,
    getSuccData,
    getStandardDev,
    parseDeltasResponses,
    save_all_data
)

from saving_data import(
    buildDict,
)

if __name__ == "__main__":

    #SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt12_cold_scale/data"
    scaling_data = "data_scaling_subj"
    staircase_data = "data_staircase1_subj"
    anchoring_data = "data_anchoring"

    # SAVING DATA
    all_means_blind = buildDict(
        "subject",
        "delta0_1",
        "stdev0_1",
        "delta7_1",
        "stdev7_1",
        "delta14_1",
        "stdev14_1",
        "delta21_1",
        "stdev21_1",
        "delta28_1",
        "stdev28_1",
        "delta35_1",
        "stdev35_1",
        "delta0_2",
        "stdev0_2",
        "delta7_2",
        "stdev7_2",
        "delta14_2",
        "stdev14_2",
        "delta21_2",
        "stdev21_2",
        "delta28_2",
        "stdev28_2",
        "delta35_2",
        "stdev35_2",
    )

    llaves = all_means_blind.keys()

    filepath = os.path.join(path, 'all_means.csv')
    
    CreateFile(path, filepath, llaves)

    ## SHUFFLE CONDITIONS NAME
    n1, n2, _, _ = CondShuffle()

    ## GO THROUGH FOLDERS & LOOK FOR SCALING SCRIPT
    for foldername in os.listdir(path):
        if foldername.startswith("test_"):
            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv') and os.path.isfile(f'{folder_path}/{staircase_data}.csv'):

                all_means_blind["subject"] = subject

                # GETTING THE DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)
                # print(scaling_df_succ)

                scaling_touch_conds = {
                    n1: {},
                    n2: {},
                }

                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)
                
                ## GETTING MEANS
                for ind, cond in enumerate(scaling_touch_conds.keys()):
                    scaling_touch_conds[cond]["scaling_means"] = []

                    for delta in deltas:
                        scaling_touch_conds[cond]["scaling_means"].append(
                                    statistics.mean(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])
                                )
                print("means", scaling_touch_conds[cond]["scaling_means"])


                for cond in scaling_touch_conds.keys():
                    mean_cond = scaling_touch_conds[cond]["scaling_means"]

                    # print(f"Means for condition {cond} are:", mean_cond)

                    for delta in deltas:
                        mean_delta = mean_cond.pop(0)
                        # print(f"Mean for delta {delta} in condition {cond} is:", mean_delta)
                        all_means_blind[f"delta{str(round(delta*10))}_{cond}"] = mean_delta
                        # print(all_means_blind[f"delta{str(round(delta*10))})_{cond}"])

                        all_data =  scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"]
                        all_means_blind[f"stdev{str(round(delta*10))}_{cond}"] = getStandardDev(all_data)
                        print("Stdev", getStandardDev(all_data))
                    

                #SAVING DATA
                save_all_data(filepath, all_means_blind, subject)

                all_means_blind.clear()
