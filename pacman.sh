#!/bin/bash

set -e  # Parar em qualquer erro

if [ "$EUID" -eq 0 ]; then
    echo "❌ Não execute este script como root. Saia do root e tente novamente."
    exit 1
fi

echo "🔧 Instalando dependências iniciais..."
sudo pacman -S --needed --noconfirm git base-devel

if ! command -v yay &> /dev/null; then
    echo "📦 Instalando yay-bin..."
    git clone https://aur.archlinux.org/yay-bin.git
    cd yay-bin
    makepkg -si --noconfirm
    cd ..
    rm -rf yay-bin
else
    echo "✅ yay já está instalado."
fi

echo "🔑 Importando chave do Chaotic-AUR..."
sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
sudo pacman-key --lsign-key 3056513887B78AEB

echo "🌐 Instalando keyring e mirrorlist do Chaotic-AUR..."
sudo pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
sudo pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'

echo "⚙️ Copiando pacman.conf personalizado..."
sudo cp ./pacman/pacman.conf /etc/pacman.conf
echo "pacman.conf personalizado copiado."

echo "Atualizando o sistema antes de instalar pacotes..."
yay -Syu --noconfirm

read -p "📦 Deseja instalar os pacotes definidos para os dotfiles? (y/n): " install_packages

if [[ "$install_packages" == "y" ]]; then
    echo "🚀 Instalando pacotes..."
    yay -S --needed --noconfirm - < ./pacman/packages.txt
    echo "✅ Todos os pacotes foram instalados."
else
    echo "⚠️ Instalação de pacotes pulada pelo usuário."
fi

echo "➕ Adicionando $USER aos grupos input e seat..."
sudo usermod -aG input "$USER"
sudo usermod -aG seat "$USER"
echo "⚠️ Para que as mudanças nos grupos tenham efeito, faça logout e login novamente."

if command -v fish &> /dev/null; then
    echo "🐟 Alterando shell padrão para fish..."
    chsh -s /bin/fish
else
    echo "⚠️ Fish não instalado. Pulei mudança de shell."
fi
