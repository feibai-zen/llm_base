cd /mnt/workspace/code/bk
bash Miniconda3-latest-Linux-x86_64.sh

PATH="/root/miniconda3/bin:$PATH"
source ~/.bashrc

conda create -n llm_base python=3.13.12
conda activate llm_base


cd /mnt/workspace/code/llm_base
sudo apt update
sudo apt install graphviz libgraphviz-dev pkg-config

pip install --upgrade pip
pip install -r requirements.txt