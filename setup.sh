#!/bin/bash

set -e

# --- Determine Paths ---
# Get the absolute path of the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set XDG_CONFIG_HOME to the the script location
export XDG_CONFIG_HOME="$SCRIPT_DIR"

echo "Script location: $SCRIPT_DIR"
echo "Setting XDG_CONFIG_HOME to: $XDG_CONFIG_HOME"

ZSHRC_FILE="$SCRIPT_DIR/.zshrc"

# add XDG_CONFIG_HOME to local zshrc
if ! grep -q "export XDG_CONFIG_HOME=" "$ZSHRC_FILE"; then
    sed -i "1i export XDG_CONFIG_HOME=\"$XDG_CONFIG_HOME\"" "$ZSHRC_FILE"
fi

if ! command -v yay &> /dev/null; then
    echo "Installing yay..."
    sudo pacman -S --needed --noconfirm git base-devel
    
    # Clone to a temporary directory
    git clone https://aur.archlinux.org/yay.git /tmp/yay
    cd /tmp/yay
    makepkg -si --noconfirm
    cd -
    rm -rf /tmp/yay
else
    echo "yay is already installed."
fi

# --- Install Packages ---
echo "Installing packages..."
yay -S --needed --noconfirm zsh neovim-nightly-bin kitty starship rxfetch openssh unzip
yay -S --needed --noconfirm qtile qtile-extras
yay -S --needed --noconfirm xorg xorg-xinit

# --- Setup Xorg ---
ln -sf "$XDG_CONFIG_HOME/.xinitrc" "$HOME/.xinitrc"
ln -sf "$XDG_CONFIG_HOME/.Xresources" "$HOME/.Xresources"

# --- Setup Oh-My-Zsh ---
# This sets the install path relative to the dynamic XDG_CONFIG_HOME
export ZSH="$XDG_CONFIG_HOME/.oh-my-zsh"

if [ ! -d "$ZSH" ]; then
    echo "Installing Oh My Zsh to $ZSH..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
else
    echo "Oh My Zsh is already installed at $ZSH."
fi

# --- ZSH Plugins ---
ZSH_CUSTOM="$ZSH/custom"

install_plugin() {
    local repo_url=$1
    local dest_dir=$2
    if [ ! -d "$dest_dir" ]; then
        echo "Cloning $(basename "$dest_dir")..."
        git clone "$repo_url" "$dest_dir"
    else
        echo "Plugin $(basename "$dest_dir") already exists."
    fi
}

install_plugin "https://github.com/zsh-users/zsh-autosuggestions" "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
install_plugin "https://github.com/zsh-users/zsh-syntax-highlighting.git" "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
install_plugin "https://github.com/zpm-zsh/ls.git" "$ZSH_CUSTOM/plugins/ls"

# --- Symlink .zshrc ---
echo "Symlinking .zshrc to $HOME/.zshrc..."
ln -sf "$ZSHRC_FILE" "$HOME/.zshrc"

# Change shell to zsh if it isn't already
if [ "$SHELL" != "$(which zsh)" ]; then
    echo "Changing default shell to zsh..."
    chsh -s "$(which zsh)"
fi

# --- Setup SSH ---
echo "Symlinking ssh config to $HOME/.ssh/config..."
ln -sf "$XDG_CONFIG_HOME/ssh/config" "$HOME/.ssh/config"

# --- Setup Dracula Themes ---
echo "Installing Dracula themes..."
THEME_DEST="$XDG_CONFIG_HOME/dracula"

# zsh
install_plugin "https://github.com/dracula/zsh.git" "$THEME_DEST/zsh"
ln -sf "$THEME_DEST/zsh/dracula.zsh-theme" "$ZSH_CUSTOM/themes/dracula.zsh-theme"

# gtk
curl -L -o "$THEME_DEST/gtk.zip" https://github.com/dracula/gtk/archive/master.zip
mkdir -p "$HOME/.themes"
unzip -o "$THEME_DEST/gtk.zip" -d "$HOME/.themes/"
mv "$HOME/.themes/gtk-master" "$HOME/.themes/Dracula"

install_plugin "https://github.com/dracula/gtk.git" "$THEME_DEST/gtk"
ln -sf "$THEME_DEST/gtk/assets" "$XDG_CONFIG_HOME/assets"
mkdir -p "$XDG_CONFIG_HOME/gtk-4.0"
ln -sf "$THEME_DEST/gtk/gtk-4.0/gtk.css" "$XDG_CONFIG_HOME/gtk-4.0/gtk.css"
ln -sf "$THEME_DEST/gtk/gtk-4.0/gtk-dark.css" "$XDG_CONFIG_HOME/gtk-4.0/gtk-dark.css"
# gsettings set org.gnome.desktop.interface gtk-theme "Dracula" 
# gsettings set org.gnome.desktop.wm.preferences theme "Dracula"

curl -L -o "$THEME_DEST/icons.zip" https://github.com/dracula/gtk/files/5214870/Dracula.zip
mkdir -p "$HOME/.icons"
unzip -o "$THEME_DEST/icons.zip" -d "$HOME/.icons/"
# gsettings set org.gnome.desktop.interface icon-theme "Dracula"

# --- Install Dev Packages ---
echo "Installing dev packages..."
yay -S --needed --noconfirm tree-sitter tree-sitter-cli pyright bash-language-server

echo "Setup complete!"
