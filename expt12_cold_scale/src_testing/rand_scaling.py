import numpy as np
from rand_cons import check_twoD


# Prepare Position Zabers
def choosing_next_pos(positions, positions_list, limit):
    """
    Function to randomly choose a position within a grid
    """
    while True:
        randomly_chosen_next = np.random.choice(
            list(positions.keys()), 1, replace=True
        )[0]
        if len(positions_list) == 0:
            positions_list.append(randomly_chosen_next)
            break
        else:
            backwards = []
            for bi in np.arange(1, limit + 0.1, 1):
                if len(positions_list) < bi:
                    break
                current_check = check_twoD(
                    positions_list, randomly_chosen_next, bi, positions
                )
                backwards.append(current_check)

            if np.all(backwards):
                positions_list.append(randomly_chosen_next)
                break

            else:
                print("WRONG VALUE!")
    return randomly_chosen_next


# Set up Trials for Conditions
def scal_setup_trial(n_trials, mags, randomised=True):
    """
    Funtion to set-up trials for a scaling eperiment.
    The number of trials will be distributed equally across the number of conditions (magnitudes).
    For instance, if we have 1 condition and you set n_trials = 10, there'll be 10 trials of this condition.
    However, if we have 2 conditions and you set n_trials = 10, there'll be 5 trials of each condition.
    Touch absent and present are coded with 0s (absent) and 1s (present), respectively.
    Conditions are coded from 0-n.
    Condition and touch absent/present come in tuples.
    """
    stimulations = []
    conds = len(mags)
    if not n_trials % (2 * conds) == 0:
        print(f"Number of trials is not divisable by {2*conds}")
        if not n_trials % 2 == 0:
            print(f"Number of trials is an odd number")
        print("WARNING: Uneven number of conditions")
        code_conds = mags
        n_cond_trials = n_trials / conds

        n_conds = np.repeat(code_conds, n_cond_trials, axis=0)
        unique, counts = np.unique(n_conds, return_counts=True)
        # print(counts)
        # print(unique)
        for u, c in zip(unique, counts):
            abs_pres = np.repeat([0, 1], c, axis=0)
            # print(abs_pres)

            for ap in abs_pres:
                stimulations.append((u, ap))
        if randomised:
            np.random.shuffle(stimulations)
        stimulations = stimulations[:n_trials]
        # print(stimulations)
    else:
        code_conds = mags
        n_cond_trials = n_trials / conds

        n_conds = np.repeat(code_conds, n_cond_trials, axis=0)
        unique, counts = np.unique(n_conds, return_counts=True)
        # print(counts)

        for u, c in zip(unique, counts):
            abs_pres = np.repeat([0, 1], c / 2, axis=0)

            for ap in abs_pres:
                stimulations.append((u, ap))
        if randomised:
            final = np.random.shuffle(stimulations)
    return stimulations
