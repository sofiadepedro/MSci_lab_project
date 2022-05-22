# %% Script to animate sdt trials

from fileinput import filename
from classes_tharnal import ReAnRaw
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3

colorMapType = 0
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation

### Data structure
import numpy as np

## Media
from imutils.video import VideoStream
from classes_tharnal import GrabNamesOrder
from plotting import framesToseconds

from local_functions import get_delta, get_numbers

import time
from saving_data import checkORcreate

if __name__ == "__main__":
    test_state = "test"
    todaydate = "04022022_1"

    folder_name = test_state + "_" + todaydate
    path_animation = checkORcreate(f"../data/{folder_name}/animations")
    print(path_animation)

    ### SUBJECT
    pattern = f".*\.hdf5$"
    path_videos = f"../data/{folder_name}/videos/"
    print(f"name is {folder_name}")
    names = GrabNamesOrder(pattern, path_videos)

    tdus = todaydate.split(todaydate)

    # ANIMATION
    for i, n in enumerate(names):
        list_splitted = n.split("_")
        try:
            delta_string = get_delta(list_splitted, "delta")
            print("delta string", delta_string)
            delta_value = get_numbers(delta_string)
            print("delta value", delta_value)
        except Exception as e:
            print(e)
            delta_value = 1

        if delta_value != 0:
            delta_value = delta_value / 10
            dat_im = ReAnRaw(f"../data/{folder_name}/videos/{n}")
            dat_im.datatoDic()
            print(n)
            means = []

            Writer = animation.writers["ffmpeg"]
            writer = Writer(fps=9, metadata=dict(artist="Me"), bitrate=1800)
            vminT = 22
            vmaxT = 30

            def animate(
                i,
                data,
                plots,
                axs,
                fixed_coor,
                diff_coor,
                means,
                sROI,
                baseline_buffer,
                deltas,
                shutter,
                momen,
                baseline_frames_buffer,
                shutter_state,
                delta_value,
            ):
                # print(shutter_state)
                widthtick = 3
                title_pad = 20
                lwD = 5
                widthtick = 5
                lenD = 15
                r = 20

                shutter_closed = 4
                shutter_open = 2

                # First subplot: 2D RAW
                ax1.clear()
                xs = np.arange(0, 160)
                ys = np.arange(0, 120)

                circles = []

                if sROI[i] == 1 and i > 14:
                    if np.shape(diff_coor[i])[1] > 1:
                        cdif = diff_coor[i][:, 0]
                        # print(cdif)
                        cy = cdif[1]
                        cx = cdif[0]
                    else:
                        cdif = diff_coor[i]
                        cy = cdif[1][0]
                        cx = cdif[0][0]

                    cir = plt.Circle(cdif[::-1], r, color="#007CB7", fill=False, lw=lwD * 1.2)
                    cir2 = plt.Circle(cdif[::-1], r, color="#CB8680", fill=False, lw=lwD * 1.2)

                    mask = (xs[np.newaxis, :] - cy) ** 2 + (
                        ys[:, np.newaxis] - cx
                    ) ** 2 < r ** 2
                    roiC = data[i][mask]
                    temp = round(np.nanmean(roiC), 2)
                    means.append(temp)

                elif sROI[i] == 0:
                    cir = plt.Circle(
                        fixed_coor[i][::-1], r, color="#007CB7", fill=False, lw=lwD * 1.2
                    )
                    cir2 = plt.Circle(
                        fixed_coor[i][::-1], r, color="#CB8680", fill=False, lw=lwD * 1.2
                    )
                    mask = (xs[np.newaxis, :] - fixed_coor[i][1]) ** 2 + (
                        ys[:, np.newaxis] - fixed_coor[i][0]
                    ) ** 2 < r ** 2
                    roiC = data[i][mask]
                    temp = round(np.nanmean(roiC), 2)
                    means.append(temp)
                else:
                    cir = plt.Circle(
                        fixed_coor[i][::-1], r, color="#007CB7", fill=False, lw=lwD * 1.2
                    )
                    cir2 = plt.Circle(
                        fixed_coor[i][::-1], r, color="#CB8680", fill=False, lw=lwD * 1.2
                    )
                    mask = (xs[np.newaxis, :] - fixed_coor[i][1]) ** 2 + (
                        ys[:, np.newaxis] - fixed_coor[i][0]
                    ) ** 2 < r ** 2
                    roiC = data[i][mask]
                    temp = round(np.nanmean(roiC), 2)
                    means.append(temp)

                ax1.imshow(data[i], cmap="hot", vmin=vminT, vmax=vmaxT)
                ax1.add_artist(cir)

                # ax1.set_title("Thermal image", pad=title_pad)
                # ax1.set_ylabel("Temperature(°C)", labelpad=title_pad)
                ax1.set_axis_off()

                # Second subplot: 2D RAW
                if shutter[i] == shutter_closed:
                    x = np.arange(0, 160, 1)
                    y = np.arange(0, 120, 1)
                    xs, ys = np.meshgrid(x, y)
                    difframe = (xs * 0) + (ys * 0)

                    if momen[i] > 0.6 and momen[i] < 1:
                        baseline_frames_buffer.append(data[i])

                elif shutter[i] == shutter_open:
                    if len(shutter_state) == 0:
                        shutter_time_open = time.time()
                        shutter_state.append(shutter_time_open)
                        # print(shutter_state)

                    meaned_baseline = np.nanmean(baseline_frames_buffer, axis=0)
                    difframe = meaned_baseline - data[i]
                    difframe[data[i] <= 18] = 0

                else:
                    x = np.arange(0, 160, 1)
                    y = np.arange(0, 120, 1)
                    xs, ys = np.meshgrid(x, y)
                    difframe = (xs * 0) + (ys * 0)

                ax4.clear()
                ax4.imshow(difframe, cmap="winter", vmin=vminDF, vmax=vmaxDF)
                ax4.add_artist(cir2)
                ax4.set_axis_off()
                # ax4.set_title("Thermal difference image", pad=title_pad)

                # MEAN TEMPERATURE
                ax2.clear()
                ax2.plot(means, lw=lwD * 1.2, color="#007CB7")
                ax2.set_ylim([21, 27])
                ax2.set_xlim([0, len(data)])
                # ax2.set_xlim([0, len(means)])
                # ax1.set_ylim([0, len(dat_im.data["image"])])
                # ax2.set_title("Mean temperature fixed ROI", pad=title_pad)

                steps = 1
                framesToseconds(ax2, steps, data)

                ax2.spines["top"].set_visible(False)
                ax2.spines["right"].set_visible(False)

                ax2.yaxis.set_tick_params(width=lwD, length=lenD)
                ax2.xaxis.set_tick_params(width=lwD, length=lenD)

                ax2.tick_params(axis="y", which="major", pad=10)
                ax2.tick_params(axis="x", which="major", pad=10)

                ax2.spines["left"].set_linewidth(lwD)
                ax2.spines["bottom"].set_linewidth(lwD)
                ax2.set_xlabel("Time (s)")
                ax2.set_ylabel("Temperature (°C)", labelpad=25)

                # Delta
                ax3.clear()
                ax3.plot(deltas[:i], lw=lwD * 1.2, color="#CB8680")
                ax3.set_ylim([0, 5])
                # ax3.set_xlim([0, len(means)])
                ax3.set_xlim([0, len(data)])
                # ax3.set_title("Delta", pad=title_pad)
                ax3.axhline(delta_value, 0, len(means), color="#007CB7", ls="--", lw=lwD)

                framesToseconds(ax3, steps, data)

                ax3.spines["top"].set_visible(False)
                ax3.spines["right"].set_visible(False)

                ax3.yaxis.set_tick_params(width=lwD, length=lenD)
                ax3.xaxis.set_tick_params(width=lwD, length=lenD)

                ax3.tick_params(axis="y", which="major", pad=10)
                ax3.tick_params(axis="x", which="major", pad=10)

                ax3.spines["left"].set_linewidth(lwD)
                ax3.spines["bottom"].set_linewidth(lwD)
                ax3.set_xlabel("Time (s)")
                ax3.set_ylabel("Change in temperature\n(ΔT °C)", labelpad=25)

                plt.tight_layout()

            ################ Plot figure
            fig = plt.figure(figsize=(35, 20))

            mc = "black"
            plt.rcParams.update(
                {
                    "font.size": 40,
                    "axes.labelcolor": "{}".format(mc),
                    "xtick.color": "{}".format(mc),
                    "ytick.color": "{}".format(mc),
                    "font.family": "sans-serif",
                }
            )

            #######################Axes
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(223)
            ax3 = fig.add_subplot(224)
            ax4 = fig.add_subplot(222)

            x = np.arange(0, 160, 1)
            y = np.arange(0, 120, 1)

            xs, ys = np.meshgrid(x, y)
            zs = (xs * 0 + 15) + (ys * 0 + 15)

            ######################Plots
            ## First subplot: 2D video
            plot1 = ax1.imshow(zs, cmap="hot", vmin=vminT, vmax=vmaxT)
            cb = fig.colorbar(plot1, ax=ax1, location = 'left', label = "Temperature (°C)")
            cb.set_ticks(np.arange(vminT, (vmaxT + 0.01), 1))
            # print(cb.ax.get_children())
            # cb.ax.get_children()[4].set_linewidth(35.0)
            cb.ax.tick_params(size = 0, width = 5)
            cb.outline.set_visible(False)
            # cb.set_ticks([])
            # cb.lines1[4].set_linewidth([2]*11)

            vminDF = 0
            vmaxDF = 5
            plot4 = ax1.imshow(zs, cmap="winter", vmin=vminDF, vmax=vmaxDF)
            cbdif = fig.colorbar(plot4, ax=ax4, location = 'left', label = "Change in Temperature\n(ΔT °C)")
            cbdif.set_ticks(np.arange(vminDF, (5 + 0.01), 1))
            cbdif.ax.tick_params(size = 0, width = 5)
            cbdif.outline.set_visible(False)
            # cbdif.set_ticks([])

            ## Second subplot: mean ROI
            plot2 = ax2.plot(
                np.arange(len(dat_im.data["image"])),
                np.arange(len(dat_im.data["image"])),
                color="black",
            )

            ## Third subplot:
            plot3 = ax3.plot(
                np.arange(len(dat_im.data["image"])),
                np.arange(len(dat_im.data["image"])),
                color="black",
            )

            # Aesthetics
            plots = [plot1, plot2, plot3]
            axes = [ax1, ax2, ax3]

            print(len(dat_im.data["image"]))

            ax2.set_xlim([0, len(dat_im.data["image"])])
            ax3.set_xlim([0, len(dat_im.data["image"])])

            baseline_buffer = []
            delta = []
            baseline_frames_buffer = []

            # Animation & save
            shutter_state = []
            print("delta value 2", delta_value)
            ani = animation.FuncAnimation(
                fig,
                animate,
                frames=len(dat_im.data["image"]),
                fargs=(
                    dat_im.data["image"],
                    plots,
                    axes,
                    dat_im.data["fixed_ROI"],
                    dat_im.data["diff_ROI"],
                    means,
                    dat_im.data["sROI"],
                    baseline_buffer,
                    dat_im.data["delta"],
                    dat_im.data["shutter_pos"],
                    dat_im.data["time_now"],
                    baseline_frames_buffer,
                    shutter_state,
                    delta_value,
                ),
                interval=1000 / 8.7,
            )

            mp4_name = "mp4_" + n
            # mp4_name = 'mp4_' + n
            ani.save(f"./{path_animation}/{mp4_name}.mp4", writer=writer)

            fig.clf()
