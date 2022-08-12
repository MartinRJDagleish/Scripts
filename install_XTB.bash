#!/bin/bash

wget https://github.com/grimme-lab/xtb/releases/download/v6.5.1/xtb-6.5.1-linux-x86_64.tar.xz -q --show-progress
wait
tar -xvf xtb-6.5.1-linux-x86_64.tar.xz 
wait 
cd xtb-6.5.1 
cd bin 
echo ""
echo "------------------"
echo "   Testing xtb    "
echo "------------------"
echo ""
xtb --version
wait 
cd /loctmp/dam63759/orca 
ln -s $(which xtb) otool_xtb
cd ..
rm -rf xtb-6.5.1-linux-x86_64.tar.xz 
echo ""
echo "------------------"
echo "Successfully installed xtb"
echo "------------------"
echo ""
