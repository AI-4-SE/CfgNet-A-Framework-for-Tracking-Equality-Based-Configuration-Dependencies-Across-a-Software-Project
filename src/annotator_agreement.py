import pandas as pd
from sklearn.metrics import cohen_kappa_score

def main():
    df = pd.read_csv("../data/literature_study/initial_set.csv")
    df_revised = pd.read_csv("../data/literature_study/initial_set_revised.csv")

    relevance_annotator_1 = df["Annotator 1"].tolist()
    relevance_annotator_2 = df["Annotator 2"].tolist()

    relevance_annotator_1_revised = df_revised["Annotator 1"].tolist()
    relevance_annotator_2_revised = df_revised["Annotator 2"].tolist()

    agreement = cohen_kappa_score(relevance_annotator_1, relevance_annotator_2)
    agreement_revsied = cohen_kappa_score(relevance_annotator_1_revised, relevance_annotator_2_revised)

    print("Annotator Agreement with intial inclusion/exlcusion criteria: ", agreement)
    print("Annotator Agreement with revsied inclusion/exclusion criteria: ", agreement_revsied)


if __name__ == "__main__":
    main()