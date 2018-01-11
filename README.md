# Unlinkability Metrics

Implementation of the local and global unlinkability metrics for biometric template protection systems evaluation proposed in [[TIFS18]](https://doi.org/10.1109/TIFS.2017.2788000).

## License
This work is licensed under license agreement provided by Hochschule Darmstadt ([h_da-License](/hda-license.pdf)).

## Instructions

### Dependencies
* seaborn
* numpy
* pylab
* matplotlib
* argparse

### Usage

1. Run evaluateUnlinkability.py 

	```python
	usage: evaluateUnlinkability.py [-h] [--omega [OMEGA]] [--nBins [NBINS]]
									[--figureTitle [FIGURETITLE]]
									[--legendLocation [LEGENDLOCATION]]
									matedScoresFile nonMatedScoresFile figureFile

	Evaluate unlinkability for two given sets of mated and non-mated linkage
	scores.

	positional arguments:
	  matedScoresFile       filename for the mated scores
	  nonMatedScoresFile    filename for the non-mated scores
	  figureFile            filename for the output figure

	optional arguments:
	  -h, --help            show this help message and exit
	  --omega [OMEGA]       omega value for the computations, if none provided,
							omega = 1
	  --nBins [NBINS]       number of bins for the computations, if none provided,
							nBins = 100
	  --figureTitle [FIGURETITLE]
							title for the output figure
	  --legendLocation [LEGENDLOCATION]
							legend location
	```

2. Input: at least 3 score files (mated and non-mated score examples provided), and optionally other parameters of the computation and the formatting of the figure obtained as output.

    The score files are loaded with the built-in function [numpy.fromfile()](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.fromfile.html).
    An example in hdf5 format has been provided, but other formats, such as a txt file with all scores separated by blank spaces
    or one score per row, can be also used.

3. Output: figure with score distributions, point-wise and global unlinkability metric results.

## References

More details in:

- [[TIFS18]](https://doi.org/10.1109/TIFS.2017.2788000) M. Gomez-Barrero, J. Galbally, C. Rathgeb, C. Busch, "General Framework to Evaluate Unlinkability
in Biometric Template Protection Systems", in IEEE Trans. on Informations Forensics and Security, 2018 (to appear)

Please remember to reference article [[TIFS18]](https://doi.org/10.1109/TIFS.2017.2788000) on any work made public, whatever the form,
based directly or indirectly on these metrics.
