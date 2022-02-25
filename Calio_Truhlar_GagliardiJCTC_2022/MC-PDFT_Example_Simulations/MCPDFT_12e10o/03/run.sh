#!/bin/bash
#SBATCH --partition=caslake
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=6
#SBATCH --job-name=SHARC
#SBATCH --time=36:00:00
#SBATCH --account=pi-lgagliardi

module load python
module load intel
module load mkl
module load gcc
module load cmake
module load hdf5/1.12.0+intelmpi-2019.up7+intel-19.1.1

conda activate local

export WRKDIR=$PWD
cd $WRKDIR

export SHARC=/home/pcalio/Apps/sharc-modified/bin

export MOLCAS_PRINT=3
export MOLCAS=/home/pcalio/Apps/OpenMolcas/builds/gnu_dev_mkl

$SHARC/sharc.x input

err=$?

exit $err
