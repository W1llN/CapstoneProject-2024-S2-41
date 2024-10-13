"""
File: gen_prompts.py
Date created: 12 Oct 2024
Author: William New (u3241279)

Description:
Outputs a file telling the experimenters what prompts
to enter into ChatGPT (GPT 4o-mini).
"""
import sqlite3
import csv


# GLOBAL VARIABLES(s)
DB_FILENAME = "abstract_db.sqlite"
PROMPTS_FILENAME = "prompts.txt"


"""
Function:    retrieve_data
Description: Opens the experiment database and gives the fields
             doi, pub_date, og_text
Inputs:      Name of file which contains the aforementioned data.
Outputs:     List of tuples containing table data (doi, pub_date,
             og_text)
"""
def retrieve_data(db_filename):
	# Open DB
	connection = sqlite3.connect(db_filename)
	cursor = connection.cursor()

	# Get data
	cursor.execute("SELECT doi, pub_date, og_text \
		        FROM abstracts")
	data = cursor.fetchall()

	# Close DB
	connection.close()

	return data


"""
Function:    modify_abstracts
Description: Appends prompts to a question of the
Inputs:      List of tuples containing data from the
             abstract_db table
Outputs:     List of abstracts (as in retrieve_data()),
             but modified to include prompt text
"""
# Modify data to have prompts included
def modify_abstracts(data):
	prompt_addition = ("Rewrite the following abstract, while "
			"retaining all information in the original:\n\n")

	outlist = []
	for article in data:
		doi = article[0]
		pub_date = article[1]
		og_text = article[2]

		prompt = prompt_addition + og_text
		outlist.append([doi, pub_date, prompt])

	return outlist


"""
Function:    write_prompts
Description: Creates and writes to file with prompts for ChatGPT (GPT 4o-mini)
Inputs:      List of prompts with extra information, name of
             file which contains the aforementioned data.
Outputs:     None
"""
def write_prompts(outlist, filename):
	with open(filename, "w+") as outfile:   # Write to TXT file
	for prompt in outlist:
		outfile.write(prompt[0] + ", " +
		              prompt[1] + "\n")  # doi, pub_date (for readability)

		outfile.write(prompt[2] + "\n")  # prompt to be copied to ChatGPT

		outfile.write("\n\n")            # extra spacing (for readability)
"""     # For csv writing instead of txt
	with open("prompts.csv", "w+") as outfile:   # Write to CSV file
	writer = csv.writer(outfile)

	for prompt in outlist:
		writer.writerow([prompt[0], prompt[1], prompt[2]])   """


# MAIN FUNCTION
def main():
	abstracts = retrieve_data(DB_FILENAME)
	prompts = modify_abstracts(abstracts)
	write_prompts(prompts, PROMPTS_FILENAME)


if __name__ == "__main__":
    main()
