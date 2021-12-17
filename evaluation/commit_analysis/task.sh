#!/bin/bash

# This script is called with two parameters. The first one is the job ID which
# is passed to the python script. The second one is the current folder so we
# know where we have to copy the results.

PROJECTNAME=cfgnet
LOCALPATH=/tmp/$USER/$PROJECTNAME/$1

# ----------------------------------------------------------------------------
# Prepare file system
# ----------------------------------------------------------------------------
# We create the folder structure the node where the job runs to save some
# network bandwidth.

# Clean up leftovers from previous failed runs
rm -rf $LOCALPATH/

# Create results folder
mkdir -p $LOCALPATH

# ----------------------------------------------------------------------------
# Prepare environment
# ----------------------------------------------------------------------------

# Create and source virtual environment
python3 -m venv $LOCALPATH/venv
source $LOCALPATH/venv/bin/activate

# Install dependencies
pip install gitpython joblib

# Install CfgNet
wheel="$(find $2 -type f -iname "*.whl")"; \
pip install $wheel

cd $LOCALPATH

# Get evaluation script
cp $2/evaluation.py $LOCALPATH

# ----------------------------------------------------------------------------
# Run evaluation
# ----------------------------------------------------------------------------

python3 evaluation.py $1

# ----------------------------------------------------------------------------
# Copy results
# ----------------------------------------------------------------------------

cp -r $LOCALPATH/out/results/* $2/results/

# ----------------------------------------------------------------------------
# Clean up
# ----------------------------------------------------------------------------

deactivate
rm -rf $LOCALPATH