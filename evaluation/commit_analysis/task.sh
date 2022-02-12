EVALUATION=results

LOCALPATH=/tmp/$USER/analysis/$1

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

cp -r $LOCALPATH/out/* $2/"$EVALUATION"

deactivate
rm -rf "$LOCALPATH"
