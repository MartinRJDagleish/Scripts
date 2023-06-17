#!/bin/bash
# -*- coding: utf-8 -*-
VERSION="0.2.2"

LICENSE=$(
  cat <<LICENSE
Author: Martin Dagleish (MRJD)

Version $VERSION

This is a wrapper script for the CENSO programme (focused on NMR calc.).

MIT License

Copyright (c) 2023 Martin Dagleish

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

LICENSE
)

# * Changelog
# * 0.2.2 - Added nO and nP with checks for queue
# * 0.2.1 - Forgot 'ulimit -s unlimited' for xTB
# * 0.2.0 - Complete rewrite to use multiple bugs -> CLI args parsing should now work
# * 0.1.0 - Initial release

#scratchdir=\$TMPDIR
olddir=$(pwd)
# ncpus=1 # <- default below not here! -> needed for nO and nP
nnodes=1
# ntaskspercore=1 #does not work with hyperthreading if simply set to 2.
queue="cupn"
orcadir="/sw/orca_5_0_4"
xtbdir="/sw/xtb/xtb-6.6.0/bin"
grimmedir="/sw/xtb" # CREST, CENSO, ANMR
nodes=""

# possible queues (Stand: 16.06.2023)
# all: 10 Nodes, 16 CPUs per Node, 80GB Hauptspeicher, 200GB Scratch
# Nodes cupnb1-8 cupnc1-2, Betriebssystem Ubuntu 18.04 (bionic)
# cupt: 7 Nodes, 24 CPUs per Node, 128GB Hauptspeicher, 1TB Scratch
# Nodes cupnode2-8, Betriebssystem Ubuntu 18.04 (bionic)
# cupn: 14 Nodes, 16 CPUs per Node, 80GB Hauptspeicher, 1TB Scratch
# Nodes cupn1-13 cupn15, Ubuntu 20.04 (focal)
# p2022: 4 Nodes, 16 CPUs per Node, 95GB Hauptspeicher, 1TB Scratch
# Nodes n2201-4, Ubuntu 20.04 (focal)
# cipn: 4 Nodes, 32 CPUs per Node (HT), 124GB Hauptspeicher, 200GB Scratch
# Nodes cipn1-4, Ubuntu 18.04 (bionic)
# cipc: 24 Nodes, 8 CPUs per Node, 32GB Hauptspeicher, 1TB Scratch
# Nodes cipnode1-24, Ubuntu 18.04 (bionic)

# -> derived from list above
# readonly Q_ALL_CPUS=16
# readonly Q_CUPT_CPUS=24
# readonly Q_CUPN_CPUS=16
# readonly Q_P2022_CPUS=16
# readonly Q_CIPN_CPUS=32
# readonly Q_CIPC_CPUS=8
#
# readonly Q_ALL_RAM=80
# readonly Q_CUPT_RAM=128
# readonly Q_CUPN_RAM=80
# readonly Q_P2022_RAM=95
# readonly Q_CIPN_RAM=124
# readonly Q_CIPC_RAM=32

declare -Ar Q_CPUS_DICT=(
  ["Q_ALL_CPUS"]=16
  ["Q_CUPT_CPUS"]=24
  ["Q_CUPN_CPUS"]=16
  ["Q_P2022_CPUS"]=16
  ["Q_CIPN_CPUS"]=32
  ["Q_CIPC_CPUS"]=8
)

