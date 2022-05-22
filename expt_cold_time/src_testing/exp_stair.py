##### HOMEMADE CODE
from classes_arduino import tryexceptArduino, movePanTilt
from grabPorts import grabPorts
from failing import (
    getNames,
    recoverData,
    recoverPickleRick,
    spaceLeftWarning,
    rewriteRecoveredData,
)
from saving_data import (
    create_temp_name,
    saveZaberPos,
    saveROI,
    saveIndv,
    rootToUser,
    changeNameTempFile,
    tempSaving,
    getSubjNumDec,
    buildDict,
    csvToDictGridIndv,
    csvToDictROIAll,
    csvToDictPanTiltsAll,
    txtToVar,
    saveHaxesAll,
    saveIndvVar,
    handle_iti_save,
    copyDict,
)
from local_functions import (
    closeEnvelope,
    thermalCalibration,
    arduinos_zabers,
    trigger_handle_reload,
    panicButton,
    homeButton,
    iti_zaber_dance_in,
    iti_zaber_dance_away,
    triggered_exception,
    deltaToZaberHeight,
    grabNextPosition,
)
from classes_audio import Sound
from index_funcs import parsing_situation, mkpaths
from classes_camera import TherCam

from classes_text import binary_response, printme
from staircases import Staircase

from globals import (
    grid,
    ROIs,
    PanTilts,
    delay_data_display,
    haxes,
    initial_staircase_temp,
    time_out_ex,
    size_ROI,
    question,
    step_sizes,
    time_out_tb,
    lower_bound_delay,
    higher_bound_delay,
    min_bound_staircase,
    centreROI,
    positions,
    max_bound_staircase,
    rule_down,
    rule_up,
    size_down,
    size_up,
)

##### READY-MADE CODE
import threading
import numpy as np
import os
import time
import simpleaudio as sa
import keyboard

