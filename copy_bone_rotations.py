# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
import bpy
import mathutils

bl_info = {
    "name": "Copy Bone Rotations",
    "author": "dskjal",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "Properties Shelf",
    "description": "Copy and paste bone rotations.",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"
}

data_src = []

def is_valid_context():
    return bpy.context.active_object.mode ==  'POSE' and len(bpy.context.selected_pose_bones) > 0
    
def sort_order(bones):
    parents = [b.parent.name if b.parent != None else '' for b in bones]
    child = None

    # find child
    for b in bones:
        if not b.name in parents:
            child = b
            break
        
    # sort order
    sort = child
    sorted = []
    while sort in bones:
        sorted.append(sort)
        sort = sort.parent
    
    return sorted
    
class CopyButton(bpy.types.Operator):
    bl_idname = 'dskjal.copybonerotations'
    bl_label = 'Copy'
    
    @classmethod
    def poll(self, context):
        return is_valid_context()
    
    def execute(self, context):
        sorted = sort_order(bpy.context.selected_pose_bones)
        global data_src
        data_src = []
        for b in sorted:
            data_src.append(b.rotation_quaternion)
        
        return {'FINISHED'}
    
class PasteButton(bpy.types.Operator):
    bl_idname = 'dskjal.pastebonerotations'
    bl_label = 'Paste'
    
    @classmethod
    def poll(self, context):
        return is_valid_context()
    
    def execute(self, context):
        sorted = sort_order(bpy.context.selected_pose_bones)
        global data_src
        
        for i in range(min(len(data_src), len(sorted))):
            sorted[i].rotation_quaternion = data_src[i]
        
        return {'FINISHED'}
    
class UI(bpy.types.Panel):
    bl_label = 'Copy Bone Rotations'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        self.layout.operator('dskjal.copybonerotations')
        self.layout.operator('dskjal.pastebonerotations')
        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()