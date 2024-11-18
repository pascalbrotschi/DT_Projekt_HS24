class Exp_Holder():
    def __init__(self, branch, data):
        self.branch = branch
        self.data = data



#Class Data Holder Config

class Data_Holder():
    def __init__(self, category, prop_list, branch, source, folder):
        self.category = category
        self.prop_list = prop_list
        self.branch = branch
        self.source = source
        self.folder = folder

		
class Prop_Holder():
    def __init__(self, pset, prop, group):
        self.pset = pset
        self.prop = prop
        self.group = group

#Hilfsfunktion zum filtern

def filterConfig(_cat_name, _conf_lst):
    try:
        serach_res = [x for x in _conf_lst if x.branch == _cat_name][0]
    except:
        serach_res = None
        
    return serach_res