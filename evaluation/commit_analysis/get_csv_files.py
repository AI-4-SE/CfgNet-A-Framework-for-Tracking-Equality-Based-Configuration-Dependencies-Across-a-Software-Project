import glob
import shutil

target = "conflict_inspection/all/"


def main():

    for repo in glob.glob("results/results/*"):
        for csv_file in glob.glob(repo + "/analysis/*"):
            name = csv_file.split("/")[-1]
            print(csv_file)
            shutil.copyfile(csv_file, target + name)
            break

    print(len(glob.glob("conflict_inspection/all_new/*")))

if __name__ == "__main__":
    main()