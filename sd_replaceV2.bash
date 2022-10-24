#!/bin/bash

mkdir -p BACKUP_V2 ;

for file in $(fd -e tex); do
  cp $file BACKUP_V2/ ;
  
  sd '\\hat(\\\w+\{\w+\})' '\hat{$1}' "$file" ; 
done
