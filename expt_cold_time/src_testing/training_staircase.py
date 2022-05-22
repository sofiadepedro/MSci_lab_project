##### OWN LIBRARIES
from local_functions import (
    thermalCalibration,
    arduinos_zabers,
    panicButton,
    homeArduinos,
    iti_zaber_dance_in,
    iti_zaber_dance_away,
    triggered_exception,
    question_staircase_rando,
    deltaToZaberHeight
)
from classes_speech import say
from index_funcs import parsing_situation, mkpaths

from classes_arduino import tryexceptArduino, movePanTilt
from grabPorts import grabPorts
from classes_audio import Sound
from classes_colther import (
    homingZabersConcu,
)
from classes_camera import TherCam
from saving_data import (
    getSubjNumDec,
    csvToDictROIAll,
    csvToDictPanTiltsAll,
    txtToVar,
    csvToDictGridIndv,
)
from classes_text import binary_response, printme
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
    step_sizes
)

#### EXTERNAL LIBRARIES
import threading
import numpy as np
import simpleaudio as sa
import time
import os
import keyboard

if __name__ == "__main__":
    try:
        # Grab ports
        ports = grabPorts()
        print(ports.ports)
        # Grab subject number
        situ, day, n_staircase = parsing_situation()
        subject_n = getSubjNumDec(day=day)

        # Check experimental situation, check and/or create folders
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )

        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()
        #### THERMAL CAMERA
        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)

        ### AUDIO
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

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

        ## RANDOMISE POSITIONS
        cells = [1, 3, 5, 2, 4, 1]
        final_order = [0, 1, 1, 1, 0, 1]

        familiar_stimulation = False
        while not familiar_stimulation:
            for i, p in enumerate(cells):
                tryexceptArduino(arduino_syringe, 6)

                # preliminary trial
                p = str(cells[i])
                cROI = ROIs[p]
                printme(f"Grid position: {p}")

                movePanTilt(arduino_pantilt, PanTilts[p])

                grid["colther"]["z"] = deltaToZaberHeight(
                    2.5, grid, p, step_sizes
                )
                iti_zaber_dance_in(zabers, arduino_pantilt, p, PanTilts, grid)

                # Feedback closure + TONE
                file_path = path_videos + "/" + f"training_stair_trial{i+1}_pos{p}"

                ev = threading.Event()
                beep_trial = threading.Thread(
                    target=beep.play,
                    args=[ev],
                    daemon=True,
                    name = "Beep thread"
                )
                beep_trial.start()

                # STIMULATION
                presentabsent = final_order[i]

                if presentabsent == 0:
                    stimulus = 3
                    time_out = np.random.randint(
                        1, 5, size=1
                    ) + np.random.random_sample(1)

                elif presentabsent == 1:
                    stimulus = 2
                    time_out = time_out_ex

                cam.targetTempAutoDiffDelta(
                    file_path,
                    initial_staircase_temp,
                    cROI,
                    r = size_ROI,
                    arduino = arduino_syringe,
                    stimulus = 2,
                    total_time_out = time_out,
                    event_camera = ev,
                )

                sa.stop_all()

                question = question_staircase_rando()
                say(question)

                answer = None
                answered = None

                beep_speech_success.play()

                ### ANSWER
                response, time_response_end = binary_response(question)

                beep_speech_success.play()
                iti_zaber_dance_away(zabers)

                panicButton()

            homeArduinos(arduino_syringe, arduino_pantilt, arduino_dimmer)
            homingZabersConcu(zabers, haxes)
            os.system("clear")
            printme("\nARE WE HAPPY WITH TRAINING? (y/n)  ")
            while True:
                if keyboard.is_pressed("y"):
                    familiar_stimulation = True
                    break
                elif keyboard.is_pressed("n"):
                    break

    except Exception as e:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_dimmer=arduino_dimmer,
            arduino_pantilt=arduino_pantilt,
            e=e,
        )

    except KeyboardInterrupt:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_dimmer=arduino_dimmer,
            arduino_pantilt=arduino_pantilt,
        )
