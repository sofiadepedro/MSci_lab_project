import os
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt

def get_delta(list_splitted, delta):
    for i in range(len(list_splitted)):
        if list_splitted[i].startswith(delta):
            return list_splitted[i]


def get_numbers(string):
    extracted_value =[int(s) for s in re.findall(r'\d+', string)]
    int_value = extracted_value[0]
    return int_value


def get_folder_path(path, foldername):
    list_splitted = foldername.split("_")
    todaydate = f"{list_splitted[1]}_{list_splitted[2]}"
    folder_path = path + f"/test_{todaydate}/data"
    return folder_path, todaydate


def CreateFile(path, filepath, llaves):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(filepath):
        file = open(filepath, "a")
        file_writer = csv.writer(file)
        file_writer.writerow(llaves)

def save_all_data(filepath, dict_name, subject):
    if os.path.getsize(filepath) == 0:
        file = open(filepath, "a")
        file_writer = csv.writer(file)
        file_writer.writerow(list(dict_name.values()))
        file.close()

    else:
        load_data = pd.read_csv(filepath, delimiter=',')

        df =  pd.DataFrame(load_data)
        # print(df)

        if subject not in df.values:
            print("\nThis value does not exists in Dataframe")
            file = open(filepath, "a")
            file_writer = csv.writer(file)
            file_writer.writerow(list(dict_name.values()))
            file.close()

        else:
            print("\nThis value exists in Dataframe")
            file = open(filepath, "a")
            file_writer = csv.writer(file)
            file_writer.writerow(list(dict_name.values()))
            file.close()

def universalMakeUp(ax, lwd, pad_size, lenD):

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_linewidth(lwd)
    ax.spines["bottom"].set_linewidth(lwd)
    ax.yaxis.set_tick_params(width=lwd, length=lenD)
    ax.xaxis.set_tick_params(width=lwd, length=lenD)
    ax.tick_params(axis="y", which="major", pad=pad_size)
    ax.tick_params(axis="x", which="major", pad=pad_size)

def textMakeUp(mc):
    plt.rcParams.update(
        {
            "font.size": 40,
            "axes.labelcolor": "{}".format(mc),
            "xtick.color": "{}".format(mc),
            "ytick.color": "{}".format(mc),
            "font.family": "sans-serif",
        }
    )