#!/bin/bash
#SBATCH --job-name=my_name
#SBATCH --output=my_name.o%j
#SBATCH --error=my_name.e%j
#SBATCH --partition=cupn
#SBATCH --ntasks=
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --distribution=cyclic
SLURM_TMPDIR=/scratch/slurm.$SLURM_JOB_ID
mkdir $SLURM_TMPDIR
ulimit -s unlimited
export OMP_STACKSIZE=40G
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_STACKSIZE=1000m
export PATH=/sw/xtb/xtb-6.6.0/bin:$PATH
export PATH=/sw/xtb:$PATH
export LD_LIBRARY_PATH=/sw/openmpi411/lib:$LD_LIBRARY_PATH
export PATH=/usr/local/bin:$PATH
export PATH=/sw/openmpi411/bin:$PATH
export PATH=/sw/orca_5_0_4:$PATH
export NBOEXE=/sw/nbo6/bin/nbo6.i4.exe
export GENEXE=/sw/nbo6/bin/gennbo.i4.exe
cp crest_conformers.xyz $SLURM_TMPDIR/
cp coord $SLURM_TMPDIR/
cp anmr_nucinfo $SLURM_TMPDIR/
cp anmr_rotamer $SLURM_TMPDIR/
cp .censorc $SLURM_TMPDIR/
cd $SLURM_TMPDIR
/sw/xtb/censo --input crest_conformers.xyz --func0 b97-d3 --solvent chcl3 --smgsolv1 smd -sm2 smd --smgsolv2 smd --prog orca --part4 on --prog4J orca -funcJ tpss-d4 -funcS tpss-d4 -basisJ pcsseg-2 -basisS pcsseg-2 -cactive off > /mnt/d/Scripts/dbg_scenso/V2/my_name.out
mv * /mnt/d/Scripts/dbg_scenso/V2/
rm -rf $SLURM_TMPDIR
