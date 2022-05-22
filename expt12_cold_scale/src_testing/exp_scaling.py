##### HOMEMADE CODE
from classes_arduino import tryexceptArduino
from grabPorts import grabPorts
from failing import (
    recoverData,
    recoveredToTempWriter,
    recoverPickleRick,
    spaceLeftWarning,
    rewriteRecoveredData,
    getNames,
)
from saving_data import (
    saveZaberPos,
    saveROI,
    saveIndv,
    rootToUser,
    changeNameTempFile,
    tempSaving,
    getSubjNumDec,
    buildDict,
    csvToDictGridAll,
    csvToDictROIAll,
    csvToDictPanTiltsAll,
    txtToVar,
    appendDataDict,
    saveHaxesAll,
    saveIndvVar,
    csvToDictGridIndv,
    create_temp_name,
)
from local_functions import (
    closeEnvelope,
    arduinos_zabers,
    trigger_handle_reload,
    panicButton,
    homeButton,
    iti_zaber_dance_away_scaling,
    iti_zaber_dance_in_scaling,
    triggered_exception,
)
from classes_audio import Sound
from index_funcs import parsing_situation, mkpaths
from classes_colther import movetostartZabers
from classes_camera import TherCam

from grabPorts import grabPorts
from classes_text import scale_reponse, printme

from rand_scaling import choosing_next_pos, scal_setup_trial
from scaling import Scaling, Anchoring
from classes_speech import initSpeak
from globals import (
    down_modifier_touch_height,
    touch_z_offset,
    grid,
    PanTilts,
    ROIs,
    stimulus,
    positions,
    size_ROI,
    centreROI,
    haxes,
    delay_data_display,
    scaling_magnitudes,
    time_out_tb,
    time_out_ex,
    lower_bound_delay,
    higher_bound_delay,
    question_scaling,
    up_modifier_touch_height,
    low_bound_scale,
    high_bound_scale,
    highest_height,
)
from def_show_anch import showing, anchoring


##### READY-MADE CODE
import threading
import numpy as np
import os
import time
import simpleaudio as sa
import csv
import keyboard
import random
from datetime import date

