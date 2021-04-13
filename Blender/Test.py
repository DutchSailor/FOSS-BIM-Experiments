import bpy
import bmesh

 


def add_mesh(name, verts, faces, edges=None, col_name="Collection"):    
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(col_name) #Defineren/krijgen van de col
    
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)

 


verts = [( 2.0,  2.0,  0.0), 
         ( 2.0, -2.0,  0.0),
         (-1.5, -2.0,  0.0),
         (-16.0, -1.0,  3.0),
         (-2.0, -2.0,  0.0)]

 


vlength = len(verts)
result = list(range(vlength))   
faces = [result]

 


#import file system.
#edges nodig? Staan nu namelijk uit.

 


add_mesh("Coordinates", verts, faces)

 

#/////////////////////////// Extra toevoegen voor extrude element

 


me = bpy.context.object.data

 

bm = bmesh.new()
bm.from_mesh(me)

 

bmesh.ops.solidify(bm, geom=[x for x in bm.faces if x.select], thickness=0.3)

 

bm.to_mesh(me)
bm.free()
me.update()