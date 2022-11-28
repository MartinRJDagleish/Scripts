#!/bin/bash

wget https://github.com/dftbplus/dftbplus/releases/download/22.1/dftbplus-22.1.x86_64-linux.tar.xz --show-progress -q
echo "******************"
echo "Download complete!"
echo "******************"
echo "" 
tar -xvf dftbplus-22.1.x86_64-linux.tar.xz 
echo ""
echo "Unpacking complete" 
echo ""
mv dftbplus-22.1.x86_64-linux dftbplus-22.1 
echo ""
echo "Rename complete"
echo ""
rm -rf dftbplus-22.1.x86_64-linux.tar.xz 
echo ""
echo "Removed .tar.xz file"
echo ""
echo "Adding bin path to PATH in bashrc"
echo ""
cd dftbplus-22.1/bin 
echo "This is the path with the bins: " $(pwd)
echo ""
echo "Adding to PATH!"
echo 'export PATH='$(pwd)':$PATH' >> ~/.bashrc
echo "DONE!"
