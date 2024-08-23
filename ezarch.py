#!/usr/bin/python3

import os
import time

bootefi = False
kernel_type = ''
disk = ''

def clear():
    time.sleep(1)
    os.system("clear")
    

def run_command_chroot(command):
    os.system(f"arch-chroot /mnt /bin/bash -c '{command}'")

def get_cpu_architecture():
    with open('/proc/cpuinfo') as f:
        cpu_info = f.read()
    if "intel" in cpu_info.lower():
        return "intel"
    elif "amd" in cpu_info.lower():
        return "amd"
    else:
        return None

def welcome():
    clear()
    print("Welcome to Steve's Arch Installer\n")
    print("Press Enter to install Arch Linux with a simple wizard.")
    print("Press Ctrl + C to install manually.")
    try:
        input()
    except KeyboardInterrupt:
        exit()

def Stage1():
    clear()
    print("Stage: [1 / 13] - Configure pacman mirror")
    print("\nArch Linux installation image has a service called \"reflector\", which automatically updates the mirrorlist, the list of software repositories used by the package manager pacman. However, due to the special network conditions caused by geographical location, enabling this service might not be suitable if you cannot connect to the default repositories.")
    print("\n[1] Use the service \"reflector\"")
    print("[2] Self-configure pacman mirror")
    print("[3] Add a URL as a pacman mirror\n")

    while True:
        choice = input(">>> ").strip()
        if choice == '1':
            os.system('systemctl start reflector')
            break
        elif choice == '2':
            os.system('systemctl stop reflector')
            print("Please configure the mirrorlist manually. Press Ctrl+X to exit nano and save changes.")
            os.system('nano /etc/pacman.d/mirrorlist')
            break
        elif choice == '3':
            os.system('systemctl stop reflector')
            print("Input a URL as a pacman mirror (e.g. mirrors.bfsu.edu.cn)")
            url = input(">>> ").strip()
            if url:
                with open("/etc/pacman.d/mirrorlist", "w") as f:
                    f.write(f"Server = https://{url}/archlinux/$repo/os/$arch\n")
            else:
                print("Invalid URL. Please try again.")
                continue
            break
        else:
            print("Invalid choice, please try again.")


def Stage2():
    clear()
    print("Stage: [2 / 13] - Configure Buzzer Kernel Module")
    print("\nWhen Tab completion fails, some devices emit a 'beep' sound from the buzzer. You can disable the buzzer in this Stage.")
    print("\n[1] Keep \"Buzzer Kernel Module\" on")
    print("[2] Disable \"Buzzer Kernel Module\" currently")
    print("[3] Disable \"Buzzer Kernel Module\" permanently\n")
    while True:
        choice = input(">>> ")
        if choice == '1':
            break
        if choice == '2':
            os.system('rmmod pcspkr')
            break
        if choice == '3':
            os.system('rmmod pcspkr')
            with open("/etc/modprobe.d/blacklist.conf", "a+") as f:
                f.write("blacklist pcspkr\n")
            break
        else:
            pass

def Stage3():
    global bootefi
    clear()
    print("Stage: [3 / 13] - Checking boot mode")
    print("\nThis section is checking your boot mode (UEFI or BIOS).\n")
    if os.path.exists('/sys/firmware/efi/efivars'):
        print("Boot mode: UEFI")
        bootefi = True
    else:
        print("Boot mode: BIOS")
        bootefi = False
    if not bootefi:
        print("\n* Your system is not using UEFI as the boot mode. For better compatibility and features, especially with modern hardware, it's recommended to use UEFI.\n")
    else:
        print("\n* Your system is using UEFI as the boot mode. This is the recommended boot mode for modern systems, providing better compatibility, security features, and faster boot times.\n")
    print("Continue in 2 secs...")
    time.sleep(3)


def Stage4():
    clear()
    print("Stage: [4 / 13] - Connecting to the network")
    print("\nThis is your network address, wireless connection will support soon.\n")
    print("=" * 13)
    os.system('ip addr')
    print("=" * 13)

def Stage5():
    clear()
    print("Stage: [5 / 13] - Testing network connection")
    response = os.system("ping -c 4 cloudflare.com")
    if response == 0:
        print("\nNetwork is up and running.")
    else:
        print("\nNetwork seems to be down. Please check your connection.")
        input("Press Enter to continue")


def Stage6():
    clear()
    print("Stage: [6 / 13] - Synchronize time")
    print("\nTo ensure accurate system operations, it's important to synchronize time across all servers regularly. This can be done using NTP (Network Time Protocol) or other time synchronization services.")
    print("\n[1] Synchronize time with NTP Server")
    print("[2] Keep NTP service close\n")
    while True:
        choice = input(">>> ")
        if choice == '1':
            os.system('timedatectl set-ntp true')
            break
        if choice == '2':
            break
        else:
            pass

def get_disk():
    clear()
    print("Available Disks:")
    os.system("lsblk -d -o NAME,SIZE,MODEL")
    disk = input("\nEnter the disk you want to use (e.g., sda): ")
    return f"/dev/{disk}"

