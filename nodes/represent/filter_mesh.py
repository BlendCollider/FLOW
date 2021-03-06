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
from bpy.props import BoolProperty, BoolVectorProperty, StringProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowMeshFilterUgen(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowMeshFilterUgen '''
    bl_idname = 'FlowMeshFilterUgen'
    bl_label = 'Mesh Filter'
    bl_icon = 'OUTLINER_OB_EMPTY'

    input_names = StringProperty(default='')
    objects_content = StringProperty(default='')
    has_objects = BoolProperty()

    def init(self, context):
        self.inputs.new('FlowSinkHoleSocket', "mesh in")
        self.outputs.new('FlowSinkHoleSocket', "filtered out")

    def process(self):
        # assume no state saving.
        self.input_names = ''
        self.objects_content = ''
        self.has_objects = False

        data = self.inputs[0].fget()
        if data and len(data) > 0:
            self.has_objects = True
            self.input_names = "|".join([str(i) for i in data['objects'].keys()])
            parts = []
            for idx, content in data['objects'].items():
                part = ('v' if 'verts' in content else '-')
                part += ('e' if 'edges' in content else '-')
                part += ('f' if 'faces' in content else '-')
                parts.append(part)
            self.objects_content = '|'.join(parts)

        self.outputs[0].fset(data)

    def draw_buttons(self, context, layout):

        icons = {
            '-': 'SNAP_VOLUME',
            'v': 'SNAP_VERTEX',  # 'VERTEXSEL',
            'e': 'SNAP_EDGE',  # 'EDGESEL',
            'f': 'SNAP_FACE',  # 'FACESEL'
        }

        if self.has_objects:
            col = layout.column()
            idxs = self.input_names.split('|')
            geometry = self.objects_content.split("|")
            for i, j in zip(idxs, geometry):
                # col.label('{idx} | {geom}'.format(idx=i, geom=j))
                row = col.row()
                left = row.split()
                left.label(i)

                right = row.split()
                for letter in j:
                    icon = icons.get(letter)
                    right.label(icon=icon, text=' ')


def register():
    bpy.utils.register_class(FlowMeshFilterUgen)


def unregister():
    bpy.utils.unregister_class(FlowMeshFilterUgen)
