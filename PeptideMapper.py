# Python script to map peptides to Position in Masterprotein
# Takes Excel and looks for Column "Master Protein Accessions" and " Annotated Sequence" and uses this information to map the Position
# If position cannot be mapped column is empty
# ToDo write a rudimentary UI 
# Written by Bizes (NHo) 2024. Coding was partially done with ChatGTP 3.5 assistance


import pandas as pd
import re
import sys
import warnings


# Main Mapping function
def find_positions(sequence, full_sequence):

    # Remove everything within brackets and the dot from both ends
    processed_sequence = re.sub(r'^\[.*?\]\.|\.?\[.*?\]$', '', sequence).upper()
    full_sequence_upper = full_sequence.upper()
    try:
        start_pos = full_sequence_upper.index(processed_sequence) + 1  # +1 for 1-based index
        end_pos = start_pos + len(processed_sequence) - 1
        return f"{start_pos}-{end_pos}"
    except ValueError:
        return ""  # Return an empty string if the sequence is not found

# Function to Split and Expand rows if there are multiple entries
# Takes a df and the Name of the Column which should be expanded
def split_and_expand(df, column):
    # Split the specified column by semicolon and create a new dataframe
    s = df[column].str.split('; ').explode()
    
    # After Expanding, copy the rest of the data from the original row
    df_expanded = df.loc[s.index].copy()
    df_expanded[column] = s.values
    
    return df_expanded
    
    
# Main Function body
if __name__ == '__main__':    
    ###########################################################
    wd = r'Put your Working directory here!'
    filename = r'Put filename here e.g. "FileToMap.xlsx"'
    ##########################################################  
    # Change only if necessary. See FAQ
    Database = sys.path[0] + r'\Database\HomoSapiens_MasterProteinSequences.xlsx'
    ##########################################################   
    print('###############################################################')
    print("Reading: " + filename)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
        df = pd.read_excel(f'{wd}/{filename}', engine='openpyxl')
        # Read database 
        MasterProteins = pd.read_excel(Database)

    print ("File successfully loaded")


    # Split up the Master Protein Accesion Column. This is necessary since some peptides
    # are mapped to multiple proteins.
    # Check for yourself if you need to filter this out! Maybe add annotation in excel if it is unique
    PeptideFiles = split_and_expand(df, 'Master Protein Accessions')


    print("Begin Peptide Mapping. Please wait, this process can take some time...")
    # Map sequence with a lambda function
    # Leavs row empty if peptide cannot be mapped
    PeptideFiles['Position in MasterProtein'] = PeptideFiles.apply(
        lambda row: f"{row['Master Protein Accessions']} [{find_positions(row['Annotated Sequence'], MasterProteins.loc[MasterProteins['Entry'] == row['Master Protein Accessions'], 'Sequence'].values[0])}]" 
        if not MasterProteins.loc[MasterProteins['Entry'] == row['Master Protein Accessions'], 'Sequence'].empty else "",
        axis=1
    )
    NumUnmapedPeptides = (PeptideFiles['Position in MasterProtein'].values == '').sum()
    
    # Write the result to an excel
    OutputName = filename.strip('.xlsx') + '_MTSMapped.xlsx'
    PeptideFiles.to_excel(f'{wd}/{OutputName}', index=False)
    print("Sequence mapping successful. File saved as: " + OutputName)
    print(str(NumUnmapedPeptides) +' Peptides could not be mapped. Check manually and refer to FAQ on Github for questions')
    print('###############################################################')

            
        
        
        