declare -Ar Q_RAM_DICT=(
  ["Q_ALL_RAM"]=80
  ["Q_CUPT_CPUS"]=128
  ["Q_CUPN_CPUS"]=80
  ["Q_P2022_RAM"]=95
  ["Q_CIPN_RAM"]=124
  ["Q_CIPC_RAM"]=32
)

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
  echo "   -np <ncpus>   	   Specify the number of processes [default: 1. Max number depends on node]"
  echo "   -nO <OMP Threads> ONLY USE WHEN YOU KNOW WHAT YOU DO: Specify the number of OMP threads [default:(calc. from -np)]"
  echo "   -nP <MAX THREADS> nCores = nO * nP; ONLY USE WHEN YOU KNOW WHAT YOU DO: Specify the number of threads for CENSO [default:(calc. from -np)]"
  echo "   -q <partition>	   Specify the partition for the job. [default: all]"
  echo "   -w <node>       	 Specify the node for the job."
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
for file in "${CENSO_nec_files[@]}"; do
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
while [[ $# -gt 0 ]]; do
  case "$1" in
  -h)

    echo
    echo "Send an CENSO NMR job to the queuing system"
    echo
    echo "Usage: $0 <name>"
    echo
    echo "   <name>   	Name of calculation (without .inp)"
    echo
    echo "Slurm Options:"
    echo "   -np <ncpus>   	   Specify the number of processes [default: 1. Max number depends on node]"
    echo "   -nO <OMP Threads> ONLY USE WHEN YOU KNOW WHAT YOU DO: Specify the number of OMP threads [default:(calc. from -np)]"
    echo "   -nP <MAX THREADS> nCores = nO * nP; ONLY USE WHEN YOU KNOW WHAT YOU DO: Specify the number of threads for CENSO [default:(calc. from -np)]"
    echo "   -q <partition>	   Specify the partition for the job. [default: all]"
    echo "   -w <node>       	 Specify the node for the job."
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
  -nO)
    if [[ -n $2 ]]; then
      nOMP="$2"
      shift 2
    fi
    ;;
  -nP)
    if [[ -n $2 ]]; then
      nCENSO_THREADS="$2"
      shift 2
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
      IFS=',' read -r -a nuclei_arr <<<"$2"

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

# Check for cores / threads / OMP ...
echo "ncpus: $ncpus"
echo "nOMP: $nOMP"
echo "nCENSO_THREADS: $nCENSO_THREADS"

# Test for valid input combinations
if [[ -z $ncpus && -z $nOMP && -z $nCENSO_THREADS ]]; then
  echo "No cores / threads / OMP set! Going to use 1 core / thread / OMP"
  echo "Going to continue..."
  nOMP=1
  nCENSO_THREADS=1
elif [[ -n $ncpus && -n $nOMP && -n $nCENSO_THREADS ]]; then
  # elif [[ -n $ncpus && (-n $nOMP || -n $nCENSO_THREADS) ]]; then
  echo "ATTENTION! You set both ncpus and OMP / CENSO THREADS! Going to ignore 'ncpus' and using OMP + CENSO threads!"
  echo "Going to continue..."
  unset ncpus
  # ↓ not needed; covered by the case below this one already ↓
  # elif [[ (-n $ncpus && -z $nOMP && -n $nCENSO_THREADS) || (-n $ncpus && -n $nOMP && -z $nCENSO_THREADS) ]]; then
  #   echo "test INVALID INPUT! Pls use both: -nO AND -nP for calculation; or just use -np!"
  #   echo "Going to exit..."
  # exit 1
elif [[ (-n $nOMP && -z $nCENSO_THREADS) || (-z $nOMP && -n $nCENSO_THREADS) ]]; then
  echo "INVALID INPUT! Pls use both: -nO AND -nP for calculation; or just use -np!"
  echo "Going to exit..."
  exit 1
fi

# now only valid inputs of ncpus, nOMP and nCENSO_THREADS are left
if [[ -n $ncpus && $ncpus -gt 1 ]]; then
  nCENSO_THREADS=$(expr $ncpus / 4)
  nOMP=$(expr $ncpus % 4)
  if [ $((ncpus % 4)) -eq 0 ]; then
    nOMP=1
  else
    nOMP=$((ncpus % 4))
  fi
else
  unset ncpus
  nCENSO_THREADS=1
  nOMP=1
fi

