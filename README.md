# GPT Sovits WSL Installer

This project provides an easy and streamlined way to install **GPT Sovits** inside a WSL instance using a Conda environment. It automates much of the setup process, so you can get started quickly without manually configuring dependencies or environments.

---

## Features

- Automated installation of GPT Sovits on WSL with no user intervention
- Utilizes Conda for managing Python environments, ensuring isolation and compatibility
- Supports automatic installation of necessary build tools like CMake
- Configurable through a simple config file to adapt to your WSL setup

---

## Prerequisites

- **Windows 10/11** with [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) properly installed and configured

---

## Setup Instructions

1. **Clone this repository** to your Windows machine.

2. **Configure your WSL machine settings:**

   - Rename `example_config.py` to `config.py`.
   - Open `config.py` and fill in the details about your WSL setup.
   - The `password` field is required for the script to automatically install CMake without manual intervention.

3. **Run the installation script:**
   run install_gpt_sovits.py to get started

---
