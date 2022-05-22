from classes_arduino import ArdUIno
from classes_arduino import tryexceptArduino, reLoad
from classes_colther import Zaber
from classes_colther import (
    moveAxisTo,
    movePanTilt,
    homingZabersConcu,
    set_up_big_three,
    movetostartZabersConcu,
    findHeight,
    steps_to_cm,
    cm_to_steps,
    movetostartZabers
)
from classes_text import waitForEnter, printme
from index_funcs import threadFunctions
from classes_text import printme
from globals import (
    touch_z_offset,
    up_modifier_touch_height,
    safe_post_z_touch,
    diff_colther_touch,
    PanTilts,
    haxes,
    default_pantilt,
    axes,
    dry_ice_pos,
    usb_port_pantilt,
    modem_port_pantilt,
    usb_port_syringe,
    modem_port_syringe,
    usb_port_dimmer,
    modem_port_dimmer,
    keydelay,
    speed,
    grid
)

from saving_data import rootToUser, changeNameTempFile
from failing import errorloc
from rand_cons import check_linear

try:
    from termios import TCIFLUSH, tcflush
except:
    pass


import os
import time
import keyboard
import random
import struct
import sys
import numpy as np


def shrink_grid(grid):
    shrank_grid = {}
    counter = 1
    for num in list(grid.keys()):
        if int(num) % 2 != 0:
            shrank_grid[str(counter)] = grid[num]
            counter += 1

    return shrank_grid


def homeArduinos(arduino_syringe, arduino_pantilt, arduino_dimmer):

    if arduino_syringe:
        tryexceptArduino(arduino_syringe, 0)

    if arduino_pantilt:
        movePanTilt(arduino_pantilt, default_pantilt)

    if arduino_dimmer:
        tryexceptArduino(arduino_dimmer, 0)


def arduinos_zabers():
    zabers = set_up_big_three(axes)
    platform1 = Zaber(1, who="serial", surname_serial="AH0614UB")

    # check colther position
    colther_x_pos = zabers["colther"]["x"].device.send("/get pos")
    colther_y_pos = zabers["colther"]["y"].device.send("/get pos")
    pos_colther = [
        not colther_x_pos.warning_flag == "--",
        not colther_y_pos.warning_flag == "--",
    ]

    # check touch position
    tactile_x_pos = zabers["tactile"]["x"].send("/get pos")
    tactile_y_pos = zabers["tactile"]["y"].send("/get pos")
    pos_tactile = [
        not tactile_x_pos.warning_flag == "--",
        not tactile_y_pos.warning_flag == "--",
    ]

    homingZabersConcu(zabers, {"colther": ["z"]})

    homingZabersConcu(zabers, {"colther": ["x"]})

    if (
        not any(pos_tactile)
        and not any(pos_colther)
        and int(colther_x_pos.data) > 1000
        and int(colther_y_pos.data) > 1000
    ):
        moveAxisTo(zabers, "colther", "y", dry_ice_pos["y"])
    homingZabersConcu(zabers, {"camera": ["z"]})
    if (
        not any(pos_tactile)
        and not any(pos_colther)
        and int(tactile_x_pos.data) > 1000
        and int(tactile_y_pos.data) > 1000
    ):
        moveAxisTo(zabers, "tactile", "x", 533332)
    homingZabersConcu(zabers, {"tactile": ["y"]})

    arduino_pantilt = ArdUIno(
        usb_port=usb_port_pantilt,
        n_modem=modem_port_pantilt,
        name="PanTilt",
    )
    arduino_pantilt.arduino.flushInput()
    time.sleep(0.1)

    # Arduino syringe motors
    arduino_syringe = ArdUIno(
        usb_port=usb_port_syringe,
        n_modem=modem_port_syringe,
        name="syringe",
    )
    arduino_syringe.arduino.flushInput()
    time.sleep(0.1)

    # Arduino dimmers
    arduino_dimmer = ArdUIno(
        usb_port=usb_port_dimmer,
        n_modem=modem_port_dimmer,
        name="dimmer",
    )
    arduino_dimmer.arduino.flushInput()
    time.sleep(0.1)

    platform1.device.send(f"set maxspeed {206408*4}")
    platform1.device.home()
    homingZabersConcu(zabers, haxes)

    return zabers, platform1, arduino_pantilt, arduino_syringe, arduino_dimmer


