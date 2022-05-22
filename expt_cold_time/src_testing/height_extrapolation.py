################################ Import stuff ################################
from grabPorts import grabPorts
from globals import (
    grid,
    positions,
    step_sizes,
    separation_grid,
    initial_staircase_temp,
)
from classes_colther import grid_calculation
from saving_data import (
    csvToDictGridIndv,
    rootToUser,
    getSubjNumDec,
    saveGridIndv,
)
from failing import errorloc
from index_funcs import parsing_situation, mkpaths
from local_functions import shrink_grid, deltaToZaberHeight

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        situ, day, _ = parsing_situation()
        print(day)

        subject_n = getSubjNumDec(day=day)
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )
        path_day_bit = path_day.rsplit("/", 3)[-1]

        # Save age and subject number
        grid["tactile"] = csvToDictGridIndv(path_data, "temp_grid_tactile.csv")

        grid["colther"] = grid_calculation("colther", separation_grid, pos=positions)
        grid["camera"] = grid_calculation("camera", separation_grid, pos=positions)

        grid["colther"] = shrink_grid(grid["colther"])
        grid["camera"] = shrink_grid(grid["camera"])

        for position in grid["camera"].keys():
            grid["colther"][position]["z"] = deltaToZaberHeight(
                initial_staircase_temp, grid, position, step_sizes
            )

        # save all z axis positions
        print(grid)
        # saveGridAll(path_data, grid)
        saveGridIndv(f"temp_grid", path_data, grid, "camera")
        saveGridIndv(f"temp_grid", path_data, grid, "colther")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
