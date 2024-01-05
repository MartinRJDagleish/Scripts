#!/bin/bash

mkdir -p BACKUP ;

for file in $(fd -e tex); do
  cp $file BACKUP/ ;
  sd '\\hat\s(\w)' '\hat{$1}' "$file" ; 
done
