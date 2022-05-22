# %%
### SCRIPT TO CHECK THE % OF 0 RESPONSES AT THRESHOLD VALUE
import os
import matplotlib.pyplot as plt

from local_functions import(
    CondShuffle,
    textMakeUp,
    get_folder_path,
    getSuccData,
    parseDeltasResponses,
    getThreshold,
    get_percentage_correct,
    universalMakeUp
) 

if __name__ == "__main__":

    ## SET PATHS
    path = "/Users/sofia/Documents/masters_project/expt12_cold_scale/data"
    scaling_data = "data_scaling_subj"
    staircase_data = "data_staircase1_subj"

    ## SHUFFLE CONDITIONS NAME
    n1, n2, c1, c2 = CondShuffle()

    #PLOT STUFF
    s_size = 100
    s_mean = 400
    lwd = 10
    pad_size = 20
    lenD = 15
    mc = "black"
    lateral_wiggle = 0.2

    textMakeUp(mc)

    ## GO THROUGH FOLDERS & LOOK FOR SCALING SCRIPT
    for foldername in os.listdir(path):
        if foldername.startswith("test_"):

            folder_path, todaydate = get_folder_path(path, foldername)
            subject = "test" + "_" + todaydate

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv'):

                ## GETTING DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)

                scaling_touch_conds = {
                    n1 : {"color": c1},
                    n2 : {"color": c2},
                }

                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)
                

                if os.path.isfile(f'{folder_path}/{staircase_data}.csv'):
                    ## GET THRESHOLD
                    threshold_value = getThreshold(test_state="test", subj=todaydate)

                    ## FIGURE PATH
                    path_figures = "/Users/sofia/Documents/masters_project/expt12_cold_scale/globalfigures"
                    figure_name = f"zeros_blindcheck_test_{todaydate}"
                    fig, ax = plt.subplots(1, 1, figsize=(20, 15))

                    for cond in scaling_touch_conds.keys():
                        ## GET % ZEROS
                        list_percentage_zeros = []
                        for delta in deltas:
                            ## GET RESPONSES FOR DELTAS
                            response = list(scaling_touch_conds[cond][f"scaling_delta{delta}_response_list"])

                            print("delta", delta)
                            print("responses", response)

                            ## GET PERCENTAGE OF 0 IN THOSE RESPONSES
                            percentage_zeros = get_percentage_correct(response, 0)
                            list_percentage_zeros.append(percentage_zeros)

                            print(f"Percentage of 0 for delta {delta} is {percentage_zeros}")
                        
                        ## PLOT
                        plt.plot(deltas, list_percentage_zeros, color = scaling_touch_conds[cond]["color"], lw = lwd)
                        plt.axvline(x = threshold_value, color = 'orange', label = 'threshold', linestyle = "dashed", lw = lwd)

                
                    universalMakeUp(ax, lwd, pad_size, lenD)

                    ax.set_xticks(deltas)

                    ax.set_ylim(-10, 110)
                    ax.set_xlabel("ΔT", labelpad=pad_size)
                    ax.set_ylabel("Percentage Zeros")
                    ax.set_title("Percentage of 0 per delta", pad=60)
                    
                    plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)