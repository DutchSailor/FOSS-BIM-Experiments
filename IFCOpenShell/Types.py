import pandas as pd
from pandas_ods_reader import read_ods

path = "C:/BlenderBIM/3bm/Standards test folder/Library.ods"
sheet_name = "walls_single_layer"
library = read_ods(path, sheet_name)

for ind in library.index:
    description = library["Description"][ind]
    #print(description)

sheet_name = "profiles_rect"
library_rectprofile = read_ods(path, sheet_name)

for ind in library_rectprofile.index:
    profile_name = library_rectprofile["Name"][ind]
    profile_width = float(library_rectprofile["Width"][ind])
    profile_height = float(library_rectprofile["Height"][ind])
    profile_material = library_rectprofile["Material"][ind]
    make_column = library_rectprofile["MakeIfcColumnType"][ind]
    make_beam = library_rectprofile["MakeIfcBeamType"][ind]
    print(make_column)