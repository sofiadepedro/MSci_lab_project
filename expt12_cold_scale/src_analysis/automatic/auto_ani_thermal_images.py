from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import os
import argparse
import time

from classes_tharnal import GrabNamesOrder, get_delta
from classes_plotting import framesToseconds
from classes_tharnal import ReAnRaw
from saving_data import checkORcreate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder name")
    parser.add_argument("-f", type=str)
    args = parser.parse_args()
    folder_name = args.f

    path = os.path.realpath(__file__)
    root_path = path.rsplit("/", 3)[0]
    path_animation = checkORcreate(f"../data/{folder_name}/animations")
    print(path_animation)

    ### SUBJECT
    pattern = f".*\.hdf5$"
    path_videos = f"../data/{folder_name}/videos/"
    names = GrabNamesOrder(pattern, path_videos)

    # ANIMATION
    for i, n in enumerate(names):
        list_splitted = n.split("_")
        try:
            delta_string = get_delta(list_splitted, "delta")
            delta_value = int(delta_string[-1])
        except:
            delta_value = 1

        if delta_value != 0:
            dat_im = ReAnRaw(f"../data/{folder_name}/videos/{n}")
            dat_im.datatoDic()
            print(n)
            means = []

            Writer = animation.writers["ffmpeg"]
            writer = Writer(fps=9, metadata=dict(artist="Me"), bitrate=1800)
            vminT = 20
            vmaxT = 28

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

                if sROI[i] == 1:
                    if np.shape(diff_coor[i])[1] > 1:
                        cdif = diff_coor[i][:, 0]
                        cy = cdif[1]
                        cx = cdif[0]
                    else:
                        cdif = diff_coor[i]
                        cy = cdif[1][0]
                        cx = cdif[0][0]

                    cir = plt.Circle(cdif[::-1], r, color="b", fill=False, lw=lwD * 1.2)
                    mask = (xs[np.newaxis, :] - cy) ** 2 + (
                        ys[:, np.newaxis] - cx
                    ) ** 2 < r ** 2
                    roiC = data[i][mask]
                    temp = round(np.mean(roiC), 2)
                    means.append(temp)

                elif sROI[i] == 0:
                    cir = plt.Circle(
                        fixed_coor[i][::-1], r, color="b", fill=False, lw=lwD * 1.2
                    )
                    mask = (xs[np.newaxis, :] - fixed_coor[i][1]) ** 2 + (
                        ys[:, np.newaxis] - fixed_coor[i][0]
                    ) ** 2 < r ** 2
                    roiC = data[i][mask]
                    temp = round(np.mean(roiC), 2)
                    means.append(temp)

                ax1.imshow(data[i], cmap="hot", vmin=vminT, vmax=vmaxT)
                ax1.add_artist(cir)

                ax1.set_title("Thermal image", pad=title_pad)
                ax1.set_axis_off()

                # Second subplot: 2D RAW
                if shutter[i] == shutter_closed:
                    x = np.arange(0, 160, 1)
                    y = np.arange(0, 120, 1)
                    xs, ys = np.meshgrid(x, y)
                    difframe = (xs * 0) + (ys * 0)

                    if momen[i] > 1.6 and momen[i] < 2:
                        baseline_frames_buffer.append(data[i])

                elif shutter[i] == shutter_open:
                    if len(shutter_state) == 0:
                        shutter_time_open = time.time()
                        shutter_state.append(shutter_time_open)

                    meaned_baseline = np.mean(baseline_frames_buffer, axis=0)
                    difframe = meaned_baseline - data[i]
                    difframe[data[i] <= 28] = 0
                    maxdif = np.max(difframe)

                else:
                    x = np.arange(0, 160, 1)
                    y = np.arange(0, 120, 1)
                    xs, ys = np.meshgrid(x, y)
                    difframe = (xs * 0) + (ys * 0)

                ax4.clear()
                ax4.imshow(difframe, cmap="winter", vmin=vminDF, vmax=vmaxDF)
                # ax4.add_artist(cir)
                ax4.set_title("Thermal difference image", pad=title_pad)

                # MEAN TEMPERATURE
                ax2.clear()
                ax2.plot(means, lw=lwD * 1.2, color="#007CB7")
                ax2.set_ylim([23, 30])
                ax2.set_xlim([0, len(means)])
                ax2.set_title("Mean temperature fixed ROI", pad=title_pad)

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

                # Delta
                ax3.clear()
                ax3.plot(deltas[:i], lw=lwD * 1.2, color="#007CB7")
                ax3.set_ylim([0, 6])
                ax3.set_xlim([0, len(means)])
                ax3.set_title("Delta", pad=title_pad)
                ax3.axhline(delta_value, 0, len(means), color="b", ls="--")

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
            cb = fig.colorbar(plot1, ax=ax1)
            cb.set_ticks(np.arange(vminT, (vmaxT + 0.01), 1))

            vminDF = 0
            vmaxDF = 5.5
            plot4 = ax1.imshow(zs, cmap="winter", vmin=vminDF, vmax=vmaxDF)
            cbdif = fig.colorbar(plot4, ax=ax4)
            cbdif.set_ticks(np.arange(vminDF, (vmaxDF + 0.01), 1))

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

            baseline_buffer = []
            delta = []
            baseline_frames_buffer = []

            # Animation & save
            shutter_state = []
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