def set_up_arduinos():

    arduino_pantilt = ArdUIno(usb_port=usb_port_pantilt, n_modem=modem_port_pantilt)
    arduino_pantilt.arduino.flushInput()
    time.sleep(0.1)

    # Arduino syringe motors
    arduino_syringe = ArdUIno(usb_port=usb_port_syringe, n_modem=modem_port_syringe)
    arduino_syringe.arduino.flushInput()
    time.sleep(0.1)

    # Arduino dimmers
    arduino_dimmer = ArdUIno(usb_port=usb_port_dimmer, n_modem=modem_port_dimmer)
    arduino_dimmer.arduino.flushInput()
    time.sleep(0.1)

    return arduino_syringe, arduino_dimmer, arduino_pantilt


def set_up_zabers():
    time.sleep(1)
    zabers = set_up_big_three(axes)
    platform1 = Zaber(1, who="serial", surname_serial="AH0614UB")
    platform1.device.send(f"set maxspeed {206408*4}")
    platform1.device.home()
    homingZabersConcu(zabers, haxes)

    return zabers, platform1


def panicButton():
    if keyboard.is_pressed("p"):
        os.system("clear")
        waitForEnter("\n\n Press enter when panic is over...")


def homeButton(zabers, arduino_pantilt):
    if keyboard.is_pressed("h"):
        os.system("clear")
        homingZabersConcu(zabers, {"colther": haxes["colther"]})
        moveAxisTo(zabers, "camera", "z", 0)
        movePanTilt(arduino_pantilt, default_pantilt)

        homingZabersConcu(zabers, {"camera": haxes["camera"]})
        homingZabersConcu(zabers, {"tactile": haxes["tactile"]})
        waitForEnter("\n\n Press enter when panic is over...")


def trigger_handle_reload(
    zabers,
    platform,
    arduino_syringe,
    arduino_pantilt,
    cam,
    n_block,
    within_block_counter,
    arduino_dimmer,
):

    homingZabersConcu(zabers, {"colther": haxes["colther"]})
    moveAxisTo(zabers, "camera", "z", 0)
    movePanTilt(arduino_pantilt, default_pantilt)
    platform.device.move_abs(0)
    homingZabersConcu(zabers, {"camera": haxes["camera"]})
    homingZabersConcu(zabers, {"tactile": haxes["tactile"]})

    thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)
    n_block += 1
    within_block_counter = 0

    return True, n_block, within_block_counter


def dryiceRiskAssess(ard_syringe, times=3):
    for i in range(times):
        tryexceptArduino(ard_syringe, 1)
        time.sleep(0.4)

        tryexceptArduino(ard_syringe, 6)
        time.sleep(0.4)

        tryexceptArduino(ard_syringe, 0)
        time.sleep(0.4)


def thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam):

    movetostartZabersConcu(
        zabers,
        "colther",
        list(reversed(haxes["colther"])),
        pos=dry_ice_pos,
    )
    # Dry ice load
    tryexceptArduino(arduino_syringe, 7)
    tryexceptArduino(arduino_syringe, 0)

    # Turn lamp on
    tryexceptArduino(arduino_dimmer, 1)

    scriptIs = sys.argv[0].split("/")[-1].split(".")[0]

    if scriptIs == "checking_stims" or scriptIs == "exp_scaling":
        check_touch(zabers)

    # Get camera out of the way
    reLoad(arduino_syringe)

    homingZabersConcu(zabers, haxes)
    os.system("clear")

    # Turn lamp off
    tryexceptArduino(arduino_dimmer, 0)

    # Subject in position
    movetostartZabersConcu(zabers, "camera", ["y"], {"y": 350000})
    os.system("clear")
    waitForEnter("\n\n Press enter when participant is comfortable and ready\n\n")

    # Shutter refresh and stabilisation
    cam.setShutterManual()
    cam.performManualff()
    printme(
        "Performing shutter refresh and taking a 10-second break\nto let the thermal image stabilise"
    )
    time.sleep(10)

    dryiceRiskAssess(arduino_syringe)

    tryexceptArduino(arduino_syringe, 4)
    printme("Resuming experiment...")


