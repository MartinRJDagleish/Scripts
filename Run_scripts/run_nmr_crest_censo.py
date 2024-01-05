#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.2.1

This is a wrapper script for the combination of CREST / CENSO and ANMR programme.

MIT License

Copyright (c) 2022 Martin Dagleish

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# * Changelog
# * 0.2.1 - Minor fixees with naming
# * 0.2.0 - First final release with all parts
# * 0.1.0 - Initial release

import os
import sys

VERSION = "0.2.1"

try:
    import argparse
except ImportError:
    print("Please install argparse. Via pip install argparse")
    sys.exit(1)
try:
    import subprocess
except ImportError:
    print("Please install subprocess. Via pip install subprocess")
    sys.exit(1)


# * OS running this script
OPERATING_SYTEM = sys.platform

# * Create the parser
crest_parser = argparse.ArgumentParser(
    prog="run_nmr_crest_censo.py",
    usage="%(prog)s input-file [options]",
    description=f"Run an CREST calculation for a given input file. -> Script Version {VERSION}",
)

crest_parser.add_argument(
    "xyz_file",  #! Positional argument
    metavar="XYZ-FILE",
    type=str,
    help="The xyz-file to run the calculation on.",
)
crest_parser.add_argument(
    "-s",
    "--solvent",  #! Positional argument
    metavar="SOLVENT",
    type=str,
    help="The solvent to use in the calculation (default: ALPB).",
)
crest_parser.add_argument(
    "-T",
    "--threads",  #! Optional argument
    metavar="ncores",
    type=int,
    default=4,
    help="Number of cores for parallel calculation. (default: %(default)s)",
)
crest_parser.add_argument(
    "-nmr",
    action="store_true",
    help="Helper option for running NMR.",
)

# * Execute the parse_args() method
args = crest_parser.parse_args()


solvent_dict = {
    "acetone": ["acetone", "Aceton", "(CH3)2CO"],
    "acetonitrile": ["acetonitrile", "ACN", "Acetonitrile", "Acetonitril", "AcN"],
    "aniline": ["aniline", "ANI", "Aniline", "Anil"],
    "benzaldehyde": ["benzaldehyde", "BEN", "Benzaldehyde", "Benzal", "Benzaldehyd"],
    "benzene": ["benzene", "Benzene", "Benzol"],
    "ch2cl2": ["ch2cl2", "CH2CL2", "DCM", "Dichloromethane", "Dichlormethan"],
    "chcl3": ["chcl3", "CHCL3", "Chloroform", "Chloroforme", "chloroform"],
    "cs2": ["cs2", "CS2", "Carbonsulfide", "Carbonsulfid", "carbonsulfide"],
    "dioxane": ["dioxane", "Dioxane", "Dioxal"],
    "dmf": ["dmf", "DMF", "Dimethylformamide", "Dimethylformamid", "dimethylformamide"],
    "dmso": ["dmso", "DMSO", "Me2SO"],
    "ether": ["ether", "ETHER", "Ether", "diethylether", "Diethylether"], # * different names for xtb and for CREST 
    "ethylacetate": ["ethylacetate", "ETAC", "Ethylacetat", "Ethylacetate"],
    "furane": ["furane", "FUR", "Furan"],
    "h2o": ["water", "WAT", "Water", "Wasser", "H2O", "h2o"], #! This was wrong -> "h2o" not "water" 
    "hexandecane": ["hexandecane", "HEX", "Hexandecane"],
    "hexane": ["hexane", "HEX", "Hexane", "Hexan"],
    "methanol": ["methanol", "METH", "Methanol"],
    "nitromethane": ["nitromethane", "NIT", "Nitromethane", "Nitromethan"],
    "octanol": ["octanol", "OCT", "Oct-OH"],
    "woctanol": ["woctanol", "WOCT", "Water octanol", "Wasser_Octanol"],
    "phenol": ["phenol", "PHEN", "Phenol"],
    "toluene": ["toluene", "TOL", "Toluene", "Toluol"],
    "thf": ["thf", "THF", "Tetrahydrofuran", "tetrahydrofurane"]
}


def get_solvent(solvent_user_inp):
    """
    Helper function for solvent from solvent_dict.
    """
    for solvent, solvent_names in solvent_dict.items():
        if solvent_user_inp in solvent_names:
            return solvent


