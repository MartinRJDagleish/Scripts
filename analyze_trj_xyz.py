#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#! IMPORTS
from typing import Optional
import numpy as np
import regex  # better than re module
from sys import argv, exit

#! CONSTANTS
MAX_GEOM = 2000
IS_XTB = False  # default value
IS_ORCA = False  # default value
IS_PLOT = False  # default value


def read_blocks_trj_xyz(
    _lines: [str], idx_geom: int
) -> [str]:  # TODO: geom_matr as return type
    """Reads a .trj.xyz file and returns the energies and geometries of a given file."""
    # _elem_list = []
    _geom_matr = np.zeros((NO_ATOMS, 3), dtype=np.float32)
    for line_idx, line in enumerate(_lines[1:]):
        if line_idx == 0:
            if IS_XTB:
                E_array[idx_geom] = read_energy_xtb(line)
            else:
                E_array[idx_geom] = read_energy_orca(line)
        else:
            line_split = line.strip().split()
            __geom_line = np.array([float(x) for x in line_split[1:]])
            # elem_sym_regex = (
            #     r"([A-Z][a-z]?)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)"
            # )
            # elem_sym_regex_pattern = regex.compile(elem_sym_regex)
            # match = elem_sym_regex_pattern.search(line)
            # if match:
                # _elem_list.append(match.group(1))
                # _geom_matr[line_idx - 1] = np.array(
                #     [
                #         float(match.group(2)),
                #         float(match.group(3)),
                #         float(match.group(4)),
                #     ]
                # )
    # return _elem_list, _geom_matr
    return _geom_matr

def read_energy_xtb(_line: str) -> Optional[float]:
    """Reads the energy from a .trj.xyz file generated by xtb."""
    xtb_E_pattern = r"energy:\s*(-?\d+\.\d+)"
    regex_pattern = regex.compile(xtb_E_pattern)
    match = regex_pattern.search(_line)
    if match:
        return float(match.group(1))
    return 0.0  # * ERROR case (not very good handling)

def read_energy_orca(_line: str) -> Optional[float]:
    """Reads the energy from a .trj.xyz file generated by ORCA."""
    orca_E_pattern = r"^\w+ \w+ [a-zA-Z-]+ [a-zA-Z0-9_\-*]+ E (-?\d+\.\d+)"
    regex_pattern = regex.compile(orca_E_pattern)
    match = regex_pattern.search(_line)
    if match:
        return float(match.group(1))
    return None


if __name__ == "__main__":
    #! FOR TESTING
    # file_path = "sources/Test.trj.xyz"
    # IS_XTB = True

    args = argv

    if len(args) == 1:
        exit("ERROR: No file path given")
    elif len(args) == 2:
        exit("ERROR: ADD XTB/ ORCA FLAG with -xtb or -orca")
    elif len(args) >= 3:
        file_path = args[1]
        for arg in args[2:]:
            if "-xtb" in arg:
                IS_XTB = True
                print("XTB FLAG DETECTED")
            elif "-orca" in arg:
                IS_ORCA = True
                print("ORCA FLAG DETECTED")
            elif "-print" in arg:
                IS_PLOT = True
                print("PRINT FLAG DETECTED")
                import matplotlib.pyplot as plt

    print("Reading file: " + file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if len(lines) > 0 and lines[0].strip().isdigit():
            NO_ATOMS = int(lines[0])
        else:
            from sys import exit

            print("INVALID FILE FORMAT: No_atoms not digit format (check first line)")
            exit(1)
    BLOCK_LEN = NO_ATOMS + 2

    geom_block_list = [
        lines[i : i + BLOCK_LEN] for i in range(0, len(lines), BLOCK_LEN)
    ]
    NO_GEOM = len(geom_block_list)
    E_array = np.zeros(NO_GEOM)

    geom_matr_list = []
    for idx_geom, block in enumerate(geom_block_list):
        geom_matr_list.append((idx_geom, read_blocks_trj_xyz(block, idx_geom)))

    print("Energies: ", E_array)
    print("You can plot these energies by adding the -plot flag")
    if IS_PLOT:
        print("Plotting Energies vs Geometries")
        X = np.arange(NO_GEOM)
        fig, ax = plt.subplots()
        ax.plot(X, E_array, "o")
        ax.set(xlabel="Geometry idx", ylabel="Energy / E_h", title="Energy vs Geometry")

        plt.show(block=True)


################################
# ORIGINAL CODE BY Nicolas N
################################
# This program is for analysis of trajectory files from Orca (structure optimizations, molecular dynamics, NEB files or relaxed surface scans)
# Programmed by N. Neuman, June 2022

# format long

# #fileName = 'CoVID4MC2MCcor_Py_2_H2O_10_MeCN_8_PBE_scan_eh_trj.xyz';
# ##fileName = 'iPrNH2_Ac2O_DMF_qmmm_scan_ac2_trj.xyz';
# ##fileName = 'PEG_458_H2O_DCM_B973c_opt_ba_trj.xyz';
# fileName = 'iPrNH2_Ac2O_DMF_qmmm_ZNEBTS_ad_MEP_ALL_trj.xyz';

# [Energies,Geometries,nAtoms,kGeom] = readTrajectoryXYZ(fileName);

# DistanceVector = zeros(kGeom,1);

# atom1 = 3;
# atom2 = 14;

# for k = 1:kGeom
#   Pos1 = Geometries{k,2}(atom1,:);
#   Pos2 = Geometries{k,2}(atom2,:);

#   DistanceVector(k) = norm(Pos2-Pos1);

# end

# figure;
# plot(DistanceVector,Energies,'sk','Linewidth',2);
# ylabel('Energy (Ha)');
# xlabel('Distance (A)');
# set(gca, "fontsize", 20);
