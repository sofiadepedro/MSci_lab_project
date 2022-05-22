# MSci_lab_project

## This repository contains the code that I have used to design the experiment, control the hardware, and analyse the data of my MSci laboratory project

### Folder "expt12_cold_scale" contains the code of my first experiment: Studying the effect of touch on cooling perceived intensities using scaling (Figure 4)
  
  ##### Folder "src_testing" contains the code used to design the experiment and control the hardware during the experimental session.
      Files "thermal_camera_check.py", "zabers_check.py, and "touch_stability.py" are used to check that the set-up is working.
      Files "master_height_finding.py" and "height_extrapolation.py" are used to adapt the height of the linear stages based on each participant.
      File "grid_roi_finding.py" to find the region of interest for each of the stimulation sites (Figure 1B, 2A).
      File "exp_scaling.py" contains the code for the scaling psychophysical paradigm.
      Files "local_functions.py" and "globals.py" contain code that is reused in various files.
    
  ##### Folder "data" contains the collected data for each of the participants.
  
  ##### Folder "src_analysis" contains the code used to analyse the data.
      File "ani_thermal_images.py" to plot thermal data (Figure 2).
      File "plot_staircase.py" to plot data from the staircase paradigm (Figure 3B).
      File "fit_linreg.py" to fit linear regression to the data (Figure 4B).
      File "plot_all_means.py" to plot the data from the scaling paradigm (Figure 4B).
      Files "local_functions.py" and "globals.py" contain code that is reused in various files.
 

### Folder "expt_cold_time" contains the code of my second experiment: Effect of onset delay between tactile and cooling stimulations in the sensitivity to a cooling input (Figure 5)
  
  ##### Folder "src_testing" contains the code used to design the experiment and control the hardware during the experimental session.
      Files "thermal_camera_check.py", "zabers_check.py, and "touch_stability.py" are used to check that the set-up is working.
      Files "master_height_finding.py" and "height_extrapolation.py" are used to adapt the height of the linear stages based on each participant.
      File "grid_roi_finding.py" to find the region of interest for each of the stimulation sites (Figure 1B, 2A).
      Files "training_staircase.py" and "exp_stair.py" contain the code for the staircase paradigm.
      File "delta_calc.py" to calculate the ΔT target threshold that was used during signal detection.
      File "exp_sdt.py" contains the code for the signal detection paradigms.
      Files "local_functions.py" and "globals.py" contain code that is reused in various files.
    
  ##### Folder "data" contains the collected data for each of the participants.
  
  ##### Folder "src_analysis" contains the code used to analyse the data.
      File "ani_thermal_images.py" to plot thermal data (Figure 2).
      File "plot_staircase.py" (Figure 3B).
      File "nice_plots.py" (Figures 5B, 5C, 5D).
      Files "local_functions.py" and "globals.py" contain code that is reused in various files.
