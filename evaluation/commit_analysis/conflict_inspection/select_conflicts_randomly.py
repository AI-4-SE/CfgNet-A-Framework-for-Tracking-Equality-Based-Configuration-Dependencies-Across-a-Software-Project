import os
import glob
import pandas as pd

target_modified_option = os.path.abspath("final_modified_option")
target_all_conflicts =  os.path.abspath("finall_all_conflicts")

def select_conflicts_randomly(target, name, modified_option, df):
    if modified_option > 0 and modified_option <= 50:
        modified_option_df = df[df.conflict_type == 'ModifiedOptionConflict']
        modified_option_df.to_csv(os.path.join(target, name + ".csv"), index=False)

            

    if modified_option > 100:
        modified_option_df = df[df.conflict_type == 'ModifiedOptionConflict']
        modified_option_df = modified_option_df.sample(50)
        modified_option_df.to_csv(os.path.join(target, name + ".csv"), index=False)


def main():
    	

    for full_name in glob.glob("all/*"):
        #print("===========================")
        file_name = full_name.split("/")[-1]
        name = file_name.split(".")[0]

        if "conflicts_kubernetes.csv" in full_name:

            df = pd.read_csv(full_name)

            missing_artifact = df[df.conflict_type == 'MissingArtifactConflict'].shape[0]
            missing_option = df[df.conflict_type == 'MissingOptionConflict'].shape[0]
            multi_value = df[df.conflict_type == 'MultiValueConflict'].shape[0]
            modified_option = df[df.conflict_type == 'ModifiedOptionConflict'].shape[0] 
            total = len(df["conflict_type"])

            assert total == sum([missing_artifact, missing_option, multi_value, modified_option])
       
            print("Missing Artifact: ", missing_artifact)
            print("Missing Option: ", missing_option)
            print("Multi Value: ", multi_value)
            print("Modified Option: ", modified_option)
            print("Total Conflict: ", total)
            
        # Select conflicts
        #    select_conflicts_randomly(target_modified_option, name, modified_option, df)
        

        #   if df.shape[0] > 0 and df.shape[0]  <= 50:
        #        df.to_csv(os.path.join(target_all_conflicts, name + ".csv"), index=False)
        
        #    if df.shape[0] > 50:
        #        df = df.sample(50)
        #        df.to_csv(os.path.join(target_all_conflicts, name + ".csv"))



    print("Number of systems: ", len(glob.glob("all/*")))
    print("Final Modified Conlficts: ", len(glob.glob(os.path.join(target_modified_option, "*"))))
    print("Final All Conlficts: ", len(glob.glob(os.path.join(target_all_conflicts, "*"))))


if __name__ == "__main__":
    main()