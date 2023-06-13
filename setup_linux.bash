#!/bin/bash 

# 1. List of programmes to install

path_to_install="~/.local/bins"
bin_list=("fzf" "exa" "nnn" "bat" "fd" "rg")
repo_list=("junegunn/fzf" "ogham/exa" "jarun/nnn" "sharkdp/bat" "sharkdp/fd" "BurntSushi/ripgrep")
# ripgrep or ripgrep all?`
install_list=()
for i in "${!bin_list[@]}"; do
    if ! command -v "${bin_list[$i]}" >/dev/null 2>&1; then
        install_list+=("$bin")
    fi
done
# DEBUG:
# echo $install_list

# idx way:
for i in "${!repo_list[@]}"; do
	echo "$i: ${repo_list[$i]}";
  # echo "${bin_list[$i]}";
  
  # Get the latest release from the API
  repo_name=${repo_list[$i]};
  release=$(curl -s "https://api.github.com/repos/your-username/$repo_name/releases/latest")

  # Get the download URL for the release asset
  download_url=$(echo "$release" | grep -o "browser_download_url.*\.tar\.gz" | cut -d '"' -f 3)

  # Create the directory for the release
  repo_install_dir=$path_to_install/$repo_name
  mkdir -p $repo_install_dir

  # Download and extract the release asset
  curl -L "$download_url" | tar -xz -C ~/bins/$repo_name --strip-components=1

  # Add the bin directory to PATH
  if [ -n "$ZSH_VERSION" ]; then
    echo 'export PATH="$HOME/bins/'$repo_name'/bin:$PATH"' >> ~/.zshrc
  else
    echo 'export PATH="$HOME/bins/'$repo_name'/bin:$PATH"' >> ~/.bashrc
  fi

done

# Reload the shell
exec "${SHELL}"


# normal way, where repo_name is the var to hold str
# for repo_name in "${repo_list[@]}"; do


