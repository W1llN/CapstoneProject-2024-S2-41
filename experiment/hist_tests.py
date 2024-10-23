"""
File: hist_tests.py
Date created: 14 Oct 2024
Author: William New (u3241279)

Description:
Outputs an ROC curve for LLM detector tests, where type
I and II errors are quantified for random sample of original
and rewritten abstracts are from its test on  (generated with
gen_tests_csv.py).
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics


# GLOBAL VARIABLE(s)
# List of tuples, with the form (filename, plot_label, subplot_loc, optional colour);
# subplot_loc is of the form (x, y), where (0, 0) is top left corner.
DETECTORS = [
	( "data/GPTZero_tests.csv",   "GPTZero",   (0, 0) , "#3c1ba0" ),
	( "data/Writefull_tests.csv", "Writefull", (1, 1),  "#f66824" ),
	( "data/Isgen_tests.csv",     "Isgen",     (1, 0),  "#1ee565" ),
	( "data/Scispace_tests.csv",  "Scispace",  (0, 1),  "#00bfb0" )
]

# Dimensions of plot
NROWS = 2
NCOLS = 2

# Number of bins in each histogram (range is predetermined as (0, 1))
BINS = 5

# Pseudo-random number generator seed (for reproducibility)
PRNG_SEED = 1

# Color for original abstract histogram
ORI_COLOUR = "#000022"
# Color for modified abstract histogram
MOD_COLOUR = "#1D75CD"


"""
Function:    retrieve_data
Description: Opens the experiment results csv and gives the
             is_writtten and detection probability.
Inputs:      Name of file which contains the aforementioned data.
Outputs:     List of tuples containing experiment results.
"""
def retrieve_data(filename):
	temp = []

	with open(filename, "r") as csv_file:
		reader = csv.reader(csv_file, delimiter=",")

		next(reader, None)  # skip column titles

		# Read results into list (temp)
		for row in reader:
			is_rewritten = row[3]
			detect_prob  = row[4]

			append_val = (is_rewritten, detect_prob)
			temp.append(append_val)
	return temp


"""
Function:    draw_hists
Description: Gets a list of tuples containing results from an experiment and
	     plots two histograms of the detector's responses. The two
	     histogram classes include one for original abstracts and another
	     for modified abstracts.
Inputs:      The filename containing the experiment data
	     List of tuples containing results for a detector, the target
	     axis for PyPlot and the filename of the test csv.
Outputs:     None
"""
def draw_hists(detector, target_axes):
	# Local variable definition
	filename      = detector[0]
	subplt_title  = detector[1]
	subplt_loc    = detector[2]
	subplt_x      = subplt_loc[0]
	subplt_y      = subplt_loc[1]
	subplt_colour = detector[3]

	# Load file
	exp_result = retrieve_data(filename)

	# Arrange data
	# Get all results for original abstracts (is_rewritten == 0)
	ori_abs = [ float(datum[1]) for datum in exp_result if (int(datum[0]) == 0) ]
	# Get all results for modified abstracts (is_rewritten == 1)
	mod_abs = [ float(datum[1]) for datum in exp_result if (int(datum[0]) == 1) ]

	# Plot histograms

	# Original abstracts histogram
	target_axes[subplt_x, subplt_y].hist(
		ori_abs,
		bins  = BINS,
		range = (0, 1),
		label = "Original Abstracts",
		color = ORI_COLOUR,
		alpha = 0.50
	)
	# Modified abstracts histogram
	target_axes[subplt_x, subplt_y].hist(
		mod_abs,
		bins  = BINS,
		range = (0, 1),
		label = "Modified Abstracts",
		color = MOD_COLOUR,
		alpha = 0.50
	)

	# Appearance configuration
	target_axes[subplt_x, subplt_y].grid(linestyle="--")
	target_axes[subplt_x, subplt_y].set_ylabel("Count")
	target_axes[subplt_x, subplt_y].set_xlabel("Probability Rating")
	target_axes[subplt_x, subplt_y].set_title(subplt_title)


# MAIN FUNCTION
def main():
	# Create PyPlot objects
	fig, main_axes = plt.subplots(nrows = NROWS, ncols = NCOLS)
	fig.suptitle(
		"Probability Ratings of GPT-4o mini Detectors \n(Original vs Modified)",
		x  = 0.05,
		y  = 0.97,
		ha = "left",
	)

	# Draw ROC for each detector
	for detector in DETECTORS:
		draw_hists(detector, main_axes)

	# Create legend
	handles, labels = plt.gca().get_legend_handles_labels()
	fig.legend(handles, labels, loc = "upper right", bbox_to_anchor = (1.0, 1.0))

	# Optimise spacing
	fig.tight_layout()

	# Render
	plt.savefig("hists.svg")
	plt.savefig("hists.png")
	plt.show()


if __name__ == "__main__":
    main()



