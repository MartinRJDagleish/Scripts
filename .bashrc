######################################################################
#
#
#           ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗
#           ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔════╝
#           ██████╔╝███████║███████╗███████║██████╔╝██║     
#           ██╔══██╗██╔══██║╚════██║██╔══██║██╔══██╗██║     
#           ██████╔╝██║  ██║███████║██║  ██║██║  ██║╚██████╗
#           ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝
#
#
######################################################################


export PATH="$HOME/bin:$PATH"
eval "$(oh-my-posh init bash --config ~/.poshthemes/clean-detailed.omp.json)"

function path_remove {
  # Delete path by parts so we can never accidentally remove sub paths
  if [ "$PATH" == "$1" ] ; then PATH="" ; fi
  PATH=${PATH//":$1:"/":"} # delete any instances in the middle
  PATH=${PATH/#"$1:"/} # delete any instance at the beginning
  PATH=${PATH/%":$1"/} # delete any instance in the at the end
}


export PATH="/loctmp/dam63759/xtb-6.5.1/bin:$PATH"
export PATH="/loctmp/dam63759/orca:$PATH"; export LD_LIBRARY_PATH="/loctmp/dam63759/orca:$LD_LIBRARY_PATH"

ulimit -s unlimited # this is necassary for xtb and anmr -> prevention of stackoverflow 

tailbat() {
	tail -f "$1" | bat --paging=never -l log 
}

alias h="history"
alias lsa="ls -a"
alias lsl="ls -l"
alias orcaw="cd /loctmp/dam63759/orca_work"
alias ..="cd .."
alias ...="cd ../.."

alias bashrc="nvim ~/.bashrc"

function largest_files() {
	echo "$(pwd)";
	echo "";
	du -h -x -s -- * | sort -r -h | head -20;
}
