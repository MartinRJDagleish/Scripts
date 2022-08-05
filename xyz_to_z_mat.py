import re

import numpy as np

space_str = "    "
empty_str = ""

with open("water.xyz", "r", encoding="utf-8") as f:
    lines = f.readlines()
    num_atoms = int(lines[0])
    atom_labels = [
        re.findall(r"[A-Z][a-z]?", line)[0] for line in lines[2 : 2 + num_atoms]
    ]
    atom_coords = np.array(
        [
            [float(x) for x in re.findall(r"[-+]?\d*\.\d+", line)]
            for line in lines[2:]
        ]
    )

    z_mat = []
    for i in range(num_atoms):
        if i == 0:
            z_mat.append([atom_labels[i], 3*(space_str,empty_str,empty_str)])
        elif i == 1:
            z_mat.append(
                [
                    atom_labels[i],
                    space_str,
                    str(i) + " ",
                    np.linalg.norm(atom_coords[i] - atom_coords[0])
                ]
            )
        elif i == 2:
            z_mat.append(
                [
                    atom_labels[i],
                    space_str,
                    str(i) + " ",
                    np.linalg.norm(atom_coords[i] - atom_coords[0]),
                    space_str,
                    str(i) + " ",
                    np.arccos(
                        np.dot(
                            atom_coords[i] - atom_coords[0],
                            atom_coords[i] - atom_coords[1],
                        )
                        / (
                            np.linalg.norm(atom_coords[i] - atom_coords[0])
                            * np.linalg.norm(atom_coords[i] - atom_coords[1])
                        )
                    )
                    * 180
                    / np.pi,
                ]
            )
        else:
            z_mat.append(
                [
                    atom_labels[i],
                    space_str,
                    str(i+1) + " ",
                    np.linalg.norm(atom_coords[i] - atom_coords[0]),
                    space_str,
                    str(i) + " ",
                    np.arccos(
                        np.dot(
                            atom_coords[i] - atom_coords[0],
                            atom_coords[i] - atom_coords[1],
                        )
                        / (
                            np.linalg.norm(atom_coords[i] - atom_coords[0])
                            * np.linalg.norm(atom_coords[i] - atom_coords[1])
                        )
                    )
                    * 180
                    / np.pi,
                    space_str,
                    str(i-1) + " ",
                    np.arccos(
                        np.dot(
                            atom_coords[i] - atom_coords[0],
                            atom_coords[i] - atom_coords[2],
                        )
                        / (
                            np.linalg.norm(atom_coords[i] - atom_coords[0])
                            * np.linalg.norm(atom_coords[i] - atom_coords[2])
                        )
                    )
                    * 180
                    / np.pi,
                ]
            )


# Write a script that converts the xyz file input to a z-matrix file output.
# For example, if you run your script with the input file water.xyz, it should
# create a file called water.zmat with the following contents:
#
# O
# H 1 0.969
# H 2 0.969 1 104.52
#
# The first line of the z-matrix should be the atom label of the first atom
# in the xyz file. The second line should be the atom label of the second atom
# in the xyz file, followed by the index of the first atom (1), and the
# distance between the two atoms.
#
# The third line should be the atom label of the third atom in the xyz file,
# followed by the index of the first atom (1), the distance between the two
# atoms, the index of the second atom (2), and the angle between the three atoms.
#
# The fourth line should be the atom label of the fourth atom in the xyz file,
# followed by the index of the first atom (1), the distance between the two
# atoms, the index of the second atom (2), the angle between the three atoms,
# the index of the third atom (3), and the dihedral angle between the four atoms.
#
# You can assume that the xyz file will always have at least 3 atoms.
#
# Hint: You can use the numpy.linalg.norm function to calculate the distance
#       between two points. For example:

    #   import numpy as np
    #   a = np.array([1, 0, 0])
    #   b = np.array([0, 1, 0])
    #   distance = np.linalg.norm(a - b)
#
# Hint: You can use the numpy.dot function to calculate the dot product of
#       two vectors. For example:
#
#       import numpy as np
#       a = np.array([1, 0, 0])
#       b = np.array([0, 1, 0])
#       dot_product = np.dot(a, b)
#
# Hint: You can use the numpy.arccos function to calculate the angle between
#       two vectors. For example:
#
#       import numpy as np
#       a = np.array([1, 0, 0])
#       b = np.array([0, 1, 0])
#       angle = np.ar
#       angle = np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
#       angle = angle * 180 / np.pi





        # elif i == 2:
        #     z_mat.append(
        #         [
        #             atom_labels[i],
        #             space_str,
        #             str(i+1) + " ",
        #             np.linalg.norm(atom_coords[i] - atom_coords[0]),
        #             0,
        #             np.linalg.norm(atom_coords[i] - atom_coords[0]),
        #         ]
        #     )
        # else:
        #     z_mat.append(
        #         [
        #             atom_coords_dict[i],
        #             2,
        #             1,
        #             np.linalg.norm(atom_coords[i] - atom_coords[1]),
        #         ]
        #     )

    for line in z_mat:
        print(*line)

    #         [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", line)],
    #     ]
    #     for idx, line in enumerate(lines[2:])
    # ]

    # atom_coords = np.array(
    #     [atom_coords_dict[idx][1] for idx in range(num_atoms)]
    # )
