EVALUATION=out

if [[ $(hostname -s) = brown* ]]; then
    LOCALPATH=/tmp/$USER/analysis
    rm -rf "$LOCALPATH"
    mkdir "$LOCALPATH"
else
    LOCALPATH=.
    rm -rf "$LOCALPATH"/venv
fi

python3 -m venv $LOCALPATH/venv
source $LOCALPATH/venv/bin/activate

wheel="$(find $1 -type f -iname "*.whl")"

pip install $wheel

pip install gitpython joblib

cd "$LOCALPATH"

rm -rf "$EVALUATION"

python3 $1/evaluation.py

cp -r out/results/* $1/results

deactivate

if [[ $(hostname -s) = brown* ]]; then
    rm -rf "$LOCALPATH"
else
    rm "$wheel"
fi
