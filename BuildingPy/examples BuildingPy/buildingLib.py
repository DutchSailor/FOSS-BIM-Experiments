from construction.panel import *
from construction.beam import *
from construction.profile import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import nameToProfile
from construction.annotation import *

project = BuildingPy("Library Profiles", "0")

# Export all steelprofiles to Speckle
lst = [
    profile_name[0]["synonyms"][0]
    for item in jsondata
    for profile_name in item.values()
]

test = nameToProfile("HEA200")

# sys.exit()
# 3D Frames
x = 0
y = 0
spacing = 1000
spacing_vert = 1500
height = 2000
count = 0
shape = "HEA"
type = "HEA"
# Mat = Material.byNameColor("Steel", Color().RGB([237, 237, 237]))

Beam.by_startpoint_endpoint(Point(0,0,0),Point(0,0,3000),"HEA300", "HEA300 van Jan", BaseSteel).write(project)
Beam.by_startpoint_endpoint_rect()
project.to_speckle("4b550fb575")

sys.exit()

for profile_name in lst:
    try:
        Mat = BaseSteel
        shape = profile_name[:3]
        #fram = Beam.by_startpoint_endpoint(Point(x, y, 0), Point(
        #    x, y, height), profile_name, profile_name, Mat).write(project)
        #ColumnTag.by_beam(fram).write(project)
        x = x + spacing
        if type == shape:
            y = y
        else:
            x = 0
            y = y + spacing_vert
            type = shape
    except:
        pass
    break

