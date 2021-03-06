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

import numpy as np

import bpy
from bpy.props import EnumProperty, IntProperty, FloatProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


def make_geometry(node):
    print(node.num_verts, node.distance)
    return {
        0: {
            'verts': np.array([])
        },
    }


class FlowLinesNode(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowLinesNode '''
    bl_idname = 'FlowLinesNode'
    bl_label = 'Lines'
    bl_icon = 'OUTLINER_OB_EMPTY'

    num_verts = IntProperty(
        name='num_verts',
        min=2, step=1, default=2,
        update=updateSD)

    distance = FloatProperty(step=0.2, name="distance", default=0.4)
    axis = EnumProperty

    def init(self, context):
        self.inputs.new("FlowScalarSocket", "num_verts").prop_name = "num_verts"
        self.inputs.new("FlowScalarSocket", "distance").prop_name = "distance"
        self.outputs.new('FlowGeometrySocket', "send")

    def draw_buttons(self, context, layout):
        pass

    def process(self):
        gref = dict(objects=make_geometry(self))
        self.outputs[0].fset(gref)


def register():
    bpy.utils.register_class(FlowLinesNode)


def unregister():
    bpy.utils.unregister_class(FlowLinesNode)
