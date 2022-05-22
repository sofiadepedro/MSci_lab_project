# %%
# Using statistics module

import statistics

data = [0.9, 0.6, 0.49727272727272764, 0.501818181818182, 1.103636363636364]

statistics.mean(data)
print("Mean of the sample is % s " % (statistics.mean(data)))

statistics.stdev(data)
print("Standard deviation of the sample is % s " % (statistics.stdev(data)))


# %%
# Using statistics module

import statistics

data = [0.9, 0.6, 0.49727272727272764, 0.501818181818182, 1.103636363636364]
mean = statistics.mean(data)
standard_deviation = statistics.stdev(data)

print(
    f"The mean of the sample is {mean} and the standard deviation is {standard_deviation}"
)


# %%
# Writing my own function

import numpy as np

# Mean
def mean(data):
    n = len(data)
    mean = sum(data) / n
    return mean


# Standard deviation
def variance(data):
    n = len(data)
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / (n - 1)
    return variance


def stdev(data):
    import math

    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev


data = np.array([0.9, 0.6, 0.49727272727272764, 0.501818181818182, 1.103636363636364])

print("Mean of the sample is % s " % (mean(data)))
print("Standard Deviation of the sample is % s " % (stdev(data)))


# %%
# Writing my own function

import numpy as np

# Mean
def mean(data):
    n = len(data)
    mean = sum(data) / n
    return mean


# Standard deviation
def variance(data):
    n = len(data)
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / (n - 1)
    return variance


def stdev(data):
    import math

    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev


data = np.array([0.9, 0.6, 0.49727272727272764, 0.501818181818182, 1.103636363636364])

mean = mean(data)
standard_deviation = stdev(data)

print(
    f"The mean of the sample is {mean} and the standard deviation is {standard_deviation}"
)


# %%
# Scatter plot

import numpy as np
import matplotlib.pyplot as plt

y = np.array([0.9, 0.6, 0.49727272727272764, 0.501818181818182, 1.103636363636364])
x = np.repeat([1], len(y))
plt.scatter(x, y)

x = np.array([1])
plt.scatter(x, mean, marker="_")

plt.tick_params(
    axis="x",  # changes apply to the x-axis
    which="both",  # both major and minor ticks are affected
    bottom=False,  # ticks along the bottom edge are off
    top=False,  # ticks along the top edge are off
    labelbottom=False,
)  # labels along the bottom edge are off

plt.ylabel("ΔT")
plt.show()

# %%
# Scatter plot

import numpy as np
import matplotlib.pyplot as plt

y = np.array([0.9, 0.6, 0.49727272727272764, 0.501818181818182, 1.103636363636364])
x = np.repeat([1], len(y))
plt.scatter(x, y)

x = np.array([1])
plt.scatter(x, mean, marker="_")

plt.xticks(x, labels=" ")

plt.ylabel("ΔT")
plt.show()
