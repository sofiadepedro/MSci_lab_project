#### OWN LIBRARIES
from saving_data import rootToUser, saveIndvVar
from index_funcs import parsing_situation, getSubjNumDec, mkpaths
from failing import errorloc, recoverPickleRick

if __name__ == "__main__":
    try:
        situ, day, n_staircase = parsing_situation()
        subject_n = getSubjNumDec(day=day)
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

        # Recover data
        name_staircase_file = "online_back_up_staircases"
        staircase1 = recoverPickleRick(path_data, name_staircase_file)

        staircase1.estimateValue()
        print(staircase1.estimated_point)
        saveIndvVar(path_data, staircase1.estimated_point, "temp_delta")
        staircase1.plotStaircase(path_figs, "staircase", "Delta", [0, 3])

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)
