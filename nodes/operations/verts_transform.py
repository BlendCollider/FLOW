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
from numpy import sin, cos

import bpy
from bpy.props import FloatProperty, EnumProperty

from core.mechanisms import updateSD
from node_tree import FlowCustomTreeNode


def do_transform(A, b, node):
    ops = node.operation
    axis = node.axis

    if ops == "ROTATE":
        t1, t2, t3 = b[0], b[1], b[2]

        if axis == 'X':
            x = [
                [1,        0,       0, 0],
                [0,  cos(t1), sin(t1), 0],
                [0, -sin(t1), cos(t1), 0],
                [0,        0,       0, 1]]
            T = np.array(x)

        elif axis == 'Y':
            y = [
                [cos(t2), 0, -sin(t2), 0],
                [0,       1,        0, 0],
                [sin(t2), 0,  cos(t2), 0],
                [0,       0,        0, 1]]
            T = np.array(y)

        elif axis == 'Z':
            z = [
                [cos(t3),  sin(t3), 0, 0],
                [-sin(t3), cos(t3), 0, 0],
                [0,        0,       1, 0],
                [0,        0,       0, 1]]
            T = np.array(z)

        return A.dot(T)

    if ops == "TRANSLATE":
        return A + b

    elif ops == "SCALE":
        tmat = [[b[0], 0,    0,    0],
                [0,    b[1], 0,    0],
                [0,    0,    b[2], 0],
                [0,    0,    0,    1]]

    # elif ops == "REFLECT":
    #     T = np.ident.tolist()
    # elif ops == "SHEER":
    #     T = np.ident.tolist()

    T = np.array(tmat)
    return A.dot(T)


class FlowVertsTransformUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowVertsTransformUgen
    ======================

    The point of this Node is to make chaining transforms possible.
    This makes explicit the order in which transforms are processed.
    '''

    bl_idname = 'FlowVertsTransformUgen'
    bl_label = 'Verts Transform'

    operation_types = [
        # internal,     ui,             "", enumidx
        ("ROTATE",      "Rotate",       "", 0),
        ("TRANSLATE",   "Translate",    "", 1),
        ("SCALE",       "Scale",        "", 2),
        # ("REFLECT",     "Reflect",      "", 3),
        # ("SHEER",       "Sheer",        "", 4),
    ]

    operation = EnumProperty(
        items=operation_types,
        name="Type of Transform",
        description="math.transform",
        default="TRANSLATE",
        update=updateSD)

    axis_options = [
        ("X", "X", "", 0),
        ("Y", "Y", "", 1),
        ("Z", "Z", "", 2)
    ]

    axis = EnumProperty(
        items=axis_options,
        name="Type of axis",
        description="offers plane to base transform on X|Y|Z",
        default="Z",
        update=updateSD)

    def init(self, context):
        self.inputs.new('ArraySocket', '4*n verts')
        self.inputs.new('VectorSocket', 'vector')
        self.outputs.new('ArraySocket', 'result')

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'operation', text='')
        if self.operation == 'ROTATE':
            row = col.row()
            row.prop(self, 'axis', expand=True)

    def process(self):
        A = self.inputs[0].fget()
        b = self.inputs[1].fget()
        if A.any and b.any:
            self.outputs[0].fset(do_transform(A, b, self))
        else:
            self.outputs[0].fset(A)


def register():
    bpy.utils.register_class(FlowVertsTransformUgen)


def unregister():
    bpy.utils.unregister_class(FlowVertsTransformUgen)