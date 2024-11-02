import util as ut
import matplotlib.pyplot as plt
import matplotlib as mpl

# mpl params
textsize = 24
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
    "figure.figsize": [12, 4],
}
mpl.rcParams.update(params)

# Path
DATA_PATH = "../../data/"

# Compensensate for XCAL trace delay
offset = ut.defaultOffset

# Pick a time
time_range = (15, 45)

fname = DATA_PATH + "sample_iperf3_traces/tcp-recv-4-2023-02-13-225402.log"
iperf_tcp, tcp_start_time = ut.read_iperf(fname)
iperf_tcp = ut.set_df_range(iperf_tcp, time_range)
iperf_tcp["throughput"] /= 1000000
(tcp_line,) = plt.plot(
    iperf_tcp["seconds"], iperf_tcp["throughput"], c="tab:blue", label="$TCP$"
)

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
tcp_ho = plt.scatter(
    ho_ts[:-1], ho_y, s=160, marker="x", color="tab:red", label=r"$HO_{tcp}$", zorder=10
)

# UDP values count
fname = DATA_PATH + "sample_iperf3_traces/udp-bw-jitter-2-2023-02-16-224741.log"
iperf_udp, start_time = ut.read_iperf(fname)
iperf_udp = ut.set_df_range(iperf_udp, time_range)
iperf_udp["throughput"] /= 1000000
(udp_line,) = plt.plot(
    iperf_udp["seconds"],
    iperf_udp["throughput"],
    c="tab:orange",
    linestyle="--",
    label="$UDP$",
)

ho_udp = ut.read_handover(
    DATA_PATH + "sample_link_layer_traces/udp-ho.csv", 2, 16, 2023
)
ho_udp["seconds"] -= offset
ho_udp["seconds"] = ho_udp["seconds"] - start_time
ho_udp = ut.set_df_range(ho_udp, time_range)
ho_ts = []
for i, r in ho_udp.iterrows():
    if "MAC RACH Attempt" in r["Message"]:
        ho_ts.append(round(r["seconds"], 1))
        # plt.axvline(r[sec], c='tab:green', label='Handover-UDP')
idx = 0
ho_y = []
for i, r in iperf_udp.iterrows():
    if idx < len(ho_ts):
        if r["seconds"] == ho_ts[idx]:
            ho_y.append(r["throughput"])
            idx += 1
    else:
        break
udp_ho = plt.scatter(
    ho_ts, ho_y, s=160, marker="^", color="tab:green", label=r"$HO_{udp}$", zorder=10
)

plt.legend(loc="upper left", ncol=1, borderpad=0, frameon=False)
plt.tight_layout()
plt.ylabel("Throughput(Mbps)")
plt.xlabel("Time(s)")
plt.savefig(
    "./fig/fig_2.pdf",
    format="pdf",
    dpi=600,
    transparent=True,
    bbox_inches="tight",
    pad_inches=0,
)

plt.show()