if __name__ == "__main__":
    try:
        # Grab ports
        ports = grabPorts()
        print(ports.ports)

        spaceLeftWarning()

        # Check experimental situation, check and/or create folders
        situ, day, _ = parsing_situation()
        subject_n = getSubjNumDec(day=day)
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )
        path_day_bit = path_day.rsplit("/", 3)[-1]

        ### DATA SCALING
        # Data stuff
        data_scaling = buildDict(
            "subject",
            "trial",
            "delta_stimulation",
            "touch",
            "response",
            "time_delay",
            "stimulus_time",
            "position",
            "failed",
            "n_block",
            "within_block_counter",
            "within_block_successful",
        )

        failed_name = "data_failedscaling"
        names_data_failed = getNames(path_data, f"{failed_name}.*\.csv")
        name_temp_file = create_temp_name(failed_name)

        _, temp_file, temp_file_name = tempSaving(
            path_data, list(data_scaling.keys()), temp_file_name=name_temp_file
        )
        printme(name_temp_file)
        printme(names_data_failed)
        data_scaling = recoverData(names_data_failed, path_data, data_scaling)

        rewriteRecoveredData(data_scaling, path_data, temp_file_name)

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

        # thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)

        ### ex vs tb conditions
        if situ == "ex":
            scaling_trials_per_mag = 28
            anchoring_trials_per_mag = 4
            trials_per_block = 42

            time_out = time_out_ex

        elif situ == "tb":
            scaling_trials_per_mag = 2
            anchoring_trials_per_mag = 4
            trials_per_block = 6

            time_out = time_out_tb

        ### Scaling file
        name_scaling_file = "online_back_up_scaling"
        if os.path.exists(f"{path_data}/{name_scaling_file}.pkl"):
            printme("RECOVERING scaling dict")
            scaling = recoverPickleRick(path_data, name_scaling_file)
        else:
            scaling = Scaling(
                trials_per_mag=scaling_trials_per_mag,
                magnitudes=scaling_magnitudes,
                start=0,
                end=5,
            )

        positions_list = []
        limit = 3
        time_stim_pres = []

        # Recover information
        grid["camera"] = csvToDictGridIndv(path_data, "temp_grid_camera.csv")
        grid["tactile"] = csvToDictGridIndv(path_data, "temp_grid_tactile.csv")
        ROIs = csvToDictROIAll(path_data)
        PanTilts = csvToDictPanTiltsAll(path_data)
        subject_n = txtToVar(path_data, "temp_subj_n")


        ### Set up Trials for condition
        if os.path.exists(f"{path_data}/online_back_up_stims.npy"):
            stims = np.load(f"{path_data}/online_back_up_stims.npy", allow_pickle=True)
            stims = stims.tolist()
            printme("GRABBING CONDS AND STIMULATION LOCATIONS FROM TEMP FILES")
        else:
            stims = scal_setup_trial(
            n_trials=scaling_trials_per_mag * len(scaling.magnitudes),
            mags=scaling.magnitudes,
        )
        print(len(stims))

        ### AUDIO
        speaker = initSpeak()
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

        print(f"\nPositions Zabers: {positions}\n")
        print(f"\nPanTilts: {PanTilts}\n")
        print(f"\nROIs: {ROIs}\n")
        print(f"\nHaxes: {haxes}")
        print(f"\nGrids Colther: {grid['colther']}\n")
        print(f"\nGrids Camera: {grid['camera']}\n")
        print(f"\nGrids Tactile: {grid['tactile']}\n")
        time.sleep(delay_data_display)


        first_time = True

        while scaling.trial < len(scaling.magnitudes) * scaling_trials_per_mag:

            if (
                first_time
                or scaling.within_block_counter >= trials_per_block
                or keyboard.is_pressed("s")
            ):
                scaling.within_block_counter = 0
                scaling.within_block_successful = 0

                while True:
                    ### INTERBLOCK
                    (
                        _,
                        scaling.block,
                        scaling.within_block_counter,
                        scaling.within_block_successful,
                    ) = trigger_handle_reload(
                        zabers=zabers,
                        platform=platform1,
                        arduino_syringe=arduino_syringe,
                        arduino_pantilt=arduino_pantilt,
                        cam=cam,
                        n_block=scaling.block,
                        within_block_counter=scaling.within_block_counter,
                        within_block_successful=scaling.within_block_successful,
                        arduino_dimmer=arduino_dimmer,
                    )

                    ### REFRESHER SHOWING
                    while True:
                        show = showing(
                            positions_list,
                            limit,
                            path_videos,
                            cam,
                            arduino_syringe,
                            arduino_pantilt,
                            arduino_dimmer,
                            zabers,
                            beep,
                            speaker,
                            beep_speech_success,
                            platform1,
                            path_data,
                            ROIs,
                            PanTilts,
                            grid,
                            first_time,
                        )

                        ### REFRESHER ANCHORING
                        anchor = anchoring(
                            scaling,
                            anchoring_trials_per_mag,
                            subject_n,
                            positions_list,
                            limit,
                            path_data,
                            path_videos,
                            path_day_bit,
                            path_day,
                            path_anal,
                            path_figs,
                            path_audios,
                            cam,
                            arduino_syringe,
                            arduino_pantilt,
                            arduino_dimmer,
                            zabers,
                            beep,
                            speaker,
                            beep_speech_success,
                            platform1,
                            ROIs,
                            PanTilts,
                            grid,
                            first_time,
                        )

                        if keyboard.is_pressed("a") and keyboard.is_pressed("r"):
                            continue
                        else:
                            break

                    if keyboard.is_pressed("s"):
                        continue
                    else:
                        break

            first_time = False

            # Prepare position ZABERS
            p = choosing_next_pos(PanTilts, positions_list, limit)
            cROI = ROIs[p]

            # Choose Current Stimulation
            current_stimulation = stims.pop(0)
            delta_target = current_stimulation[0]

            # Feedback closure + TONE
            ev = threading.Event()
            beep_trial = threading.Thread(target=beep.play, args=[ev])
            beep_trial.name = "Beep thread"
            beep_trial.daemon = True
            beep_trial.start()

            # TOUCH THREADS
            ev_touch = None
            modifier = down_modifier_touch_height
            touch = grid["tactile"][p]["z"] + round(touch_z_offset * modifier)
            untouch = (
                grid["tactile"][p]["z"] - touch_z_offset * up_modifier_touch_height
            )

            if current_stimulation[1] == 1:
                ev_touch = threading.Event()

                def UpDown(touch, untouch):
                    movetostartZabers(zabers, "tactile", "z", touch, ev_touch)
                    printme("Touching...")

                    ev_touch.clear()

                    movetostartZabers(
                        zabers,
                        "tactile",
                        "z",
                        untouch,
                        ev_touch,
                    )
                    printme("Untouching...")

                touch_thread = threading.Thread(target=UpDown, args=[touch, untouch])
                touch_thread.name = "Touch thread"
                touch_thread.daemon = True
                touch_thread.start()

            ### Prepare Time Out
            print("delta_target", delta_target)
            if delta_target == 0:
                stimulus = 3
                if len(time_stim_pres) == 0:
                    time_out = np.random.randint(
                        1, 5, size=1
                    ) + np.random.random_sample(1)
                elif len(time_stim_pres) >= 1:
                    time_out = np.random.choice(time_stim_pres)
            elif delta_target != 0:
                stimulus = 2
                if situ == "ex":
                    time_out = time_out_ex
                elif situ == "tb":
                    time_out = time_out_tb

            # STIMULATION
            if delta_target == 0:
                grid["colther"] = csvToDictGridIndv(path_data, highest_height)
                # print(grid["colther"])
            else:
                grid["colther"] = csvToDictGridIndv(
                    path_data, f"temp_grid_{str(round(delta_target*10))}_colther.csv"
                )
            print(grid["colther"])
            # print(f"Colther grid{grid['colther'][str(p)]}")
            # print(f"Camera grid{grid['camera'][str(p)]}")

            iti_zaber_dance_in_scaling(zabers, p, grid, arduino_pantilt, PanTilts)

            tryexceptArduino(arduino_syringe, 6)

            print(grid["colther"])

            printme(f"Trial number: {scaling.trial}")
            printme(f"Grid position: {p}")
            printme(f"Delta stimulation: {delta_target}")
            printme(f"Touch: {current_stimulation[1]}")
            printme(f"Block number: {scaling.block}")
            printme(f"Within block trial counter: {scaling.within_block_counter}")
            printme(
                f"Within block successful trials: {scaling.within_block_successful}"
            )
            printme(f"Trials left: {len(stims)}")

            file_path = (
                path_videos
                + "/"
                + f"scaling_trial{scaling.trial}_delta{str(int(delta_target*10))}_pos{p}"
            )

            cam.targetTempAutoDiffDelta(
                file_path,
                delta_target,
                cROI,
                size_ROI,
                arduino_syringe,
                stimulus,
                time_out,
                ev,
                ev_touch,
            )

            delta = 0

            # Terminate trial
            sa.stop_all()

            start = time.time()

            delay = np.random.uniform(lower_bound_delay, higher_bound_delay)
            time.sleep(delay)

            ## ANSWER
            if cam.shutter_open_time < 0.4:
                cam.failed_trial = True

            if not cam.failed_trial:
                qs = question_scaling
                beep_speech_success.play()

                response, time_response_end = scale_reponse(
                    qs,
                    start=low_bound_scale,
                    end=high_bound_scale,
                )

                scaling.magnitudes_done.append(current_stimulation)

                scaling.within_block_counter += 1
                scaling.within_block_successful += 1
                scaling.trial += 1

                beep_speech_success.play()

                print("SUCCESSFUL stimulation")

                this_trial_n = scaling.trial

            elif cam.failed_trial:
                response = 3
                time_response_end = 0
                stims.append(current_stimulation)
                scaling.within_block_counter += 1
                print("UNSUCCESSFUL stimulation")
                this_trial_n = 0

            ### SAVE RESPONSES
            tempRowToWrite = [
                subject_n,
                this_trial_n,
                delta_target,
                current_stimulation[1],
                int(response),
                delay,
                cam.shutter_open_time,
                p,
                cam.failed_trial,
                scaling.block,
                scaling.within_block_counter,
                scaling.within_block_successful,
            ]
            data_scaling = appendDataDict(data_scaling, tempRowToWrite)

            temp_file = open(f"{path_data}/{temp_file_name}.csv", "a")
            temp_data_writer = csv.writer(temp_file)
            temp_data_writer.writerow(tempRowToWrite)
            temp_file.close()

            scaling.saveScaling(path_data, name_scaling_file)
            np.save(f"{path_data}/online_back_up_stims", stims)

            iti_zaber_dance_away_scaling(zabers)

            panicButton()
            homeButton(zabers, arduino_pantilt)

        saveZaberPos("temp_zaber_pos", path_data, positions)
        saveROI("temp_ROI", path_data, centreROI)
        saveHaxesAll(path_data, haxes)

        name_subj_file = f"data_scaling_subj"
        saveIndv(name_subj_file, path_data, data_scaling)
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
            outcome="failedscaling",
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
            outcome="failedscaling",
        )
