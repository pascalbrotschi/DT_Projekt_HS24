import pandas as pd
import os
import Helpers.Data_Helpers as hlp

#Globale Variablen - Listen

conf_lst = []

#Generate Filter Form

def read_source_data():

    #Alle Grundlagen einlesen > IFC + Excel-Elementplan

    print("Start: Starte Grunddatein einlesen...")

    source_folder = input("Pfad zum Basisordner eingeben >>> ")
    xls_file_name = "Elementplan.xlsx"
    xls_file = os.path.join(source_folder, xls_file_name)

    check_file = os.path.isfile(xls_file)

    #print(check_file)

    if(check_file):

        s_data_category = pd.read_excel(xls_file, "Objektkatalog")
        s_data_attributes = pd.read_excel(xls_file, "Attributsliste")

        #Daten aus dem Elementplan auslesen und strukturiert speichern

        col_count = len(s_data_category.columns)

        for index, row in s_data_category.iterrows():  

            if col_count > 3:  
        
                for gr in range(3,col_count):
                    attr_group_conf = s_data_category.iloc[index,gr]
                    
                    if(str(attr_group_conf).lower() == "x"):
                        current_attr_in_group = s_data_attributes[s_data_attributes["Gruppe"] == s_data_category.columns[gr]]
                        print(current_attr_in_group)               
                        
                        prop_lst = []

                        for _i, _r in current_attr_in_group.iterrows():

                            p_h = hlp.Prop_Holder(_r["Pset"], _r["Property"], _r["Gruppe"])
                            prop_lst.append(p_h)            

                        _target_obj = hlp.filterConfig(row["Branch"], conf_lst)

                        if _target_obj != None:

                            print("Adding to Configuration: ")
                            print("Klasse: " + row["IfcClass"])

                            _target_obj.prop_list.extend(prop_lst)

                        else:
                            print("Creating Configuration: ")
                            print("Klasse: " + row["IfcClass"])    

                            d_h = hlp.Data_Holder(row["IfcClass"], prop_lst, row["Branch"], row["Quelle"], source_folder)
                            conf_lst.append(d_h)

                        print("Finished Creating Configuration")

        return (conf_lst, source_folder)

print(conf_lst)