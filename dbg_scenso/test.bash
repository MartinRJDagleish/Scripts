#!/bin/bash 
# -*- coding: utf-8 -*-
#scratchdir=\$TMPDIR
olddir=$(pwd)
ncpus=1
nnodes=1
# ntaskspercore=1 #does not work with hyperthreading if simply set to 2.
queue="cupn"
orcadir="/sw/orca_5_0_4"
xtbdir="/sw/xtb/xtb-6.6.0/bin"
grimmedir="/sw/xtb" # CREST, CENSO, ANMR
nodes=""


# check if input file is given and/or existing
if [ -z "$1" ]; then
    echo
    echo "Send an CENSO NMR job to the queuing system"
    echo
    echo "Usage: $0 <name>"
    echo
    echo "   <name>   	Name of calculation (without .inp)"
    echo
    echo "Slurm Options:"
    echo "   -np <ncpus>   	Specify the number of processes [default: 1. Max number depends on node]"
    echo "   -q <partition>	Specify the partition for the job. [default: all]"
    echo "   -w <node>       	Specify the node for the job."
    echo
    echo "CENSO NMR Options:"
    echo "   --nuc <nuclei>          Chose the nuclei for which the NMR shielding constants should be calculated. (Comma sep.) [default: 1H, possible: 1H, 13C, 19F, 29Si, 31P]"
    echo "   --freq <frequency>	     Change the lamor frequency for the NMR shielding constants calculation. (Format: 300.0) [default: 300 MHz (1H), resonable: 300 (1H), 162 (31P), ...]"
    echo "   --func0 <functional>    Change the functional for the Part0: Cheap prescreening of conformers. [default: B97-D3]"
    echo "   --funcNMR <functional>  Change the functional for the Part4: NMR property (shielding and shift). [default: TPSS-D4]"
    echo "   --B <basis set>         Basis set for the NMR calculation (shielding and shift). [default: pcsseg-2, also possible: pcsseg-3, pcseg-1, ...]"
    echo "   --S <solvent>           Solvent for the NMR calculation (shielding and shift). [default: chcl3, also possible: acetonitrile, benzene, ...]"
    echo
    exit 0
fi


# get file name as variable
# name=`echo "$1" | sed "s/\.inp//" | sed "s/.\///"`
name="$(echo "$1")"
shift 
#! IF THE ABOVE DOES NOT WORK: name = `echo "$1"`

CENSO_nec_files=("crest_conformers.xyz" "coord" "anmr_nucinfo" "anmr_rotamer")
for file in "${CENSO_nec_files[@]}";
do
    if [ ! -f "$file" ]; then
        echo
        echo "$file not found. Pls provide a valid input"
        echo
        echo "The following files are needed for a CENSO NMR calculation:"
        echo "  crest_conformers.xyz"
        echo "  coord"
        echo "  anmr_nucinfo"
        echo "  anmr_rotamer"
        echo
        exit 1
    fi
done


