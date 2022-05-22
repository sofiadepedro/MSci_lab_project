#####################################################################
# Zabers
#####################################################################
modem_port_touch = 41
modem_port_camera = 31
modem_port_tactile = 3

usb_port_camera = 1
usb_port_tactile = 9
usb_port_touch = 1

zaber_models = {
    "colther": {"x": "end_X-LSQ150B", "y": "end_A-LSQ150B", "z": "end_A-LSQ150B"},
    "camera": {"x": "end_LSM100B-T4", "y": "end_LSM200B-T4", "z": "end_LSM100B-T4"},
    "tactile": {"x": "end_LSM100B-T4", "y": "end_LSM200B-T4", "z": "end_LSM100B-T4"},
}
zaber_models_end = {
    "end_X-LSQ150B": 305381,
    "end_A-LSQ150B": 305381,
    "end_LSM100B-T4": 533333,
    "end_LSM200B-T4": 1066667,
}

step_sizes = {"colther": 0.49609375, "camera": 0.1905, "tactile": 0.1905}

rules = {
    "colther": {"x": True, "y": True, "z": True},
    "camera": {"x": False, "y": True, "z": True},
    "tactile": {"x": False, "y": True, "z": True},
}

pos_init = {"x": 30000, "y": 750000, "z": 0}
pos_knuckle = {"x": 300000, "y": 180000, "z": 0}
pos_centre = {"x": 250000, "y": 240472, "z": 0}

default_speed = 153600
speed = 153600 * 4

dry_ice_pos = {"x": 0, "y": 290000, "z": 0}

# For dict of zabers
axes = {
    "colther": ["x", "y", "z"],
    "camera": ["y", "x", "z"],
    "tactile": ["x", "y", "z"],
}

# Order of movement
haxes = {
    "colther": ["z", "x", "y"],
    "camera": ["x", "z", "y"],
    "tactile": ["y", "x", "z"],
}

move_platform_camera = 0
move_platform_camera_4 = 0

current_device = "tactile"
positions = {
    "colther": {"x": 233126, "y": 106874, "z": 0},
    "camera": {"x": 49507, "y": 535098, "z": 287000},
    "tactile": {"x": 336000, "y": 380000, "z": 270000},
}

init_grid = {"x": 50000, "y": 800000, "z": 70000}
init_meta = {"x": 110000, "y": 170000, "z": 10000}


grid = {"colther": None, "camera": None, "tactile": None}

stability = {
    0: {"x": 533333, "y": 0, "z": 511000},
    1: {"x": 183333, "y": 660000, "z": 500000},
}

touch_z_offset = 52494
tactile_y_save = 413491
base_touch = 20000
tactile_x_save = 533332

z_ds = {"colther": 40000, "camera": 0}

amount = 10000

#####################################################################
# Arduino
#####################################################################
default_pantilt = (44, 0, 158)
PanTilts = {
    "1": (37, 84, 66),
    "2": (24, 101, 48),
    "3": (29, 83, 61),
    "4": (39, 95, 63),
    "5": (31, 97, 57),
}

modem_port_pantilt = 2
modem_port_dimmer = 33
modem_port_syringe = 1

usb_port_pantilt = 1
usb_port_dimmer = 1
usb_port_syringe = 1

#####################################################################
# Thermal Camera
#####################################################################
vminT = 26
vmaxT = 32

temp = -1
indx0, indy0 = 1, 1
centreROI = 1, 2
ROIs = {}
#####################################################################
# Staircase
#####################################################################
min_bound_staircase = 0.2
max_bound_staircase = 3

rule_down = 3
rule_up = 1

size_down = 0.1
size_up = 0.14

initial_staircase_temp = 1.5
#####################################################################
# SDT
#####################################################################
conditions = {
    0: {"name": "no_touch", "touch": 0, "delay": 0, "touch_in": 0.01, "cold_in": 0.51},
    1: {"name": "touch_0delay", "touch": 1, "delay": 0, "touch_in": 0.51, "cold_in": 0.51},
    2: {"name": "touch_0-5_delay", "touch": 1, "delay": 0.5, "touch_in": 0.51, "cold_in": 1.51},
    3: {"name": "touch_1_delay", "touch": 1, "delay": 1, "touch_in": 0.51, "cold_in": 2.51},
    4: {"name": "touch_1-5_delay", "touch": 1, "delay": 1.5, "touch_in": 0.51, "cold_in": 3.51},
    # 5: {"name": "touch_2_delay", "touch": 1, "delay": 2, "touch_in": 0.51, "cold_in": 0.51},
}
name_sdt_file = "online_back_up_conds"

#####################################################################
# Miscellaneous
#####################################################################
size_ROI = 15
question = (
    "Was there any temperature change during the tone? 0: NO, 1: YES    "
)
time_out_ex = 10
time_out_tb = 8
delay_data_display = 1
up_modifier_touch_height = 0.8
down_modifier_touch_height = 0.4
diff_colther_touch = 19000
safe_post_z_touch = 330000
park_touch = {"x": 533332, "z": 330000}
separation_grid = 8
lower_bound_delay = 0.1
higher_bound_delay = 0.4
keydelay = 0.15