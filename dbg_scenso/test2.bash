while getopts u: flag; do 
    case "${flag}" in 
        u) var=${OPTARG};; 
        *) echo "unknown flag" ;; 
    esac
done


echo "var: $var"