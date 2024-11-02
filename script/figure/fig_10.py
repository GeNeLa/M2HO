import util as ut
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# mpl params
textsize = 20
params = {
    "axes.labelsize": textsize,
    "font.size": textsize,
    "legend.fontsize": textsize,
    "legend.handlelength": 1.5,
    "legend.numpoints": 1,
    "xtick.labelsize": textsize,
    "ytick.labelsize": textsize,
    "lines.linewidth": 2.5,
    "text.usetex": False,
    "figure.figsize": [6, 3],
}
mpl.rcParams.update(params)

# Path
DATA_PATH = "../../data/"

# Define line styles, colors, and plot parameters
line_styles = ["solid", "dotted", "dashed", "dashdot", (0, (3, 5, 1, 5, 1, 5))]
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

# Create a figure and set of subplots
fig, axs = plt.subplots(1, 4, figsize=(18, 3), sharey=True)


# read one trace
def read_graph(fname):
    result = {}
    with open(fname, "r") as fin:
        while True:
            line = fin.readline().strip()
            if line == "":
                break
            algo = line
            sub_result = []
            while True:
                line = fin.readline().strip()
                if line == "":
                    break
                sub_result.append(float(line))
            result[algo] = sub_result
    return result


# Plotting on each subplot
# cell = {"sub-6GHz": 0, "mmWave": 1}
# sub6-mmW = (0, 1)
ho_type = [(0, 0), (0, 1), (1, 1), (1, 0)]
for subplot_i, ax in enumerate(axs):
    i, j = ho_type[subplot_i]
    ".."
    data_dict = read_graph(DATA_PATH + f"/results/overall-tput-{i}-{j}.txt")
    for k, key in enumerate(data_dict.keys()):
        x, y = ut.ecdf(data_dict[key])
        x = np.insert(x, 0, x[0])
        y = np.insert(y, 0, 0.0)
        y = [v * 100 for v in y]
        ax.plot(x, y, label=key, linestyle=line_styles[k], color=colors[k])
        ax.grid(True)
    if subplot_i == 0:
        ax.set_ylabel("CDF(%)")
        # Creating a shared legend on top
        fig.legend(
            labels=list(data_dict.keys()),
            loc="upper center",
            ncol=5,
            borderpad=0,
            frameon=False,
        )
    ax.set_xlabel("Tput.(Mbps)")

# Adjusting layout
plt.tight_layout(rect=[0, 0, 1, 0.9])  # Adjust rect to fit the legend

# Save the figure
fig.savefig(
    "./fig/fig_10.pdf",
    format="pdf",
    dpi=600,
    transparent=True,
    bbox_inches="tight",
    pad_inches=0,
)

plt.show()