def Stage7():
    global disk
    clear()
    print("Stage [7 / 13] - Automatic Disk Partition\n")
    disk = get_disk()
    os.system(f"sgdisk -n 1:0:+1G -t 1:ef00 {disk}")
    os.system(f"sgdisk -n 2:0:-5G -t 2:8300 {disk}")
    os.system(f"sgdisk -n 3:0:0 -t 3:8200 {disk}")
    print("\nDisk partitioning completed.")

def Stage8():
    global disk
    clear()
    print("Stage [8 / 13] - Format Partition")
    print("\nAutomatic formatting in progress...\n")
    os.system(f"mkfs.fat -F32 {disk}1")
    os.system(f"mkfs.ext4 {disk}2")
    os.system(f"mkswap {disk}3")
    print("\nPartition formatting completed.")

def Stage9():
    global disk
    clear()
    print("Stage [9 / 13] - Mount Partition")
    print("\nAutomatic mounting in progress...\n")
    root_partition = f"{disk}2"
    boot_partition = f"{disk}1"
    swap_partition = f"{disk}3"
    print(f"Mounting {root_partition} to /mnt...")
    os.system(f"mount {root_partition} /mnt")
    os.makedirs("/mnt/boot", exist_ok=True)
    print(f"Mounting {boot_partition} to /mnt/boot...")
    os.system(f"mount {boot_partition} /mnt/boot")
    os.system(f"swapon {swap_partition}")
    print("\nMounted partitions:")
    os.system("lsblk -o NAME,MOUNTPOINT,SIZE,FSTYPE,LABEL,UUID")
    print("\nPartition mount completed successfully.")

def Stage10():
    clear()
    print("Stage [10 / 13] - Setting the hostname")
    print("\nThe hostname serves as the network identifier. If you're installing it just for fun, you can edit anything as needed.\n")
    os.makedirs("/mnt/etc/", exist_ok=True)
    with open('/mnt/etc/hostname', "w") as f:
        f.write(input(">>>"))

def Stage11():
    global kernel_type
    clear()
    print("Stage [11 / 13] - Select a kernel")
    print("\nSelect a kernel to install.\n")
    print("[1] linux: Stable version, the latest features.")
    print("[2] linux-lts: Long-Term Support version, ideal for a stable experience.")
    print("[3] linux-zen: Optimized kernel for improved performance.")
    print("[4] linux-hardened: Focuses on enhanced security.")
    print("[5] linux-rt: Optimized for real-time performance.")
    while True:
        choice = input(">>> ")
        if choice == '1':
            kernel_type = 'linux'
            break
        if choice == '2':
            kernel_type = 'linux-lts'
            break
        if choice == '3':
            kernel_type = 'linux-zen'
            break
        if choice == '4':
            kernel_type = 'linux-hardened'
            break
        if choice == '5':
            kernel_type = 'linux-rt'
            break
        else:
            pass


def Stage12():
    clear()
    print("Stage [12 / 13] - Install the base system")
    print("\nAutomatic configure in progress...")
    if "amd" in get_cpu_architecture():
        ucode = 'amd-ucode'
    if "intel".lower() in get_cpu_architecture():
        ucode = 'intel-ucode'
    os.system(f"pacstrap /mnt base pacman networkmanager vim sudo zsh zsh-completions grub efibootmgr fastfetch {ucode} {kernel_type} linux-firmware")

