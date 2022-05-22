################################ Import stuff ################################
##### HOMEMADE CODE
from grabPorts import grabPorts
from local_functions import closeEnvelope, arduinos_zabers, triggered_exception

from classes_colther import movetostartZabersConcu

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()

        input("Press enter to check next point")
        movetostartZabersConcu(
            zabers,
            "tactile",
            ["x", "y", "z"],
            pos={"x": 533333, "y": 0, "z": 511000},
        )
        # "x": 533332, "y": 61000, "z": 330000

        input("Press enter to check next point")
        movetostartZabersConcu(
            zabers,
            "tactile",
            ["x", "y", "z"],
            pos={"x": 183333, "y": 660000, "z": 500000},
        )

        input("Press enter to finish next point")
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
