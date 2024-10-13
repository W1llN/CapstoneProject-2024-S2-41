"""
File: gen_tests.py
Date created: 13 Oct 2024
Author: William New (u3241279)

Description:
Outputs a file telling the experimenters which
abstracts to enter into a detection service,
alongside whether it was rewritten or original.
"""
import sqlite3
import random


# GLOBAL VARIABLE(s)
NUM_TESTS = 25
DB_FILE = "abstract_db.sqlite"
OUT_FILE = "test_abstracts.txt"


"""
Function:    test_indices
Description: Return a list of random tuples sampling
             a range without placement
Inputs:      Size of input list, and number of samples
Outputs:     A 2-tuple where first element is the random index,
             second element is randomly "OR" (original)
             or "RE" (rewritten).
Example:     test_indices(10, 4) == [(4,"RE"), (7,"OR"), (0,"OR"), (9,"RE")]
"""
def test_indices(in_size, num_s, seed = 1):
	random.seed(seed)  # for reproducibility / testing
	indices = random.sample(range(in_size), num_s)

	out_list = []
	for index in indices:
		rand = random.randint(0, 1)
		if (rand == 1):
			out_str = "OR" # Original
		else:
			out_str = "RE" # Rewritten

		out_tuple = (index, out_str)
		out_list.append(out_tuple)

	return out_list


"""
Function: retrieve_data
Description: Opens the experiment database and gives the fields
             doi, pub_date, og_text, rep_text
Inputs:      Name of file which contains the aforementioned data.
Outputs:     List of tuples containing table data (doi, pub_date,
             og_text, rep_text)
"""
def retrieve_data(db_filename):
	# Open DB
	connection = sqlite3.connect(db_filename)
	cursor = connection.cursor()

	# Get data
	cursor.execute("SELECT doi, pub_date, og_text, rep_text \
		        FROM abstracts")
	data = cursor.fetchall()

	# Close DB
	connection.close()

	return data


"""
Function:    gen_submissions
Description: Creates and writes to a file with the abstracts
             alongside the article doi and whether it was modified.
Inputs:      Abstracts data structure to be filtered and outputted,
             name of file which contains the aforementioned data.
Outputs:     None
"""
def gen_tests(abstracts_data, index_list, out_filename):
	with open("tests.txt", "w+") as outfile:   # Write to TXT file
		for index_tuple in index_list:
			# Get tuple which chooses article
			i = index_tuple[0]
			rewritten = index_tuple[1]

			# Get chosen article's data
			article  = abstracts_data[i]
			doi      = article[0]
			pub_date = article[1]
			og_text  = article[2]
			rep_text = article[3]

			# Write data to file
			outfile.write( doi + ", " + pub_date + ",\n" )
			if rewritten == "OR":
				outfile.write( "ORIGINAL ABSTRACT\n\n" + og_text )
			elif rewritten == "RE":
				outfile.write( "REWRITTEN ABSTRACT\n\n" + rep_text )
			else:
				outfile.write("error: could not write abstract")
			outfile.write("\n\n\n\n\n")

	return


# MAIN FUNCTION
def main():
	abstracts = retrieve_data(DB_FILE)
	indices = test_indices(len(abstracts), NUM_TESTS)
	gen_tests(abstracts, indices, OUT_FILE)


if __name__ == "__main__":
    main()

