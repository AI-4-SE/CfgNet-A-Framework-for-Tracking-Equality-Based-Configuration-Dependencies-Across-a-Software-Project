EVALUATION=out

# if [[ $(hostname -s) = brown* ]]; then
LOCALPATH=/tmp/$USER/analysis/$1
    # rm -rf "$LOCALPATH"
    # mkdir "$LOCALPATH"
# else
    # LOCALPATH=.
    # rm -rf "$LOCALPATH"/venv
# fi

python3 -m venv $LOCALPATH/venv
source $LOCALPATH/venv/bin/activate

wheel="$(find $2 -type f -iname "*.whl")"

pip install $wheel

pip install gitpython joblib

cd "$LOCALPATH"

rm -rf "$EVALUATION"

echo "======================="
echo "Start commit history analysis!"

cp $2/evaluation.py .
python3 evaluation.py $1

echo "======================="
echo "Commit History Analysis done!"

# cp -r out/results/* $2/results
cp -r $LOCALPATH/out/* $2/results/

deactivate
# if [[ $(hostname -s) = brown* ]]; then
    rm -rf "$LOCALPATH"
# else
#     rm "$wheel"
# fi
