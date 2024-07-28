# PeptideMapper
 
Python script to map Peptides to the Location of the Peptide in the Master Protein.
Use this together with the MTS Mapper to find MTS sequences in proteomic data. The script can be used to convert DynaTMT processed data for MTS mapper processing. Might be usefull when looking at translation data.

**Input:**

Get input from DynaTMT.

Open Script and fill in the Working directory
```
wd = r'Put your Working directory here!'
filename = r'Put filename here e.g. "FileToMap.xlsx"
```

Run script and wait.

# FAQ
**1. Script crashes:**

   Check output of the script in terminal. 
   Check Requirements and install missing dependencies.
   If Issue persists create open Issue

   
**2. I have unmapped peptides**

 The Protein Database used by this script was taken from Uniprot and only contains Review Proteins.
 Ambigious, not annoated Proteins can therefore not be mapped. If needed you can download the Masterprotein sequence from Uniprot with less stringent filters and add them to the database. Please check the database file and fill in accordingly.

 
**3. Is it possible to map Peptides from other organisms?**

 In theory yes.
 Please download the Reference Proteome of choice from Uniprot and change the Script accordingly to use the different database excel file.
 ```
 Database = sys.path[0] + r'\Database\HomoSapiens_MasterProteinSequences.xlsx'
 ```
 Refer to the original Database file to ensure that all necessary information is downloaded from Uniprot.
