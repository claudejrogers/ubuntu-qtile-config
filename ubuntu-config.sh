#!/bin/sh

# This script is to configure Ubuntu 22.04 LTS after installation

log() {
    message=$1
    level=$2
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
    date=$(date +"%Y-%m-%d %H:%M:%S")
    if [ "$level" = "error" ]; then
        msg="${RED}[$date]${NC} $message"
    elif [ "$level" = "warning" ]; then
        msg="${YELLOW}[$date]${NC} $message"
    elif [ "$level" = "success" ]; then
        msg="${GREEN}[$date]${NC} $message"
    elif [ "$level" = "info" ]; then
        msg="${BLUE}[$date]${NC} $message"
    fi
    echo -e "$msg"
}

# Update and upgrade
log "Updating and upgrading packages" "info"
sudo apt update
sudo apt upgrade -y

# Install build-essential
log "Installing build-essential" "info"
sudo apt install -y build-essential
sudo apt install -y cmake pkg-config libfreetype6-dev libfontconfig1-dev libxcb-xfixes0-dev libxkbcommon-dev python3 python3-dev python3-pip python3.10-venv
sudo apt-get install software-properties-common

# Install Fuse for appimages 
log "Installing Fuse" "info"
sudo apt install -y fuse 

# Install nodejs and npm
log "Installing nodejs and npm" "info"
sudo apt install -y nodejs npm

# Install some basic tools
log "Installing basic tools" "info"
sudo apt install -y vim git curl wget

# Install neovim
log "Installing neovim" "info"
sudo add-apt-repository ppa:neovim-ppa/unstable -y
sudo apt-get -y update
sudo apt-get -y install neovim
sudo update-alternatives --install /usr/bin/editor editor /usr/bin/nvim 60
sudo update-alternatives --config editor

# Install alacritty
log "Installing alacritty" "info"
sudo add-apt-repository ppa:aslatter/ppa -y
sudo apt install -y alacritty

# Configure alacritty
mkdir -p ~/.config/alacritty
wget https://raw.githubusercontent.com/claudejrogers/ubuntu-qtile-config/main/alacritty/alacritty.yml
alacritty_config="./alacrity.yml"
# check if alacritty config file exists
# move it to ~/.config/alacritty if it exists
if [ -f "$alacritty_config" ]; then
    log "Alacritty config file exists at $alacritty_config" "success"
    mv "$alacritty_config" ~/.config/alacritty/alacritty.yml
else
    log "Alacritty config file does not exist at $alacritty_config" "error"
    log "Proceeding without configuring alacritty" "warning"
fi


# Install zsh
sudo apt install -y zsh

# Install rust
log "Installing rust" "info"
log "Keyboard input required" "warning"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"

# Install brave browser
log "Installing brave browser" "info"
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list
sudo apt update
sudo apt install -y brave-browser

# Install some fonts
log "Installing the Meslo font" "info"
mkdir -p ~/.local/share/fonts
wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.2/Meslo.zip
unzip Meslo.zip -d ~/.local/share/fonts
fc-cache -fv
rm Meslo.zip

# Configure neovim
log "Configuring neovim using nvim-lua kickstart" "info"
git clone https://github.com/nvim-lua/kickstart.nvim.git "${XDG_CONFIG_HOME:-$HOME/.config}"/nvim
nvim --headless "+Lazy! sync" +qa

# Install rofi, picom, and other packages for qtile
log "Installing prerequisites for qtile" "info"
sudo apt install -y rofi htop aptitude picom

# Install qtile
log "Installing qtile" "info"
# normal pip installation seems broken, and I need to specify older versions of some packages
# pip install cffi==1.15.1
# pip install xcffib==1.3.0
# pip install dbus-next==0.2.3
# pip install cairocffi==1.4.0
# pip install qtile==0.22.1

# # Install qtile from git
pip install xcffib
pip install git+https://github.com/qtile/qtile.git

# Install dependencies for qtile
pip install psutil

# Check if qtile is installed and get qtile path
qtile_path=$(which qtile)
if [ -z "$qtile_path" ]; then
    log "Qtile is not installed" "error"
    exit 1
fi
log "Qtile is installed at $qtile_path" "success"

# Create desktop entry for qtile
log "Creating desktop entry for qtile" "info"
cat > ~/qtile.desktop <<EOF
[Desktop Entry]
Name=Qtile
Comment=Qtile Window Manager
Exec=$qtile_path start
Type=Application
Keywords=wm;tiling
EOF

sudo mv ~/qtile.desktop /usr/share/xsessions/

# Copy qtile config
mkdir -p ~/.config/qtile
wget https://raw.githubusercontent.com/claudejrogers/ubuntu-qtile-config/main/qtile/config.py
qtile_config="./config.py"
# check if qtile config file exists
# move it to ~/.config/qtile if it exists
if [ -f "$qtile_config" ]; then
    log "Qtile config file exists at $qtile_config" "success"
    mv "$qtile_config" ~/.config/qtile/config.py
else
    log "Qtile config file does not exist at $qtile_config" "error"
    log "Proceeding without configuring qtile" "warning"
fi

# Configure GTK themes
log "Configuring GTK themes" "info"
cat > ~/.gtkrc-2.0 <<EOF
gtk-theme-name="Yaru-blue-dark"
gtk-icon-theme-name="Yaru-blue-dark"
EOF

mkdir -p ~/.config/gtk-3.0
cat > ~/.config/gtk-3.0/settings.ini <<EOF
[Settings]
gtk-theme-name=Yaru-blue-dark
gtk-icon-theme-name=Yaru-blue-dark
EOF

# Download rofi themes/config
log "Downloading rofi themes/config" "info"
mkdir -p ~/.config/rofi
wget https://raw.githubusercontent.com/claudejrogers/ubuntu-qtile-config/main/rofi/config.rasi
wget https://raw.githubusercontent.com/claudejrogers/ubuntu-qtile-config/main/rofi/doom-one.rasi
mkdir -p ~/.config/rofi/themes
mv doom-one.rasi ~/.config/rofi/themes
mv config.rasi ~/.config/rofi
mkdir -p ~/.local/scripts
wget https://raw.githubusercontent.com/claudejrogers/ubuntu-qtile-config/main/scripts/powermenu.sh
mv powermenu.sh ~/.local/scripts


# Install mambaforge python
# TODO: install mambaforge python

# Switch shell to zsh
log "Switching shell to zsh and installing oh-my-zsh" "info"
chsh -s $(which zsh)

# Install oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"