#!/bin/bash

build_wheel() {
    git clone git@github.com:digital-bauhaus/CfgNet.git cfgnet
    cd cfgnet
    git checkout "$2"
    poetry build
    wheel="$(find dist -type f -iname "*.whl")"; \
    cp "$wheel" "$1"
    cd "$1"
    rm -rf cfgnet
}

rm -rf error output out
mkdir error
mkdir output

if ! command -v poetry &> /dev/null
then
    echo "Poetry could not be found"
    echo "Install instructions: https://python-poetry.org/docs/#installation"
    exit
fi

if [ "$#" -ne 1 ]; then
    branch=main
else
    branch="$1"
fi

if ! command -v cfgnet &> /dev/null
then
    build_wheel "$PWD" "$branch"
fi

if [ "$HOSTNAME" = "tesla" ]; then
    sbatch array.sbatch
else
    bash ./task.sh $(pwd)
fi