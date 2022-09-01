#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.2.2

This is a wrapper script for the CENSO programme. 

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
# * 0.2.2 - Added postprocess lines for multiline strings and more readable code 
# * 0.2.1 - Fixed typo and added float checker. 
# * 0.2.0 - Added nucleus option, writes .censorc and requestes lamor frequency
# * 0.1.1 - Fixed namespace error
# * 0.1.0 - Initial release

VERSION = "0.2.2"

import os
import sys

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
    prog="run_censo.py",
    usage="%(prog)s input-file [options]",
    description=f"Run an CENSO calculation for a given input file. -> Script Version {VERSION}",
)
crest_parser.add_argument(
    "nucles",
    type=str,
    default="1H",
    nargs="+",
    help="Choose the NMR calculation to run. Possible: \
        1H, 13C, 31P, 28Si space separated for more than one \
            (default: %(default)s)",
)
crest_parser.add_argument(
    "--freq",
    type=str,
    default="300",
    help="Choose the lamor frequency for the appriopiate nucleus for the NMR \
        calculation to run. Reasonable: 300 (1H), 162 (31P), ... \
            (default: %(default)s)",
)
crest_parser.add_argument(
    "--input",  #! Positional argument
    metavar="CONFORMERS",
    type=str,
    default="crest_conformers.xyz",
    help="Conformers file to run the calculation on. (default: %(default)s)",
)
crest_parser.add_argument(
    "--func0",  #! Positional argument
    metavar="FUNC",
    type=str,
    default="b97-d3",
    help="Functional for prescreening. (default: %(default)s)",
)
crest_parser.add_argument(
    "--funcNMR",  #! Positional argument
    metavar="FUNC",
    type=str,
    default="tpss-d4",
    help="Functional for NMR calculation (J and S). (default: %(default)s)",
)
crest_parser.add_argument(
    "-B",  #! Positional argument
    "--basis",
    metavar="BASIS",
    type=str,
    default="pcsseg-3",
    help="Basis for NMR calculation (J and S) (default: %(default)s)",
)
crest_parser.add_argument(
    "-s",
    "--solvent",  #! Positional argument
    metavar="SOLVENT",
    type=str,
    help="The solvent to use in the calculation (default: ALPB).",
)
# crest_parser.add_argument(
#     "-T",
#     "--threads",  #! Optional argument
#     metavar="ncores",
#     type=int,
#     default=4,
#     help="Number of cores for parallel calculation. (default: %(default)s)",
# )

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
    "ether": [
        "ether",
        "ETHER",
        "Ether",
        "diethylether",
        "Diethylether",
    ],  # * different names for xtb and for CREST
    "ethylacetate": ["ethylacetate", "ETAC", "Ethylacetat", "Ethylacetate"],
    "furane": ["furane", "FUR", "Furan"],
    "h2o": [
        "water",
        "WAT",
        "Water",
        "Wasser",
        "H2O",
        "h2o",
    ],  #! This was wrong -> "h2o" not "water"
    "hexandecane": ["hexandecane", "HEX", "Hexandecane"],
    "hexane": ["hexane", "HEX", "Hexane", "Hexan"],
    "methanol": ["methanol", "METH", "Methanol"],
    "nitromethane": ["nitromethane", "NIT", "Nitromethane", "Nitromethan"],
    "octanol": ["octanol", "OCT", "Oct-OH"],
    "woctanol": ["woctanol", "WOCT", "Water octanol", "Wasser_Octanol"],
    "phenol": ["phenol", "PHEN", "Phenol"],
    "toluene": ["toluene", "TOL", "Toluene", "Toluol"],
    "thf": ["thf", "THF", "Tetrahydrofuran", "tetrahydrofurane"],
}


def get_solvent(solvent_user_inp):
    """
    Helper function for solvent from solvent_dict.
    """
    for solvent, solvent_names in solvent_dict.items():
        if solvent_user_inp in solvent_names:
            return solvent

def isfloat(num):
    """
    Helper function for checking if a string is a float.
    """
    try:
        float(num)
        return True
    except ValueError:
        return False

# * postprocess the multiline string
def postprocess_str(multl_str):
    lines = multl_str.split('\n')
    lines = [line.strip() for line in lines[:-1]]
    return lines 

