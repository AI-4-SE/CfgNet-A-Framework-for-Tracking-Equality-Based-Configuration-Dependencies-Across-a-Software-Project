# Evaluation

Important: This script assumes that it's run on our Slurm cluster if the hostname is `tesla` or starts with `brown`.

You can start the evaluation by running `run.sh`. It takes an optional
parameter which is a Git tree-ish (e.g.  `master`) that will be used for
CfgNet.  The result files will be in `results/`.  You can find the modified
repositories in `out/`.
