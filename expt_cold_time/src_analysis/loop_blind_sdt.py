import os
import pandas as pd
import random

from local_functions import (
    get_folder_path,
    CreateFile,
    save_all_data
)
from globals import(
    conditions
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
        "condition",
        "correct_present",
        "hit_rate",
        "false_alarm_rate",
        "correct_sdt"
    )

    llaves = sdt_blind_data.keys()

    filepath = os.path.join(path, 'blind_sdt.csv')
    
    CreateFile(path, filepath, llaves)

    ##CONDITIONS
    sdt_conds = [0, 1, 2, 3, 4]
    random.shuffle(sdt_conds)

    
    #LOOK FOR FILE

    for foldername in os.listdir(path):
        if foldername.startswith("test_"):
            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            if os.path.isfile(f'{folder_path}/{sdt_data}.csv'):
                folder_name = foldername
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
                random.shuffle(conditions_loop)
                for cond in conditions_loop:
                    print(f"Correct present: {tables_per_condition[cond][f'correct_{cond}']['correc_present']}")
                    print('hit rate:', tables_per_condition[cond][f'sdt_{cond}']['hit_rate'])
                    print('fa_rate:', tables_per_condition[cond][f'sdt_{cond}']['fa_rate'])
                    
                    sdt_blind_data["subject"] = subject
    
                    if cond == 0:
                        sdt_blind_data["condition"] = sdt_conds[0]
                    elif cond == 1:
                        sdt_blind_data["condition"] = sdt_conds[1]
                    elif cond == 2:
                        sdt_blind_data["condition"] = sdt_conds[2]
                    elif cond == 3:
                        sdt_blind_data["condition"] = sdt_conds[3]
                    elif cond == 4:
                        sdt_blind_data["condition"] = sdt_conds[4]
                    
                    
                    sdt_blind_data["correct_present"] = tables_per_condition[cond][f'correct_{cond}']['correc_present']
                    sdt_blind_data["hit_rate"] = tables_per_condition[cond][f'sdt_{cond}']['hit_rate']
                    sdt_blind_data["false_alarm_rate"] = tables_per_condition[cond][f'sdt_{cond}']['fa_rate']
                    sdt_blind_data["correct_sdt"] = tables_per_condition[cond][f'sdt_{cond}']['correct']
                

                    #SAVING DATA
                    save_all_data(filepath, sdt_blind_data, subject)

                    sdt_blind_data.clear()