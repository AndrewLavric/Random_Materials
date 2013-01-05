bl_info={
    "name":"Random materials",
    "author":"Andrew Lavric",
    "version":(0,2),
    "blender":(2,6,5),
    "location":"View3D > Object Tools",
    "description":"Random materials",
    "category":"Object",
    "wiki_url":"https://github.com/AndrewLavric/Random_Materials.git",
    "tracker_url":"https://github.com/AndrewLavric/Random_Materials.git"}

import bpy
import random
import bmesh

bpy.types.Scene.rand_color_r=bpy.props.FloatProperty(name='R',description='Red',min=0,max=1,subtype='FACTOR')
bpy.types.Scene.rand_color_g=bpy.props.FloatProperty(name='G',description='Green',min=0,max=1,subtype='FACTOR')
bpy.types.Scene.rand_color_b=bpy.props.FloatProperty(name='B',description='Blue',min=0,max=1,subtype='FACTOR')
bpy.types.Scene.static_color_r=bpy.props.BoolProperty(name='Static',description='Static Red')
bpy.types.Scene.static_color_g=bpy.props.BoolProperty(name='Static',description='Static Green')
bpy.types.Scene.static_color_b=bpy.props.BoolProperty(name='Static',description='Static Blue')
bpy.types.Scene.invert_rand_color_r=bpy.props.BoolProperty(name='Invert',description='Invert Red')
bpy.types.Scene.invert_rand_color_g=bpy.props.BoolProperty(name='Invert',description='Invert Green')
bpy.types.Scene.invert_rand_color_b=bpy.props.BoolProperty(name='Invert',description='Invert Blue')
bpy.types.Scene.number_materials=bpy.props.IntProperty(name='Number',description='Numbers of materials (0 - unlimited)',min=0)
bpy.types.Scene.change_static_spec=bpy.props.BoolProperty(name='Specular',description='you can change specular property (default specular = 0)')
bpy.types.Scene.static_spec=bpy.props.FloatProperty(name='Specular',description='Static specular',min=0,max=1,subtype='FACTOR')

class random_mat_panel(bpy.types.Panel):
    bl_idname="matPanel"
    bl_label="Random Assigner Material"
    bl_space_type='VIEW_3D'
    bl_region_type='TOOLS'
    def draw(self,context):
        layout=self.layout
        layout.prop(bpy.context.scene,'number_materials')
        layout.prop(bpy.context.scene,'change_static_spec')
        if(bpy.context.scene.change_static_spec):
            layout.prop(bpy.context.scene,'static_spec')
        row=layout.row()
        row.prop(bpy.context.scene,'static_color_r')
        row.prop(bpy.context.scene,'invert_rand_color_r')
        layout.prop(bpy.context.scene,'rand_color_r')
        row=layout.row()
        row.prop(bpy.context.scene,'static_color_g')
        row.prop(bpy.context.scene,'invert_rand_color_g')
        layout.prop(bpy.context.scene,'rand_color_g')
        row=layout.row()
        row.prop(bpy.context.scene,'static_color_b')
        row.prop(bpy.context.scene,'invert_rand_color_b')
        layout.prop(bpy.context.scene,'rand_color_b')
        layout.operator("object.random_material")
        layout.operator("delete.all_materials")


def object_number_materials():
    red=bpy.context.scene.rand_color_r
    green=bpy.context.scene.rand_color_g
    blue=bpy.context.scene.rand_color_b
    number=bpy.context.scene.number_materials
    if(bpy.context.scene.change_static_spec):
        spec=bpy.context.scene.static_spec
    else:spec=0
    list=[]
    for mat in bpy.data.materials:
        if(mat.name[:3]=="mat"):
            list.append(mat)
        if(len(list)==number):
            break
    if(len(list)<number):
        while(len(list)<number):
            list.append(bpy.data.materials.new("mat"))
    for i in list:
        if(bpy.context.scene.static_color_r):
            i.diffuse_color.r=red
        else:
            i.diffuse_color.r=red+random.uniform(0,1-red)
        if(bpy.context.scene.invert_rand_color_r):
            i.diffuse_color.r=1-i.diffuse_color.r
        if(bpy.context.scene.static_color_g):
            i.diffuse_color.g=green
        else:
            i.diffuse_color.g=green+random.uniform(0,1-green)
        if(bpy.context.scene.invert_rand_color_g):
            i.diffuse_color.g=1-i.diffuse_color.g
        if(bpy.context.scene.static_color_b):
            i.diffuse_color.b=blue
        else:
            i.diffuse_color.b=blue+random.uniform(0,1-blue)
        if(bpy.context.scene.invert_rand_color_b):
            i.diffuse_color.b=1-i.diffuse_color.b
        i.specular_intensity=spec
    for obj in bpy.context.selected_objects:
        obj.active_material=list[random.randint(0,number-1)]

