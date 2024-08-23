# "EasyArch" Arch Linux Installer

EasyArch is a script designed to simplify the installation of Arch Linux with a step-by-step wizard. It automates the setup process, making it easier for both beginners and experienced users.

## Features

- **Mirror Configuration**: Choose to use a default mirror, configure manually, or add a custom mirror URL.
- **Network Setup**: Connects to the network and tests the connection. (no support wifi now)
- **Disk Partitioning**: Automates disk partitioning with options for EFI, root, and swap partitions.
- **Formatting and Mounting**: Automatically formats and mounts partitions.
- **System Configuration**: Sets hostname, installs and configures the base system, and optionally installs a desktop environment.

## Installation

To install using this script, run the following command:

```bash
curl -sSL https://install.stevesukqwq.top | bash
