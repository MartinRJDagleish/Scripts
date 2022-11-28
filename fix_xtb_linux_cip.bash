#!/bin/bash

echo 'ulimit -s unlimited' >> ~/.bashrc
echo 'export OMP_STACKSIZE=4G # 4 GB per OMP thread' >> ~/.bashrc
echo 'export OMP_NUM_THREADS=6,1 # <ncores,1>' >> ~/.bashrc
echo 'export OMP_MAX_ACTIVE_LEVELS=1' >> ~/.bashrc
echo 'export MKL_NUM_THREADS=6' >> ~/.bashrc

source ~/.bashrc

