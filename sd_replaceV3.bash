#!/bin/bash

mkdir -p BACKUP_V3 ;

for file in $(fd -e tex); do
  cp $file BACKUP_V3/ ;
  sd '\\hat\s(\w)' '\hat{$1}' "$file" ; 
done