#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()

    user_inp = args.input
    filename, ext = os.path.splitext(user_inp)
    namespace = filename.split(".")[0]  # * remove the .xtbopt or .xtb from the name
        
    # * Options for CENSO run
    options = []

    options.append("--input")
    options.append(args.input)  # * default or custom input file
    options.append("--func0")
    options.append(args.func0)  # * default or custom functional for prescreening
    options.append("--solvent")
    if args.solvent:
        try:
            SOLVENT = get_solvent(args.solvent)
            if SOLVENT:
                options.append(SOLVENT)
            else:
                raise ValueError("Solvent not found")
        except ValueError:
            print(
                f"The solvent '{args.solvent}' is not supported.\nPossible solvents are:\n\n \
                    {', '.join(solvent_dict.keys())}"
            )
            sys.exit(1)
    options.append("-smgsolv1")
    options.append("smd")
    options.append("-sm2")
    options.append("smd")
    options.append("--smgsolv2")
    options.append("smd")
    options.append("--prog")
    options.append("orca")
    # * NMR options
    options.append("--part4")
    options.append("on")
    options.append("--prog4J")
    options.append("orca")
    options.append("-funcJ")
    options.append(args.funcNMR)
    options.append("-funcS")
    options.append(args.funcNMR)
    options.append("-basisJ")
    options.append(args.basis)
    options.append("-basisS")
    options.append(args.basis)
    options.append("-cactive")
    options.append("off")

    # * mkdir tmp folder for CENSO run
    censo_path = os.path.join(cwd, "censo_tmp")
    if not os.path.isdir(censo_path):
        os.mkdir(censo_path)

    # * copy necassary files to tmp folder
    copy_filelst = [
        "crest_conformers.xyz",
        "coord",
        "anmr_nucinfo",
        "anmr_rotamer",
    ]
    for filename in copy_filelst:
        if os.path.isfile(os.path.join(cwd, filename)):
            subprocess.run(
                ["mv", filename, censo_path], stdout=subprocess.PIPE, check=True
            )
        else:
            print(f"File {filename} not found! This may cause errors for CENSO!")
            raise FileNotFoundError(
                f"File {filename} not found! This may cause errors for CENSO!"
            )

    os.chdir(censo_path)
    
    for nuc in args.nucles:
        if "1H" in nuc:
            h_nmr_bool = "on"
        else: 
            h_nmr_bool = "off"
            
        if "13C" in nuc:
            c_nmr_bool = "on"
        else: 
            c_nmr_bool = "off"
            
        if "19F" in nuc:
            f_nmr_bool = "on"
        else: 
            f_nmr_bool = "off"
            
        if "29Si" in nuc:
            si_nmr_bool = "on"
        else: 
            si_nmr_bool = "off"
            
        if "31P" in nuc:
            p_nmr_bool = "on"
        else: 
            p_nmr_bool = "off"     
            
    freq = args.freq
    if not isfloat(freq):
        print("Please enter a number for the frequency.")
        sys.exit(1)
               

    # * Writing the .censorc file for CENSO calculation
    with open(f".censorc", "w", encoding="utf-8") as f:        
        default_censorc = f"""
        $CENSO global configuration file: .censorc
        $VERSION:1.2.0 

        ORCA: /loctmp/dam63759/orca
        ORCA version: 5.0.3
        GFN-xTB: /loctmp/dam63759/xtb-6.5.1/bin/xtb
        CREST: /loctmp/dam63759/crest/crest
        mpshift: /path/including/binary/mpshift-binary
        escf: /path/including/binary/escf-binary

        #COSMO-RS
        ctd = BP_TZVP_C30_1601.ctd cdir = "/software/cluster/COSMOthermX16/COSMOtherm/CTDATA-FILES" ldir = "/software/cluster/COSMOthermX16/COSMOtherm/CTDATA-FILES"
        $ENDPROGRAMS

        $CRE SORTING SETTINGS:
        $GENERAL SETTINGS:
        nconf: all                       # ['all', 'number e.g. 10 up to all conformers'] 
        charge: 0                        # ['number e.g. 0'] 
        unpaired: 0                      # ['number e.g. 0'] 
        solvent: benzene                 # ['gas', 'acetone', 'acetonitrile', 'aniline', 'benzaldehyde', 'benzene', 'ccl4', '...'] 
        prog_rrho: xtb                   # ['xtb'] 
        temperature: 298.15              # ['temperature in K e.g. 298.15'] 
        trange: [273.15, 378.15, 5]      # ['temperature range [start, end, step]'] 
        multitemp: on                    # ['on', 'off'] 
        evaluate_rrho: on                # ['on', 'off'] 
        consider_sym: on                 # ['on', 'off'] 
        bhess: on                        # ['on', 'off'] 
        imagthr: automatic               # ['automatic or e.g., -100    # in cm-1'] 
        sthr: automatic                  # ['automatic or e.g., 50     # in cm-1'] 
        scale: automatic                 # ['automatic or e.g., 1.0 '] 
        rmsdbias: off                    # ['on', 'off'] 
        sm_rrho: alpb                    # ['alpb', 'gbsa'] 
        progress: off                    # ['on', 'off'] 
        check: on                        # ['on', 'off'] 
        prog: orca                       # ['tm', 'orca'] 
        func: r2scan-3c                  # ['b3-lyp', 'b3lyp', 'b3lyp-3c', 'b3lyp-d3', 'b3lyp-d3(0)', 'b3lyp-d4', 'b3lyp-nl', '...'] 
        basis: automatic                 # ['automatic', 'def2-TZVP', 'def2-mSVP', 'def2-mSVP', 'def2-mSVP', 'def2-mSVP', '...'] 
        maxthreads: 2                    # ['number of threads e.g. 2'] 
        omp: 4                           # ['number cores per thread e.g. 4'] 
        balance: off                     # ['on', 'off'] 
        cosmorsparam: automatic          # ['automatic', '12-fine', '12-normal', '13-fine', '13-normal', '14-fine', '...'] 

        $PART0 - CHEAP-PRESCREENING - SETTINGS:
        part0: on                        # ['on', 'off'] 
        func0: b97-d3                    # ['b3-lyp', 'b3lyp', 'b3lyp-3c', 'b3lyp-d3', 'b3lyp-d3(0)', 'b3lyp-d4', '...'] 
        basis0: def2-SV(P)               # ['automatic', 'def2-SV(P)', 'def2-TZVP', 'def2-mSVP', 'def2-mSVP', 'def2-mSVP', '...'] 
        part0_gfnv: gfn2                 # ['gfn1', 'gfn2', 'gfnff'] 
        part0_threshold: 4.0             # ['number e.g. 4.0'] 

        $PART1 - PRESCREENING - SETTINGS:
        # func and basis is set under GENERAL SETTINGS
        part1: on                        # ['on', 'off'] 
        smgsolv1: smd                    # ['alpb_gsolv', 'cosmo', 'cosmors', 'cosmors-fine', 'cpcm', 'dcosmors', '...'] 
        part1_gfnv: gfn2                 # ['gfn1', 'gfn2', 'gfnff'] 
        part1_threshold: 3.5             # ['number e.g. 5.0'] 

        $PART2 - OPTIMIZATION - SETTINGS:
        # func and basis is set under GENERAL SETTINGS
        part2: on                        # ['on', 'off'] 
        prog2opt: prog                   # ['tm', 'orca', 'prog', 'automatic'] 
        part2_threshold: 2.5             # ['number e.g. 4.0'] 
        sm2: smd                         # ['cosmo', 'cpcm', 'dcosmors', 'default', 'smd'] 
        smgsolv2: smd                    # ['alpb_gsolv', 'cosmo', 'cosmors', 'cosmors-fine', 'cpcm', 'dcosmors', '...'] 
        part2_gfnv: gfn2                 # ['gfn1', 'gfn2', 'gfnff'] 
        ancopt: on                       # ['on'] 
        hlow: 0.01                       # ['lowest force constant in ANC generation, e.g. 0.01'] 
        opt_spearman: on                 # ['on', 'off'] 
        part2_P_threshold: 99            # ['Boltzmann sum threshold in %. e.g. 95 (between 1 and 100)'] 
        optlevel2: automatic             # ['crude', 'sloppy', 'loose', 'lax', 'normal', 'tight', 'vtight', 'extreme', '...'] 
        optcycles: 8                     # ['number e.g. 5 or 10'] 
        spearmanthr: -4.0                # ['value between -1 and 1, if outside set automatically'] 
        radsize: 10                      # ['number e.g. 8 or 10'] 
        crestcheck: off                  # ['on', 'off'] 

        $PART3 - REFINEMENT - SETTINGS:
        part3: off                       # ['on', 'off'] 
        prog3: prog                      # ['tm', 'orca', 'prog'] 
        func3: pw6b95                    # ['b3-lyp', 'b3lyp', 'b3lyp-3c', 'b3lyp-d3', 'b3lyp-d3(0)', 'b3lyp-d4', 'b3lyp-nl', '...'] 
        basis3: def2-TZVPD               # ['DZ', 'QZV', 'QZVP', 'QZVPP', 'SV(P)', 'SVP', 'TZVP', 'TZVPP', 'aug-cc-pV5Z', '...'] 
        smgsolv3: smd                    # ['alpb_gsolv', 'cosmo', 'cosmors', 'cosmors-fine', 'cpcm', 'dcosmors', '...'] 
        part3_gfnv: gfn2                 # ['gfn1', 'gfn2', 'gfnff'] 
        part3_threshold: 99              # ['Boltzmann sum threshold in %. e.g. 95 (between 1 and 100)'] 

        $NMR PROPERTY SETTINGS:
        $PART4 SETTINGS:
        part4: on                     # ['on', 'off'] 
        couplings: on                    # ['on', 'off'] 
        progJ: orca                      # ['tm', 'orca', 'prog'] 
        funcJ: pbe0                      # ['b3-lyp', 'b3lyp', 'b3lyp-3c', 'b3lyp-d3', 'b3lyp-d3(0)', 'b3lyp-d4', 'b3lyp-nl', '...'] 
        basisJ: def2-TZVP                # ['DZ', 'QZV', 'QZVP', 'QZVPP', 'SV(P)', 'SVP', 'TZVP', 'TZVPP', 'aug-cc-pV5Z', '...'] 
        sm4J: smd                        # ['cosmo', 'cpcm', 'dcosmors', 'smd'] 
        shieldings: on                   # ['on', 'off'] 
        progS: prog                      # ['tm', 'orca', 'prog'] 
        funcS: pbe0                      # ['b3-lyp', 'b3lyp', 'b3lyp-3c', 'b3lyp-d3', 'b3lyp-d3(0)', 'b3lyp-d4', 'b3lyp-nl', '...'] 
        basisS: def2-TZVP                # ['DZ', 'QZV', 'QZVP', 'QZVPP', 'SV(P)', 'SVP', 'TZVP', 'TZVPP', 'aug-cc-pV5Z', '...'] 
        sm4S: smd                        # ['cosmo', 'cpcm', 'dcosmors', 'smd'] 
        reference_1H: TMS                # ['TMS'] 
        reference_13C: TMS               # ['TMS'] 
        reference_19F: CFCl3             # ['CFCl3'] 
        reference_29Si: TMS              # ['TMS'] 
        reference_31P: TMP               # ['TMP', 'PH3'] 
        1H_active: {h_nmr_bool}                   # ['on', 'off'] 
        13C_active: {c_nmr_bool}                   # ['on', 'off'] 
        19F_active: {f_nmr_bool}                  # ['on', 'off'] 
        29Si_active: {si_nmr_bool}                 # ['on', 'off'] 
        31P_active: {p_nmr_bool}                   # ['on', 'off'] 
        resonance_frequency: {freq}       # ['MHz number of your experimental spectrometer setup'] 

        $OPTICAL ROTATION PROPERTY SETTINGS:
        $PART5 SETTINGS:
        optical_rotation: off            # ['on', 'off'] 
        funcOR: pbe                      # ['functional for opt_rot e.g. pbe'] 
        funcOR_SCF: r2scan-3c            # ['functional for SCF in opt_rot e.g. r2scan-3c'] 
        basisOR: def2-SVPD               # ['basis set for opt_rot e.g. def2-SVPD'] 
        frequency_optical_rot: [589.0]   # ['list of freq in nm to evaluate opt rot at e.g. [589, 700]'] 
        $END CENSORC
        """

        f.writelines(postprocess_str(default_censorc))

    # *---------------------------------#
    # * Run the calculation
    with open(f"{namespace}_censo.out", "w", encoding="utf-8") as out:
        subprocess.run(["censo", *options], stdout=out, check=True)
    # *---------------------------------#

    print("\n" + 40 * "-")
    print("*" + "CENSO RUN FINISHED!".center(38, " ") + "*")
    print(40 * "-")

    print("\n" + 40 * "-")
    print("*" + "YOU MAY START THE ANMR RUN NOW!".center(38, " ") + "*")
    print(40 * "-")
