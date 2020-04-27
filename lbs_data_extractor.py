from pathlib import Path
import numpy as np


def get_data_dict(folder):
	data_dict = {}

	# Get dictionary of sequences (key = PDB ID, value = list of sequences)
	pathlist = Path(folder).glob('**/*.pisite')
	for path in pathlist:
		f = open(path, 'r')
		contents = f.readlines()

		pdb_id = contents[1][8:].strip().lower() + ":" + contents[2][8:].strip()
		seq = ""
		binding_partners = {}
		i = 0
		 
		for line in contents:
			if line[0] == ' ':

				cols = line.strip().split()
				seq = seq + cols[2]

				for bind_part in cols[4:]:
					part_id = bind_part[2:8]
					if part_id in binding_partners:
						binding_partners[part_id].append(i)
					else:
						binding_partners[part_id] = [i]
				i += 1

		data_dict[pdb_id] = (numerize_sequence(seq), binding_partners)

		f.close()

	return data_dict


def numerize_sequence(seq):
	return [ord(aa) - ord('A') for aa in seq]


def get_data(folder):
	x_data = []
	y_data = []

	data_dict = get_data_dict(folder)
	SEQ = 0
	BPS = 1

	y_data = {'act_' + str(i): [] for i in range(2000)}

	for pdb_id in data_dict:
		for bp in data_dict[pdb_id][BPS]:
			if bp in data_dict and pdb_id in data_dict[bp][BPS]:
				seq_a = data_dict[pdb_id][SEQ]
				seq_b = data_dict[bp][SEQ]
				seq_a.extend([0] * (1000 - len(seq_a)))
				seq_b.extend([0] * (1000 - len(seq_b)))
				x_data.append([seq_a, seq_b])

				# lbs = [np.zeros([1]) for _ in range(2000)] #(len(seq_a) + len(seq_b))
				for i in range(2000):
					if i in data_dict[pdb_id][BPS][bp] or i - len(seq_a) in data_dict[bp][BPS][pdb_id]:
						y_data['act_' + str(i)].append(1)
					else:
						y_data['act_' + str(i)].append(0)

				# for i in data_dict[pdb_id][BPS][bp]:
				# 	lbs[i] = 1
				# for i in data_dict[bp][BPS][pdb_id]:
				# 	lbs[len(seq_a) + i][0] = 1
				# y_data.append(lbs)

	y_data = {y: np.array(y_data[y]) for y in y_data}

	return x_data, y_data

# get_data('pisite.flat.all\\all')