# %% 
import os
import matplotlib.pyplot as plt
import statistics
from scipy import stats 

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
)

if __name__ == "__main__":
    ## SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt12_cold_scale/data"
    scaling_data = "data_scaling_subj"
    staircase_data = "data_staircase1_subj"

    # SAVING DATA
    slope_data_blind = buildDict(
        "subject",
        "slope_1",
        "intercept_1",
        "rvalue_1",
        "pvalue_1",
        "stderr_1",
        "slope_2",
        "intercept_2",
        "rvalue_2",
        "pvalue_2",
        "stderr_2",
    )

    llaves = slope_data_blind.keys()

    filepath = os.path.join(path, 'slope_median_blind.csv')
    
    CreateFile(path, filepath, llaves)

    ## SHUFFLE CONDITIONS NAME
    n1, n2, c1, c2 = CondShuffle()


    ## GO THROUGH FOLDERS & LOOK FOR SCALING SCRIPT
    for foldername in os.listdir(path):
        slope_data_blind.clear()
        if foldername.startswith("test_"):

            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv') and os.path.isfile(f'{folder_path}/{staircase_data}.csv'):
                slope_data_blind["subject"] = subject
                
                ## GETTING DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)

                scaling_touch_conds = {
                    n1 : {"color": c1},
                    n2 : {"color": c2},
                }

                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)
                
                ## GETTING MEANS
                for ind, cond in enumerate(scaling_touch_conds.keys()):
                    scaling_touch_conds[cond]["scaling_medians"] = []

                    for delta in deltas:
                        scaling_touch_conds[cond]["scaling_medians"].append(
                                    statistics.median(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])
                                )


                ## GET SLOPE, INTERCEPT, MIN AND MAX VALUE
                for cond in scaling_touch_conds.keys():
                    # slope_data_blind[f"slope_{cond}"], slope_data_blind[f"intercept_{cond}"] = stats.linregress(deltas, scaling_touch_conds[cond]["scaling_means"], cond)

                    (slope_data_blind[f"slope_{cond}"], slope_data_blind[f"intercept_{cond}"], slope_data_blind[f"rvalue_{cond}"], slope_data_blind[f"pvalue_{cond}"], slope_data_blind[f"stderrt_{cond}"]) = stats.linregress(deltas, scaling_touch_conds[cond]["scaling_medians"])

    

                ## SAVING DATA
                save_all_data(filepath, slope_data_blind, subject)