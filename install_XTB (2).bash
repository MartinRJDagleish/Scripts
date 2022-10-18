#!/bin/bash

cd /tmp 
echo "Now in /tmp"
echo "Starting download of XTB"
wget https://github.com/grimme-lab/xtb/releases/download/v6.5.1/xtb-6.5.1-linux-x86_64.tar.xz -q --show-progress
wait
tar -xvf xtb-6.5.1-linux-x86_64.tar.xz 
wait 
mkdir -p /usr/local/bin/xtb
cd xtb-6.5.1
mv xtb-6.5.1 /usr/local/bin/xtb
cd /usr/local/bin/xtb/bin 
chmod +x xtb
echo ""
echo "------------------"
echo "   Testing xtb    "
echo "------------------"
echo ""
xtb --version
# wait 
# # cd /loctmp/dam63759/orca 
# # ln -s $(which xtb) otool_xtb
# cd ..
cd /tmp 
rm -rf xtb-6.5.1-linux-x86_64.tar.xz
echo ""
echo "------------------"
echo "Successfully installed xtb"
echo "------------------"
echo ""
