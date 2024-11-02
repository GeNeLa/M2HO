# Mobicom24-M2HO-artifact

> \[MobiCom'24\] M2HO: Mitigating the Adverse Effects of 5G Handovers on TCP

This repository contains the dataset and scripts from MobiCom'24 paper, [_M2HO_: Mitigating the Adverse Effects of 5G Handovers on TCP](https://www.sigmobile.org/mobicom/2024/).

## Dataset

Here we release the dataset of our measurement traces and results.
This artifact is structured as followed:

```
data
├── measurements
│   ├── 202302
│   │   ├── 13
│   │   │   ├── 2-M1.drm - XCAL5 link-layer trace
│   │   │   ├── 2-M1.csv - Parsed RRC messages
│   │   │   ├── iperf-server-tcp-2-2023-02-06-093814.log - iPerf3 server log
│   │   │   ├── tcp-recv-2-2023-02-06-013858.log - iPerf3 client log
│   │   │   ├── pcap-server-tcp-2-2023-02-06-093814.pcap - TCP server packet trace
│   │   │   ├── udp-bw-recv-1-2023-02-06-013612.log - iPerf3 UDP client log
│   ....
│
└── results
    ├── overall-tput-0-0.txt - results for generating eval figures
    └── ...

script
├── experiment
│   ├── device/... - scripts for device to conduct measurement experiments
│   └── server/... - scripts for server to conduct measurement experiments
│
├── figure
│   ├── fig_10.py - Generate figure x in paper
│   └── ...
│
└── processing
    ├── parse_dci.py - Extract DCI information from XCAL5
    └── ...
```

The experiments are conducted in several different environment and mobility. Our measurement contains several different type of trace.
The XCAL DRM format can be read by ACCUVER XCAL5 and similar tools.
The RRC traces are exported by XCAL5.
The 5G layer 2 messages are extraced from XCAL5 using our script `xcalguiparser.py`.

## Instructions

We provided scripts and instructions for the following objectives:

- Conduct experiments
- Process data
- Generate figures

If hardware/software requirements cannot be met, feel free to reach out to the authors for demo or remote access.

### Conduct Experiments

**Server**
A server with high bandwidth (>1.5Gbps) is needed to fully explore the throughput of mmWave.

**Windows PC**
For collecting link-layer traces, install XCAL5 in Windows laptop.
Install [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools) for Windows.
The `adb` utility can be used to open a terminal to control device.

**Mobile phone**

- To perform link-layer measurements, an XCAL5 compatible phone is needed. Refer to the compatbility sheet in `script/experiment` to select a mobile phone.
- To perform TCP receiver side packet capture, a rooted phone is needed.

Experiments can be conducted separately if one phone cannot meet both requirements.

**Configure scripts**
Configure server IP and port in `script/experiment/device/client-run.sh` and `script/experiment/server/server-run.sh` .
Put scripts from `script/experiment/device` folder into an executable location in the phone, for example `/data/local/tmp/`.

#### TCP iPerf3 Test

To perform iPerf3 test, simply run iPerf3 at both sides. We can enable packet capture at server/client side if possible using tcpdump. XCAL5 should be used simultaneously if possible.

```bash
# At server TCP CUBIC (use b option for BBR)
./server-run.sh c
# At mobile client
./client-run.sh t
```

#### UDP Sequential Test

This test overcome issues where the XCAL5 compatible phones cannot perform receiver side TCP/UDP capturing. The flood sender sends UDP packets with incremental sizes. By observing link-layer packet sizes collected in XCAL5, we can correlate link-layer packet to transport layer packet, without need of packet capturing at client

To perform UDP flooding test, server sends UDP packets to client as fast as possible, while XCAL collects link-layer data at the same time.

```bash
# At server
python3 flood-sender.py
# At mobile client
./client-run.sh u
```

### Process Data

Follow the instructions below to setup Python3 environment for parsing, processing and plotting the data.

1. The scripts require python3 to be installed on the machine. We recommend that you also set up a python virtual environment such as [venv](https://docs.python.org/3/library/venv.html).

For example, assuming you're in a POSIX shell (bash...):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Activate the environment and install the required python packages

```bash
pip3 install -r requirements.txt
```

### Extracting Traces from XCAL5

[XCAL5](https://www.accuver.com/products/network-optimization/XCAL) can be installed on Windows machine. If assistance is needed, please contact the authors for remote access and demo.

The `script/processing/` folder contains helper scripts to batch process data from XCAL5 GUI views. Currently supported XCAL views: "Signalling Message", "5GNR NSA Status Information (Mobile1)", "Qualcomm DM Message (Mobile1)". But the script shoule be easily extensible to support more views.

- `xcalparser.py`: Interactive parser to inspect message from XCAL5 views
- `parse_dci.py` and `parse_mac_pdsch.py`: Parse X number of messages from XCAL5 DCI and MAC

To obtain 5G layer 2 message interactively for debugging, run the `script/processing/xcalguiparser.py` when XCAL5 is running in the replay mode.

### Generate Plots

Run the scripts in `script/figure`.
The generated results will be put in `script/figure/fig`.
