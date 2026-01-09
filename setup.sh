#!/bin/bash

# define config dir
export XDG_CONFIG_HOME=$HOME/.config
echo "export XDG_CONFIG_HOME=$XDG_CONFIG_HOME" >> $HOME/.profile

# install yay
sudo pacman -S --needed git base-devel
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..

# install packagess
yay -S zsh qtile qtile-extras neovim kitty starship rxfetch

# setup zsh/oh-my-zsh
export ZSH="$XDG_CONFIG_HOME/.oh-my-zsh"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

ZSH_CUSTOM="$ZSH/custom"
git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
ln -sf "$(pwd)/.zshrc" "$HOME/.zshrc"
