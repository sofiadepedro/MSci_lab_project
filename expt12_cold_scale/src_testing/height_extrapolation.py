################################ Import stuff ################################
from grabPorts import grabPorts
from globals import grid, positions, colther_heights, step_sizes, diff_colther_touch, separation_grid
from classes_colther import grid_calculation, cm_to_steps, steps_to_cm
from saving_data import (
    csvToDictGridIndv,
    rootToUser,
    getSubjNumDec,
    saveGridAll,
    saveGridIndv,
)
from failing import errorloc
from index_funcs import parsing_situation, mkpaths
from local_functions import shrink_grid

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

        for mags in colther_heights.keys():
            # calculate z for each distance
            for v in grid["camera"].keys():
                print(v)
                z_cm_colther = (
                    steps_to_cm(grid["tactile"][v]["z"], step_sizes["tactile"])
                    + steps_to_cm(diff_colther_touch, step_sizes["colther"])
                    - colther_heights[mags]
                )
                grid["colther"][v]["z"] = cm_to_steps(
                    z_cm_colther, step_sizes["colther"]
                )

            saveGridIndv(
                f"temp_grid_{str(round(float(mags)*10))}", path_data, grid, "colther"
            )

        # save all z axis positions
        print(grid)
        # saveGridAll(path_data, grid)
        saveGridIndv(f"temp_grid", path_data, grid, "camera")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")


# for z_d in globals.z_ds.keys():
#     for k in globals.grid["tactile"].keys():
#         globals.grid[z_d][k]["z"] = globals.grid["tactile"][k]['z'] - globals.z_ds[z_d]
#         print(globals.z_ds)
