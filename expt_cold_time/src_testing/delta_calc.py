from saving_data import rootToUser, saveIndvVar, csvToDictGridIndv, saveGridIndv
from index_funcs import parsing_situation, getSubjNumDec, mkpaths
from failing import errorloc, recoverPickleRick
from globals import grid, step_sizes
from classes_text import printme
from local_functions import deltaToZaberHeight

if __name__ == "__main__":
    try:
        situ, day, n_staircase = parsing_situation()
        subject_n = getSubjNumDec(day=day)
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

        # Import data data
        grid["colther"] = csvToDictGridIndv(path_data, "temp_grid_colther.csv")
        grid["tactile"] = csvToDictGridIndv(path_data, "temp_grid_tactile.csv")
        name_staircase_file = "online_back_up_staircases"
        staircase = recoverPickleRick(path_data, name_staircase_file)

        # Get delta estimation
        staircase.estimateValue()
        printme(f"Estimated point: {staircase.estimated_point}")
        # Save delta estimation
        saveIndvVar(path_data, staircase.estimated_point, "temp_delta")
        # Plot staircase and save
        staircase.plotStaircase(path_figs, "staircase", "Delta", [0, 3], show=False)

        # Calculate colther height for each position with estimated delta
        for position in grid["camera"].keys():
            grid["colther"][position]["z"] = deltaToZaberHeight(
                staircase.estimated_point, grid, position, step_sizes
            )
        # Save colther grid
        saveGridIndv(f"temp_grid", path_data, grid, "colther")

        # Set folder permissions to current user
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)
