import ifcopenshell
# import bonsai.tool as tool
import re
import sys

def extract_step_id_from_profile(profile_str, pattern=r'[,|\(]#(\d+)'):
    """Extract the step ID from the profile string looking for ,# or (#."""
    match = re.search(pattern, profile_str)
    return int(match.group(1)) if match else None

model = ifcopenshell.open("C:/Users/mikev/Downloads/linktest2.ifc")

profile_name="UNP160"

profile = next((p for p in model.by_type('IfcArbitraryClosedProfileDef') if p.ProfileName == profile_name), None)
print("profile")
print(profile)

profile_curve_step_id = extract_step_id_from_profile(str(profile))
profile_curve = model.by_id(profile_curve_step_id)
print("profile_curve")
print(profile_curve)

print("profile_curve[1]")
print(profile_curve[1])

points_list_step_id = extract_step_id_from_profile(str(profile_curve))
print(points_list_step_id)

points_list = model.by_id(points_list_step_id)
print(points_list)
print(len(points_list[0]))

points_list = points_list[0]

point_list_new = []

for curve in profile_curve[1]:
    if len(curve[0]) == 2:
        point_list_new.append(points_list[curve[0][0]-1])
        point_list_new.append(points_list[curve[0][1]-1])
    if len(curve[0]) == 3:
        point_list_new.append(points_list[curve[0][0]-1])
        point_list_new.append(points_list[curve[0][1]-1])
        point_list_new.append(points_list[curve[0][2]-1])

#print(curve[0])
print(point_list_new)


#coord_list = points_list.CoordList
#print(f"Gevonden {len(coord_list)} punten in de coördinatenlijst.")


#for point in coord_list:
#    print(point)

sys.exit()
