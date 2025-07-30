import subprocess
import os
import os as os_module
import shutil
from config import wsl_machine_name, wsl_user, wsl_paswd
import stat
import time

def handle_remove_readonly(func, path, exc):
    import errno
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        # Change the file to writable
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

def is_gptsovits_env_installed(os, wsl_machine_name= wsl_machine_name, wsl_user=wsl_user):
    env_name = "GPTSoVits"

    if os == "windows":
        result = subprocess.run([
            "wsl",
            "-d", wsl_machine_name,
            "-u", wsl_user,
            "bash",
            "-ilc",
            "conda env list"
        ], capture_output=True, text=True)
    
    elif os == "linux":
        result = subprocess.run([
        "bash", "-i", "-c", 
        "source ~/miniconda3/etc/profile.d/conda.sh && conda env list"
        ], capture_output=True, text=True)

    else:
        raise ValueError(f"Unsupported OS: {os}")

    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        # Extract environment name considering '*'
        if line.startswith("*"):
            name = line.split()[1]
        else:
            name = line.split()[0]

        if name == env_name:
            return True

    return False

def install_conda(os):
    if os == "windows": 
     subprocess.run([
      'wsl', '-d', wsl_machine_name, '-u', wsl_user,
      'bash', '-ilc',
      'curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh'
      ], check=True)
 
     subprocess.run([
         'wsl', '-d', wsl_machine_name, '-u', wsl_user,
         'bash', '-ilc',
         'bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3'
     ], check=True)
 
     subprocess.run([
         'wsl', '-d', wsl_machine_name, '-u', wsl_user,
         'bash', '-ilc',
         '$HOME/miniconda3/bin/conda init'
     ], check=True)
 
     subprocess.run([
         'wsl', '-d', wsl_machine_name, '-u', wsl_user,
         'bash', '-ilc',
         'rm Miniconda3-latest-Linux-x86_64.sh'
     ], check=True)
 
     print("Miniconda installation complete!")

    elif os == "linux":
        home = os_module.path.expanduser("~")
        installer = "Miniconda3-latest-Linux-x86_64.sh"
    
        cmds = f'''
            curl -O https://repo.anaconda.com/miniconda/{installer} && \
            bash {installer} -b -p {home}/miniconda3 && \
            {home}/miniconda3/bin/conda init && \
            rm {installer}
        '''
    
        subprocess.run(cmds, shell=True, executable="/bin/bash", check=True)
    
        print("Miniconda installation complete!")

def create_conda_env(os_type, wsl_machine_name= wsl_machine_name, wsl_user = wsl_user, env_name="GPTSoVits", python_version="3.10"):
    channels = [
        "https://repo.anaconda.com/pkgs/main",
        "https://repo.anaconda.com/pkgs/r"
    ]

    if os_type == "windows":
        for channel in channels:
            subprocess.run([
                "wsl", "-d", wsl_machine_name, "-u", wsl_user,
                f"/home/{wsl_user}/miniconda3/bin/conda", "tos", "accept",
                "--override-channels", "--channel", channel
            ], check=True)

        subprocess.run([
            "wsl", "-d", wsl_machine_name, "-u", wsl_user,
            f"/home/{wsl_user}/miniconda3/bin/conda", "create",
            "-n", env_name, f"python={python_version}", "-y"
        ], check=True)

    elif os_type == "linux":
     conda_path = os.path.expanduser("~/miniconda3/bin/conda")
     
     for channel in channels:
        subprocess.run([
            conda_path, "tos", "accept", "--override-channels","--channel", channel
        ], check=True)
 
     subprocess.run([
        "bash", "-c",
        f"source ~/.bashrc && {conda_path} create -n {env_name} python={python_version} -y"
    ], check=True)