if __name__ == "__main__":
    try:
        # Grab ports
        ports = grabPorts()
        print(ports.ports)

        spaceLeftWarning()

        # Check experimental situation, check and/or create folders
        situ, day, n_staircase = parsing_situation()

        subject_n = getSubjNumDec(day=day)
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )
        path_day_bit = path_day.rsplit("/", 3)[-1]

        # Data stuff
        data = buildDict(
            "subject",
            "trial",
            "delta_stimulation",
            "delta_target",
            "reversed",
            "response",
            "reaction_time",
            "time_delay",
            "stimulus_time",
            "position",
            "failed",
            "n_block",
            "within_block_counter",
        )
        temp_data = copyDict(data)
        temp_data["subject"] = subject_n

        failed_name = f"data_failedstaircase"

        # Check whether data and recover
        names_data_failed = getNames(path_data, f"{failed_name}.*\.csv")
        name_temp_file = create_temp_name(failed_name)

        _, temp_file, temp_file_name = tempSaving(
            path_data, list(data.keys()), temp_file_name=name_temp_file
        )

        data = recoverData(names_data_failed, path_data, data)
        rewriteRecoveredData(data, path_data, temp_file_name)

        ################### LOAD HARDWARE ##################
        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()

        ### THERMAL CAMERA
        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)

        if situ == "ex":
            stop_reversals = 25
            time_out = time_out_ex

        elif situ == "tb":
            stop_reversals = 5
            time_out = time_out_tb

        name_staircase_file = f"online_back_up_staircases"
        if os.path.exists(f"{path_data}/{name_staircase_file}.pkl"):
            printme(f"RECOVERING staircase dict")
            staircase = recoverPickleRick(path_data, name_staircase_file)
        else:
            staircase = Staircase(
                total_reversals=stop_reversals,
                initial=initial_staircase_temp,
                direction="down",
            )

        printme(staircase)
        trial_positions = []
        limit = 3

        # Recover information
        grid["camera"] = csvToDictGridIndv(path_data, "temp_grid_camera.csv")
        grid["colther"] = csvToDictGridIndv(path_data, "temp_grid_colther.csv")
        grid["tactile"] = csvToDictGridIndv(path_data, "temp_grid_tactile.csv")
        ROIs = csvToDictROIAll(path_data)
        PanTilts = csvToDictPanTiltsAll(path_data)
        subject_n = txtToVar(path_data, "temp_subj_n")

        print(f"\nROIs: {ROIs}\n")
        print(f"\nPanTilts: {PanTilts}\n")
        print(f"\nHaxes: {haxes}")
        print(f"\nGrids Colther: {grid['colther']}\n")
        print(f"\nGrids Camera: {grid['camera']}\n")
        print(f"\nGrids Tactile: {grid['tactile']}\n")
        time.sleep(delay_data_display)

        ### AUDIO
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

        # get positions with constraints online
        while staircase.reversals < staircase.total_reversals:
            # Interblock
            if keyboard.is_pressed("s"):
                (
                    _,
                    staircase.block,
                    staircase.within_block_counter
                ) = trigger_handle_reload(
                    zabers=zabers,
                    platform=platform1,
                    arduino_syringe=arduino_syringe,
                    arduino_pantilt=arduino_pantilt,
                    cam=cam,
                    n_block=staircase.block,
                    within_block_counter=staircase.within_block_counter,
                    arduino_dimmer=arduino_dimmer,
                )

            tryexceptArduino(arduino_syringe, 6)

            # Prepare position ZABERS
            randomly_chosen_next, trial_positions = grabNextPosition(trial_positions, limit)
            temp_data["position"] = randomly_chosen_next
            cROI = ROIs[temp_data["position"]]

            # Feedback closure + TONE
            ev = threading.Event()
            beep_trial = threading.Thread(
                target=beep.play,
                args=[ev],
                daemon=True,
                name = "Beep thread"
            )
            beep_trial.start()

            movePanTilt(arduino_pantilt, PanTilts[temp_data["position"]])

            grid["colther"]["z"] = deltaToZaberHeight(
                staircase.stimulation, grid, temp_data["position"], step_sizes
            )

            iti_zaber_dance_in(
                zabers, arduino_pantilt, temp_data["position"], PanTilts, grid
            )

            printme(f"Trial number: {staircase.trial}")
            printme(f"Grid position: {temp_data['position']}")
            printme(f"Delta stimulation: {staircase.stimulation}")
            printme(f"Delta tracked stimulation: {staircase.tracked_stimulation}")
            printme(f"Block number: {staircase.block}")
            printme(f"Within block trial counter: {staircase.within_block_counter}")
            printme(
                f"Within block SUCCESSFUL trial counter: {staircase.within_block_successful_counter}"
            )

            file_path = (
                path_videos
                + "/"
                + f"staircase_trial{staircase.trial}_delta{round(staircase)}_pos{temp_data['position']}"
            )

            cam.targetTempAutoDiffDelta(
                file_path,
                staircase.stimulation,
                cROI,
                r = size_ROI,
                arduino = arduino_syringe,
                stimulus = 2,
                total_time_out = time_out,
                event_camera = ev,
            )

            # ############### Terminate trial
            sa.stop_all()

            ### ANSWER
            print("HEIGHT IS:",  grid["colther"]["z"])
            if not cam.failed_trial:
                temp_data["time_delay"] = np.random.uniform(
                    lower_bound_delay, higher_bound_delay
                )
                time.sleep(temp_data["time_delay"])

                beep_speech_success.play()
                temp_data["response"], temp_data["reaction_time"] = binary_response(
                    question
                )
                response = temp_data["response"]
            else:
                response = 3
                time_response_end = 0

            if not cam.failed_trial:
                beep_speech_success.play()

            if cam.shutter_open_time < 0.4:
                cam.failed_trial = True

            if not cam.failed_trial:
                print("SUCCESSFUL stimulation")
                staircase.reversal(temp_data["response"])
                staircase.within_block_successful_counter += 1

            if cam.failed_trial == True:
                temp_data["trial"] = 0
            else:
                temp_data["trial"] = staircase.trial

            temp_data["n_block"] = staircase.block
            temp_data["delta_stimulation"] = staircase.stimulation
            temp_data["delta_target"] = staircase.tracked_stimulation
            temp_data["reversed"] = staircase.reversed_bool
            temp_data["stimulus_time"] = cam.shutter_open_time
            temp_data["failed"] = cam.failed_trial
            temp_data["within_block_counter"] = staircase.within_block_counter

            data = handle_iti_save(
                list(temp_data.values()), data, path_data, temp_file_name
            )

            # Tracking algorithm
            if not cam.failed_trial:
                print("we are here")
                staircase.XupYdownFixedStepSizesTrackingAlgorithm(
                    rule_down,
                    rule_up,
                    size_down,
                    size_up,
                    0.2
                )

            staircase.clampBoundary(min_bound_staircase, max_bound_staircase)

            printme(f"Staircase reversals: {staircase.reversals}")

            if cam.failed_trial == False:
                staircase.last_response = int(response)

            tryexceptArduino(arduino_syringe, 4)

            if cam.failed_trial == False:
                staircase.trial += 1

            staircase.within_block_counter += 1

            staircase.saveStaircase(path_data, name_staircase_file)

            iti_zaber_dance_away(zabers)

            panicButton()
            homeButton(zabers, arduino_pantilt)

        saveZaberPos("temp_zaber_pos", path_data, positions)
        saveROI("temp_ROI", path_data, centreROI)
        saveHaxesAll(path_data, haxes)

        name_subj_file = f"data_staircase_subj"
        saveIndv(name_subj_file, path_data, data)
        changeNameTempFile(path_data, outcome="success")
        if os.path.exists(f"./src_testing/temp_folder_name.txt"):
            os.remove(f"./src_testing/temp_folder_name.txt")
        saveIndvVar("./src_testing", path_day_bit, "temp_folder_name")

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

        closeEnvelope(
            zabers, platform1, arduino_syringe, arduino_pantilt, arduino_dimmer
        )

    except Exception as e:
        triggered_exception(
            path_day=path_day,
            path_anal=path_anal,
            path_data=path_data,
            path_figs=path_figs,
            path_videos=path_videos,
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_pantilt=arduino_pantilt,
            arduino_dimmer=arduino_dimmer,
            e=e,
            outcome=f"failedstaircase",
        )

    except KeyboardInterrupt:
        triggered_exception(
            path_day=path_day,
            path_anal=path_anal,
            path_data=path_data,
            path_figs=path_figs,
            path_videos=path_videos,
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_pantilt=arduino_pantilt,
            arduino_dimmer=arduino_dimmer,
            outcome=f"failedstaircase",
        )
