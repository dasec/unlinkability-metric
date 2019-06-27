'''
Implementation of the local and global unlinkability metrics for biometric template protection systems evaluation.
More details in:


[TIFS18] M. Gomez-Barrero, J. Galbally, C. Rathgeb, C. Busch, "General Framework to Evaluate Unlinkability
in Biometric Template Protection Systems", in IEEE Trans. on Informations Forensics and Security, vol. 3, no. 6, pp. 1406-1420, June 2018

Please remember to reference article [TIFS18] on any work made public, whatever the form,
based directly or indirectly on these metrics.
'''

__author__ = "Marta Gomez-Barrero"
__copyright__ = "Copyright (C) 2017 Hochschule Darmstadt"
__license__ = "License Agreement provided by Hochschule Darmstadt (https://github.com/dasec/unlinkability-metric/blob/master/hda-license.pdf)"
__version__ = "2.0"

import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import seaborn as sns
import argparse

######################################################################
### Parameter and arguments

parser = argparse.ArgumentParser(description='Evaluate unlinkability for two given sets of mated and non-mated linkage scores.')
parser.add_argument('matedScoresFile', help='filename for the mated scores', type=str)
parser.add_argument('nonMatedScoresFile', help='filename for the non-mated scores', type=str)
parser.add_argument('figureFile', help='filename for the output figure', type=str)
parser.add_argument('--omega', help='omega value for the computations, if none provided, omega = 1', nargs='?', default=1., type=float)
parser.add_argument('--nBins', help='number of bins for the computations, if none provided, nBins = min(length(matedScoresFile) / 10, 100)', nargs='?', default=-1, type=int)
parser.add_argument('--figureTitle', help='title for the output figure', nargs='?', default='Unlinkability analysis', type=str)
parser.add_argument('--legendLocation', help='legend location', nargs='?', default='upper right', type=str)


args = parser.parse_args()
matedScoresFile = args.matedScoresFile
nonMatedScoresFile = args.nonMatedScoresFile
figureFile = args.figureFile
figureTitle = args.figureTitle
legendLocation = args.legendLocation
omega = args.omega
nBins = args.nBins


######################################################################
### Evaluation

# load scores
matedScores = numpy.fromfile(matedScoresFile)
nonMatedScores = numpy.fromfile(nonMatedScoresFile)

if nBins == -1:
	nBins = min(len(matedScores)/10,100)

# define range of scores to compute D
bin_edges = numpy.linspace(min([min(matedScores), min(nonMatedScores)]), max([max(matedScores), max(nonMatedScores)]), num=nBins + 1, endpoint=True)
bin_centers = (bin_edges[1:] + bin_edges[:-1]) / 2 # find bin centers

# compute score distributions (normalised histogram)
y1 = numpy.histogram(matedScores, bins = bin_edges, density = True)[0]
y2 = numpy.histogram(nonMatedScores, bins = bin_edges, density = True)[0]

# Compute LR and D
LR = numpy.divide(y1, y2, out=numpy.ones_like(y1), where=y2!=0)
D = 2*(omega*LR/(1 + omega*LR)) - 1
D[omega*LR <= 1] = 0
D[y2 == 0] = 1 # this is the definition of D, and at the same time takes care of inf / nan

# Compute and print Dsys
Dsys = numpy.trapz(x = bin_centers, y = D* y1)
print(Dsys)


### Plot final figure of D + score distributions

plt.clf()

sns.set_context("paper",font_scale=1.7, rc={"lines.linewidth": 2.5})
sns.set_style("white")

ax = sns.kdeplot(matedScores, shade=False, label='Mated', color=sns.xkcd_rgb["medium green"])
x1,y1 = ax.get_lines()[0].get_data()
ax = sns.kdeplot(nonMatedScores, shade=False, label='Non-Mated', color=sns.xkcd_rgb["pale red"],linewidth=5, linestyle='--')
x2,y2 = ax.get_lines()[1].get_data()

ax2 = ax.twinx()
lns3, = ax2.plot(bin_centers, D, label='$\mathrm{D}_{\leftrightarrow}(s)$', color=sns.xkcd_rgb["denim blue"],linewidth=5)

# print omega * LR = 1 lines
index = numpy.where(D <= 0)
ax.axvline(bin_centers[index[0][0]], color='k', linestyle='--')

#index = numpy.where(LR > 1)
#ax.axvline(bin_centers[index[0][2]], color='k', linestyle='--')
#ax.axvline(bin_centers[index[0][-1]], color='k', linestyle='--')


# Figure formatting
ax.spines['top'].set_visible(False)
ax.set_ylabel("Probability Density")
ax.set_xlabel("Score")
ax.set_title("%s, $\mathrm{D}_{\leftrightarrow}^{\mathit{sys}}$ = %.2f" % (figureTitle, Dsys),  y = 1.02)

labs = [ax.get_lines()[0].get_label(), ax.get_lines()[1].get_label(), ax2.get_lines()[0].get_label()]
lns = [ax.get_lines()[0], ax.get_lines()[1], lns3]
ax.legend(lns, labs, loc = legendLocation)

ax.set_ylim([0, max(max(y1), max(y2)) * 1.05])
ax.set_xlim([bin_edges[0]*0.98, bin_edges[-1]*1.02])
ax2.set_ylim([0, 1.1])
ax2.set_ylabel("$\mathrm{D}_{\leftrightarrow}(s)$")

plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.15)
plt.gcf().subplots_adjust(right=0.88)
pylab.savefig(figureFile)
