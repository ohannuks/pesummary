from pesummary.gw.file.strain import StrainData
from pesummary.io import read
import requests

# First we download the GW190814 posterior samples.
data = requests.get(
    "https://dcc.ligo.org/public/0168/P2000183/008/GW190814_posterior_samples.h5"
)
with open("GW190814_posterior_samples.h5", "wb") as f:
    f.write(data.content)

# # Next we fetch the LIGO Livingston data around the time of GW190814
L1_data = StrainData.fetch_open_data('L1', 1249852257.01 - 20, 1249852257.01 + 5)

# We then read in the posterior samples and generate the maximum likelihood
# waveform in the time domain
samples = read("GW190814_posterior_samples.h5").samples_dict["C01:SEOBNRv4PHM"]
maxL = samples.maxL_td_waveform("SEOBNRv4PHM", 1. / 4096, 20., project="L1")
# Next we plot the data
fig = L1_data.plot(
    type="td", merger_time=1249852257.01, window=(-0.1, 0.04),
    template={"L1": maxL}, bandpass_frequencies=[50., 300.]
)
fig.savefig("GW190814.png")
fig.close()