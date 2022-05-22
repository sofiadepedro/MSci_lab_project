## GET SLOPE & INTECEPT OF LINEAR REGRESSION OF ALL DATA, MEAN & MEDIAN 
import os
import statistics


from saving_data import buildDict
from local_functions import(
    CreateFile,
    CondShuffle,
    get_folder_path,
    getSuccData,
    parseDeltasResponses,
    get_linregression,
    save_all_data,
)

if __name__ == "__main__":
    ## SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt12_cold_scale/data"
    scaling_data = "data_scaling_subj"

    ## SAVING DATA
    compare_data_blind = buildDict(
        "subject",
        "mean_slope_1",
        "median_slope_1",
        "rawdata_slope_1",
        "mean_intercept_1",
        "median_intercept_1",
        "rawdata_intercept_1",
        "mean_slope_2",
        "median_slope_2",
        "rawdata_slope_2",
        "mean_intercept_2",
        "median_intercept_2",
        "rawdata_intercept_2"
    )

    llaves = compare_data_blind.keys()

    filepath = os.path.join(path, 'compare_data_blind.csv')
    
    CreateFile(path, filepath, llaves)

    ## SHUFFLE CONDITIONS NAME
    n1, n2, c1, c2 = CondShuffle()

    ## GO THROUGH FOLDERS & LOOK FOR SCALING SCRIPT
    for foldername in os.listdir(path):
        if foldername.startswith("test_"):

            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv'):
                compare_data_blind.clear()
                compare_data_blind["subject"] = subject
                
                ## GETTING DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)

                scaling_touch_conds = {
                    n1 : {"color": c1},
                    n2 : {"color": c2},
                }

                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)
                
                for ind, cond in enumerate(scaling_touch_conds.keys()):
                    scaling_touch_conds[cond]["scaling_means"] = []

                    for delta in deltas:
                        scaling_touch_conds[cond]["scaling_means"].append(
                                    statistics.mean(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])
                                )
                print("means", scaling_touch_conds[cond]["scaling_means"])

        
                for ind, cond in enumerate(scaling_touch_conds.keys()):
                    scaling_touch_conds[cond]["scaling_medians"] = []

                    for delta in deltas:
                        scaling_touch_conds[cond]["scaling_medians"].append(
                                    statistics.median(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])
                                )
                        print("median", scaling_touch_conds[cond]["scaling_medians"])
                
                for cond in scaling_touch_conds.keys():
                    compare_data_blind[f"mean_slope_{cond}"], _ = get_linregression(deltas, scaling_touch_conds[cond]["scaling_means"], cond)
                    compare_data_blind[f"median_slope_{cond}"], _ = get_linregression(deltas, scaling_touch_conds[cond]["scaling_medians"], cond)
                    compare_data_blind[f"rawdata_slope_{cond}"], _ = get_linregression(list(scaling_touch_conds[cond]["table"]["delta_stimulation"]),list(scaling_touch_conds[cond]["table"]["response"]), cond)

                    _, compare_data_blind[f"mean_intercept_{cond}"] = get_linregression(deltas, scaling_touch_conds[cond]["scaling_means"], cond)
                    _, compare_data_blind[f"median_intercept_{cond}"] = get_linregression(deltas, scaling_touch_conds[cond]["scaling_medians"], cond)
                    _, compare_data_blind[f"rawdata_intercept_{cond}"] = get_linregression(list(scaling_touch_conds[cond]["table"]["delta_stimulation"]),list(scaling_touch_conds[cond]["table"]["response"]), cond)


                ## SAVING DATA
                save_all_data(filepath, compare_data_blind, subject)

                compare_data_blind.clear()