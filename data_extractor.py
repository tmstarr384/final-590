import re
from pathlib import Path
import numpy as np
import pandas as pd


def format_x_data(folder):
	print("Generating data...")

	seq_dict = {}

	# Get dictionary of sequences (key = PDB ID, value = list of sequences)
	pathlist = Path(folder).glob('**/*.fasta')
	for path in pathlist:
		f = open(path, "r")
		 
		contents = f.readlines()
		pdb_id = re.findall(r'>(.{4})_', contents[0])[0]
		sequence = contents[1].strip()
		if pdb_id in seq_dict:
			seq_dict[pdb_id].append(sequence)
		else:
			seq_dict[pdb_id] = [sequence]

		f.close()

	# Turns dictionary into numpy array
	numerized_seqs = np.zeros([len(seq_dict), 10, 1000])
	seqs = list(seq_dict.values())
	for i in range(len(seqs)):
		for j in range(10):
			for k in range(1000):
				if j < len(seqs[i]) and k < len(seqs[i][j]):
					numerized_seqs[i][j][k] = ord(seqs[i][j][k]) - ord('A')

	return numerized_seqs

def format_y_data(filename, categorize=False):
	df = pd.read_excel(filename, sheet_name='MyResult')
	affins = df['pKd pKi pIC50'].tolist()

	if not categorize:
		return affins

	aff_categorized = []
	for affin in affins:
	    if affin < 6:
	        category = 0 #"low"
	    elif affin < 8:
	        category = 1 #"med"
	    else:
	        category = 2 #"high"
	    aff_categorized.append(category)

	# print(aff_categorized.count("low"))
	# print(aff_categorized.count("med"))
	# print(aff_categorized.count("high"))

	return aff_categorized


# print(len(format_x_data("rcsb_pdb_protprot_seq\\rcsb_pdb_fasta_files_20200423161018")))