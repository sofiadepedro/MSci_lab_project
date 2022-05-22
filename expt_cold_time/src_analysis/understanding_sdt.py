# %%
import pandas as pd

from scipy.stats import norm
import math

Z = norm.ppf

mydata = [
    ["1", "0", "1"],
    ["1", "0", "1"],
    ["1", "0", "0"],
    ["1", "0", "0"],
    ["1", "0", "0"],
    ["1", "1", "1"],
    ["1", "1", "1"],
    ["1", "1", "1"],
    ["1", "1", "1"],
    ["1", "1", "0"],
    ["0", "0", "0"],
    ["0", "0", "0"],
    ["0", "0", "0"],
    ["0", "0", "0"],
    ["0", "0", "0"],
    ["0", "1", "0"],
    ["0", "1", "0"],
    ["0", "1", "0"],
    ["0", "1", "0"],
    ["0", "1", "0"],
]


table = pd.DataFrame(mydata, columns = ["touch", "cold", "response"])
print(table)

# %%
table_cold = table.loc[table["cold"] == '1']
table_nocold = table.loc[table["cold"] == '0']


present_yes = table_cold.loc[table_cold["response"] == '1']
present_no = table_cold.loc[table_cold["response"] == '0']

absent_yes = table_nocold.loc[table_nocold["response"] == '1']
absent_no = table_nocold.loc[table_nocold["response"] == '0']

hits = len(present_yes.loc[:, "response"])
misses = len(present_no.loc[:, "response"])

fas = len(absent_yes.loc[:,"response"])
crs = len(absent_no.loc[:, "response"])

print("Hits:", hits)
print("Misses:", misses)
print("False ALarm:", fas)
print("Correct rejection:", crs)

# correc_present = round(hits / sum(hits, misses), 3)
# correc_absent = round(crs / sum(crs, fas), 3)

# %% 
# Calculate hit_rate and avoid d' infinity
hits += 0.5
hit_rate = hits / (hits + misses + 1)

# Calculate false alarm rate and avoid d' infinity
fas += 0.5
fa_rate = fas / (fas + crs + 1)

print("Hit Rate:", hit_rate)
print("False Alarm:", fa_rate)

# Return d', beta, c and Ad'

d = Z(hit_rate) - Z(
    fa_rate
)  # Hint: normalise the centre of each curvey and subtract them (find the distance between the normalised centre

beta = math.exp((Z(fa_rate) ** 2 - Z(hit_rate) ** 2) / 2)

c = (
    Z(hit_rate) + Z(fa_rate)
) / 2  # Hint: like d prime but you add the centres instead, find the negative value and half it

Ad = norm.cdf(d / math.sqrt(2))

correct = (hits + crs) / (hits + misses + fas + crs)

print("d':", d)
print("response bias:", c)
print("Correct answers:", correct)

