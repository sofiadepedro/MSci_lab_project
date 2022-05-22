# %%
import pandas as pd
from sdt_analysis import correctPercSDT, tableTosdtDoble, SDTloglinear
from globals import conditions
import random

# %%
folder_name = 'test_01042022_2'
filename = "data_all"

table_data = pd.read_csv(f"../data/{folder_name}/data/{filename}.csv")

nofailed_table_data = table_data.loc[table_data["failed"] == False]
cleaned_table_data = nofailed_table_data.loc[
    nofailed_table_data["stimulus_time"] > 0.4
]

tables_per_condition = {}


# %%

to_rand_mani = ["touch", "notouch"]
# np.random.shuffle(to_rand_mani)
# to_rand_cond = [0, 1, 2]
# np.random.shuffle(to_rand_cond)

for cond in cleaned_table_data["condition_block"].unique():
    tables_per_condition[cond] = {
        "table": cleaned_table_data.loc[cleaned_table_data["condition_block"] == cond]
    }
    tables_per_condition[cond]['touch'] = conditions[cond]['touch']

# %%

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

# %%
conditions_loop = list(tables_per_condition.keys())
random.shuffle(conditions_loop)
for cond in conditions_loop:
    # print(f"Correct present: {tables_per_condition[cond][f'correct_{cond}']['correc_present']}")
    # print('hit rate:', tables_per_condition[cond][f'sdt_{cond}']['hit_rate'])
    # print('fa_rate:', tables_per_condition[cond][f'sdt_{cond}']['fa_rate'])
    print(f"correct_sdt{cond}:", tables_per_condition[cond][f'sdt_{cond}']['correct'])
