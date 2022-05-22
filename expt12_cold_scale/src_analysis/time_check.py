# %%
import os
import matplotlib.pyplot as plt 

from local_functions import(
    CondShuffle,
    textMakeUp,
    get_folder_path,
    getSuccData,
    parseDeltasResponses,
    universalMakeUp
)


if __name__ == "__main__":
    # SET PATHS
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

            if os.path.isfile(f'{folder_path}/{scaling_data}.csv') and os.path.isfile(f'{folder_path}/{staircase_data}.csv'):
               
                ## GETTING DATA
                scaling_df_succ = getSuccData(test_state="test", subj=todaydate)

                scaling_touch_conds = {
                    n1 : {"color": c1},
                    n2 : {"color": c2},
                }

                scaling_touch_conds, deltas = parseDeltasResponses(scaling_df_succ, scaling_touch_conds)
                        

                ## PLOT
                path_figures = "/Users/sofia/Documents/masters_project/expt12_cold_scale/globalfigures"
                figure_name = f"time_response_blindcheck_test_{todaydate}"

                fig, ax = plt.subplots(1, 1, figsize=(20, 15))
                
                for cond in scaling_touch_conds.keys():
                    plt.scatter(
                        list(scaling_touch_conds[cond]["table"]["stimulus_time"]), 
                        list(scaling_touch_conds[cond]["table"]["response"]), 
                        c = scaling_touch_conds[cond]["color"]
                    )
                
                universalMakeUp(ax, lwd, pad_size, lenD)
            
                ax.set_xlim(0, 11)
                ax.set_ylim(-10, 110)
                ax.set_xlabel("Time (s)", labelpad=pad_size)
                ax.set_ylabel("Perceived intensity")
                ax.set_title("Time Check", pad=60)
                plt.savefig(f"{path_figures}/{figure_name}.png", transparent=True)