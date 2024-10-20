"""
File: tpr_fpr_tests.py
Date created: 14 Oct 2024
Author: William New (u3241279)

Description:
Outputs false positive rate and true positive rate curves 
for LLM detector tests (parametrised by decision threshold). 
Data are a random sample of original and rewritten abstracts 
are from GPT 4o-mini (generated with gen_tests_csv.py).
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics


# GLOBAL VARIABLE(s)
# List of tuples, with the form (filename, plot_label, subplot_loc, colour);
# subplot_loc is of the form (x, y), where (0, 0) is top left corner.
DETECTORS = [
	( "data/GPTZero_tests.csv",   "GPTZero",   (0, 0) ),
	( "data/Writefull_tests.csv", "Writefull", (1, 1) ),
	( "data/Isgen_tests.csv",     "Isgen",     (1, 0) ),
	( "data/Scispace_tests.csv",  "Scispace",  (0, 1) )
]

# Dimensions of plot
NROWS = 2
NCOLS = 2

# Color for curves
TPR_COLOUR = "#1d75fd"
FPR_COLOUR = "#ff2222"

# Plotting x-axis resolution
POINT_RES = 1000

LINE_ALPHA = 0.85  # for all lines


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
			is_rewritten = int(row[3])
			detect_prob  = float(row[4])

			append_val = (is_rewritten, detect_prob)
			temp.append(append_val)
	return temp

"""
Function:    get_fpr
Description: Gets a list of tuples containing results from an experiment and
	     outputs false positive rate as a function of decision threshold.
Inputs:      The filename containing the experiment data, and the target
	     axis for PyPlot.
Outputs:     None
"""
def get_fpr(data, thresh):
	# Create counts for false, true, negative, positive
	tp_count = 0   # true positive
	fp_count = 0   # false positive

	tn_count = 0   # true negative
	fn_count = 0   # false negative

	# Count up data for a given threshold
	for datum in data:
		is_rewritten = datum[0]
		probability_rating = datum[1]

		if probability_rating > thresh:   # positive reading
			if is_rewritten == 1:    # true positive
				tp_count += 1
			elif is_rewritten == 0:  # false positive
				fp_count += 1

		elif probability_rating <= thresh:   # negative reading
			if is_rewritten == 0:    # true negative
				tn_count += 1
			elif is_rewritten == 1:  # false negative
				fn_count += 1

	# Calculate false positive rate (fpr)
	try:
		fpr = (fp_count) / (fp_count + tn_count)
		return fpr
	except ZeroDivisionError:
		return None


"""
Function:    get_tpr
Description: Gets a list of tuples containing results from an experiment and
	     outputs true positive rate as a function of decision threshold.
Inputs:      The filename containing the experiment data, and the target
	     axis for PyPlot.
Outputs:     None
"""
def get_tpr(data, thresh):
	# Create counts for false, true, negative, positive
	tp_count = 0   # true positive
	fp_count = 0   # false positive

	tn_count = 0   # true negative
	fn_count = 0   # false negative

	# Count up data for a given threshold
	for datum in data:
		is_rewritten = datum[0]
		probability_rating = datum[1]

		if probability_rating > thresh:   # positive reading
			if is_rewritten == 1:    # true positive
				tp_count += 1
			elif is_rewritten == 0:  # false positive
				fp_count += 1

		elif probability_rating <= thresh:   # negative reading
			if is_rewritten == 0:    # true negative
				tn_count += 1
			elif is_rewritten == 1:  # false negative
				fn_count += 1

	# Calculate true positive rate (fpr)
	try:
		tpr = (tp_count) / (tp_count + fn_count)
		return tpr
	except ZeroDivisionError:
		return None


"""
Function:    draw_fpr_curve
Description: Gets a test csv containing results from an experiment and
	     plots false positive rate as a function of (variable) decision threshold.
Inputs:      The filename containing the experiment data, and the target
	     axis for PyPlot.
Outputs:     None
"""
def draw_fpr_curve(detector, target_axes):
	# Local variable definition
	filename      = detector[0]
	subplt_title  = detector[1]
	subplt_loc    = detector[2]
	subplt_x      = subplt_loc[0]
	subplt_y      = subplt_loc[1]

	# Load file
	exp_result = retrieve_data(filename)

	# Create data
	thresh_arr = np.linspace(0, 1, POINT_RES)
	# map get_fpr onto array
	fpr_arr = [ get_fpr(exp_result, thr) for thr in thresh_arr ]

	# Plot data
	target_axes[subplt_x, subplt_y].plot(thresh_arr,
				             fpr_arr,
				             label = "False Positive Rate",
				             color = FPR_COLOUR,
				             alpha = LINE_ALPHA)

	# Appearance configuration
	target_axes[subplt_x, subplt_y].grid(linestyle="--")
	target_axes[subplt_x, subplt_y].set_ylabel("Rate")
	target_axes[subplt_x, subplt_y].set_xlabel("Threshold")
	target_axes[subplt_x, subplt_y].set_title(subplt_title)


"""
Function:    draw_tpr_curve
Description: Gets a test csv containing results from an experiment and
	     plots true positive rate as a function of (variable) decision threshold.
Inputs:      The filename containing the experiment data, and the target
	     axis for PyPlot.
Outputs:     None
"""
def draw_tpr_curve(detector, target_axes):
	# Local variable definition
	filename      = detector[0]
	subplt_title  = detector[1]
	subplt_loc    = detector[2]
	subplt_x      = subplt_loc[0]
	subplt_y      = subplt_loc[1]

	# Load file
	exp_result = retrieve_data(filename)

	# Create data
	thresh_arr = np.linspace(0, 1, POINT_RES)
	# map get_fpr onto array
	tpr_arr = [ get_tpr(exp_result, thr) for thr in thresh_arr ]

	# Plot data
	target_axes[subplt_x, subplt_y].plot(thresh_arr,
				             tpr_arr,
				             label = "True Positive Rate",
				             color = TPR_COLOUR,
				             alpha = LINE_ALPHA)

	# Appearance configuration
	target_axes[subplt_x, subplt_y].grid(linestyle="--")
	target_axes[subplt_x, subplt_y].set_ylabel("Rate")
	target_axes[subplt_x, subplt_y].set_xlabel("Threshold")
	target_axes[subplt_x, subplt_y].set_title(subplt_title)




# MAIN FUNCTION
def main():
	# Create PyPlot objects
	fig, main_axes = plt.subplots(nrows = NROWS, ncols = NCOLS)
	fig.suptitle(
		"True Positive Rate and False Positive Rate\nof GPT 4o-mini Detectors",
		x  = 0.05,
		y  = 0.97,
		ha = "left",
	)

	# Draw ROC for each detector
	for detector in DETECTORS:
		draw_tpr_curve(detector, main_axes)
		draw_fpr_curve(detector, main_axes)

	# Create legend
	handles, labels = plt.gca().get_legend_handles_labels()
	fig.legend(handles, labels, loc = "upper right", bbox_to_anchor = (0.97, 1.0))

	# Optimise spacing
	fig.tight_layout()

	# Render
	plt.savefig("tpr_fpr.svg")
	plt.savefig("tpr_fpr.png")
	plt.show()


if __name__ == "__main__":
    main()

