# %%
import pandas as pd
import matplotlib.pyplot as plt
from globals import(
    conditions,
    part_to_use,
)
from local_functions import(
    universalMakeUp,
    textMakeUp 
)
import statistics

# %%
old_sdt_df = pd.read_csv("../data/sdt.csv")


sdt_df = old_sdt_df.drop(index= [3, 4, 5])

mean_data = {}

sdt_data = {}

# %%
print(sdt_df)
for i in range(1, 5):
    mean_data[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"] = sdt_df[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"].mean()

# %%
counter = 0

while counter < len(part_to_use):
    for i in range(1, 5):
        sdt_data[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"] = sdt_df[f"dif-{conditions[i]['name']}-{conditions[0]['name']}"]

    counter += 1


# %%
#PLOT DIFFERENCES OF D VS CONDITION
lwd = 10
pad_size = 20
lenD = 15
mc = "black"
lateral_wiggle = 0.2

textMakeUp(mc)

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(mean_data.values()), color='blue', linewidth='5')

ax.plot(list(sdt_data.values()))

plt.axhline(y=0, color='black', linestyle='--')


universalMakeUp(ax, lwd, pad_size, lenD)

x_axis = [0, 1, 2, 3]
ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("difference of d")
ax.set_title("SDT plot", pad=60)

# %%
#PLOT D VS CONDITION

d_prime_data = {}
mean_d_prime = {}

for i in range(0, 5):
    mean_d_prime[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"].mean()


for i in range(0, 5):
    d_prime_data[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"]

print(mean_d_prime)
print(d_prime_data)

lwd = 10
pad_size = 20
lenD = 15
mc = "black"
lateral_wiggle = 0.2

textMakeUp(mc)

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(mean_d_prime.values()), color='blue', linewidth='5')
ax.plot(list(d_prime_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

x_axis = [0, 1, 2, 3, 4]
ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("d values")
ax.set_title("SDT plot", pad=60)


# %%
cond_0 = {}
cond_1 = {}
cond_2 = {}
cond_3 = {}
cond_4 = {}

for i in range(0, 5):
    if i == 0:
        cond_0[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"]
        condi_0 = list(cond_0[f"d-{conditions[i]['name']}"])
        mean_0 = sdt_df[f"d-{conditions[i]['name']}"].mean()
        print(condi_0)
    if i == 1:
        cond_1[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"]
        condi_1 = list(cond_1[f"d-{conditions[i]['name']}"])
        mean_1 = sdt_df[f"d-{conditions[i]['name']}"].mean()
    if i == 2:
        cond_2[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"]
        condi_2 = list(cond_2[f"d-{conditions[i]['name']}"])
        mean_2 = sdt_df[f"d-{conditions[i]['name']}"].mean()
    if i == 3:
        cond_3[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"]
        condi_3 = list(cond_3[f"d-{conditions[i]['name']}"])
        mean_3 = sdt_df[f"d-{conditions[i]['name']}"].mean()
    if i == 4:
        cond_4[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"]
        condi_4 = list(cond_4[f"d-{conditions[i]['name']}"])
        mean_4 = sdt_df[f"d-{conditions[i]['name']}"].mean()


sd_0 = statistics.stdev(condi_0)
sd_1 = statistics.stdev(condi_1)
sd_2 = statistics.stdev(condi_2)
sd_3 = statistics.stdev(condi_3)
sd_4 = statistics.stdev(condi_4)

print(f"sd for condition 0 is", sd_0)
print(f"sd for condition 1 is", sd_1)
print(f"sd for condition 2 is", sd_2)
print(f"sd for condition 3 is", sd_3)
print(f"sd for condition 4 is", sd_4)



# %%
lwd = 10
pad_size = 20
lenD = 15
mc = "black"
lateral_wiggle = 0.2

textMakeUp(mc)

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

plot_cond = {}

counter = 0
while counter < len(part_to_use):
    for i in range(0, 5, 4):
        plot_cond[f"d-{conditions[i]['name']}"] = sdt_df[f"d-{conditions[i]['name']}"]
    counter += 1

ax.plot(list(plot_cond.values()))
ax.plot(0, mean_0, marker='o', markersize=25)
ax.plot(1, mean_4, marker='o', markersize=25)





universalMakeUp(ax, lwd, pad_size, lenD)

x_axis = [0, 1]
ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("d values")
ax.set_title("SDT plot", pad=60)


# %%
#PLOT C VS CONDITION

c_data = {}
mean_c = {}

for i in range(0, 5):
    mean_c[f"c-{conditions[i]['name']}"] = sdt_df[f"c-{conditions[i]['name']}"].mean()


for i in range(0, 5):
    c_data[f"c-{conditions[i]['name']}"] = sdt_df[f"c-{conditions[i]['name']}"]

print(c_data)
print(mean_c)

lwd = 10
pad_size = 20
lenD = 15
mc = "black"
lateral_wiggle = 0.2

textMakeUp(mc)

fig, ax = plt.subplots(1, 1, figsize=(20, 15))

ax.plot(list(mean_c.values()), color='blue', linewidth='5')
ax.plot(list(c_data.values()))

universalMakeUp(ax, lwd, pad_size, lenD)

x_axis = [0, 1, 2, 3, 4]
ax.set_xticks(x_axis)

ax.set_xlabel("Conditions", labelpad=pad_size)
ax.set_ylabel("Response bias (c)")
ax.set_title("SDT plot", pad=60)
