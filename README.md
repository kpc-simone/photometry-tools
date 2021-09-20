# photometry-tools
Scripts for loading, processing, and analyzing photometry data

## Usage

in /scripts, do:

`python plot_photometry.py [SRf] [pre-baseline start] [pre-baseline end] [post-baseline start] [post-baseline end]`

Where 
`SRf`: Desired final sampling rate in Hz

`[pre-/post-]-baseline [start/end]`: start or end of pre- or post-baseline periods, used for photobleaching correction as well as transformation of timeseries to zscore



