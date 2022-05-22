# %%
import os
import pandas as pd

from local_functions import (
    CreateFile,
    save_all_data
)
from globals import(
    conditions,
    part_to_use
)
from sdt_analysis import (
    correctPercSDT, 
    tableTosdtDoble, 
    SDTloglinear
)
from saving_data import(
    buildDict,
)

# %% 
if __name__ == "__main__":
    #SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt_cold_time/data"
    sdt_data = "data_all"

    correct_trials = []
    hit_rate = []
    false_alarm_rate = []
    misses = []
    correct_rejection = []
    #SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt_cold_time/data"
    sdt_data = "data_all"

    #SAVING DATA
    sdt_blind_data = buildDict(
        "subject",
        f"correctTrials-{conditions[0]['name']}",
        f"correctTrials-{conditions[1]['name']}",
        f"correctTrials-{conditions[2]['name']}",
        f"correctTrials-{conditions[3]['name']}",
        f"correctTrials-{conditions[4]['name']}",
        f"hits-{conditions[0]['name']}",
        f"hits-{conditions[1]['name']}",
        f"hits-{conditions[2]['name']}",
        f"hits-{conditions[3]['name']}",
        f"hits-{conditions[4]['name']}",
        f"falseAlarm-{conditions[0]['name']}",
        f"falseAlarm-{conditions[1]['name']}",
        f"falseAlarm-{conditions[2]['name']}",
        f"falseAlarm-{conditions[3]['name']}",
        f"falseAlarm-{conditions[4]['name']}",
        f"misses-{conditions[0]['name']}",
        f"misses-{conditions[1]['name']}",
        f"misses-{conditions[2]['name']}",
        f"misses-{conditions[3]['name']}",
        f"misses-{conditions[4]['name']}",
        f"correctRejec-{conditions[0]['name']}",
        f"correctRejec-{conditions[1]['name']}",
        f"correctRejec-{conditions[2]['name']}",
        f"correctRejec-{conditions[3]['name']}",
        f"correctRejec-{conditions[4]['name']}",
        f"hitRate-{conditions[0]['name']}",
        f"hitRate-{conditions[1]['name']}",
        f"hitRate-{conditions[2]['name']}",
        f"hitRate-{conditions[3]['name']}",
        f"hitRate-{conditions[4]['name']}",
        f"falseRate-{conditions[0]['name']}",
        f"falseRate-{conditions[1]['name']}",
        f"falseRate-{conditions[2]['name']}",
        f"falseRate-{conditions[3]['name']}",
        f"falseRate-{conditions[4]['name']}",

        
    )

    llaves = sdt_blind_data.keys()

    filepath = os.path.join(path, 'raw_data.csv')
    
    CreateFile(path, filepath, llaves)

    #LOOK FOR FILE
    for i in part_to_use:

        sdt_blind_data.clear()

        folder_name = f"test_{i}"
    
        filename = sdt_data

        #GET DATA
        table_data = pd.read_csv(f"../data/{folder_name}/data/{filename}.csv")


        nofailed_table_data = table_data.loc[table_data["failed"] == False]
        cleaned_table_data = nofailed_table_data.loc[
            nofailed_table_data["stimulus_time"] > 0.4
        ]

        tables_per_condition = {}
        
        #CONDITIONS
        to_rand_mani = ["touch", "notouch"]
        

        for cond in cleaned_table_data["condition_block"].unique():
            tables_per_condition[cond] = {
                "table": cleaned_table_data.loc[cleaned_table_data["condition_block"] == cond]
            }
            tables_per_condition[cond]['touch'] = conditions[cond]['touch']


        for cond in tables_per_condition:
            tables_per_condition[cond][f"correct_{cond}"] = correctPercSDT(
                tableTosdtDoble(tables_per_condition[cond]["table"], tables_per_condition[cond]["touch"], "response"), "response"
            )

            tables_per_condition[cond][f"sdt_{cond}"] = SDTloglinear(
                tables_per_condition[cond][f"correct_{cond}"]["hits"],
                tables_per_condition[cond][f"correct_{cond}"]["misses"],
                tables_per_condition[cond][f"correct_{cond}"]["fas"],
                tables_per_condition[cond][f"correct_{cond}"]["crs"],
            )


        conditions_loop = list(tables_per_condition.keys())

        sdt_blind_data["subject"] = folder_name

        for i in range(0, 5):
            sdt_blind_data[f"correctTrials-{conditions[i]['name']}"] = tables_per_condition[i][f'sdt_{i}']['correct']
        for i in range(0, 5):
            sdt_blind_data[f"hits-{conditions[i]['name']}"] = tables_per_condition[i][f'correct_{i}']['hits']
        for i in range(0, 5):
            sdt_blind_data[f"falseAlarm-{conditions[i]['name']}"] = tables_per_condition[i][f'correct_{i}']['fas']
        for i in range(0, 5):
            sdt_blind_data[f"misses-{conditions[i]['name']}"] = tables_per_condition[i][f'correct_{i}']['misses']
        for i in range(0, 5):
            sdt_blind_data[f"correctRejec-{conditions[i]['name']}"] = tables_per_condition[i][f'correct_{i}']['crs']
        for i in range(0, 5):
            sdt_blind_data[f"hitRate-{conditions[i]['name']}"] = tables_per_condition[i][f'sdt_{i}']['hit_rate']
        for i in range(0, 5):
            sdt_blind_data[f"falseRate-{conditions[i]['name']}"] = tables_per_condition[i][f'sdt_{i}']['fa_rate']

            
            
        
        #SAVING DATA
        save_all_data(filepath, sdt_blind_data, folder_name)

        sdt_blind_data.clear()