def closeEnvelope(zabers, platform, arduino_syringe, arduino_pantilt, arduino_dimmer):

    #### HOMER ARDUINOS & ZABERS
    # check colther position

    # check colther position
    colther_x_pos = zabers["colther"]["x"].device.send("/get pos")
    colther_y_pos = zabers["colther"]["y"].device.send("/get pos")
    pos_colther = [
        not colther_x_pos.warning_flag == "--",
        not colther_y_pos.warning_flag == "--",
    ]

    # check touch position
    tactile_x_pos = zabers["tactile"]["x"].send("/get pos")
    tactile_y_pos = zabers["tactile"]["y"].send("/get pos")
    pos_tactile = [
        not tactile_x_pos.warning_flag == "--",
        not tactile_y_pos.warning_flag == "--",
    ]

    homingZabersConcu(zabers, {"colther": ["z", "x", "y"]})

    homingZabersConcu(zabers, {"camera": ["z"]})

    if platform:
        platform.device.move_abs(0)

    homingZabersConcu(zabers, {"tactile": ["y"]})

    homeArduinos(arduino_syringe, arduino_pantilt, arduino_dimmer)
    homingZabersConcu(zabers, {"camera": ["x", "y"]})
    homingZabersConcu(zabers, haxes)


def iti_zaber_dance_away(zabers):
    funcs = [
        [moveAxisTo, [zabers, "colther", "z", 0]],
        [moveAxisTo, [zabers, "camera", "x", 0]],
        [moveAxisTo, [zabers, "colther", "x", 120000]],
        [moveAxisTo, [zabers, "colther", "y", 90000]],
    ]
    threadFunctions(funcs)


def iti_zaber_dance_in(zabers, arduino_pantilt, p, pantilt, grid):

    funcs = [
        [
            movetostartZabersConcu,
            [zabers, "camera", ["x", "y", "z"], grid["camera"][str(p)]],
        ],
        [movePanTilt, [arduino_pantilt, pantilt[p]]],
    ]
    threadFunctions(funcs)

    movetostartZabersConcu(zabers, "camera", ["z"], pos=grid["camera"][str(p)])
    movetostartZabersConcu(
        zabers,
        "colther",
        list(reversed(haxes["colther"])),
        pos=grid["colther"][str(p)],
    )


def iti_zaber_dance_in_sdt(zabers, p, grid, arduino_pantilt, PanTilts):

    funcs = [
        [
            movetostartZabersConcu,
            [
                zabers,
                "tactile",
                ["z"],
                (grid["tactile"][p]["z"] - touch_z_offset * up_modifier_touch_height),
            ],
        ],
        [
            movetostartZabersConcu,
            [zabers, "tactile", ["x", "y"], grid["tactile"][str(p)]],
        ],
    ]
    threadFunctions(funcs)

    funcs = [
        [
            movetostartZabersConcu,
            [zabers, "camera", ["x", "y", "z"], grid["camera"][str(p)]],
        ],
        [movePanTilt, [arduino_pantilt, PanTilts[p]]],
    ]
    threadFunctions(funcs)

    movetostartZabersConcu(
        zabers,
        "colther",
        ["x", "y"],
        pos=grid["colther"][str(p)],
    )

    movetostartZabersConcu(
        zabers,
        "colther",
        ["z"],
        pos=grid["colther"][str(p)],
    )


def grabNextPosition(positions, limit):
    while True:
        randomly_chosen_next = np.random.choice(list(PanTilts.keys()), 1, replace=True)[
            0
        ]
        if len(positions) == 0:
            positions.append(randomly_chosen_next)
            break
        else:
            backwards = []
            for bi in np.arange(1, limit + 0.1, 1):
                current_check = check_linear(positions, randomly_chosen_next, bi)
                backwards.append(current_check)

            if np.all(backwards):
                positions.append(randomly_chosen_next)
                break
            else:
                print("WRONG VALUE!")
    return randomly_chosen_next, positions


def iti_zaber_dance_away_sdt(zabers):
    funcs = [
        [moveAxisTo, [zabers, "colther", "z", 0]],
        [moveAxisTo, [zabers, "camera", "x", 0]],
        [moveAxisTo, [zabers, "colther", "x", 140000]],
        [moveAxisTo, [zabers, "colther", "y", 110000]],
    ]
    threadFunctions(funcs)


