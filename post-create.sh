#!/usr/bin/env bash
set -e

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install clang

sudo apt update
sudo apt install -y clang libclang-dev llvm-dev
