### Homemade code
from classes_arduino import tryexceptArduino
from classes_colther import homingZabersConcu, moveAxisTo
from classes_text import printme, scale_reponse, binary_response
from classes_speech import say
from rand_scaling import choosing_next_pos
from local_functions import (
    panicButton,
    iti_zaber_dance_in,
    iti_zaber_dance_away,
    closeEnvelope,
)
from failing import (
    getNames,
    recoverData,
    rewriteRecoveredData,
)
from saving_data import (
    apendAll,
    tempSaving,
    buildDict,
    appendDataDict,
    csvToDictGridIndv,
    apendAll,
    create_temp_name,
)
from scaling import Scaling, Anchoring
import globals

from globals import lowest_height, highest_height, scaling_magnitudes

### Ready-made code
import threading
import keyboard

import simpleaudio as sa
import os
import csv
import random
import numpy as np
from datetime import date


def showing(
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
    platform,
    path_data,
    ROIs,
    PanTilts,
    grid,
    first_time,
):
    showing_counter = 0
    showing_stimulation = False
    showing_mags = [0, 1]
    random.shuffle(showing_mags)

    homingZabersConcu(zabers, {"tactile": ["y", "x", "z"]})
    moveAxisTo(zabers, "camera", "y", 482604)

    while not showing_stimulation:
        while showing_counter < 2:
            if keyboard.is_pressed("q"):
                iti_zaber_dance_away(zabers)
                break

            # Prepare position ZABERS
            p = choosing_next_pos(globals.PanTilts, positions_list, limit)
            cROI = ROIs[p]

            # Feedback closure + TONE
            ev = threading.Event()
            beep_trial = threading.Thread(target=beep.play, args=[ev])
            beep_trial.name = "Beep thread"
            beep_trial.daemon = True
            beep_trial.start()

            # STIMULATION
            random_chosen_showing_mag = showing_mags.pop(0)

            if random_chosen_showing_mag == 0:
                stimulus = 3
                delta_target = 0
                time_out = np.random.randint(1, 5, size=1) + np.random.random_sample(1)
                sentence = "That was how 0 feels like"
                globals.grid["colther"] = csvToDictGridIndv(path_data, highest_height)

            elif random_chosen_showing_mag == 1:
                stimulus = 2
                delta_target = scaling_magnitudes[-1]
                time_out = globals.time_out_ex
                sentence = "That was how 100 feels like"
                globals.grid["colther"] = csvToDictGridIndv(path_data, lowest_height)

            iti_zaber_dance_in(zabers, arduino_pantilt, p, PanTilts, grid)

            tryexceptArduino(arduino_syringe, 6)

            file_path = (
                path_videos
                + "/"
                + f"showing_trial{showing_counter+1}_delta{str(round(delta_target*10))}_pos{p}"
            )

            printme(f"Showing trial: {showing_counter}")
            printme(f"Grid Position: {p}")
            printme(f"Delta: {delta_target}")

            cam.targetTempAutoDiffDelta(
                file_path,
                delta_target,
                cROI,
                globals.size_ROI,
                arduino_syringe,
                stimulus,
                time_out,
                ev,
            )
            globals.delta = 0

            sa.stop_all()

            if cam.shutter_open_time < 0.4:
                cam.failed_trial = True

            if not cam.failed_trial:

                say(sentence)

                beep_speech_success.play()
                globals.stimulus = 4

                showing_counter += 1

            if cam.failed_trial:
                showing_mags.append(random_chosen_showing_mag)

            iti_zaber_dance_away(zabers)

            panicButton()

        os.system("clear")

        # Move to ANCHORING?
        if first_time:
            printme("\nARE WE HAPPY WITH SHOWING? (y/n)  ")
            while True:
                if keyboard.is_pressed("y"):
                    showing_stimulation = True
                    break
                elif keyboard.is_pressed("n"):
                    break
        elif keyboard.is_pressed("r"):
            continue
        else:
            showing_stimulation = True
            break


