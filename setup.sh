#!/bin/bash

path=~/.config/pystromo

# install program
mkdir $path
cp -r * $path/
chmod +x $path/pystromo*

# install launcher
cp pystromo ~/bin/
chmod +x ~/bin/pystromo


# Add tab completion to bash
tabcomplete='
# Pystromo tab completion function
_pystromo() {
	COMPREPLY=()
	local flag=${COMP_WORDS[1]}
	local index=$COMP_CWORD
	[ -z $index ] && index=0
	if [[ $flag == "-"* ]] && [ $index == 2 ] || [ $index == 1 ]; then
		COMPREPLY=($(compgen -W "$(ls *.map 2>/dev/null;cd ~/.config/pystromo/config;ls *.map 2>/dev/null)" -- ${COMP_WORDS[COMP_CWORD]}))
	else
		COMPREPLY=($(compgen -c -- ${COMP_WORDS[COMP_CWORD]}))
	fi
	return 0
}
complete -F _pystromo pystromo'

file=~/bashrc
meh=$(grep _pystromo $file)
if [ $? -eq 1 ]; then
	echo $tabcomplete >> $file
fi


echo "Next bit needs to run as root"

#check uinput
meh=$(lsmod | grep uinput)
if [ $? -eq 1 ]; then
	echo "Starting uinput kernel module"
	echo uinput | sudo tee /etc/modules-load.d/uinput.conf
	sudo modprobe uinput
fi

# also add rules
sudo cp config/52-pystromo-suse.rules /etc/udev/rules.d/


















