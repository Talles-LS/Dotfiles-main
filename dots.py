#!/usr/bin/env python3

import os
import shutil
import subprocess
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

def clear():
    os.system("clear")

def title():
    clear()
    banner = """
     ░█▀█░█░█░█▀▀░█▀█░▀█▀░█▀▄░█▀▀░▀░█▀▀
     ░█▀█░▄▀▄░█▀▀░█░█░░█░░█░█░█▀▀░░░▀▀█
     ░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀░░▀▀▀░░░▀▀▀
     ░█▀▄░█▀█░▀█▀░█▀▀░▀█▀░█░░░█▀▀░█▀▀
     ░█░█░█░█░░█░░█▀▀░░█░░█░░░█▀▀░▀▀█
     ░▀▀░░▀▀▀░░▀░░▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀
    """
    console.print(Panel.fit(banner, title="[bold red]DOTFILES INSTALLER", subtitle="by Axenide"))


def show_menu():
    title()
    graphics = questionary.select("Escolha sua placa gráfica:", choices=["NVIDIA", "Open Source (AMD/Intel/Nouveau)"]).ask()
    keyboard = questionary.select("Layout de teclado:", choices=["US", "LATAM"]).ask()
    return graphics, keyboard


def copy_config(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(src, dest)


def stow_dotfiles():
    title()
    console.print("🔗 Aplicando dotfiles com stow...", style="bold green")
    # Usar --restow para garantir re-aplicação sem mover arquivos
    subprocess.run(["stow", "--restow", "dots"], check=True)


def install_packages():
    title()
    if questionary.confirm("Deseja instalar os pacotes necessários agora?").ask():
        subprocess.run(["bash", "pacman.sh"], check=True)
    else:
        console.print("⚠️ Instalação de pacotes pulada.", style="bold yellow")


def install_tpm():
    title()
    if questionary.confirm("Instalar plugins do Tmux (TPM)?").ask():
        tpm_dir = os.path.expanduser("~/.tmux/plugins/tpm")
        # Remove pasta tpm inteira, não só o diretório pai
        subprocess.run(["rm", "-rf", tpm_dir], check=True)
        os.makedirs(os.path.dirname(tpm_dir), exist_ok=True)
        subprocess.run(["git", "clone", "https://github.com/tmux-plugins/tpm", tpm_dir], check=True)

        install_script = os.path.join(tpm_dir, "scripts", "install_plugins.sh")
        if os.path.isfile(install_script):
            subprocess.run([install_script], check=True)
        else:
            console.print(f"❌ Script de instalação TPM não encontrado: {install_script}", style="bold red")
    else:
        console.print("⚠️ Instalação do TPM pulada.", style="bold yellow")


def apply_theme():
    if os.path.exists("./example_wallpaper.jpg"):
        try:
            subprocess.run(["matugen", "image", "./example_wallpaper.jpg"], check=True, stdout=subprocess.DEVNULL)
        except FileNotFoundError:
            console.print("⚠️ 'matugen' não encontrado, pulei aplicação do tema.", style="yellow")
    else:
        console.print("⚠️ Wallpaper exemplo não encontrado. Pulei Matugen.", style="yellow")


def main():
    title()
    graphics, keyboard = show_menu()

    gpu_conf = "./options/nvidia.conf" if graphics == "NVIDIA" else "./options/nvidia-dummy.conf"
    copy_config(gpu_conf, "./dots/.config/hypr/source/nvidia.conf")

    layout = "us.conf" if keyboard == "US" else "latam.conf"
    copy_config(f"./options/{layout}", "./dots/.config/hypr/source/keyboard.conf")

    stow_dotfiles()
    install_packages()
    install_tpm()
    apply_theme()

    clear()
    console.print(Panel.fit("✅ Setup concluído!\n🔗 github.com/Axenide", style="bold green", title="Finalizado"))


if __name__ == "__main__":
    main()
