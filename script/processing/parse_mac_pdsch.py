# Filter in Qualcomm DM Message: 5GNR-MAC Layer-NR5G MAC PDSCH Status
import xcalparser
import pandas as pd

tab = xcalparser.PDSCHMsg()

result = []
n = 4000  # Number of messages to parse
while n > 0:
    if len(tab.data) > 0:
        result.append(tab.data[-1])
    n -= 1
    tab.parse_next()

df = pd.concat(result, ignore_index=True)
df.to_csv("./pdsch-{}.csv".format("vz-120-ap-1"))
