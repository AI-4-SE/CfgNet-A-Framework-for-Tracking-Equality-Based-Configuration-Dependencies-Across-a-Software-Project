import os
import glob
import pandas as pd

target = os.path.abspath("final")

def select_conflicts_randomly(target, name, modified_option, df):
    if modified_option > 0 and modified_option <= 100:
        modified_option_df = df[df.conflict_type == 'ModifiedOptionConflict']
        modified_option_df.to_csv(os.path.join(target, name + ".csv"), index=False)
            

    if modified_option > 100:
        modified_option_df = df[df.conflict_type == 'ModifiedOptionConflict']
        modified_option_df = modified_option_df.sample(100)
        modified_option_df.to_csv(os.path.join(target, name + ".csv"), index=False)

def main():
    	

    for full_name in glob.glob("all/*"):
        #print("===========================")
        file_name = full_name.split("\\")[-1]
        name = file_name.split(".")[0]
        #print("Name: ", name)

        df = pd.read_csv(full_name)

        missing_artifact = df[df.conflict_type == 'MissingArtifactConflict'].shape[0]
        missing_option = df[df.conflict_type == 'MissingOptionConflict'].shape[0]
        multi_value = df[df.conflict_type == 'MultiValueConflict'].shape[0]
        modified_option = df[df.conflict_type == 'ModifiedOptionConflict'].shape[0] 
        total = len(df["conflict_type"])

        assert total == sum([missing_artifact, missing_option, multi_value, modified_option])
       
        #print("Missing Artifact: ", missing_artifact)
        #print("Missing Option: ", missing_option)
        #print("Multi Value: ", multi_value)
        #print("Modified Option: ", modified_option)
        #print("Total Conflict: ", total)
        
        # Select conflicts
        # select_conflicts_randomly(target, name, modified_option, df)

    print("Number of systems: ", len(glob.glob("all/*")))
    print("Final Systems: ", len(glob.glob(os.path.join(target, "*"))))



if __name__ == "__main__":
    main()