# ! NEW
# WRITE A .censorc file with the given options
mod_censorc=$(
  cat <<-EOF
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

#------------------------------------------------------------------------------------------------
# add shebang
echo -e "#!/bin/bash" >$name.qs

# set SLURM options
echo "#SBATCH --job-name=$name" >>$name.qs
echo "#SBATCH --output=$name.o%j" >>$name.qs
echo "#SBATCH --error=$name.e%j" >>$name.qs
if [ -z $nodes ]; then
  echo "#SBATCH --partition=$queue" >>$name.qs
else
  echo "#SBATCH --nodelist=$nodes" >>$name.qs
  echo "#SBATCH --partition=$queue" >>$name.qs
fi
echo "#SBATCH --ntasks=$ncpus" >>$name.qs
echo "#SBATCH --nodes=$nnodes" >>$name.qs
echo "#SBATCH --cpus-per-task=1" >>$name.qs
#echo "#SBATCH --ntasks-per-core=$ntaskspercore" >> $name.qs
#echo "#SBATCH --tasks-per-node=$ncpus" >> $qsfile
#echo '#SBATCH --time=1000:00:00' >> $qsfile
echo "#SBATCH --distribution=cyclic" >>$name.qs

# create working directory in scratch
echo 'SLURM_TMPDIR=/scratch/slurm.$SLURM_JOB_ID' >>$name.qs
echo 'mkdir $SLURM_TMPDIR' >>$name.qs

# set environment
# xtb settings
echo -e 'ulimit -s unlimited' >>$name.qs
echo -e 'export OMP_STACKSIZE=40G' >>$name.qs
echo -e 'export OMP_NUM_THREADS=1' >>$name.qs
echo -e 'export MKL_NUM_THREADS=1' >>$name.qs
echo -e 'export OMP_STACKSIZE=1000m' >>$name.qs
echo -e 'export PATH='"$xtbdir"':$PATH' >>$name.qs
echo -e 'export PATH='"$grimmedir"':$PATH' >>$name.qs

# OpenMPI + ORCA settings
echo -e 'export LD_LIBRARY_PATH=/sw/openmpi411/lib:$LD_LIBRARY_PATH' >>$name.qs
echo -e 'export PATH=/usr/local/bin:$PATH' >>$name.qs
echo -e 'export PATH=/sw/openmpi411/bin:$PATH' >>$name.qs
echo -e 'export PATH='"$orcadir"':$PATH' >>$name.qs
echo -e 'export NBOEXE=/sw/nbo6/bin/nbo6.i4.exe' >>$name.qs
echo -e 'export GENEXE=/sw/nbo6/bin/gennbo.i4.exe' >>$name.qs

#! COPY the necessary files to the scratch directory
for file in "${CENSO_nec_files[@]}"; do
  echo -e 'cp '"$file"' $SLURM_TMPDIR/' >>$name.qs
done
#! write the new .censorc file
echo "$mod_censorc" >.censorc
echo "Modified .censorc written to $PWD/.censorc"
echo -e 'cp .censorc $SLURM_TMPDIR/' >>$name.qs

# IF restart is given -> calculations already done
# Version 1 with rsync?

# Version 2 with cp

# ! ------------------------------------------------------
# ! create CENSO CLI call with all given options
# ! ------------------------------------------------------

censo_call="${grimmedir}/censo --input crest_conformers.xyz --func0 ${func0} \
--solvent ${solvent} --smgsolv1 smd -sm2 smd --smgsolv2 smd --prog orca --part4 on \
--prog4J orca -funcJ ${funcNMR} -funcS ${funcNMR} -basisJ ${basis_set} -basisS ${basis_set} \
-cactive off > ${olddir}/${name}.out"

#* copy relevant ORCA files to scratch
# echo -e "OLDDIR=$olddir" >> $name.qs
# echo -e "inp=$name.inp" >> $name.qs
# echo -e 'cp $inp $SLURM_TMPDIR/$inp' >> $name.qs
# echo -e 'cp $OLDDIR/'"$name.gbw"' $SLURM_TMPDIR/ 2> /dev/null' >> $name.qs

# copying all files which are mentioned in a '%moinp "moinp_file.anything"'-line by reading them into an array
# moinp_files=($(grep 'moinp' $name.inp | awk '{gsub("\"", ""); print $2}' | tr -d '\r'))
# for (( file=0; file<${#moinp_files[@]}; file++ ))
# do
#     echo -e 'cp $OLDDIR/'"${moinp_files[$file]}"' $SLURM_TMPDIR/' >> $name.qs
# done

# go to scratch, do the job, copy back files, clean up
echo -e 'cd $SLURM_TMPDIR' >>$name.qs
echo -e "$censo_call" >>$name.qs
echo -e "mv * $olddir/" >>$name.qs
echo -e 'rm -rf $SLURM_TMPDIR' >>$name.qs

# execute $name.qs job file via SLURM
# OLD: sbatch -o $name.o%j -e $name.e%j "$@" $name.qs
# sbatch -o $name.o%j -e $name.e%j $name.qs
