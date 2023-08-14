import pandas as pd
from pandas_ods_reader import read_ods
import sys

path_base_svg = "C:/BlenderBIM/3bm/Arceringen ed/patterns_3bm.svg"
path_new_svg = "C:/BlenderBIM/3bm/Arceringen ed/patterns_3bm_new.svg"
path = "C:/BlenderBIM/3bm/Standards test folder/Library.ods"

def rgb_to_hex(r, g, b):
  return ("#" + '{:02X}' * 3).format(r, g, b)

#RGB TO HEX CUT PATTERNS
sheet_name = "cut_patterns"
library = read_ods(path, sheet_name)
for ind in library.index:
    rgb = library["BackgroundRGB"][ind]
    try:
        red = int(rgb.split(',')[0])
        green = int(rgb.split(',')[1])
        blue = int(rgb.split(',')[2])
        #print(rgb_to_hex(red, green, blue))
    except:
        #print("")
        test = "test"
    #cutpatterns.append([name, pattern])

#RGB TO HEX MATERIALS
sheet_name = "materials"
library = read_ods(path, sheet_name)
for ind in library.index:
    rgb = library["RGB"][ind]
    try:
        red = int(rgb.split(',')[0])
        green = int(rgb.split(',')[1])
        blue = int(rgb.split(',')[2])
        print(rgb_to_hex(red, green, blue))
    except:
        print("")
    #cutpatterns.append([name, pattern])

sys.exit()
sheet_name = "cut_patterns"
library = read_ods(path, sheet_name)

#CUTPATTERNS WITHOUT MATERIAL IMPACT
cutpatterns = []
for ind in library.index:
    name = library["Name"][ind]
    pattern = library["Name"][ind]
    #print(description)
    cutpatterns.append([name, pattern])


#def create_svg_pattern(name, suffix, scalefactor, background):


#<pattern id="metselwerk_50" width="3" height="3" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
#    <path style="fill: #cd7c61;" d="M 0 0 3 0 3 3 0 3" />
#    <line x1="1" y1="0" x2="1" y2="3" style="stroke:black; stroke-width:0.25" />
#    <line x1="1.5" y1="0" x2="1.5" y2="3" style="stroke:black; stroke-width:0.25" />
#</pattern>


sheet_name = "materials"
library = read_ods(path, sheet_name)
for ind in library.index:
    description = library["CombiArcering"][ind]
    #print(description)
    cutpatterns.append(description)


uniquepatterns = set(cutpatterns)

print(uniquepatterns)
print(len(uniquepatterns))