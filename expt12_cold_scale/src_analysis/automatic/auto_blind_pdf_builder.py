# %%
import numpy as np
import pandas as pd
from sdt_analysis import *
import random
import matplotlib.pyplot as plt
import os
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, portrait, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PyPDF2 import PdfFileMerger
from classes_tharnal import *
from classes_plotting import *
from datetime import date
import pandas as pd
import time
import argparse
from saving_data import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Folder name")
    parser.add_argument("-f", type=str)
    args = parser.parse_args()
    folder_name = args.f

    name_figures = [
        "staircase",
        "perc_no_pos_staircase",
        "perc_correct_A",
        "perc_correct_B",
        "perc_correct_C",
        "ab_correct_A",
        "ab_correct_B",
        "ab_correct_C",
        "hr_fa_rates_A",
        "hr_fa_rates_B",
        "hr_fa_rates_C",
        "d_prime_A",
        "d_prime_B",
        "d_prime_C",
        "c_bias_A",
        "c_bias_B",
        "c_bias_C",
        "perc_no_pos_sdt",
        "time_dist_sdt_pos1",
        "time_dist_sdt_pos2",
        "time_dist_sdt_pos3",
        "time_dist_sdt_pos4",
        "time_dist_staircase_pos1",
        "time_dist_staircase_pos2",
        "time_dist_staircase_pos3",
        "time_dist_staircase_pos4",
    ]

    path = os.path.realpath(__file__)
    root_path = path.rsplit("/", 3)[0]

    table_data = pd.read_csv(f"{root_path}/data/{folder_name}/data/data_all.csv")

    nofailed_table_data = table_data.loc[table_data["failed"] == False]
    nofailed_table_data = nofailed_table_data.loc[
        nofailed_table_data["stimulus_time"] > 0.4
    ]

    cleaned_table_data = nofailed_table_data.loc[table_data["fake"] == 0]
    cleaned_table_data = cleaned_table_data.loc[table_data["responses"] != 2]

    tables_per_condition = {}
    conds = [0, 1, 2]
    names_blind = ["A", "B", "C"]

    blind_touch = [0, 1]

    random.shuffle(blind_touch)

    while len(conds) > 0:
        random.shuffle(conds)
        random.shuffle(names_blind)

        chosen = conds.pop(0)
        chosen_label = names_blind.pop(0)

        tables_per_condition[chosen_label] = {
            "table": cleaned_table_data.loc[cleaned_table_data["condition"] == chosen]
        }

    for i in ["A", "B", "C"]:
        tables_per_condition[i][f"correct_{blind_touch[0]}"] = correctPercSDT(
            tableTosdtDoble(tables_per_condition[i]["table"], 1)
        )
        tables_per_condition[i][f"correct_{blind_touch[1]}"] = correctPercSDT(
            tableTosdtDoble(tables_per_condition[i]["table"], 0)
        )

        tables_per_condition[i][f"sdt_{blind_touch[0]}"] = SDTloglinear(
            tables_per_condition[i][f"correct_{blind_touch[0]}"]["hits"],
            tables_per_condition[i][f"correct_{blind_touch[0]}"]["misses"],
            tables_per_condition[i][f"correct_{blind_touch[0]}"]["fas"],
            tables_per_condition[i][f"correct_{blind_touch[0]}"]["crs"],
        )
        tables_per_condition[i][f"sdt_{blind_touch[1]}"] = SDTloglinear(
            tables_per_condition[i][f"correct_{blind_touch[1]}"]["hits"],
            tables_per_condition[i][f"correct_{blind_touch[1]}"]["misses"],
            tables_per_condition[i][f"correct_{blind_touch[1]}"]["fas"],
            tables_per_condition[i][f"correct_{blind_touch[1]}"]["crs"],
        )

        all_in = [
            tables_per_condition[i][f"correct_{blind_touch[0]}"][f"correc_present"],
            tables_per_condition[i][f"correct_{blind_touch[0]}"]["correc_absent"],
            tables_per_condition[i][f"correct_{blind_touch[1]}"]["correc_present"],
            tables_per_condition[i][f"correct_{blind_touch[1]}"]["correc_absent"],
        ]

        # print(tables_per_condition[i][f"correct_{blind_touch[0]}"])

        ab_in = [
            tables_per_condition[i][f"sdt_{blind_touch[0]}"]["correct"],
            tables_per_condition[i][f"sdt_{blind_touch[1]}"]["correct"],
        ]

        all_in = np.asarray(all_in)
        ab_in = np.asarray(ab_in)

        ####################################
        ### PLOT PERC CORRECT  'perc_correct_A', 'perc_correct_B', 'perc_correct_C',
        ####################################
        fig, ax = plt.subplots(figsize=(5, 3))

        ax.bar(np.arange(1, len(all_in) + 0.1, 1), all_in)

        for index, xpos in enumerate(np.arange(1, len(all_in) + 0.1, 1)):
            ax.text(xpos, all_in[index] + 0.1, str(round(all_in[index], 2)))
        ax.set_xticks([1, 2, 3, 4])
        ax.set_ylim([0, 1])
        ax.set_yticks(np.arange(0, 1.01, 0.1))

        ax.set_ylabel("Perc correct")
        ax.set_title(f"{i}")

        plt.savefig(f"{root_path}/data/{folder_name}/figures/perc_correct_{i}.png")
        fig.clf()

        ####################################
        ### PLOT PERC CORRECT within sdt condition 'ab_correct_A', 'ab_correct_B', 'ab_correct_C',
        ####################################
        fig, ax = plt.subplots(figsize=(5, 3))

        ax.bar(np.arange(1, len(ab_in) + 0.1, 1), ab_in)

        for index, xpos in enumerate(np.arange(1, len(ab_in) + 0.1, 1)):
            ax.text(xpos, ab_in[index] + 0.1, str(round(ab_in[index], 2)))

        ax.set_xticks([1, 2])
        ax.set_ylim([0, 1])

        ax.set_ylabel("Perc correct")
        ax.set_title(f"{i}")
        ax.set_yticks(np.arange(0, 1.01, 0.1))

        plt.savefig(f"{root_path}/data/{folder_name}/figures/ab_correct_{i}.png")
        fig.clf()

        ####################################
        ### HIT AND FA RATE 'hr_fa_rates_A', 'hr_fa_rates_B', 'hr_fa_rates_C',
        ####################################
        fig, ax = plt.subplots(figsize=(5, 3))

        hits_fas = [
            tables_per_condition[i][f"sdt_{blind_touch[0]}"][f"hit_rate"],
            tables_per_condition[i][f"sdt_{blind_touch[0]}"][f"fa_rate"],
            tables_per_condition[i][f"sdt_{blind_touch[1]}"][f"hit_rate"],
            tables_per_condition[i][f"sdt_{blind_touch[1]}"][f"fa_rate"],
        ]
        poses_rates = [1, 2, 3, 4]
        ax.bar(poses_rates, hits_fas)

        for index, xpos in enumerate(poses_rates):
            ax.text(xpos, hits_fas[index] + 0.1, str(round(hits_fas[index], 2)))

        ax.set_xticks(poses_rates)
        ax.set_ylim([0, 1])

        labelsx = [item.get_text() for item in ax.get_xticklabels()]
        ticks_names = [
            "HR-A-loglinear",
            "FA-A-loglinear",
            "HR-B-loglinear",
            "FA-B-loglinear",
        ]

        for j in enumerate(ticks_names):
            labelsx[j[0]] = j[1]

        ax.set_xticklabels(labelsx, rotation=90)
        plt.tight_layout()

        ax.set_ylabel("Rates")

        plt.savefig(f"{root_path}/data/{folder_name}/figures/hr_fa_rates_{i}.png")
        fig.clf()

        ####################################
        ### d PRIME 'd_prime_A', 'd_prime_B', 'd_prime_C',
        ####################################
        fig, ax = plt.subplots(figsize=(5, 3))

        ds_das = [
            tables_per_condition[i][f"sdt_{blind_touch[0]}"]["d"],
            tables_per_condition[i][f"sdt_{blind_touch[1]}"]["d"],
        ]
        poses_ds = [1, 2]
        ax.bar(poses_ds, ds_das)

        for index, xpos in enumerate(poses_ds):
            ax.text(xpos, ds_das[index] + 0.1, str(round(ds_das[index], 2)))

        ax.set_xticks(poses_ds)
        ax.set_ylim([0, 4])

        labelsx = [item.get_text() for item in ax.get_xticklabels()]
        ticks_names = ["d-A-loglinear", "d-B-loglinear"]

        for j in enumerate(ticks_names):
            labelsx[j[0]] = j[1]

        ax.set_xticklabels(labelsx, rotation=90)
        plt.tight_layout()

        ax.set_ylabel("d-prime")

        plt.savefig(f"{root_path}/data/{folder_name}/figures/d_prime_{i}.png")
        fig.clf()

        ####################################
        ### Response bias 'c_bias_A', 'c_bias_B', 'c_bias_C',
        ####################################
        # BEH bias with extremes AND loglinear
        fig, ax = plt.subplots(figsize=(5, 3))

        cs_ces = [
            tables_per_condition[i][f"sdt_{blind_touch[0]}"]["c"],
            tables_per_condition[i][f"sdt_{blind_touch[1]}"]["c"],
        ]

        poses_cs = [1, 2]
        ax.bar(poses_cs, cs_ces)

        for index, xpos in enumerate(poses_cs):
            ax.text(xpos, cs_ces[index] + 0.1, str(round(cs_ces[index], 2)))

        ax.set_xticks(poses_cs)
        ax.set_ylim([-2, 2])

        labelsx = [item.get_text() for item in ax.get_xticklabels()]
        ticks_names = ["c-A-loglinear", "c-B-loglinear"]

        for j in enumerate(ticks_names):
            labelsx[j[0]] = j[1]

        ax.set_xticklabels(labelsx, rotation=90)
        plt.tight_layout()

        ax.set_ylabel("c-prime")
        ax.set_title(f"{i}")

        plt.savefig(f"{root_path}/data/{folder_name}/figures/c_bias_{i}.png")
        fig.clf()

    ############################################################################
    # Time distribution by point SDT
    filename_SDT = "data_all"
    table_data = pd.read_csv(f"{root_path}/data/{folder_name}/data/{filename_SDT}.csv")
    table_cold = table_data.loc[table_data["cold"] == 1]
    table_nocold = table_data.loc[table_data["cold"] == 0]

    cold_bool = np.asarray(table_data["cold"])
    touch_bool = np.asarray(table_data["touch"])
    responses_bool = np.asarray(table_data["responses"])

    for pospos in range(1, 5):
        names_SDT = grabManyvideos(
            root_path, folder_name, pattern=f"sdt_.*\_pos{pospos}.hdf5$"
        )
        times_cold = []

        for isdt, n in enumerate(names_SDT):
            if (isdt + 1) in list(table_cold["trial"]):
                # print(n, isdt +1)
                dat_im = ReAnRaw(f"{root_path}/data/{folder_name}/videos/{n}")
                dat_im.datatoDic()
                try:
                    temp_value = dat_im.data["time_now"][-1][0]
                except:
                    temp_value = 0

                times_cold.append(temp_value)

        # SDT time distribution COLD
        fig, ax = plt.subplots(figsize=(5, 3))

        n, bins, patches = plt.hist(
            times_cold, bins=10, color="k", alpha=0.7, rwidth=0.85
        )

        ax.set_title(f"Time trial distribution COLD stimulation POSITION {pospos}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency")
        ax.set_xlim([0, 14])
        ax.set_ylim(0)
        plt.tight_layout()

        plt.savefig(
            f"{root_path}/data/{folder_name}/figures/time_dist_sdt_pos{pospos}.png"
        )

    ############################################################################
    # Time distribution by point STAIRCASE

    for pospos in range(1, 5):
        names_SDT = grabManyvideos(
            root_path, folder_name, pattern=f"staircase.*\_pos{pospos}.hdf5$"
        )
        times_cold = []

        for isdt, n in enumerate(names_SDT):
            dat_im = ReAnRaw(f"{root_path}/data/{folder_name}/videos/{n}")
            dat_im.datatoDic()
            times_cold.append(dat_im.data["time_now"][-1][0])

        # SDT time distribution COLD
        fig, ax = plt.subplots(figsize=(5, 3))

        n, bins, patches = plt.hist(
            times_cold, bins=10, color="k", alpha=0.7, rwidth=0.85
        )

        ax.set_title(f"Time trial distribution COLD stimulation POSITION {pospos}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency")
        ax.set_xlim([0, 14])
        ax.set_ylim(0)
        plt.tight_layout()

        plt.savefig(
            f"{root_path}/data/{folder_name}/figures/time_dist_staircase_pos{pospos}.png"
        )

    ##############################################################################
    ########################## CREATE PDF SECTION for subj #######################
    ##############################################################################
    try:
        os.remove(f"{root_path}/data/{folder_name}/figures/section_subj.pdf")
    except:
        print("REMOVE")
        pass

    doc = SimpleDocTemplate(
        f"{root_path}/data/{folder_name}/figures/section_subj.pdf",
        pagesize=landscape(A4),
        rightMargin=0,
        leftMargin=0,
        topMargin=18,
        bottomMargin=18,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Justify", alignment=TA_JUSTIFY, fontName="Helvetica-Bold", fontSize=15
        )
    )

    Subj = []

    # n_subj = f'Subject {ns + 1}'

    # Subj.append(Paragraph(n_subj, styles["Justify"]))

    image_table_write = []
    for pair in pairwise(name_figures):

        temp_pair = []
        for partnerfig in pair:
            if partnerfig:
                # print(partnerfig)
                try:
                    graph = Image(
                        f"{root_path}/data/{folder_name}/figures/{partnerfig}.png",
                        5 * inch,
                        3 * inch,
                    )
                    temp_pair.append(graph)
                except:
                    print("COULNT FIND IMAGE")
                    pass

        image_table_write.append(temp_pair)

    table = Table(image_table_write)

    # failed_total = [f"Failed touch trials: {temp_summary['failed-touch']}",
    #                 f"Failed no touch trials: {temp_summary['failed-notouch']}",
    #                 f"Usable touch trials: {temp_summary['usable-touch']}",
    #                 f"Usable no touch trials: {temp_summary['usable-notouch']}"]

    Subj.append(table)
    # for ft in failed_total:
    #     Subj.append(Paragraph(ft, styles["Justify"]))

    doc.build(Subj)
