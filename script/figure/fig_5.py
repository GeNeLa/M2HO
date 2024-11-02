import util as ut
import matplotlib.pyplot as plt
import matplotlib as mpl

# mpl params
textsize = 18
params = {
    "axes.labelsize": textsize,
    "font.size": textsize,
    "legend.fontsize": textsize - 4,
    "xtick.labelsize": textsize,
    "ytick.labelsize": textsize,
    "lines.linewidth": 1.5,
    "text.usetex": False,
    "figure.figsize": [5, 2],
}
mpl.rcParams.update(params)

# Compensensate for XCAL trace delay
offset = ut.defaultOffset

# Path
DATA_PATH = "../../data/"

# Pick a time
time_range = (10, 40)

fname = DATA_PATH + "sample_iperf3_traces/tcp-recv-4-2023-02-13-225402.log"

iperf_tcp, tcp_start_time = ut.read_iperf(fname)
iperf_tcp = ut.set_df_range(iperf_tcp, time_range)
iperf_tcp["throughput"] /= 1000000

ho_tcp = ut.read_handover(
    DATA_PATH + "sample_link_layer_traces/tcp-ho.csv", 2, 13, 2023
)
ho_tcp["seconds"] -= offset
ho_tcp["seconds"] = ho_tcp["seconds"] - tcp_start_time
ho_tcp = ut.set_df_range(ho_tcp, time_range)
ho_ts = []
for i, r in ho_tcp.iterrows():
    if "MAC RACH Attempt" in r["Message"]:
        ho_ts.append(round(r["seconds"], 1))
        # plt.axvline(r[sec], c='tab:red')
idx = 0
ho_y = []
for i, r in iperf_tcp.iterrows():
    if idx < len(ho_ts) - 1:
        if r["seconds"] == ho_ts[idx]:
            ho_y.append(r["throughput"])
            idx += 1
    else:
        break

# CW
fname = DATA_PATH + "sample_iperf3_traces/iperf-sender-tcp-4-2023-02-14-065333.log"
df_sender, start_time = ut.read_iperf(fname, sender=True)
df_sender = ut.set_df_range(df_sender, time_range)

# plot
fig, ax = plt.subplots()

ax.plot(iperf_tcp["seconds"], iperf_tcp["throughput"], c="tab:blue", label="TCP")
ax.set_xlabel("Time(s)", labelpad=0)
ax.set_ylabel("Tput(Mbps)     ", labelpad=0)

ax2 = ax.twinx()
c = "tab:green"
ax2.plot(
    df_sender["seconds"],
    df_sender["snd_cwnd"] / 1000000,
    linestyle="--",
    label="CW",
    color=c,
    zorder=10,
)

ax.scatter(
    [ho_ts[0], ho_ts[2]],
    [ho_y[0], ho_y[2]],
    s=60,
    marker="^",
    color="tab:red",
    label="Horizontal HO",
    zorder=20,
)
ax.scatter(
    [ho_ts[1]],
    [ho_y[1]],
    s=60,
    marker="o",
    color="tab:orange",
    label="Vertical HO",
    zorder=20,
)

fig.legend(
    frameon=False,
    bbox_transform=ax.transAxes,
    bbox_to_anchor=(1.85, -0.3),
    loc="lower right",
    ncol=1,
    borderpad=0,
    handletextpad=0.5,
    columnspacing=0.1,
    labelspacing=0.5,
)

plt.ylabel("CW(MB)")
plt.xlabel("Time (s)", labelpad=0)
plt.tight_layout()
plt.savefig(
    "./fig/fig_5.pdf",
    dpi=600,
    transparent=True,
    bbox_inches="tight",
    pad_inches=0,
)
plt.show()
