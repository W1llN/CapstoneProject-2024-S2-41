"""
File: roc_test.py
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
# List of tuples, with the form (filename, line_label)
DETECTORS = [("test_gptzero.csv", "GPTZero (n=10)")]


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
Function:    draw_ROC
Description: Gets a list of tuples containing results from an experiment and
	     plots the ROC_AUR curve associated with it (uses SciKit Learn)
Inputs:      The filename containing the experiment data
List of tuples containing results for a detector, the target axis for PyPlot and the filename of the
Outputs:     None
"""
def draw_ROC(filename, target_ax, line_label):
	# Load file
	exp_result = retrieve_data(filename)

	# Arrange data
	is_rewritten_list = [ int(datapoint[0]) for datapoint in exp_result ]
	probability_list  = [ float(datapoint[1]) for datapoint in exp_result ]

	# Compute and plot ROC
	display = metrics.RocCurveDisplay.from_predictions(y_true = is_rewritten_list,
							   y_pred = probability_list,
							   ax=target_ax, name=line_label)


# MAIN FUNCTION
def main():
	# Create PyPlot objects
	fig, main_ax = plt.subplots()
	main_ax.set_title("Receiver Operating Characteristic (ROC) curves")
	main_ax.grid(linestyle="--")

	# Draw ROC for each detector
	for detector in DETECTORS:
		draw_ROC(detector[0], main_ax, detector[1])

	# Render
	plt.show()


if __name__ == "__main__":
    main()

