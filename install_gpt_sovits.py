import subprocess
import os
import shutil
from config import wsl_machine_name, wsl_user, wsl_paswd
import stat

def is_gptsovits_env_installed():
    result = subprocess.run([
        "wsl",
        "-d", "Ubuntu-20.04",
        "-u", "andre",
        "bash",
        "-ilc",
        "conda env list"
    ], capture_output=True, text=True)

    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Extract environment name considering '*'
        if line.startswith("*"):
            name = line.split()[1]
        else:
            name = line.split()[0]

        if name == "GPTSoVits":
            return True
    return False

def handle_remove_readonly(func, path, exc):
    import errno
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        # Change the file to writable
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

# pull gpt sovits git
subprocess.run([
    'git', 'clone', 'https://github.com/RVC-Boss/GPT-SoVITS.git'
])

# add status to api file
with open('GPT-SoVITS/api.py', 'a') as f: f.write('\n@app.get("/status")\nasync def get_status():\n    return JSONResponse(content={"status": "online"})\n')

if is_gptsovits_env_installed():
    pass
else:
  # Create conda env
  subprocess.run([
      'wsl', '-d', wsl_machine_name, '-u', wsl_user,
      '/home/andre/miniconda3/bin/conda', 'create', '-n', 'GPTSoVits', 'python=3.10', '-y'
  ])

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