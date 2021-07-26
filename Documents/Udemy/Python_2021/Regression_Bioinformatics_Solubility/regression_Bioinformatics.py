import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Descriptors

st.set_option('deprecation.showPyplotGlobalUse', False)

# Helper Functions
def AromaticProportion(m):
    aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
    aa_count = []
    for i in aromatic_atoms:
        if i==True:
            aa_count.append(1)
    AromaticAtom = sum(aa_count)
    HeavyAtom = Descriptors.HeavyAtomCount(m)
    AR = AromaticAtom/HeavyAtom
    return AR

def generate(smiles, verbose=False):
    
    moldata= []
    for elem in smiles:
        mol=Chem.MolFromSmiles(elem)
        moldata.append(mol)

    baseData= np.arange(1,1)
    i=0
    for mol in moldata:

        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)

        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds,
                        desc_AromaticProportion])

        if(i==0):
            baseData=row
        else:
            baseData=np.vstack([baseData, row])
        i=i+1

    columnNames=["MolLogP","MolWt","NumRotatableBonds","AromaticProportion"]
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)

    return descriptors

st.write("""
         # Molecular Solubility Prediction Web App
         """)

expander_bar = st.beta_expander("About")
expander_bar.markdown("""
    * **Python libraries:** pandas, streamlit, numpy, pickle, PIL, matplotlib, rdkit
    * **Description:** This app predicts the **Sulubility values ** for an imput molecule!
    * **Data:** John S. Delaney. [ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** 2004, 44, 3, 1000-1005.
        ***
    * **To find a molecule of your interest use https://pubchem.ncbi.nlm.nih.gov/ and use SMILES notation**
""")

######################
# Input molecules (Side Panel)

st.sidebar.header('User Input Features')

## Read SMILES input
SMILES_input = "NCCCC\nCCC\nCN"

SMILES = st.sidebar.text_area("SMILES input", SMILES_input)
SMILES = "C\n" + SMILES #Adds C as a dummy, first item
SMILES = SMILES.split('\n')

st.header('Input SMILES')
SMILES[1:] # Skips the dummy first item

## Calculate molecular descriptors
st.header('Computed molecular descriptors')
X = generate(SMILES)
X[1:] # Skips the dummy first item

######################
# Pre-built model
# Reads in saved model
load_model = pickle.load(open('solubility_model.pkl', 'rb'))

# Apply model to make predictions
prediction = load_model.predict(X)
#prediction_proba = load_model.predict_proba(X)

st.header('Predicted LogS values')
prediction[1:] # Skips the dummy first item