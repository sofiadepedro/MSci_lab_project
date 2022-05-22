##### HOMEMADE CODE
from classes_arduino import tryexceptArduino, movePanTilt
from grabPorts import grabPorts
from failing import (
    getNames,
    recoverData,
    recoveredToTempWriter,
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
    appendDataDict,
    saveHaxesAll,
    saveIndvVar,
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
)
from classes_audio import Sound
from index_funcs import parsing_situation, mkpaths
from classes_camera import TherCam
from classes_arduino import movePanTilt
from grabPorts import grabPorts
from classes_text import binary_response, printme
from rand_cons import check_linear
from staircases import Staircase
from classes_speech import initSpeak
from globals import (
    grid,
    ROIs,
    PanTilts,
    stimulus,
    delay_data_display,
    haxes,
    stimulus,
    initial_staircase_temp,
    time_out_ex,
    size_ROI,
    answer,
    answered,
    question_staircase,
    delta,
    stimulus,
    time_out_tb,
    lower_bound_delay,
    higher_bound_delay,
    frames,
    min_bound_staircase,
    centreROI,
    positions,
    max_bound_staircase,
    rule_down,
    rule_up,
    size_down,
    size_up,
    middle_height,
)

##### READY-MADE CODE
import threading
import numpy as np
import os
import time
import simpleaudio as sa
import csv
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
            "time_delay",
            "stimulus_time",
            "position",
            "staircase",
            "failed",
            "n_block",
            "within_block_counter",
        )

        failed_name = f"data_failedstaircase{n_staircase}"

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

        name_staircase_file = f"online_back_up_staircases{n_staircase}"
        if os.path.exists(f"{path_data}/{name_staircase_file}.pkl"):
            printme(f"RECOVERING staircase{n_staircase} dict")
            staircase1 = recoverPickleRick(path_data, name_staircase_file)
        else:
            staircase1 = Staircase(
                total_reversals=stop_reversals,
                initial=initial_staircase_temp,
                direction="down",
            )

        printme(staircase1)
        positions_list = []
        limit = 3

        # Recover information
        grid["camera"] = csvToDictGridIndv(path_data, "temp_grid_camera.csv")
        grid["colther"] = csvToDictGridIndv(path_data, middle_height)
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
        speaker = initSpeak()
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

        # get positions with constraints online
        while staircase1.reversals < staircase1.total_reversals:
            # Interblock
            if keyboard.is_pressed("s"):
                (
                    _,
                    staircase1.block,
                    staircase1.within_block_counter,
                    staircase1.within_block_successful_counter,
                ) = trigger_handle_reload(
                    zabers=zabers,
                    platform=platform1,
                    arduino_syringe=arduino_syringe,
                    arduino_pantilt=arduino_pantilt,
                    cam=cam,
                    n_block=staircase1.block,
                    within_block_counter=staircase1.within_block_counter,
                    within_block_successful=staircase1.within_block_successful_counter,
                    arduino_dimmer=arduino_dimmer,
                )

            stimulus = 6
            tryexceptArduino(arduino_syringe, stimulus)
            stimulus = 4

            # Prepare position ZABERS
            while True:
                randomly_chosen_next = np.random.choice(
                    list(PanTilts.keys()), 1, replace=True
                )[0]
                if len(positions_list) == 0:
                    positions_list.append(randomly_chosen_next)
                    break
                else:
                    backwards = []
                    for bi in np.arange(1, limit + 0.1, 1):
                        current_check = check_linear(
                            positions_list, randomly_chosen_next, bi
                        )
                        backwards.append(current_check)

                    if np.all(backwards):
                        positions_list.append(randomly_chosen_next)
                        break
                    else:
                        print("WRONG VALUE!")

            p = randomly_chosen_next
            cROI = ROIs[p]

            # Feedback closure + TONE
            ev = threading.Event()
            beep_trial = threading.Thread(target=beep.play, args=[ev])
            beep_trial.name = "Beep thread"
            beep_trial.daemon = True
            beep_trial.start()

            # STIMULATION
            stimulus = 2
            ss = 1

            movePanTilt(arduino_pantilt, PanTilts[p])

            iti_zaber_dance_in(zabers, arduino_pantilt, p, PanTilts, grid)

            printme(f"Staircase: {n_staircase}")
            printme(f"Trial number: {staircase1.trial}")
            printme(f"Grid position: {p}")
            printme(f"Delta stimulation: {staircase1.stimulation}")
            printme(f"Block number: {staircase1.block}")
            printme(f"Within block trial counter: {staircase1.within_block_counter}")
            printme(
                f"Within block SUCCESSFUL trial counter: {staircase1.within_block_successful_counter}"
            )

            # function to round a float to 2 and then multiply by 100, then string
            def round_to_2(x):
                return str(round(x * 100) / 100)

            file_path = (
                path_videos
                + "/"
                + f"staircase{n_staircase}_trial{staircase1.trial}_delta{round(staircase1)}_pos{p}"
            )

            cam.targetTempAutoDiffDelta(
                file_path,
                staircase1.stimulation,
                cROI,
                size_ROI,
                arduino_syringe,
                stimulus,
                time_out,
                ev,
            )

            # ############### Terminate trial
            sa.stop_all()

            start = time.time()

            delay = np.random.uniform(lower_bound_delay, higher_bound_delay)
            time.sleep(delay)

            ### ANSWER
            if not cam.failed_trial:
                beep_speech_success.play()
                response, time_response_end = binary_response(question_staircase)
            else:
                response = 3
                time_response_end = 0

            if not cam.failed_trial:
                beep_speech_success.play()

            if cam.shutter_open_time < 0.4:
                cam.failed_trial = True

            if not cam.failed_trial:
                print("SUCCESSFUL stimulation")
                staircase1.reversal(int(response))
                staircase1.within_block_successful_counter += 1

            if cam.failed_trial == True:
                this_trial_n = 0
            else:
                this_trial_n = staircase1.trial

            ### SAVE RESPONSES
            tempRowToWrite = [
                subject_n,
                this_trial_n,
                staircase1.stimulation,
                staircase1.tracked_stimulation,
                staircase1.reversed_bool,
                int(response),
                delay,
                cam.shutter_open_time,
                p,
                ss,
                cam.failed_trial,
                staircase1.block,
                staircase1.within_block_counter,
            ]
            data = appendDataDict(data, tempRowToWrite)
            # print(data)

            temp_file = open(f"{path_data}/{temp_file_name}.csv", "a")
            temp_data_writer = csv.writer(temp_file)
            temp_data_writer.writerow(tempRowToWrite)
            temp_file.close()

            # Tracking algorithm
            if not cam.failed_trial:
                staircase1.XupYdownFixedStepSizesTrackingAlgorithm(
                    rule_down,
                    rule_up,
                    size_down,
                    size_up,
                )

            staircase1.clampBoundary(min_bound_staircase, max_bound_staircase)

            printme(staircase1.stimulation)
            printme(staircase1.tracked_stimulation)

            printme(f"Staircase {n_staircase} reversals: {staircase1.reversals}")

            if cam.failed_trial == False:
                staircase1.last_response = int(response)

            stimulus = 4
            tryexceptArduino(arduino_syringe, stimulus)

            frames = []

            if cam.failed_trial == False:
                staircase1.trial += 1

            staircase1.within_block_counter += 1

            staircase1.saveStaircase(path_data, name_staircase_file)

            iti_zaber_dance_away(zabers)

            panicButton()
            homeButton(zabers, arduino_pantilt)

        saveZaberPos("temp_zaber_pos", path_data, positions)
        saveROI("temp_ROI", path_data, centreROI)
        saveHaxesAll(path_data, haxes)

        name_subj_file = f"data_staircase{n_staircase}_subj"
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
            outcome=f"failedstaircase{n_staircase}",
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
            outcome=f"failedstaircase{n_staircase}",
        )
