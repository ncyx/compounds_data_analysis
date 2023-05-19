import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from IPython.display import display
from matplotlib.ticker import MaxNLocator
from matplotlib import ticker
import math
from matplotlib.pyplot import cm
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import AllChem
from rdkit.Chem import rdFMCS
from rdkit.Chem.Draw import rdDepictor
pd.set_option('display.max_colwidth', None)

screening_comps = pd.read_csv('/filename', sep=';')
screening_comps = screening_comps.drop(index=(83))

def search_and_analysis_comp(dataframe):
    '''
    code for automated calculation on the compound and its visualization
    '''
    
    comp_identified = input('4 digits of the compound(s) of interest (sep by space): ')
    conc_condition = input('should concentration be calculated? y/n: ')
    comp_identified_list = comp_identified.split()
    smiles_list = []
    
    for i in range(len(comp_identified_list)):
        comp_of_interest = dataframe[dataframe['ID'].str.contains(comp_identified_list[i])]
        
        if len(comp_of_interest) == 0:
            raise Exception("No matches found!")

        if len(comp_of_interest) != 1:
            for j in comp_of_interest['ID']:
                if j[len(j)-4:] == comp_identified_list[i]:
                    comp_of_interest = comp_of_interest[comp_of_interest['ID'] == j]

        MW_comp = float(dataframe['MW'][comp_of_interest.index])
        mass_comp = float(dataframe['Amount_mg'][comp_of_interest.index])
        amount_comp = float(mass_comp/MW_comp)
        concentration_comp = (amount_comp / 100e-6)
        if conc_condition == 'y':
            print('compound',comp_identified_list[i], 'concentration: ', concentration_comp, 'mM')
            
        smiles_comp = dataframe['Smile'][comp_of_interest.index].to_string()
        IPythonConsole.drawOptions.addAtomIndices = False
        IPythonConsole.molSize = 400,400
        smiles_comp_corr = smiles_comp[5:]
        smiles_chem_mol = Chem.MolFromSmiles(smiles_comp_corr)
        smiles_list.append(smiles_chem_mol)
    
    display(Draw.MolsToGridImage((smiles_list[0],smiles_list[1]), subImgSize=(500,500)))
    
    return comp_of_interest, smiles_list
dataframes,smiles = search_and_analysis_comp(screening_comps)

def view_difference(mol1, mol2):
    '''
    took and adapted from RDKit cookbook
    '''
    rdDepictor.SetPreferCoordGen(True)
    IPythonConsole.drawOptions.minFontSize=20
    
    mcs = rdFMCS.FindMCS([mol1,mol2])
    mcs_mol = Chem.MolFromSmarts(mcs.smartsString)
    match1 = mol1.GetSubstructMatch(mcs_mol)
    target_atm1 = []
    for atom in mol1.GetAtoms():
        if atom.GetIdx() not in match1:
            target_atm1.append(atom.GetIdx())
            match2 = mol2.GetSubstructMatch(mcs_mol)
            
    target_atm2 = []
    for atom in mol2.GetAtoms():
        if atom.GetIdx() not in match2:
            target_atm2.append(atom.GetIdx())
    
    display(Draw.MolsToGridImage([mol1, mol2],subImgSize=(500,500),
                                 highlightAtomLists=[target_atm1, target_atm2]))
    
view_difference(smiles[0], smiles[1])
