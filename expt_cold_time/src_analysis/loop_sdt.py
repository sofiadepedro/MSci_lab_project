import os
from unicodedata import name
import pandas as pd
import random

from local_functions import (
    get_folder_path,
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

if __name__ == "__main__":
    #SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt_cold_time/data"
    sdt_data = "data_all"

    #SAVING DATA
    sdt_blind_data = buildDict(
        "subject",
        f"d-{conditions[0]['name']}",
        f"d-{conditions[1]['name']}",
        f"d-{conditions[2]['name']}",
        f"d-{conditions[3]['name']}",
        f"d-{conditions[4]['name']}",
        f"dif-{conditions[1]['name']}-{conditions[0]['name']}",
        f"dif-{conditions[2]['name']}-{conditions[0]['name']}",
        f"dif-{conditions[3]['name']}-{conditions[0]['name']}",
        f"dif-{conditions[4]['name']}-{conditions[0]['name']}",
        f"c-{conditions[0]['name']}",
        f"c-{conditions[1]['name']}",
        f"c-{conditions[2]['name']}",
        f"c-{conditions[3]['name']}",
        f"c-{conditions[4]['name']}",
    )

    llaves = sdt_blind_data.keys()

    filepath = os.path.join(path, 'sdt.csv')
    
    CreateFile(path, filepath, llaves)

    
    #LOOK FOR FILE
    for i in part_to_use:
        sdt_blind_data.clear()

        participant = part_to_use[i]["name"]

        folder_name = f"test_{participant}"

    
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
        # np.random.shuffle(to_rand_mani)
        # to_rand_cond = [0, 1, 2]
        # np.random.shuffle(to_rand_cond)

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
            sdt_blind_data[f"d-{conditions[i]['name']}"] = tables_per_condition[i][f'sdt_{i}']['d']
        
        for i in range(1, 5):
            sdt_blind_data[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"] = tables_per_condition[i][f'sdt_{i}']['d'] - tables_per_condition[0][f'sdt_{0}']['d']
        
        for i in range(0, 5):
            sdt_blind_data[f"c-{conditions[i]['name']}"] = tables_per_condition[i][f'sdt_{i}']['c']

        #SAVING DATA
        save_all_data(filepath, sdt_blind_data, folder_name)

        sdt_blind_data.clear()
        
        print('conditions_lopp', conditions_loop)