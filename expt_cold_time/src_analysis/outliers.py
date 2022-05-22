# %%
import pandas as pd
import statistics as stat
import numpy as np

from globals import(
    conditions,
    part_to_use
)
from sdt_analysis import (
    correctPercSDT, 
    tableTosdtDoble, 
    SDTloglinear
)

# %%
#SET PATHS
path = "/Users/sofia/Documents/masters_project/expt_cold_time/data"
sdt_data = "data_all"

## CREATE LISTS
dif_0= []
dif_1 = []
dif_2 = []
dif_3 = []

#LOOK FOR FILE
for i in part_to_use:

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


    dif_0.append(tables_per_condition[1][f'sdt_{1}']['d'] - tables_per_condition[0][f'sdt_{0}']['d'])
    dif_1.append(tables_per_condition[2][f'sdt_{2}']['d'] - tables_per_condition[0][f'sdt_{0}']['d'])
    dif_2.append(tables_per_condition[3][f'sdt_{3}']['d'] - tables_per_condition[0][f'sdt_{0}']['d'])
    dif_3.append(tables_per_condition[4][f'sdt_{4}']['d'] - tables_per_condition[0][f'sdt_{0}']['d'])

    
print('dif_0:', dif_0)
print('dif_1:', dif_1)
print('dif_2:', dif_2)
print('dif_3:', dif_3)
# %%
### MEDIANS
median_dif_0 = stat.median(dif_0)
median_dif_1 = stat.median(dif_1)
median_dif_2 = stat.median(dif_2)
median_dif_3 = stat.median(dif_3)

print('median_dif_0:', median_dif_0)
print('median_dif_1:', median_dif_1)
print('median_dif_2:', median_dif_2)
print('median_dif_3:', median_dif_3)

# %%
### FIRST QUARTILE
first_quartile_dif_0 = np.quantile(dif_0, 0.25)
first_quartile_dif_1 = np.quantile(dif_1, 0.25)
first_quartile_dif_2 = np.quantile(dif_2, 0.25)
first_quartile_dif_3 = np.quantile(dif_3, 0.25)

print('first_quartile_dif_0:', first_quartile_dif_0)
print('first_quartile_dif_1:', first_quartile_dif_1)
print('first_quartile_dif_2:', first_quartile_dif_2)
print('first_quartile_dif_3:', first_quartile_dif_3)

# %%
### THIRD QUARTILE
third_quartile_dif_0 = np.quantile(dif_0, 0.75)
third_quartile_dif_1 = np.quantile(dif_1, 0.75)
third_quartile_dif_2 = np.quantile(dif_2, 0.75)
third_quartile_dif_3 = np.quantile(dif_3, 0.75)

print('third_quartile_dif_0:', third_quartile_dif_0)
print('third_quartile_dif_1:', third_quartile_dif_1)
print('third_quartile_dif_2:', third_quartile_dif_2)
print('third_quartile_dif_3:', third_quartile_dif_3)

# %%
### IQR
IQR_dif_0 = third_quartile_dif_0 - first_quartile_dif_0
IQR_dif_1 = third_quartile_dif_1 - first_quartile_dif_1
IQR_dif_2 = third_quartile_dif_2 - first_quartile_dif_2
IQR_dif_3 = third_quartile_dif_3 - first_quartile_dif_3

print('IQR_dif_0:', IQR_dif_0)
print('IQR_dif_1:', IQR_dif_1)
print('IQR_dif_2:', IQR_dif_2)
print('IQR_dif_3:', IQR_dif_3)

# %%
###Check for low outliers
low_outliers_dif_0 = first_quartile_dif_0 - 1.5 * IQR_dif_0
low_outliers_dif_1 = first_quartile_dif_1 - 1.5 * IQR_dif_0
low_outliers_dif_2 = first_quartile_dif_2 - 1.5 * IQR_dif_0
low_outliers_dif_3 = first_quartile_dif_3 - 1.5 * IQR_dif_0

print('low_outliers_dif_0:', low_outliers_dif_0)
print('low_outliers_dif_1:', low_outliers_dif_1)
print('low_outliers_dif_2:', low_outliers_dif_2)
print('low_outliers_dif_3:', low_outliers_dif_3)

# %%
###Check for high outliers
high_outliers_dif_0 = third_quartile_dif_0 + 1.5 * IQR_dif_0
high_outliers_dif_1 = third_quartile_dif_1 + 1.5 * IQR_dif_0
high_outliers_dif_2 = third_quartile_dif_2 + 1.5 * IQR_dif_0
high_outliers_dif_3 = third_quartile_dif_3 + 1.5 * IQR_dif_0

print('high_outliers_dif_0:', high_outliers_dif_0)
print('high_outliers_dif_1:', high_outliers_dif_1)
print('high_outliers_dif_2:', high_outliers_dif_2)
print('high_outliers_dif_3:', high_outliers_dif_3)