#! NEW
# opts=true
# while [[ $# -gt 0 && $opts == true ]]; do
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h)
      echo
      echo "Send a CENSO NMR job to the queuing system"
      echo
      echo "Usage: $0 <name>"
      echo
      echo "   <name>   	Name of calculation (without .inp)"
      echo
      echo "Slurm Options:"
      echo "   -np <ncpus>   	Specify the number of processes [default: 1. Max number depends on node]"
      echo "   -q <partition>	Specify the partition for the job. [default: all]"
      echo "   -w <node>       	Specify the node for the job."
      echo
      echo "CENSO NMR Options:"
      echo "   --nuc <nuclei>          Choose the nuclei for which the NMR shielding constants should be calculated. (Comma separated, NO SPACE) [default: 1H, possible: 1H, 13C, 19F, 29Si, 31P]"
      echo "   --freq <frequency>      Change the Larmor frequency for the NMR shielding constants calculation. (Format: 300.0) [default: 300 MHz (1H), reasonable: 300 (1H), 162 (31P), ...]"
      echo "   --func0 <functional>    Change the functional for Part0: Cheap prescreening of conformers. [default: B97-D3]"
      echo "   --funcNMR <functional>  Change the functional for Part4: NMR property (shielding and shift). [default: TPSS-D4]"
      echo "   --B <basis set>         Basis set for the NMR calculation (shielding and shift). [default: pcsseg-2, also possible: pcsseg-3, pcseg-1, ...]"
      echo "   --S <solvent>           Solvent for the NMR calculation (shielding and shift). [default: chcl3, also possible: acetonitrile, benzene, ...]"
      echo
      exit 0
      ;;
    -np)
      if [[ -n $2 ]]; then
        ncpus="$2"
        shift 2
      else
        echo "Error: $1 requires an argument"
        exit 1
      fi
      ;;
    -q)
      if [[ -n $2 ]]; then
        partition="$2"
        shift 2
      else
        echo "Error: $1 requires an argument"
        exit 1
      fi
      ;;
    -w)
      if [[ -n $2 ]]; then
        node="$2"
        shift 2
      else
        echo "Error: $1 requires an argument"
        exit 1
      fi
      ;;
    --nuc)
        if [[ $2 == *,* ]]; then
            IFS=',' read -r -a nuclei_arr <<< "$2"

            for element in "${nuclei_arr[@]}"; do
                nuclei+=("$element")
            done
                shift 2
        else
            nuclei=("$2")
            shift 2
        fi
        echo "rest $@"
        ;;
    --freq)
      if [[ -n $2 ]]; then
        freq="$2"
        shift 2
      else
        echo "Error: $1 requires an argument"
        exit 1
      fi
      ;;
    --func0)
      if [[ -n $2 ]]; then
        func0="$2"
        shift 2
      else
        echo "Error: $1 requires an argument"
        exit 1
      fi
      ;;
    --funcNMR)
      if [[ -n $2 ]]; then
        funcNMR="$2"
        shift 2
      else
        echo "Error: $1 requires an argument"
        exit 1
      fi
      ;;
    --B)
      if [[ -n $2 ]]; then
        basis_set="$2"
        shift 2
      else
        echo "Error: $1 requires an argument"
        exit 1
      fi
      ;;
    --S)
      echo "$@"
      if [[ -n $2 ]]; then
        solvent="$2"
        shift 2
      else
        echo "Error: $1 requires an argument"
        exit 1
      fi
      ;;
    *)
        # opts=false
        break
      ;;
  esac
done

#! DEFAULT VALUES IF NOT SET
nuclei="${nuclei:=1H}"
freq="${freq:=300.0}"
func0="${func0:=b97-d3}"
funcNMR="${funcNMR:=tpss-d4}"
basis_set="${basis_set:=pcsseg-2}"
solvent="${solvent:=chcl3}"

# ECHO THE SET VALUES
echo "Name: $name"
echo "Nuclei: ${nuclei[@]}"
echo "Frequency: $freq"
echo "Functional Part0: $func0"
echo "Functional Part4: $funcNMR"
echo "Basis set: $basis_set"
echo "Solvent: $solvent"


# ! NEW
declare -A nuc_bool_dict=(
    ["1H"]="off"
    ["13C"]="off"
    ["19F"]="off"
    ["29Si"]="off"
    ["31P"]="off"
)

for nuc in ${nuclei[@]}; do
    if [[ ${nuc_bool_dict[$nuc]+_ } ]]; then
        nuc_bool_dict[$nuc]="on"
    else
        echo "Invalid nucleus: $nuc"
    fi
done

# Print settings
echo "Nuclei settings:"
for key in "${!nuc_bool_dict[@]}"; do
    echo "  $key: ${nuc_bool_dict[$key]}"
done

# ! NEW
# check the freq for being a numerical value with a dot
if [[ "$freq" =~ [0-9]+(\.[0-9]+)?$ ]]; then
    echo "Choosen frequency value: $freq"
else
    echo "Invalid frequency value: $freq, pls enter as a numerical value with a dot, e.g. 300.0"
fi