def install_gpt_sovits(os):
 if os == "windows":
   # pull gpt sovits git
   subprocess.run([
       'git', 'clone', 'https://github.com/RVC-Boss/GPT-SoVITS.git'
   ])
   
   # add status to api file
   with open('GPT-SoVITS/api.py', 'a') as f: f.write('\n@app.get("/status")\nasync def get_status():\n    return JSONResponse(content={"status": "online"})\n')
   
   if is_gptsovits_env_installed("windows"):
       pass
   else:
     # Create conda env
     create_conda_env("windows", wsl_machine_name, wsl_user)
   
   # Install requirments
   shutil.move("GPT-SoVITS/requirements.txt", "requirements.txt")
   shutil.move("GPT-SoVITS/extra-req.txt", "extra-req.txt")
   
   subprocess.run([
       'wsl', '-d', wsl_machine_name, '-u', wsl_user,
       'bash', '-ilc',
       f'source ~/miniconda3/etc/profile.d/conda.sh && conda activate GPTSoVits && echo {wsl_paswd} | sudo -S apt update && sudo apt install -y build-essential cmake'
   ])
   
   subprocess.run([
       'wsl', '-d', wsl_machine_name, '-u', wsl_user,
       'bash', '-ilc',
       'source ~/miniconda3/etc/profile.d/conda.sh && conda activate GPTSoVits && pip install -r extra-req.txt --no-deps'
   ])
   
   subprocess.run([
       'wsl', '-d', wsl_machine_name, '-u', wsl_user,
       'bash', '-ilc',
       'source ~/miniconda3/etc/profile.d/conda.sh && conda activate GPTSoVits && pip install -r requirements.txt'
   ])
   
   shutil.move("requirements.txt", "GPT-SoVITS/requirements.txt")
   shutil.move("extra-req.txt", "GPT-SoVITS/extra-req.txt")
   
   # git clone pretrained model
   subprocess.run([
       'git', 'clone', 
       'https://huggingface.co/hfl/chinese-roberta-wwm-ext-large',
       'GPT-SoVITS/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large'
   ])
   
   # Download other model from hugging face
   subprocess.run(
       'git clone --filter=blob:none --no-checkout https://huggingface.co/lj1995/GPT-SoVITS.git model_folder && '
       'cd model_folder && '
       'git sparse-checkout init --cone && '
       'git sparse-checkout set chinese-hubert-base && '
       'git checkout main',
       shell=True, check=True)
   
   shutil.move("model_folder/chinese-hubert-base", "GPT-SoVITS/GPT_SoVITS/pretrained_models/chinese-hubert-base")
   shutil.rmtree('model_folder', onerror=handle_remove_readonly)

 elif os == "linux":
    subprocess.run([
       'git', 'clone', 'https://github.com/RVC-Boss/GPT-SoVITS.git'
   ])
    
    # add status to api file
    with open('GPT-SoVITS/api.py', 'a') as f: f.write('\n@app.get("/status")\nasync def get_status():\n    return JSONResponse(content={"status": "online"})\n')

    if is_gptsovits_env_installed("linux"):
       pass
    else:
     create_conda_env("linux")

    # Install requirments 
    shutil.move("GPT-SoVITS/requirements.txt", "requirements.txt")
    shutil.move("GPT-SoVITS/extra-req.txt", "extra-req.txt")

    subprocess.run([
    'bash', '-ilc',
    'source ~/miniconda3/etc/profile.d/conda.sh && '
    'conda activate GPTSoVits && '
    f'echo {wsl_paswd} | sudo -S apt update && '
    'sudo apt install -y build-essential cmake'
    ])

    subprocess.run(
    'source ~/miniconda3/etc/profile.d/conda.sh && conda activate GPTSoVits && pip install -r extra-req.txt --no-deps',
    shell=True, executable='/bin/bash', check=True
    )

    subprocess.run(
    'source ~/miniconda3/etc/profile.d/conda.sh && conda activate GPTSoVits && pip install -r requirements.txt',
    shell=True, executable='/bin/bash', check=True
    )

    shutil.move("requirements.txt", "GPT-SoVITS/requirements.txt")
    shutil.move("extra-req.txt", "GPT-SoVITS/extra-req.txt")

    # git clone pretrained model
    subprocess.run([
        'git', 'clone', 
        'https://huggingface.co/hfl/chinese-roberta-wwm-ext-large',
        'GPT-SoVITS/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large'
    ], check=True)

    # Download other model from hugging face using sparse checkout
    subprocess.run(
        'git clone --filter=blob:none --no-checkout https://huggingface.co/lj1995/GPT-SoVITS.git model_folder && '
        'cd model_folder && '
        'git sparse-checkout init --cone && '
        'git sparse-checkout set chinese-hubert-base && '
        'git checkout main',
        shell=True, check=True
    )

    shutil.move("model_folder/chinese-hubert-base", "GPT-SoVITS/GPT_SoVITS/pretrained_models/chinese-hubert-base")

    shutil.rmtree('model_folder', onerror=handle_remove_readonly)

if __name__ == "__main__":
    current_os = os.name

    wsl_command = "cd /mnt/c/Users/Driek/Documents/Python_scripts/Projects/GptSovits-installer python3 install_gpt_sovits.py"
    wsl_command_2 = "python3 /mnt/c/Users/Driek/Documents/Python_scripts/Projects/GptSovits-installer/exspet_Tos.py"

    if current_os == "nt":
        # Windows
        try:
            subprocess.run(['wsl', '-d', wsl_machine_name, '-u', wsl_user, 'bash', '-ilc', 'conda --version'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            install_conda("windows")

        install_gpt_sovits("windows")
    elif current_os == "posix":
        # Linux
        conda_available = subprocess.run( ['bash', '-i', '-c', 'source ~/miniconda3/etc/profile.d/conda.sh && conda --version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

        if not conda_available:
            install_conda("linux")

        install_gpt_sovits("linux")
