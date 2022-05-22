import numpy as np
import pandas as pd
from sdt_analysis import *
import matplotlib.pyplot as plt
import os
import argparse
import random

mc = "black"
plt.rcParams.update(
    {
        "font.size": 40,
        "axes.labelcolor": "{}".format(mc),
        "xtick.color": "{}".format(mc),
        "ytick.color": "{}".format(mc),
        "font.family": "sans-serif",
    }
)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Folder name")
    parser.add_argument("-f", type=str)
    args = parser.parse_args()
    folder_name = args.f

    path = os.path.realpath(__file__)
    root_path = path.rsplit("/", 3)[0]

    table_data = pd.read_csv(f"{root_path}/data/{folder_name}/data/data_all.csv")
    nofailed_table_data = table_data.loc[table_data["failed"] == False]
    cleaned_table_data = nofailed_table_data.loc[
        nofailed_table_data["stimulus_time"] > 0.4
    ]

    tables_per_position = {}
    percs_poses = []

    for i, cond in enumerate(cleaned_table_data["position"].unique()):
        tables_per_position[cond] = {
            "table": cleaned_table_data.loc[cleaned_table_data["position"] == cond]
        }
        tables_per_position[cond]["responses"] = (
            tables_per_position[cond]["table"]["responses"].value_counts().to_dict()
        )
        try:
            perc_no = round(
                tables_per_position[cond]["responses"][0]
                / sum(tables_per_position[cond]["responses"].values())
                * 100
            )
        except:
            perc_no = 0
        percs_poses.append(perc_no)

    fig = plt.figure(figsize=(35, 20))
    ax = fig.add_subplot(111)
    random.shuffle(percs_poses)

    for i, perc_no in enumerate(percs_poses):
        ax.bar(i, perc_no, color="k")
        ax.text(i, perc_no + 0.1, str(round(perc_no, 2)))

    ax.set_ylabel("Perc NO")
    ax.set_xlabel("Positions")
    ax.set_ylim([0, 100])

    plt.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)

    plt.savefig(f"{root_path}/data/{folder_name}/figures/perc_no_pos_sdt.png")