#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()

    xyz_file = args.xyz_file

    filename, ext = os.path.splitext(xyz_file)
    namespace = filename.split(".")[0]  #* remove the .xtbopt or .xtb from the name

    # 1. Run CREST
    crest_options = []

    # * Standard GFN2
    crest_options.append("--gfn2")
    crest_options.append("--nmr")

    if args.solvent:
        try:
            SOLVENT = get_solvent(args.solvent)
            if SOLVENT:
                crest_options.append(f"--alpb {SOLVENT}")
            else:
                raise ValueError("Solvent not found")
        except ValueError:
            print(
                f"The solvent '{args.solvent}' is not supported.\nPossible solvents are:\n\n \
                    {', '.join(solvent_dict.keys())}"
            )
            sys.exit(1)

    if args.threads > 1:
        crest_options.append("-T " + str(args.threads))

    # * mkdir temp1 folder for xtb files
    temp1_path = os.path.join(cwd, "temp1")
    if not os.path.isdir(temp1_path):
        os.mkdir(temp1_path)

    # * copy .xyz file to temp1 folder
    subprocess.run(["cp", xyz_file, temp1_path], stdout=subprocess.PIPE, check=True)

    os.chdir(temp1_path)

    # *---------------------------------#
    # * Run the CREST Calculation
    if not args.nmr:
        censo_dirname = f"{namespace}_censo"
        with open(f"{namespace}_crest.out", "w", encoding="utf-8") as out:
            subprocess.run(
                ["crest", f"{filename}.xyz", *crest_options], stdout=out, check=True
            )

        print("\n" + 40 * "-")
        print("*" + "CREST RUN FINISHED!".center(38, " ") + "*")
        print(40 * "-")

        # * Run CENSO
        print("Starting the CENSO calculation...")
        print("")

        if os.path.exists(censo_dirname):
            os.rmdir(censo_dirname)

        os.mkdir(censo_dirname)

        subprocess.run(
            [
                "cp",
                "crest_conformers.xyz",
                "coord",
                "anmr_nucinfo",
                "anmr_rotamer",
                f"{namespace}_censo",
            ],
            check=True,
        )

        os.chdir(censo_dirname)

        # * actual CENSO call
        with open(f"{namespace}_censo.out", "w", encoding="utf-8") as out:
            subprocess.run(
                [
                    "censo",
                    "--input",
                    "crest_conformers.xyz",
                    "-func0",
                    "b97-d3",
                    "--solvent",
                    SOLVENT,
                    "-smgsolv1",
                    "smd",
                    "-sm2",
                    "smd",
                    "--smgsolv2",
                    "smd",
                    "--prog",
                    "orca",
                    # NMR options
                    "-part4",
                    "on",
                    "-prog4J",
                    "orca",
                    "-funcJ",
                    "tpss-d4",
                    "-funcS",
                    "tpss-d4",
                    "-basisJ",
                    "pcsseg-3",
                    "-basisS",
                    "pcsseg-3",
                    # has to be changed in .censorc file
                    # "-31P_active",
                    # "on",
                    # "-resonance_frequency",
                    # "162",
                    "-cactive",
                    "off",
                ],
                check=True,
                stdout=out,
            )
        print("\n" + 40 * "-")
        print("*" + "CREST RUN FINISHED!".center(38, " ") + "*")
        print(40 * "-")

        # * Run ANMR
        print("Starting the ANMR calculation...")
        print("")
        with open(f"{namespace}_anmr.out", "w", encoding="utf-8") as out:
            subprocess.run(
                [
                    "anmr",
                    "--orca",
                    "--plain",
                    # plain: coupling constants are read from the CONFXX/NMR/nmrprop.dat written by CENSO
                    # instead of the output files of the used QM program package,
                    # whose formatting often changes with new versions
                    "-mf",  # mf: use the frequenz in MHz
                    "162",
                    "-mss",  # max spinsystem size
                    "12",
                ],
                check=True,
                stdout=out,
            )
        import numpy as np

        data = np.genfromtxt("anmr.dat")
        THRESHOLD = 0.001
        data2 = data[np.logical_not(data[:, 1] < THRESHOLD)]
        data2 = np.insert(data2, 0, (data[0][0], THRESHOLD), axis=0)
        data2 = np.insert(data2, len(data2), (data[-1][0], THRESHOLD), axis=0)
        np.savetxt("newanmr.dat", data2, fmt="%2.5e")

        print("\n" + 40 * "-")
        print("*" + "ANMR RUN FINISHED!".center(38, " ") + "*")
        print(40 * "-")

        # * Run ANMR
        print("Starting the NMRplot plotting...")
        print("")

        subprocess.run(
            ["nmrplot.py", "-i", "newanmr.dat", "-o", namespace + "_nmrplot"],
            check=True,
        )
        print("\n" + 40 * "-")
        print("*" + "PLOTTING DONE!".center(38, " ") + "*")
        print(40 * "-")

    elif args.nmr:
        print("Starting the ANMR calculation...")
        print("")
        # * ANMR run
        with open(f"{namespace}_anmr.out", "w", encoding="utf-8") as out:
            subprocess.run(
                [
                    "anmr",
                    "--orca",
                    "--plain",
                    # plain: coupling constants are read from the CONFXX/NMR/nmrprop.dat written by CENSO
                    # instead of the output files of the used QM program package,
                    # whose formatting often changes with new versions
                    "-mf",  # mf: use the frequenz in MHz
                    "400",
                    "-mss",  # max spinsystem size
                    "12",
                ],
                check=True,
                stdout=out,
            )
        import numpy as np

        data = np.genfromtxt("anmr.dat")
        THRESHOLD = 0.001
        data2 = data[np.logical_not(data[:, 1] < THRESHOLD)]
        data2 = np.insert(data2, 0, (data[0][0], THRESHOLD), axis=0)
        data2 = np.insert(data2, len(data2), (data[-1][0], THRESHOLD), axis=0)
        np.savetxt("newanmr.dat", data2, fmt="%2.5e")
        
        print("\n" + 40 * "-")
        print("*" + "ANMR RUN FINISHED!".center(38, " ") + "*")
        print(40 * "-")

        # * Run ANMR
        print("Starting the NMRplot plotting...")
        print("")

        subprocess.run(
            ["nmrplot.py", "-i", "newanmr.dat", "-o", namespace + "_nmrplot"],
            check=True,
        )
        print("\n" + 40 * "-")
        print("*" + "PLOTTING DONE!".center(38, " ") + "*")
        print(40 * "-")

    # os.chdir("..")
    # subprocess.run(
    #     ["cp", f"{temp1_path}/{namespace}.out", cwd],
    #     stdout=subprocess.PIPE,
    #     check=True,
    # )

    # print(40 * "-")
    # print("*" + "Output copied to CWD".center(38, " ") + "*")
    # print(40 * "-")