def triggered_exception(
    zabers=None,
    platform=None,
    path_day=None,
    path_anal=None,
    path_data=None,
    path_videos=None,
    path_figs=None,
    arduino_syringe=None,
    arduino_dimmer=None,
    arduino_pantilt=None,
    e=None,
    outcome="failed",
):

    if e:
        errorloc(e)
    else:
        print("Keyboard Interrupt")

    if path_data:
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
        changeNameTempFile(path_data, outcome=outcome)

    if zabers:
        # check colther position
        colther_x_pos = zabers["colther"]["x"].device.send("/get pos")
        colther_y_pos = zabers["colther"]["y"].device.send("/get pos")
        pos_colther = [
            not colther_x_pos.warning_flag == "--",
            not colther_y_pos.warning_flag == "--",
        ]

        # check touch position
        tactile_x_pos = zabers["tactile"]["x"].send("/get pos")
        tactile_y_pos = zabers["tactile"]["y"].send("/get pos")
        pos_tactile = [
            not tactile_x_pos.warning_flag == "--",
            not tactile_y_pos.warning_flag == "--",
        ]

        if (
            not any(pos_tactile)
            and not any(pos_colther)
            and int(tactile_x_pos.data) < 1000
            and int(tactile_y_pos.data) < 1000
        ):
            moveAxisTo(zabers, "tactile", "z", safe_post_z_touch)

        homingZabersConcu(zabers, {"colther": ["z", "x", "y"]})

        homingZabersConcu(zabers, {"camera": ["z"]})
        homingZabersConcu(zabers, {"camera": ["x", "y"]})

        if platform:
            platform.device.move_abs(0)

        homingZabersConcu(zabers, {"tactile": ["y"]})

    if arduino_syringe:
        arduino_syringe.arduino.write(struct.pack(">B", 0))
        time.sleep(0.1)

    if arduino_pantilt:
        arduino_pantilt.arduino.write(struct.pack(">B", 8))
        time.sleep(keydelay)
        arduino_pantilt.arduino.write(
            struct.pack(
                ">BBB",
                default_pantilt[0],
                default_pantilt[1],
                default_pantilt[2],
            )
        )
        time.sleep(0.1)

    if arduino_dimmer:
        arduino_dimmer.arduino.write(struct.pack(">B", 0))

    if zabers:
        homingZabersConcu(zabers, haxes, speed=speed)


def question_staircase_rando():
    yes_no_list = ["0 if NO", "1 if YES"]
    random.shuffle(yes_no_list)
    question_staircase = f"Was there any temperature change during the tone? Press {yes_no_list[0]}, or {yes_no_list[1]}    "
    print(question_staircase)
    return question_staircase


def check_touch(zabers):
    try:
        tcflush(sys.stdin, TCIFLUSH)
    except:
        printme("\n Could not flush the input buffer \n")
    input("Press enter to check next point")
    movetostartZabersConcu(
        zabers,
        "tactile",
        ["x", "y", "z"],
        pos={"x": 183333, "y": 660000, "z": 500000},
    )

    input("Press enter to finish next point")
    #### HOMER ARDUINOS & ZABERS
    homingZabersConcu(zabers, {"tactile": haxes["tactile"]})


def deltaToZaberHeight(delta, grid, position, step_sizes):
    height = findHeight(delta)
    z_cm_colther = (
        steps_to_cm(grid["tactile"][position]["z"], step_sizes["tactile"])
        + steps_to_cm(diff_colther_touch, step_sizes["colther"])
        - height
    )
    zaber_height = cm_to_steps(z_cm_colther, step_sizes["colther"])

    return zaber_height

def grabOrDefault(name_file, path_data, default, pickle_allowed=False):
    if os.path.exists(f"{path_data}/{name_file}.npy"):
        value = np.load(f"{path_data}/{name_file}.npy", allow_pickle=pickle_allowed)
        printme(f"{name_file}: {value}")

    else:
        value = default

    return value

def randomiseOrderSave(conditions, path_data, name = 'randomised_conds'):
    conditions_keys = list(conditions.keys())
    np.random.shuffle(conditions_keys)
    # Save the randomised order
    np.save(f"{path_data}/{name}", conditions)
    return conditions_keys

def UpDown(touch, event, zabers, data, grid):

    movetostartZabers(zabers, "tactile", "z", touch, event)
    printme("Touching...")

    event.clear()
    untouch = grid["tactile"][str(data["position"])]["z"] - touch_z_offset

    movetostartZabers(
        zabers,
        "tactile",
        "z",
        untouch,
        event,
    )
    printme("Untouching...")

def gimmeSubBlockStims(situ):
    if situ == 'tb':
        n_trials_cond = 5
    elif situ == 'ex':
        n_trials_cond = 22

    stims = [0, 1] * n_trials_cond
    # randomise the order
    stims = list(np.random.permutation(stims))

    return stims