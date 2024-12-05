import streamlit as st
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Draw
import py3Dmol
from stmol import showmol

# Configuración de la barra lateral
#st.sidebar.image("img/gpx4.png", caption="Jesus Alvarado-Huayhuaz")
st.sidebar.title("Sideróforos")
st.sidebar.markdown("Visualización interactiva de moléculas desde un archivo CSV.")

# Cargar el archivo CSV
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error al cargar el archivo CSV: {e}")
        return None

# Leer el archivo CSV cargado por el usuario
csv_path = "sideroforo_web.csv"  # Nombre del archivo
data = load_data(csv_path)

if data is not None:
    # Validar columnas necesarias
    if "SMILES" not in data.columns or "Name" not in data.columns:
        st.error("El archivo CSV debe contener las columnas 'SMILES' y 'Name'.")
    else:
        st.title("Visualización de Sideróforos")
        
        # Mostrar un slider para seleccionar una molécula
        molecule_index = st.slider("Selecciona una molécula", 0, len(data) - 1, 0)
        selected_row = data.iloc[molecule_index]
        
        # Extraer datos de la molécula seleccionada
        smiles = selected_row["SMILES"]
        name = selected_row["Name"]
        
        # Mostrar información de la molécula
        st.subheader(f"Nombre: {name}")
        st.text(f"Código SMILES: {smiles}")
        
        # Generar la representación 2D de la molécula
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            Draw.MolToFile(mol, "molecule.png")
            st.image("molecule.png", caption="Representación 2D de la molécula")
        else:
            st.error("No se pudo generar la representación molecular a partir del código SMILES.")
        
        # Visualización en 3D
        st.subheader("Visualización en 3D")
        def show_3d(smi):
            mol = Chem.MolFromSmiles(smi)
            mol = Chem.AddHs(mol)
            Chem.AllChem.EmbedMolecule(mol)
            Chem.AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
            mblock = Chem.MolToMolBlock(mol)
            viewer = py3Dmol.view(width=500, height=400)
            viewer.addModel(mblock, "mol")
            viewer.setStyle({"stick": {}})
            viewer.zoomTo()
            showmol(viewer, height=400, width=500)

        show_3d(smiles)
else:
    st.warning("El archivo CSV no contiene datos válidos o no está cargado.")