def object_random_materials():
    red=bpy.context.scene.rand_color_r
    green=bpy.context.scene.rand_color_g
    blue=bpy.context.scene.rand_color_b
    if(bpy.context.scene.change_static_spec):
        spec=bpy.context.scene.static_spec
    else:spec=0
    for i in bpy.context.selected_objects:
        if(not(i.active_material)):
            i.active_material=bpy.data.materials.new("mat")
        if(i.active_material.users>1):
            i.active_material=bpy.data.materials.new("mat")
        color=i.active_material.diffuse_color
        if(bpy.context.scene.static_color_r):
            color.r=red
        else:
            color.r=red+random.uniform(0,1-red)
        if(bpy.context.scene.invert_rand_color_r):
            color.r=1-color.r
        if(bpy.context.scene.static_color_g):
            color.g=green
        else:
            color.g=green+random.uniform(0,1-green)
        if(bpy.context.scene.invert_rand_color_g):
            color.g=1-color.g
        if(bpy.context.scene.static_color_b):
            color.b=blue
        else:
            color.b=blue+random.uniform(0,1-blue)
        if(bpy.context.scene.invert_rand_color_b):
            color.b=1-color.b
        i.active_material.specular_intensity=spec

def edit_random_materials():
    red=bpy.context.scene.rand_color_r
    green=bpy.context.scene.rand_color_g
    blue=bpy.context.scene.rand_color_b
    if(bpy.context.scene.change_static_spec):
        spec=bpy.context.scene.static_spec
    else:spec=0
    mesh=bpy.context.active_object.data
    bm=bmesh.from_edit_mesh(mesh)
    obj=bpy.context.active_object
    if(len(obj.material_slots)==0):
        obj.active_material=bpy.data.materials.new('mat')
    select_list=[]
    for face in bm.faces:
        if face.select:
            bpy.ops.object.material_slot_add()
            obj.active_material=bpy.data.materials.new('mat')
            bpy.ops.object.material_slot_assign()
            face.select=False
            select_list.append(face)
            color=bpy.context.active_object.active_material.diffuse_color
            if(bpy.context.scene.static_color_r):
                color.r=red
            else:
                color.r=red+random.uniform(0,1-red)
            if(bpy.context.scene.invert_rand_color_r):
                color.r=1-color.r
            if(bpy.context.scene.static_color_g):
                color.g=green
            else:
                color.g=green+random.uniform(0,1-green)
            if(bpy.context.scene.invert_rand_color_g):
                color.g=1-color.g
            if(bpy.context.scene.static_color_b):
                color.b=blue
            else:
                color.b=blue+random.uniform(0,1-blue)
            if(bpy.context.scene.invert_rand_color_b):
                color.b=1-color.b
            bpy.context.active_object.active_material.specular_intensity=spec
    for face in select_list:
        face.select=True

def edit_number_materials():
    mesh=bpy.context.active_object.data
    bm=bmesh.from_edit_mesh(mesh)
    if(len(bpy.context.active_object.material_slots)==0):
        bpy.context.active_object.active_material=bpy.data.materials.new('mat')
    select_list=[]
    list_mat=[]
    red=bpy.context.scene.rand_color_r
    green=bpy.context.scene.rand_color_g
    blue=bpy.context.scene.rand_color_b
    if(bpy.context.scene.change_static_spec):
        spec=bpy.context.scene.static_spec
    else:spec=0
    number=bpy.context.scene.number_materials
    while(len(list_mat)<number):
        list_mat.append(bpy.data.materials.new("mat"))
    for i in list_mat:
        if(bpy.context.scene.static_color_r):
            i.diffuse_color.r=red
        else:
            i.diffuse_color.r=red+random.uniform(0,1-red)
        if(bpy.context.scene.invert_rand_color_r):
            i.diffuse_color.r=1-i.diffuse_color.r
        if(bpy.context.scene.static_color_g):
            i.diffuse_color.g=green
        else:
            i.diffuse_color.g=green+random.uniform(0,1-green)
        if(bpy.context.scene.invert_rand_color_g):
            i.diffuse_color.g=1-i.diffuse_color.g
        if(bpy.context.scene.static_color_b):
            i.diffuse_color.b=blue
        else:
            i.diffuse_color.b=blue+random.uniform(0,1-blue)
        if(bpy.context.scene.invert_rand_color_b):
            i.diffuse_color.b=1-i.diffuse_color.b
        i.specular_intensity=spec
    for face in bm.faces:
        if face.select:
            bpy.ops.object.material_slot_add()
            bpy.context.active_object.active_material=list_mat[random.randint(0,number-1)]
            bpy.ops.object.material_slot_assign()
            face.select=False
            select_list.append(face)
    for face in select_list:
        face.select=True

class mat_assigner(bpy.types.Operator):
    bl_idname="object.random_material"
    bl_label="Assign random material"
    bl_description="Use this to assign a random colored material"
    bl_optin={'REGISTER','UNDO'}
    def execute(self,context):
        if(bpy.context.mode=='OBJECT'):
            if(bpy.context.scene.number_materials!=0):
                object_number_materials()
            else:
                object_random_materials()
        if(bpy.context.mode=='EDIT_MESH'):
            if(bpy.context.scene.number_materials!=0):
                edit_number_materials()
            else:
                edit_random_materials()
        return{'FINISHED'}


class delete_all_materials(bpy.types.Operator):
    bl_idname="delete.all_materials"
    bl_label="Delete all materials"
    bl_description="Delete all materials that have zero users"
    bl_optin={'REGISTER','UNDO'}
    def execute(self,context):
        for mat in bpy.data.materials:
            if(mat.users==0):
                bpy.data.materials.remove(mat)
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__": 
    register()
