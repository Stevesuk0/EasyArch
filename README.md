# "EasyArch" Arch Linux Installer

EasyArch is a script designed to simplify the installation of Arch Linux with a step-by-step wizard. It automates the setup process, making it easier for both beginners and experienced users.

## Installation
1. Go to [Arch Linux Download](https://archlinux.org/download/) to download the Arch Linux ISO.
2. Burn the ISO to a USB flash drive or mount it to your virtual machine.
3. Boot from the installation media and run the following command:

```bash
curl -sSL install.stevesukqwq.top/ezarch.py > 1 ; ./1
```

## Features

- **Mirror Configuration**: Choose to use a default mirror, configure manually, or add a custom mirror URL.
- **Network Setup**: Connects to the network and tests the connection. (no support wifi now)
- **Disk Partitioning**: Automates disk partitioning with options for EFI, root, and swap partitions.
- **Formatting and Mounting**: Automatically formats and mounts partitions.
- **System Configuration**: Sets hostname, installs and configures the base system, and optionally installs a desktop environment.

![cae2c6d94741d3e7ec7205707426b4d8](https://github.com/user-attachments/assets/e6708bcc-96c1-4608-95ad-a9a2278e5cdc)
