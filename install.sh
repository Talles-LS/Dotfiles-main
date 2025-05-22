#!/bin/bash
set -e

# Atualiza base e instala pacman base packages
sudo pacman -Syu --needed --noconfirm git stow python python-pip

# Verifica se yay está instalado, instala se não
if ! command -v yay &> /dev/null; then
  echo "yay não encontrado, instalando..."
  git clone https://aur.archlinux.org/yay-bin.git
  cd yay-bin
  makepkg -si --noconfirm
  cd ..
  rm -rf yay-bin
fi

# Agora instala os pacotes AUR python-questionary e python-rich com yay
yay -Syu --noconfirm --needed python-questionary python-rich

# Roda o script python
python ./dots.py
