################################ Import stuff ################################
from grabPorts import grabPorts
import globals
from classes_colther import (
    movetostartZabersConcu,
    grid_calculation,
    homingZabersConcu,
)
from saving_data import (
    rootToUser,
    saveIndvVar,
    numberSubjDay,
    apendSingle,
    setSubjNumDec,
    saveGridIndv,
    check_file_path_save,
)
from classes_text import (
    agebyExperimenter,
    printme,
    sexbyExperimenter,
    handednessbyExperimenter,
)
from failing import pusherWarning, spaceLeftWarning
from index_funcs import parsing_situation, mkpaths
from local_functions import (
    closeEnvelope,
    arduinos_zabers,
    shrink_grid,
    triggered_exception,
)

import os

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        pusherWarning(n_pushes=3000)
        spaceLeftWarning()

        situ, day, _ = parsing_situation()
        print(day)

        if situ == "tb":
            subject_n = numberSubjDay()
        elif situ == "ex":
            subject_n = numberSubjDay("y")

        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )
        path_day_bit = path_day.rsplit("/", 3)[-1]

        if os.path.exists(f"./src_testing/temp_folder_name.txt"):
            os.remove(f"./src_testing/temp_folder_name.txt")

        saveIndvVar("./src_testing", path_day_bit, "temp_folder_name")

        if situ == "tb":
            age = 1
            sex = 0
            handedness = 3
        elif situ == "ex":
            age = agebyExperimenter()
            handedness = handednessbyExperimenter()
            sex = sexbyExperimenter()

        print(f"\nSubject's number within day: {subject_n}\n")
        print(f"\nSubject's age: {age}\n")

        todaydate, time_now = setSubjNumDec(age, subject_n, situ)

        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()

        # Save age, sex and subject number
        check_file_path_save(path_data, "age", age, subject_n)
        check_file_path_save(path_data, "sex", sex, subject_n)
        check_file_path_save(path_data, "handedness", handedness, subject_n)
        saveIndvVar(path_data, subject_n, "temp_subj_n")

        #### MOVE TO FIRST POINT: DEFAULT POSITION
        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(globals.haxes["colther"])),
            pos=globals.dry_ice_pos,
        )

        height_check = False
        globals.grid["tactile"] = grid_calculation("tactile", globals.separation_grid, pos=globals.positions)
        globals.grid["tactile"] = shrink_grid(globals.grid["tactile"])
        print(globals.grid["tactile"])

        input("Press enter when you are ready to find the heights")

        movetostartZabersConcu(
            zabers,
            "tactile",
            globals.haxes["tactile"],
            pos=globals.grid["tactile"]["1"],
        )

        while not height_check:
            #### Get grid positions for touch
            ### Move Zaber TOUCH to each position
            zabers["colther"]["x"].gridUpDown(zabers, "tactile")

            #     homingZabersConcu(zabers, globals.haxes)
            #     #### Check whether we are happy with grid positions
            while True:
                ans = input("\nAre we happy with the touch position? (y/n)  ")
                if ans[-1] in ("y", "n"):
                    if ans[-1] == "y":
                        # print(ans)
                        height_check = True
                        break
                    else:

                        break

                else:
                    printme("Only 'y' and 'n' are valid responses")

        globals.grid = zabers["colther"]["x"].gridZs
        homingZabersConcu(zabers, globals.haxes)

        # save all z axis positions
        saveGridIndv("temp_grid", path_data, globals.grid, "tactile")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

        #### HOMER ARDUINOS & ZABERS
        closeEnvelope(
            zabers, platform1, arduino_syringe, arduino_pantilt, arduino_dimmer
        )

    except Exception as e:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_pantilt=arduino_pantilt,
            arduino_dimmer=arduino_dimmer,
            e=e,
        )

    except KeyboardInterrupt:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_pantilt=arduino_pantilt,
            arduino_dimmer=arduino_dimmer,
        )
