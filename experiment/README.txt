Pipeline of Python scripts is as follows:

1. Run gen_prompts.py and enter the generated prompts into GPT 4o-mini
	1.1. If GPT-modified abstracts are already in abstract_db.sqlite,
	     then skip step 1.

2. Run gen_tests_csv.py to generate test files
	2.1. Move the created files into the "data" folder (this
	     will overwrite existing data, if there are already
	     existing files in "data", then skip step 2 or copy
       only the files not filled in.)

3. Fill in the test.csv files in "data"

4. Run visualisation scripts
	4.1. roc_tests.py will generate an ROC-AUR plot for all services.
	4.2. hist_tests.py will produce histograms for each service's readings.