def anchoring(
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
    platform,
    ROIs,
    PanTilts,
    grid,
    first_time,
):
    ### DATA ANCHORING
    # Data stuff
    data_anchoring = buildDict(
        "subject",
        "trial",
        "delta_stimulation",
        "response",
        "stimulus_time",
        "position",
        "failed",
        "n_block",
    )
    failed_name = "data_failedanchoring"
    names_data_failed = getNames(path_data, f"{failed_name}.*\.csv")
    name_temp_file = create_temp_name(failed_name)

    anch_temp_data_writer, anch_temp_file, anch_temp_file_name = tempSaving(
        path_data, list(data_anchoring.keys()), temp_file_name=name_temp_file
    )
    printme(names_data_failed)

    data_anchoring = recoverData(names_data_failed, path_data, data_anchoring)

    rewriteRecoveredData(data_anchoring, path_data, anch_temp_file_name)

    ### Anchoring
    anchoring_stimulation = False
    homingZabersConcu(zabers, {"tactile": ["y", "x", "z"]})
    moveAxisTo(zabers, "camera", "y", 482604)
    while not anchoring_stimulation:
        anchoring_trial_counter = 0
        anchoring_mags = [0, 0, 1, 1]
        random.shuffle(anchoring_mags)
        while anchoring_trial_counter < anchoring_trials_per_mag:
            if keyboard.is_pressed("q"):
                iti_zaber_dance_away(zabers)
                break

            # Prepare position ZABERS
            p = choosing_next_pos(PanTilts, positions_list, limit)
            cROI = ROIs[p]

            ev = threading.Event()
            beep_trial = threading.Thread(target=beep.play, args=[ev])
            beep_trial.name = "Beep thread"
            beep_trial.daemon = True
            beep_trial.start()

            # STIMULATION
            stimulus = 2

            randomly_chosen_anchoring_mag = anchoring_mags.pop(0)

            if randomly_chosen_anchoring_mag == 0:
                stimulus = 3
                delta_target = 0
                time_out = np.random.randint(1, 5, size=1) + np.random.random_sample(1)
                globals.grid["colther"] = csvToDictGridIndv(path_data, highest_height)

            elif randomly_chosen_anchoring_mag == 1:
                stimulus = 2
                delta_target = scaling_magnitudes[-1]
                time_out = globals.time_out_ex
                globals.grid["colther"] = csvToDictGridIndv(path_data, lowest_height)

            iti_zaber_dance_in(zabers, arduino_pantilt, p, PanTilts, grid)

            tryexceptArduino(arduino_syringe, 6)

            file_path = (
                path_videos
                + "/"
                + f"anchoring_block{scaling.block}_trial{anchoring_trial_counter+1}_delta{str(round(delta_target*10))}_pos{p}"
            )

            printme(f"Anchoring trial: {anchoring_trial_counter}")
            printme(f"Grid Position: {p}")
            printme(f"Delta: {delta_target}")

            cam.targetTempAutoDiffDelta(
                file_path,
                delta_target,
                cROI,
                globals.size_ROI,
                arduino_syringe,
                stimulus,
                time_out,
                ev,
            )
            globals.delta = 0

            sa.stop_all()

            if cam.shutter_open_time < 0.4:
                cam.failed_trial = True

            if not cam.failed_trial:
                sentence = globals.question_anchoring
                # speak(speaker, qs)
                say(globals.question_anchoring)

                beep_speech_success.play()

                anchoring_response, time_response_end = binary_response(
                    sentence, values={"0": "0", "100": "100"}
                ) 

                beep_speech_success.play()
                globals.stimulus = 4
                iti_zaber_dance_away(zabers)

                anchoring_trial_counter += 1

            elif cam.failed_trial:
                anchoring_response = 3
                time_response_end = 0
                anchoring_mags.append(randomly_chosen_anchoring_mag)

            ### SAVE RESPONSES
            anchTempRowToWrite = [
                subject_n,
                anchoring_trial_counter,
                delta_target,
                int(anchoring_response),
                cam.shutter_open_time,
                p,
                cam.failed_trial,
                scaling.block,
            ]
            data_anchoring = appendDataDict(data_anchoring, anchTempRowToWrite)
            # print(data_anchoring)

            anch_temp_file = open(f"{path_data}/{anch_temp_file_name}.csv", "a")
            anch_temp_data_writer = csv.writer(anch_temp_file)
            anch_temp_data_writer.writerow(anchTempRowToWrite)
            anch_temp_file.close()

            iti_zaber_dance_away(zabers)

            panicButton()

        apendAll(path_data, 1, data_anchoring, file="data_anchoring")

        closeEnvelope(
            zabers, platform, arduino_syringe, arduino_pantilt, arduino_dimmer
        )

        os.system("clear")
        if first_time:
            printme("\nARE WE HAPPY WITH ANCHORING? (y/n)  ")
            while True:
                if keyboard.is_pressed("y"):
                    anchoring_stimulation = True
                    break
                elif keyboard.is_pressed("n"):
                    break
        elif keyboard.is_pressed("r"):
            continue
        else:
            anchoring_stimulation = True
            break
