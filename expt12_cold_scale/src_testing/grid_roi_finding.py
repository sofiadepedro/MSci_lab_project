##### OWN LIBRARIES
from local_functions import (
    thermalCalibration,
    arduinos_zabers,
    closeEnvelope,
    triggered_exception,
)
from index_funcs import parsing_situation, mkpaths
from failing import errorloc
from classes_arduino import tryexceptArduino, movePanTilt
from grabPorts import grabPorts
from classes_colther import (
    movetostartZabersConcu,
)
from classes_camera import TherCam
from saving_data import (
    getSubjNumDec,
    csvToDictGridIndv,
    saveROIAll,
    savePanTiltAll,
    saveGridIndv,
    rootToUser,
    csvToDictPanTiltsAll
)
from globals import (
    grid,
    vminT,
    vmaxT,
    dry_ice_pos,
    haxes,
    size_ROI,
    rules,
    PanTilts,
    park_touch,
    lowest_height,
)

##### EXTERNAL LIBRARIES
import threading
import os

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        situ, day, _ = parsing_situation()
        subject_n = getSubjNumDec(day=day)
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )

        try:
            grid["camera"] = csvToDictGridIndv(path_data, "temp_grid_camera.csv")
            grid["tactile"] = csvToDictGridIndv(path_data, "temp_grid_tactile.csv")
            PanTilts = csvToDictPanTiltsAll(path_data)

            print(PanTilts)
            print(PanTilts["1"])
            print(grid)
        except Exception as e:
            errorloc(e)

        grid["colther"] = csvToDictGridIndv(path_data, lowest_height)

        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()

        cam = TherCam(vminT=vminT, vmaxT=vmaxT)
        cam.startStream()
        cam.setShutterManual()

        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(haxes["colther"])),
            pos=dry_ice_pos,
        )
        os.system("clear")

        thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)

        movetostartZabersConcu(zabers, "tactile", ["z", "x"], pos=park_touch)

        print(PanTilts)
        movePanTilt(arduino_pantilt, PanTilts["1"])

        movetostartZabersConcu(zabers, "camera", ["x", "y"], pos=grid["camera"]["1"])
        movetostartZabersConcu(zabers, "camera", ["z"], pos=grid["camera"]["1"])
        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(haxes["colther"])),
            pos=grid["colther"]["1"],
        )

        manual = threading.Thread(
            target=zabers["colther"]["x"].gridCon3pantiltScaling,
            args=[
                zabers,
                arduino_pantilt,
                platform1,
                arduino_syringe,
                PanTilts,
                grid,
                haxes,
                rules,
            ],
            daemon=True,
        )
        manual.start()

        cam.plotLiveROINEcheck(r=size_ROI)

        tryexceptArduino(arduino_syringe, 7)

        grid["camera"] = zabers["colther"]["x"].gridcamera

        saveROIAll(path_data, zabers["colther"]["x"].rois)
        savePanTiltAll(path_data, zabers["colther"]["x"].PanTilts)
        saveGridIndv("temp_grid", path_data, grid, "camera")

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

        closeEnvelope(
            zabers, platform1, arduino_syringe, arduino_pantilt, arduino_dimmer
        )

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
