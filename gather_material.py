import pandas as pd

def analyze_materials(file_path):
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Load the 'Analysis' sheet
    df = pd.read_excel(xls, sheet_name='Analysis')
    
    # Extract unique materials from the 'Material' column
    unique_materials = df['Material'].unique()
    
    # Print the list of unique materials
    print("Materialien, die in der Tabelle vorkommen:")
    for material in unique_materials:
        print(f"- {material}")

# Specify the path to your Excel file
file_path = 'C:\Users\pasca\OneDrive - Hochschule Luzern\Programmieren\DT_Projekt_HS24\IFC_Auszug_MAT.xlsx'

# Call the function to analyze materials
analyze_materials(file_path)