def Stage13():
    clear()
    print("Stage [13 / 13] - System Configuration")
    print("Automatic configuration in progress...\n")

    print("\nStep 1: Generating filesystem table...")
    os.makedirs('/mnt/etc', exist_ok=True)
    os.system('genfstab -U /mnt > /mnt/etc/fstab')
    os.system('cat /mnt/etc/fstab')
    
    print("\nStep 2: Configuring host file...")
    with open('/mnt/etc/hosts', "w") as f:
        f.write("127.0.0.1 localhost\n::1 localhost")
    os.system('cat /mnt/etc/hosts')

    print("\nStep 3: Installing bootloader...")
    run_command_chroot("grub-install --target=x86_64-efi --efi-directory=/boot")
    
    print("\nStep 4: Configuring bootloader...")
    with open("/mnt/etc/default/grub", 'r') as f:
        line = f.read().split("\n")
    for i in range(len(line)):
        if 'GRUB_CMDLINE_LINUX_DEFAULT' in line[i]:
            line[i] = "GRUB_CMDLINE_LINUX_DEFAULT=\"loglevel=5 ibt=off nowatchdog\""
    with open("/mnt/etc/default/grub", 'w') as f:
        f.writelines(line)
    run_command_chroot("grub-mkconfig -o /boot/grub/grub.cfg")

    print("\nStep 5: Synchronizing hardware clock...")
    run_command_chroot("hwclock --systohc")

    print("\nStep 6: Setting locale...")
    with open("/mnt/etc/locale.gen", "w") as f:
        f.write("en_US.UTF-8 UTF-8\n")
    run_command_chroot("locale-gen")
    with open("/mnt/etc/locale.conf", "w") as f:
        f.write("LANG=en_US.UTF-8")
    
    print("\nStep 7: Synchronizing pacman mirror list...")
    with open("/etc/pacman.d/mirrorlist") as f:
        mirrorlist = f.read()
    with open("/mnt/etc/pacman.d/mirrorlist", "w") as f:
        f.write(mirrorlist)

    print("\nStep 8: Enable networking...")
    run_command_chroot("systemctl start networkmanager")


    clear()
    print("Stage [13 / 13] - Setting user")
    print("Please choose a password for the root account. For security reasons, the password will be hidden.\n")
    run_command_chroot('passwd root')
    create_user = input("\nWould you like to create a new user account? (yes/no): ").strip().lower()
    if create_user == 'yes':
        username = input("Enter the username for the new account: ").strip()
        run_command_chroot(f"useradd -m -G wheel -s /bin/zsh {username}")
        print(f"Setting password for the user {username}...\n")
        run_command_chroot(f"passwd {username}")
        print(f"User {username} created and password set.\n")
        print("Configuring sudoers file...")
        with open("/mnt/etc/sudoers", 'r') as f:
            line = f.read().split("\n")
            for i in range(len(line)):
                if '#%wheel ALL=(ALL:ALL) ALL' in line[i]:
                    line[i] = "%wheel ALL=(ALL:ALL) ALL"
            with open("/mnt/etc/sudoers", 'w') as f:
                f.writelines(line)
        
        
        

    clear()
    print("Stage [13 / 13] - Desktop Environment Installation")
    install_desktop = input("\nWould you like to install a desktop environment? (yes/no): ").strip().lower()
    if install_desktop == 'yes':
        print("\nSelect a desktop environment:")
        print("[1] GNOME (default)")
        print("[2] KDE Plasma")
        print("[3] XFCE")
        print("[4] Cinnamon")
        print("[5] LXQt")
        print("[6] Mate")
        print("[7] Deepin")
        desktop_choice = input(">>> ").strip()

        if desktop_choice == '1' or desktop_choice == '':
            print("Installing GNOME...")
            run_command_chroot("pacman -Syu --noconfirm gnome gnome-extra")
            run_command_chroot("systemctl enable gdm")
        elif desktop_choice == '2':
            print("Installing KDE Plasma...")
            run_command_chroot("pacman -Syu --noconfirm plasma kde-applications")
            run_command_chroot("systemctl enable sddm")
        elif desktop_choice == '3':
            print("Installing XFCE...")
            run_command_chroot("pacman -Syu --noconfirm xfce4 xfce4-goodies")
            run_command_chroot("systemctl enable lightdm")
        elif desktop_choice == '4':
            print("Installing Cinnamon...")
            run_command_chroot("pacman -Syu --noconfirm cinnamon")
            run_command_chroot("systemctl enable lightdm")
        elif desktop_choice == '5':
            print("Installing LXQt...")
            run_command_chroot("pacman -Syu --noconfirm lxqt")
            run_command_chroot("systemctl enable sddm")
        elif desktop_choice == '6':
            print("Installing Mate...")
            run_command_chroot("pacman -Syu --noconfirm mate mate-extra")
            run_command_chroot("systemctl enable lightdm")
        elif desktop_choice == '7':
            print("Installing Deepin...")
            run_command_chroot("pacman -Syu --noconfirm deepin deepin-extra")
            run_command_chroot("systemctl enable lightdm")
        else:
            print("Invalid selection. Skipping desktop environment installation.")
        
        if desktop_choice == '3':
            run_command_chroot("pacman -Syu --noconfirm xdg-desktop-portal-kde")
        else:
            run_command_chroot("pacman -Syu --noconfirm xdg-desktop-portal")
        
        print("Desktop environment installation complete.\n")

        
    clear()
    print("\nSystem configuration completed. Installation is done!\n")


    

def end():
    clear()
    print("Installation Finished!")
    print("\nArch Linux has been successfully installed on your computer. You can stay in the LiveCD environment to perform additional configurations or reboot into your new system.\n")
    print("Useful Resources:")
    print("- Arch Linux Wiki: https://wiki.archlinux.org/")
    print("- Arch User Repository: https://aur.archlinux.org/")
    print("- Official Forums: https://bbs.archlinux.org/")
    print("- Arch IRC Channel: #archlinux on libera.chat\n")
    run_command_chroot('fastfetch')
    print("\nBy stepping into the world of Linux, you're embracing a tool of freedom and endless possibilities.")
    print("** Be brave in your exploration, every challenge is an opportunity to grow! **\n\n")
    choice = input("Would you like to reboot now? (y/n): ")
    if choice.lower() == 'y':
        os.system("reboot")
    else:
        print("You can manually reboot the system later by typing 'reboot'.")



welcome()
Stage1()
Stage2()
Stage3()
Stage4()
Stage5()
Stage6()
try:
    Stage7()
    Stage8()
    Stage9()
    Stage10()
    Stage11()
    Stage12()
    Stage13()
    end()
except:
    os.system('umount -R /mnt')
