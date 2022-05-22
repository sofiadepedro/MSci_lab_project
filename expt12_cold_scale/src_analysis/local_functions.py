import os
import csv
from this import d
import pandas as pd
from failing import recoverPickleRick
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, norm
import re
import statistics
import random

Z = norm.ppf

## PLOTS
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

def plot_alldata(x, y, c, lateral_wiggle, s_size):
    plt.scatter(
            np.random.uniform(
                (x[0] - lateral_wiggle), (x[0] + lateral_wiggle), size=len(x)
            ),
            y,
            c = c,
            alpha=0.5,
            s=s_size,
        )

def plot_linregression(x, y, c, lwd, label):
    (slope, intercept, rvalue, pvalue, stderr) = linregress(x,y)

    y_pred = intercept + slope*np.array(x)
    plt.plot(x,y_pred, color=c, lw=lwd, label=label)
    plt.legend(frameon=False)


## DATA
def getData(test_state, subj):
    path_data = "../data"

    test_state = test_state
    subj = subj
    file_name = "data_scaling_subj"

    scaling_df = pd.read_csv(f"{path_data}/{test_state}_{subj}/data/{file_name}.csv")
    return scaling_df


def getSuccData(test_state, subj):
    scaling_df = getData(test_state, subj)
  
    scaling_df_succ = scaling_df.loc[scaling_df["failed"] == False]
    return scaling_df_succ


def get_linregression(x, y, cond):
    (slope, intercept, rvalue, pvalue, stderr) = linregress(x,y)
    return slope, intercept


def getThreshold(test_state, subj):

    folder_name = test_state + "_" + subj

    path_data = f"../data/{folder_name}/data/"

    name_staircase_file = "online_back_up_staircases1"
    staircase1 = recoverPickleRick(path_data, name_staircase_file)

    staircase1.estimateValue()
    return staircase1.estimated_point


def get_delta(list_splitted, delta):
    for i in range(len(list_splitted)):
        if list_splitted[i].startswith(delta):
            return list_splitted[i]


def get_numbers(string):
    extracted_value =[int(s) for s in re.findall(r'\d+', string)]
    int_value = extracted_value[0]
    return int_value

def extractAnchoringDataFrame(df):
    index = df.loc[df['subject'] == "subject"].iloc[-1].name + 1
    sub_df = df.loc[index:]

    data_frame = pd.DataFrame(sub_df)

    return data_frame


def parseDeltasResponses(scaling_df_succ, scaling_touch_conds):
    for ind, cond in enumerate(scaling_touch_conds.keys()):
        scaling_touch_conds[cond]["table"] = scaling_df_succ.loc[
            scaling_df_succ["touch"] == ind
        ]
        deltas = scaling_touch_conds[cond]["table"]["delta_stimulation"].unique()
        deltas = np.sort(deltas)
        scaling_touch_conds[cond]["scaling_means"] = []

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
    return scaling_touch_conds, deltas


def get_folder_path(path, foldername):
    list_splitted = foldername.split("_")
    todaydate = f"{list_splitted[1]}_{list_splitted[2]}"
    folder_path = path + f"/test_{todaydate}/data"
    return folder_path, todaydate

def get_percentage_correct(all_values_list, delta):
    percentage = (all_values_list.count(delta)/len(all_values_list))*100
    return percentage

def getStandardDev(sample):
    standard_dev = statistics.stdev(sample)
    return standard_dev

def CondShuffle():
    name = ["1", "2"]
    random.shuffle(name)
    n1 = name.pop(0)
    n2 = name.pop(0)

    color = ["#794493", "#477DBD"]
    random.shuffle(color)
    c1 = color.pop(0)
    c2 = color.pop(0)

    return n1, n2, c1, c2


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

def nearest_largest_value2 (n, values):
    return min(v for v in values if v >= n)


def sdt_in_scaling(response_0, response_x):
    cold_present = np.array(response_x)

    present_yes = list(cold_present[np.nonzero(cold_present)])
    print(present_yes)

    present_no = list(cold_present[np.where(cold_present == 0)])
    print(present_no)


    cold_absent = np.array(response_0)

    absent_yes = list(cold_absent[np.nonzero(cold_absent)])
    print(absent_yes)

    absent_no = list(cold_absent[np.where(cold_absent == 0)])
    print(absent_no)

    hits = len(present_yes)
    misses = len(present_no)
    fas = len(absent_yes)
    crs = len(absent_no)

    # Floors an ceilings are replaced by half hits and half FA's
    half_hit = 0.5 / (hits + misses)
    half_fa = 0.5 / (fas + crs)

    # Calculate hit_rate and avoid d' infinity
    hit_rate = hits / (hits + misses)
    if hit_rate == 1:
        hit_rate = 1 - half_hit
    if hit_rate == 0:
        hit_rate = half_hit

    # Calculate false alarm rate and avoid d' infinity
    fa_rate = fas / (fas + crs)
    # print(fa_rate)
    if fa_rate == 1:
        fa_rate = 1 - half_fa
    if fa_rate == 0:
        fa_rate = half_fa

    print(hit_rate)
    print(fa_rate)

    # Return d', and c
    d = Z(hit_rate) - Z(
            fa_rate
        )  # Hint: normalise the centre of each curvey and subtract them (find the distance between the normalised centre

    c = (
        Z(hit_rate) + Z(fa_rate)
    ) / 2 

    print("d_touch is:", d)
    print("c_touch is:", c)

    return hit_rate, fa_rate, d, c