import pandas as pd
from sklearn.metrics import cohen_kappa_score

def create_snowballing_sample():
    df = pd.read_csv("../data/literature_study/snowballing.csv")
    
    df_relevant = df[df["Annotator 1"] == "relevant"]
    df_not_relevant = df[df["Annotator 1"] == "not-relevant"]
    df_not_found = df[df["Annotator 1"] == "not found"]
    df_not_accessible= df[df["Annotator 1"] == "not accessible"]

    assert sum([len(df_not_relevant), len(df_not_found), len(df_not_accessible), len(df_relevant)]) == 943
    
    print("Length relevant: ", len(df_relevant)) # 20% von 82 => 16
    print("Length not-relevant: ", len(df_not_relevant)) # 20% von 861 = 172

    df_relevant_sample = df_relevant.sample(41)
    df_not_relevant_sample = df_not_relevant.sample(143)

    df_snowballing_sample = pd.concat([df_relevant_sample, df_not_relevant_sample])

    df_snowballing_sample.to_csv("../data/literature_study/snowballing_sample.csv", index=False)


def calculate_annotator_agreement_initial_set():
    df = pd.read_csv("../data/literature_study/initial_set.csv")
    df_revised = pd.read_csv("../data/literature_study/initial_set_revised.csv")

    relevance_annotator_1 = df["Annotator 1"].tolist()
    relevance_annotator_2 = df["Annotator 2"].tolist()

    relevance_annotator_1_revised = df_revised["Annotator 1"].tolist()
    relevance_annotator_2_revised = df_revised["Annotator 2"].tolist()

    agreement = cohen_kappa_score(relevance_annotator_1, relevance_annotator_2)
    agreement_revised = cohen_kappa_score(relevance_annotator_1_revised, relevance_annotator_2_revised)

    print("Annotator Agreement with initial inclusion/exclusion criteria: ", agreement)
    print("Annotator Agreement with revised inclusion/exclusion criteria: ", agreement_revised)


def calculate_annotator_agreement_snowballing_sample():
    df = pd.read_csv("../data/literature_study/snowballing_sample.csv")

    relevance_annotator_1 = df["Annotator 1"].tolist()
    relevance_annotator_2 = df["Annotator 2"].tolist()

    agreement = cohen_kappa_score(relevance_annotator_1, relevance_annotator_2)

    print("Annotator Agreement for snowballing sample : ", agreement)


def create_final_set():
    df = pd.read_csv("../data/literature_study/snowballing.csv")
    df_final = df[df["Annotator 1"] == "relevant"]
    df_final.to_csv("../data/literature_study/final_set.csv", index=False)


if __name__ == "__main__":
    #calculate_annotator_agreement_initial_set()  
    #create_snowballing_sample()
    #create_final_set()
    calculate_annotator_agreement_snowballing_sample()
    #pass