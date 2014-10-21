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

from random import random
import numpy as np

import bpy
from bpy.props import StringProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowDuplivertOne(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowDuplivertOne , with extras i hope'''
    bl_idname = 'FlowDuplivertOne'
    bl_label = 'Duplivert Ugen'
    bl_icon = 'OUTLINER_OB_EMPTY'

    name_parent = StringProperty(description="obj's verts are used to duplicate child")
    name_child = StringProperty(description="name of object to duplicate")

    def init(self, context):
        self.inputs.new("FlowArraySocket", "Rotations")

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop_search(self, 'name_parent', bpy.data, 'objects', text='parent')

        if self.name_child and self.name_parent:
            ob = bpy.data.objects[self.name_parent]
            layout.prop(ob, "dupli_type", expand=True)

            if ob.dupli_type == 'FRAMES':
                split = layout.split()

                col = split.column(align=True)
                col.prop(ob, "dupli_frames_start", text="Start")
                col.prop(ob, "dupli_frames_end", text="End")

                col = split.column(align=True)
                col.prop(ob, "dupli_frames_on", text="On")
                col.prop(ob, "dupli_frames_off", text="Off")

                layout.prop(ob, "use_dupli_frames_speed", text="Speed")

            elif ob.dupli_type == 'VERTS':
                layout.prop(ob, "use_dupli_vertices_rotation", text="Rotation")

            elif ob.dupli_type == 'FACES':
                row = layout.row()
                row.prop(ob, "use_dupli_faces_scale", text="Scale")
                sub = row.row()
                sub.active = ob.use_dupli_faces_scale
                sub.prop(ob, "dupli_faces_scale", text="Inherit Scale")

            elif ob.dupli_type == 'GROUP':
                layout.prop(ob, "dupli_group", text="Group")

        col.prop_search(self, 'name_child', bpy.data, 'objects', text='child')

    def process(self):
        objects = bpy.data.objects
        if self.name_parent and self.name_child:
            obj_parent = objects[self.name_parent]
            obj_child = objects[self.name_child]
            if not (obj_child.parent == obj_parent):
                obj_child.parent = obj_parent

            if obj_child.use_dupli_vertices_rotation:

                val = self.inputs['Rotations'].fget()
                if val.any():
                    verts = obj_parent.data.vertices
                    if not (len(val) == len(verts)):
                        # no fullrepeat atm.
                        print('sizes don\'t match')
                        print(len(val), len(verts))
                        return
                else:
                    return

                iterot = (v[:3] for v in val)

                ''' maybe use foreach.set here?..
                    temporary implementation
                '''

                for idx, v in enumerate(verts):
                    new_val = next(iterot, None)
                    if isinstance(new_val, np.ndarray):
                        v.normal = new_val
                    else:
                        break

                # race condition with bmesh node, this should be done last..
                # update is pointless I think..
                # obj_parent.data.update()


def register():
    bpy.utils.register_class(FlowDuplivertOne)


def unregister():
    bpy.utils.unregister_class(FlowDuplivertOne)