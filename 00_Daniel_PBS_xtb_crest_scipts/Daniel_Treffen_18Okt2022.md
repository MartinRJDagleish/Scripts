# Infos von Daniel 

Intel Compiler statt GNU Compiler für xTB verwenden -> siehe GitHub page 
von xTB 
-> `ifort` statt `gfort` oder `gcc`

```bash
export FC=ifort CC=icc
```

Daniel bevorzugt CMake statt meson. -> Heutzutage fast keine build scripts mehr, 
sondern CMake. 

xTB build flags:
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
make -C build
make -C build test
```

ergänzend: `-j [<jobs>], --parallel [<jobs>]` -> Anzahl der parallelen Jobs bzw. der zu nutzenden Threads

-> PBS Script für `job submit` in ORCA_Work bei ATHENE 

