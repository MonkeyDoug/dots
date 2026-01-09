export ZSH="$XDG_CONFIG_HOME/.oh-my-zsh"

ZSH_THEME="dracula"

plugins=(colored-man-pages git ls zsh-autosuggestions vi-mode z zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh
source $XDG_CONFIG_HOME/.zsh_after
