##### HOMEMADE CODE
from classes_arduino import tryexceptArduino
from grabPorts import grabPorts
from failing import (
    recoverData,
    rewriteRecoveredData,
    spaceLeftWarning,
    getNames
)
from saving_data import (
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
    csvtoDictZaber,
    saveIndvVar,
    apendAll,
    globalsToDict,
    copyDict,
    create_temp_name,
    handle_iti_save
)
from local_functions import (
    closeEnvelope,
    thermalCalibration,
    arduinos_zabers,
    trigger_handle_reload,
    panicButton,
    iti_zaber_dance_in_sdt,
    iti_zaber_dance_away_sdt,
    grabNextPosition,
    grabOrDefault,
    randomiseOrderSave,
    UpDown,
    gimmeSubBlockStims
)
from classes_audio import Sound
from index_funcs import parsing_situation, mkpaths
from classes_colther import (
    triggered_exception,
    movetostartZabersConcu,
)
from classes_camera import TherCam

from grabPorts import grabPorts
from classes_text import printme, binary_response

from globals import (
    grid,
    haxes,
    dry_ice_pos,
    delay_data_display,
    touch_z_offset,
    name_sdt_file,
    question,
    lower_bound_delay,
    higher_bound_delay,
    time_out_ex,
    time_out_tb,
    conditions,
    size_ROI
)

##### READY-MADE CODE
from threading import Thread, Event
import numpy as np
import os
import time
import simpleaudio as sa
import sys
import keyboard

sys.setrecursionlimit(50000)