# ! NEW
# WRITE A .censorc file with the given options
mod_censorc=$(cat <<-EOF
\$CENSO global configuration file: .censorc
\$VERSION:1.2.0

ORCA: $orcadir
ORCA version: 5.0.4
GFN-xTB: $xtbdir/xtb
CREST: $grimmedir/crest
mpshift: /path/including/binary/mpshift-binary
escf: /path/including/binary/escf-binary

#COSMO-RS
ctd = BP_TZVP_C30_1601.ctd cdir = "/software/cluster/COSMOthermX16/COSMOtherm/CTDATA-FILES" ldir = "/software/cluster/COSMOthermX16/COSMOtherm/CTDATA-FILES"
\$ENDPROGRAMS

\$CRE SORTING SETTINGS:
\$GENERAL SETTINGS:
nconf: all                       # ['all', 'number e.g. 10 up to all conformers']
charge: 0                        # ['number e.g. 0']
unpaired: 0                      # ['number e.g. 0']
solvent: $solvent                # ['gas', 'acetone', 'acetonitrile', 'aniline', 'benzaldehyde', 'benzene', 'ccl4', '...']
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
maxthreads: 1                    # ['number of threads e.g. 2']
omp: $ncpus                      # ['number cores per thread e.g. 4']
balance: off                     # ['on', 'off']
cosmorsparam: automatic          # ['automatic', '12-fine', '12-normal', '13-fine', '13-normal', '14-fine', '...']

\$PART0 - CHEAP-PRESCREENING - SETTINGS:
part0: on                        # ['on', 'off']
func0: b97-d3                    # ['b3-lyp', 'b3lyp', 'b3lyp-3c', 'b3lyp-d3', 'b3lyp-d3(0)', 'b3lyp-d4', '...']
basis0: def2-SV(P)               # ['automatic', 'def2-SV(P)', 'def2-TZVP', 'def2-mSVP', 'def2-mSVP', 'def2-mSVP', '...']
part0_gfnv: gfn2                 # ['gfn1', 'gfn2', 'gfnff']
part0_threshold: 4.0             # ['number e.g. 4.0']

\$PART1 - PRESCREENING - SETTINGS:
# func and basis is set under GENERAL SETTINGS
part1: on                        # ['on', 'off']
smgsolv1: smd                    # ['alpb_gsolv', 'cosmo', 'cosmors', 'cosmors-fine', 'cpcm', 'dcosmors', '...']
part1_gfnv: gfn2                 # ['gfn1', 'gfn2', 'gfnff']
part1_threshold: 3.5             # ['number e.g. 5.0']

\$PART2 - OPTIMIZATION - SETTINGS:
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

\$PART3 - REFINEMENT - SETTINGS:
part3: off                       # ['on', 'off']
prog3: prog                      # ['tm', 'orca', 'prog']
func3: pw6b95                    # ['b3-lyp', 'b3lyp', 'b3lyp-3c', 'b3lyp-d3', 'b3lyp-d3(0)', 'b3lyp-d4', 'b3lyp-nl', '...']
basis3: def2-TZVPD               # ['DZ', 'QZV', 'QZVP', 'QZVPP', 'SV(P)', 'SVP', 'TZVP', 'TZVPP', 'aug-cc-pV5Z', '...']
smgsolv3: smd                    # ['alpb_gsolv', 'cosmo', 'cosmors', 'cosmors-fine', 'cpcm', 'dcosmors', '...']
part3_gfnv: gfn2                 # ['gfn1', 'gfn2', 'gfnff']
part3_threshold: 99              # ['Boltzmann sum threshold in %. e.g. 95 (between 1 and 100)']

\$NMR PROPERTY SETTINGS:
\$PART4 SETTINGS:
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
1H_active: ${nuc_bool_dict["1H"]} # ['on', 'off']
13C_active: ${nuc_bool_dict["13C"]} # ['on', 'off']
19F_active: ${nuc_bool_dict["19F"]} # ['on', 'off']
29Si_active: ${nuc_bool_dict["29Si"]} # ['on', 'off']
31P_active: ${nuc_bool_dict["31P"]} # ['on', 'off']
resonance_frequency: $freq       # ['MHz number of your experimental spectrometer setup']

\$OPTICAL ROTATION PROPERTY SETTINGS:
\$PART5 SETTINGS:
optical_rotation: off            # ['on', 'off']
funcOR: pbe                      # ['functional for opt_rot e.g. pbe']
funcOR_SCF: r2scan-3c            # ['functional for SCF in opt_rot e.g. r2scan-3c']
basisOR: def2-SVPD               # ['basis set for opt_rot e.g. def2-SVPD']
frequency_optical_rot: [589.0]   # ['list of freq in nm to evaluate opt rot at e.g. [589, 700]']
\$END CENSORC
EOF
)

