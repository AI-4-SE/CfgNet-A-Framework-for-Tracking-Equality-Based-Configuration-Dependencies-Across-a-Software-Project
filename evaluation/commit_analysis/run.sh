#!/bin/bash

rm -rf results error output
mkdir results
mkdir error
mkdir output

build_wheel() {
    if [ "$#" -ne 2 ]; then
        echo "Illegal number of parameters"
        echo "Usage:"
        echo -e "\t$0 PATH BRANCH"
    fi

    git clone git@github.com:digital-bauhaus/configuration-network.git cfgnet
    cd cfgnet
    git checkout "$2"
    poetry build
    wheel="$(find dist -type f -iname "*.whl")"; \
    cp "$wheel" "$1"
    cd "$1"
    rm -rf cfgnet
}

tables() {
    poetry run generate_tables.py
}

plots() {
    poetry add pandas
    poetry run ./plot_results.sh
}

if ! command -v poetry &> /dev/null
then
    echo "Poetry could not be found"
    echo "Install instructions: https://python-poetry.org/docs/#installation"
    exit
fi

if [ "$#" -ne 1 ]; then
    branch=master
else
    branch="$1"
fi

build_wheel $PWD "$branch"
sbatch array.sbatch