if __name__ == "__main__":

    try:
        ports = grabPorts()
        print(ports.ports)
        situ, day, _ = parsing_situation()
        subject_n = getSubjNumDec(day=day)

        spaceLeftWarning()

        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )
        path_day_bit = path_day.rsplit("/", 3)[-1]

        print(path_day_bit)

        # Build the dictionary of all the data
        data = buildDict(
            "subject",
            "trial",
            "response",
            "reaction_time",
            "condition_block",
            "cold",
            "touch",
            "time_delay",
            "stimulus_time",
            "position",
            "failed",
            "n_block",
            "within_block_counter",
            "touch_in",
            "cold_in"
        )
        temp_data = copyDict(data)
        temp_data["subject"] = subject_n

        # Check whether there previous data
        failed_name = f"data_failedsdt"
        names_data_failed = getNames(path_data, f"{failed_name}.*\.csv")
        name_temp_file = create_temp_name(failed_name)

        _, temp_file, temp_file_name = tempSaving(
            path_data, list(data.keys()), temp_file_name=name_temp_file
        )

        data = recoverData(names_data_failed, path_data, data)
        rewriteRecoveredData(data, path_data, temp_file_name)

        if situ == 'tb':
            n_trials_cond = 5*2
        elif situ == 'ex':
            n_trials_cond = 22*2


        trials_counter = int(grabOrDefault("trial_n", path_data, 1))
        n_nofailed_trials = int(grabOrDefault("n_nofailed_trials", path_data, 0))
        n_block = int(grabOrDefault("n_block", path_data, 1))
        within_block_counter = int(grabOrDefault("within_block_counter", path_data, 1))
        current_block = int(grabOrDefault("current_block", path_data, 0))

        subBlock_stims = grabOrDefault("subBlock_stims", path_data, [], pickle_allowed=True)
        if len(subBlock_stims) == 0:
            subBlock_stims = gimmeSubBlockStims(situ)
            print("creating new order")
        else:
            subBlock_stims = subBlock_stims.tolist()

        order_block = grabOrDefault("order_block", path_data, [], pickle_allowed=True)
        if len(order_block) == 0:
            order_block = randomiseOrderSave(
                conditions, path_data
            )
            current_block = order_block.pop(0)
        else:
            order_block = order_block.tolist()

        # print("order block here: ", order_block)

        grid = csvToDictGridAll(path_data)
        ROIs = csvToDictROIAll(path_data)
        PanTilts = csvToDictPanTiltsAll(path_data)
        delta = txtToVar(path_data, "temp_delta")
        subject_n = txtToVar(path_data, "temp_subj_n")
        target_delta = round(float(delta), 2)

        ################### Load hardware ##################
        ### Arduinos & Zabers
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()

        ### Thermal camera
        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(haxes["colther"])),
            pos=dry_ice_pos,
        )

        thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)

        ################### Print info ##################
        print(f"\nROIs: {ROIs}\n")
        print(f"\nPanTilts: {PanTilts}\n")
        print(f"\nHaxes: {haxes}")
        print(f"\nGrids Colther: {grid['colther']}\n")
        print(f"\nGrids Camera: {grid['camera']}\n")
        print(f"\nGrids Tactile: {grid['tactile']}\n")
        print(f"\nPeak delta temperature {target_delta}\n")
        time.sleep(delay_data_display)

        ### Set-up audio
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

        # Some variables for the experiment
        time_sti_pres = []
        trial_positions = []
        limit = 3
        for i in grid["tactile"]:
            grid["tactile"][i]["z"] = (
                grid["tactile"][i]["z"] - touch_z_offset
            )
        first_approach = True

        while len(order_block) > 0:
            if len(subBlock_stims) == 0:
                current_block = order_block.pop(0)
                subBlock_stims = gimmeSubBlockStims(situ)
            np.save(f"{path_data}/order_block", order_block)
            np.save(f"{path_data}/current_block", current_block)
            while len(subBlock_stims) > 0:
                #### Check next position
                randomly_chosen_next, trial_positions = grabNextPosition(trial_positions, limit)
                temp_data["position"] = randomly_chosen_next
                cROI = ROIs[temp_data["position"]]
                temp_data["cold"] = subBlock_stims.pop(0)

                #### MOVE OUT
                #### Move colther up
                iti_zaber_dance_away_sdt(zabers)
                ##### STOP DURING ITI
                panicButton()
                if keyboard.is_pressed("s") or (len(subBlock_stims) == n_trials_cond and not first_approach):
                    (
                        first_approach,
                        n_block,
                        within_block_counter,
                    ) = trigger_handle_reload(
                            zabers=zabers,
                            platform=platform1,
                            arduino_syringe=arduino_syringe,
                            arduino_pantilt=arduino_pantilt,
                            cam=cam,
                            n_block=n_block,
                            within_block_counter=within_block_counter,
                            arduino_dimmer=arduino_dimmer,
                        )

                tryexceptArduino(arduino_syringe, 6)

                ##### PRINT SOME DATA
                printme(f"Trial number: {trials_counter}")
                printme(f"Grid position: {temp_data['position']}")
                printme(f"Fixed ROI for this position: {cROI}")
                printme(f"Current block {current_block}")
                printme(f"Successful trials: {n_nofailed_trials}")
                printme(f"Trials left sub-block: {len(subBlock_stims)}")
                printme(f"Within block counter: {within_block_counter}")
                printme(f"Trial type: {temp_data['cold']}")

                ##### MOVE IN
                # Move and colther camera to its position
                iti_zaber_dance_in_sdt(zabers, temp_data["position"], grid, arduino_pantilt, PanTilts)

                ##### PREPARE TIME OUT
                if temp_data["cold"] == 0:
                    stimulus = 3
                    if len(time_sti_pres) == 0:
                        time_out = np.random.randint(
                            1, 5, size=1
                        ) + np.random.random_sample(1)
                    else:
                        time_out = np.random.choice(time_sti_pres)

                elif temp_data["cold"] == 1:
                    stimulus = 2
                    if situ == "ex":
                        time_out = time_out_ex
                    elif situ == "tb":
                        time_out = time_out_tb

                ##### PREPARE TONE THREAD
                ev = Event()
                beep_trial = Thread(
                    target=beep.play,
                    args=[ev],
                    daemon=True,
                    name="Beep thread",
                )
                beep_trial.start()

                ##### PREPARE TOUCH THREADS
                ev_touch = None

                touch = grid["tactile"][str(temp_data["position"])]["z"] + touch_z_offset

                if conditions[current_block]["touch"] == 1:
                    ev_touch = Event()

                    touch_thread = Thread(
                        target=UpDown,
                        args=[touch, ev_touch, zabers, temp_data, grid],
                        daemon=True,
                        name="Touch thread",
                    )
                    touch_thread.start()

                ##### STIMULATION
                file_path = path_videos + "/" + f"sdt_trial{trials_counter}_pos{temp_data['position']}"
                cam.targetTempAutoDiffDelta(
                    file_path,
                    target_delta,
                    cROI,
                    size_ROI,
                    arduino_syringe,
                    stimulus,
                    time_out,
                    ev,
                    ev_touch,
                    conditions[current_block]["cold_in"],
                    conditions[current_block]["touch_in"],
                )
                sa.stop_all()

                # centre shutter
                tryexceptArduino(arduino_syringe, 4)
                first_approach = False

                ##### CHECK WHETHER THE STIMULATION WAS SUCCESSFUL
                if cam.shutter_open_time < 0.4:
                    cam.failed_trial = True

                if conditions[current_block]["touch"] == 1 and not cam.failed_trial:
                    if cam.shutter_open_time:
                        time_sti_pres.append(cam.shutter_open_time)

                if not cam.failed_trial:
                    n_nofailed_trials += 1
                    temp_data["trial"] = n_nofailed_trials
                    temp_data["time_delay"] = np.random.uniform(
                        lower_bound_delay, higher_bound_delay
                    )
                    time.sleep(temp_data["time_delay"])

                    beep_speech_success.play()
                    temp_data["response"], temp_data["reaction_time"] = binary_response(
                        question
                    )
                else:
                    temp_data["time_delay"] = 0
                    temp_data["response"] = 3
                    temp_data["reaction_time"] = 0
                    temp_data["trial"] = 0
                    subBlock_stims.append(temp_data["cold"])

                temp_data["condition_block"] = current_block
                temp_data["touch"] = conditions[current_block]["touch"]
                temp_data["stimulus_time"] = cam.shutter_open_time
                temp_data["failed"] = cam.failed_trial
                temp_data["n_block"] = n_block
                temp_data["within_block_counter"] = within_block_counter
                temp_data["touch_in"] = conditions[current_block]["touch_in"]
                temp_data["cold_in"] = conditions[current_block]["cold_in"]

                data = handle_iti_save(
                    list(temp_data.values()), data, path_data, temp_file_name
                )

                np.save(f"{path_data}/subBlock_stims", subBlock_stims)
                np.save(f"{path_data}/trial_n", trials_counter)
                np.save(f"{path_data}/n_nofailed_trials", n_nofailed_trials)
                np.save(f"{path_data}/n_block", n_block)
                np.save(f"{path_data}/within_block_counter", within_block_counter)

                trials_counter += 1
                within_block_counter += 1

        iti_zaber_dance_away_sdt(zabers)
        if os.path.exists(f"./src_testing/temp_folder_name.txt"):
            saveIndvVar("./src_testing", path_day_bit, "temp_folder_name")

        apendAll(path_data, 1, data)

        name_subj_file = f"data_subj"
        saveIndv(name_subj_file, path_data, data)
        all_globals = globalsToDict(globals)
        saveIndv("all_globals", path_data, all_globals)

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

        changeNameTempFile(path_data, outcome="success")

        name_temp_online = ["trial_n", f"{name_sdt_file}"]
        for nto in name_temp_online:
            if os.path.exists(f"{path_data}/{nto}.npy"):
                os.remove(f"{path_data}/{nto}.npy")

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
            outcome="data_failedsdt",
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
            outcome="data_failedsdt",
        )
