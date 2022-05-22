# %%
import os
from cv2 import threshold
import pandas as pd
from scipy.stats import norm
import math
import numpy as np

Z = norm.ppf

from local_functions import(
    getThreshold,
    getSuccData,
    nearest_largest_value2,
    sdt_in_scaling,
    get_folder_path,
    CreateFile,
    save_all_data
)

from saving_data import(
    buildDict,
)

if __name__ == "__main__":

    path = '/Users/sofia/Documents/masters_project/expt12_cold_scale/data'

    scaling_filepath = os.path.join(path, "data_scaling_subj.csv")
    staircase_filepath = os.path.join(path, "data_staircase1_subj.csv")

      ## SAVING DATA
    sdt_scaling = buildDict(
        "subject",
        "hit_rate_notouch",
        "fa_rate_notouch",
        "d_notouch",
        "c_notouch",
        "hit_rate_touch",
        "fa_rate_touch",
        "d_touch",
        "c_touch",
        "Threshold",	
        "Closest_intensity",
    )


    llaves = sdt_scaling.keys()

    filepath = os.path.join(path, 'sdt_in_scaling.csv')
    
    CreateFile(path, filepath, llaves)


    for foldername in os.listdir(path):
        if foldername.startswith("test_"):
            sdt_scaling.clear()
            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            sdt_scaling["subject"] = subject

            ## GET THRESHOLD
            threshold_value = getThreshold(test_state="test", subj=todaydate)
            print(threshold_value)

            ## GET VALUES FOR 0 and X CONDITION
            intensity_values = [0, 0.7, 1.4, 2.1, 2.8, 3.5]

            closest_value = nearest_largest_value2(threshold_value, intensity_values)
            print(closest_value)

            scaling_df_succ = getSuccData(test_state="test", subj=todaydate)

            scaling_touch_conds = {
                "notouch": {"color": "#794493", "name": "Cold"},
                "touch": {"color": "#477DBD", "name": "Cold + Touch"},
            }


            for ind, cond in enumerate(scaling_touch_conds.keys()):
                scaling_touch_conds[cond]["table"] = scaling_df_succ.loc[
                    scaling_df_succ["touch"] == ind
                ]
                deltas = scaling_touch_conds[cond]["table"]["delta_stimulation"].unique()

                for delta in deltas:
                    key_delta = f"scaling_delta{delta}"
                    scaling_touch_conds[cond][key_delta] = scaling_touch_conds[cond]["table"].loc[
                        scaling_touch_conds[cond]["table"]["delta_stimulation"] == delta
                    ]

                    key_delta_list = f"scaling_delta{delta}_list"
                    scaling_touch_conds[cond][key_delta_list] = list(
                        scaling_touch_conds[cond][key_delta]["delta_stimulation"]
                    )

                    key_delta_response_list = f"scaling_delta{delta}_response_list"
                    scaling_touch_conds[cond][key_delta_response_list] = list(
                        scaling_touch_conds[cond][key_delta]["response"]
                    )

            response_0_touch = []
            response_0_notouch = []
            response_x_touch = []
            response_x_notouch = []


            for delta in deltas:
                if delta == 0:
                    response_0_notouch.append(scaling_touch_conds["notouch"][f"scaling_delta{delta}_response_list"])
                    response_0_touch.append(scaling_touch_conds["touch"][f"scaling_delta{delta}_response_list"])
                
                if delta == closest_value:
                    print(delta)
                    response_x_notouch.append(scaling_touch_conds["notouch"][f"scaling_delta{delta}_response_list"])
                    response_x_touch.append(scaling_touch_conds["touch"][f"scaling_delta{delta}_response_list"])

            print (response_0_touch)
            print (response_0_notouch)
            print (response_x_touch)
            print (response_x_notouch)

            ## DO SDT ANALYSIS

            #Sensitivity without notouch
            sdt_scaling["hit_rate_notouch"], sdt_scaling["fa_rate_notouch"], sdt_scaling["d_notouch"], sdt_scaling["c_notouch"] = sdt_in_scaling(response_0_notouch, response_x_notouch)

            #Sensitivity without touch
            sdt_scaling["hit_rate_touch"], sdt_scaling["fa_rate_touch"], sdt_scaling["d_touch"], sdt_scaling["c_touch"]  = sdt_in_scaling(response_0_touch, response_x_touch)

            sdt_scaling["threshold"] = threshold_value
            sdt_scaling["closest_intensity"] = closest_value



            ## SAVE
            save_all_data(filepath, sdt_scaling, subject)

            sdt_scaling.clear()

