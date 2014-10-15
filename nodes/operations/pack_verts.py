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
from bpy.props import BoolProperty, BoolVectorProperty, StringProperty

from core.mechanisms import updateSD
from node_tree import FlowCustomTreeNode


def add_repeat_last(c, diffsize):
    if len(c) == 0:
        return np.zeros((diffsize))
    c2 = np.array([c[-1]]).repeat(diffsize)
    return np.concatenate((c, c2), 0)


def combine(x, y, z, w):
    if x.any() or y.any() or z.any() or w.any():
        m = [(len(c) if c.any() else 0) for c in (x, y, z, w)]
        x_len, y_len, z_len, w_len = m
        longest = max(m)

        if not (x_len == longest):
            x = add_repeat_last(x, (longest - x_len))
        if not (y_len == longest):
            y = add_repeat_last(y, (longest - y_len))
        if not (z_len == longest):
            z = add_repeat_last(z, (longest - z_len))
        if not (w_len == longest):
            # should all be 1 ?
            w = add_repeat_last(w, (longest - w_len))

        return np.vstack((x, y, z, w)).T
    else:
        return np.array([])


class FlowPackVertsUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    Flow Pack Mesh

    Packs np.arrays of X Y and Z values to a single verts object.
    Inserts repeat 0 arrays when socket is empty.
    '''

    bl_idname = 'FlowPackVertsUgen'
    bl_label = 'Pack Verts'

    def init(self, context):
        self.inputs.new('ArraySocket', "x")
        self.inputs.new('ArraySocket', "y")
        self.inputs.new('ArraySocket', "z")
        self.inputs.new('ArraySocket', "w")
        self.outputs.new('ArraySocket', "4*n")

    def process(self):
        x = self.inputs[0].fget()
        y = self.inputs[1].fget()
        z = self.inputs[2].fget()
        w = self.inputs[3].fget()
        data = combine(x, y, z, w)
        self.outputs[0].fset(data)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(FlowPackVertsUgen)


def unregister():
    bpy.utils.unregister_class(FlowPackVertsUgen)
