bl_info = {
    "name": "Batch FBX Exporter for Unity",
    "description": "Exports each object in the scene as an FBX file",
    "author": "Stellar Wolf Entertainment",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "File > Export > Batch > Unity FBX",
    "warning": "This addon is still in development and may not behave as expected.",
    "category": "Import-Export",
}

import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper

def move_to_origin(obj):
    original_location = obj.location.copy()
    obj.location = (0, 0, 0)
    return original_location

def move_back_to_original_location(obj, original_location):
    # Move the object back to its original location
    obj.location = original_location

def get_object_hierarchy(obj):
    # Recursive function to get the entire hierarchy of an object
    hierarchy = [obj]

    if obj.children:
        for child in obj.children:
            hierarchy.extend(get_object_hierarchy(child))

    return hierarchy

def batch_fbx_export_objects(directory_path):
    for scene in bpy.data.scenes:
        bpy.context.window.scene = scene

        for obj in bpy.data.objects:
            if obj.type == "MESH":
                object_hierarchy = get_object_hierarchy(obj)

                for obj_in_hierarchy in object_hierarchy:
                    obj_in_hierarchy.select_set(True)
                original_locations = [move_to_origin(obj_in_hierarchy) for obj_in_hierarchy in object_hierarchy]

                file_path = bpy.path.abspath(directory_path + obj.name + ".fbx")
                bpy.ops.export_scene.fbx(
                    filepath=file_path,
                    use_selection=True,
                    axis_forward='-Z',
                    axis_up='Y',
                    global_scale=1.0,
                    apply_unit_scale=True,
                    apply_scale_options='FBX_SCALE_ALL',
                    bake_space_transform=True,
                    object_types={'MESH'},
                    use_mesh_modifiers=True,
                    mesh_smooth_type='FACE',
                    use_mesh_edges=False,
                    use_tspace=True,
                    use_custom_props=False,
                    use_armature_deform_only=False,
                    bake_anim=False,
                    bake_anim_use_all_actions=False,
                    bake_anim_use_nla_strips=False,
                    bake_anim_use_all_bones=False,
                    path_mode='AUTO'
                )

                for obj_in_hierarchy, original_location in zip(object_hierarchy, original_locations):
                    move_back_to_original_location(obj_in_hierarchy, original_location)

                for obj_in_hierarchy in object_hierarchy:
                    obj_in_hierarchy.select_set(False)

class BatchFBXExportOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "object.batch_fbx_export"
    bl_label = "Batch FBX Export"
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = ".fbx"

    
    directory_path: StringProperty(
        name="Directory Path",
        description="Select the directory where the files will be saved",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        batch_fbx_export_objects(self.directory_path + "/" if self.directory_path else "")
        return {'FINISHED'}

def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(BatchFBXExportOperator.bl_idname)

def register():
    bpy.utils.register_class(BatchFBXExportOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(BatchFBXExportOperator)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
