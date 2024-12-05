#import streamlit as st
#from rdkit import Chem
#from rdkit.Chem import Draw, AllChem
#import py3Dmol
import pandas as pd
import streamlit as st
import sys

import streamlit.components.v1 as components
import py3Dmol
from stmol import showmol
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem







# Cargar datos desde el archivo CSV
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Función para mostrar la molécula en 3D
def showm(smi, style='stick'):
    mol = Chem.MolFromSmiles(smi)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
    mblock = Chem.MolToMolBlock(mol)
    
    view = py3Dmol.view(width=400, height=400)
    view.addModel(mblock, 'mol')
    view.setStyle({style: {}})
    view.zoomTo()
    view.show()

# Configuración de la página
st.set_page_config(page_title="Visualización de Moléculas", layout="wide")

# Título y descripción
st.title("Visualización de Moléculas en 2D y 3D 🧪")
st.markdown("Busca moléculas usando SMILES desde el archivo `sideroforo_web.csv`. Visualiza su representación en **2D y 3D**.")

# Cargar datos
csv_file = "sideroforo_web.csv"  # Cambia este path según sea necesario
data = load_data(csv_file)

# Sidebar
st.sidebar.header("Opciones de Búsqueda")
smiles_input = st.sidebar.text_input("Escribe el SMILES para buscar:", "FCCC(=O)[O-]")
mol_name = st.sidebar.selectbox("Selecciona una molécula del dataset:", data['name'])

# Procesar la entrada del SMILES
selected_row = data[data['name'] == mol_name].iloc[0]
smiles_to_display = smiles_input if smiles_input else selected_row['SMILES']

try:
    # Mostrar estructura 2D
    mol = Chem.MolFromSmiles(smiles_to_display)
    Draw.MolToFile(mol, "mol_image.png")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Estructura 2D")
        st.image("mol_image.png")
    with c2:
        st.subheader("Estructura 3D")
        showm(smiles_to_display)
except Exception as e:
    st.error(f"Error procesando el SMILES: {e}")

# Mostrar la tabla de datos del CSV
st.subheader("Datos de Moléculas en el Dataset")
st.dataframe(data)
