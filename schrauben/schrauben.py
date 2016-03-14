# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2015 - Bernd Hahnebach <bernd@bimstatik.org>            *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

"""
Script for generation of bolts
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Elements as AllplanElements
import NemAll_Python_Utility as AllplanUtil
import GeometryValidate as GeometryValidate


print('###############################################################')
print('###############################################################')
print('BEGINN')
print('###############################################################')

print('Load schrauben.py')


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """

    element = Box(doc)

    return element.create(build_ele)


class Box():
    """
    Definition of class Box
    """

    def __init__(self, doc):
        """
        Initialisation of class Box

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.reinf_ele_list = None
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements, handles and reinforcement.
        """

        self.add_complete_bolt(build_ele)

        return (self.model_ele_list, self.handle_list, self.reinf_ele_list)


    def add_complete_bolt(self, build_ele):
        """
        Add the  complete bolt as BRep3D

        Args:
            build_ele:  the building element.
        """

        #----------------- get the input values and check if they are valid
        bolt_to_create = build_ele.sbs_screw.value
        bolt_color = build_ele.sbs_color.value
        bolt_klemmlaenge = build_ele.sbs_length.value  # thickness of the bolted elements
        print(bolt_to_create)
        print(bolts_sbs_data[bolt_to_create])
        if bolt_to_create not in bolts_sbs_data:
            print('Error: bolt_to_create not found!')
            return
        if not bolt_klemmlaenge:
            bolt_klemmlaenge = 3 * bolts_sbs_data[bolt_to_create]['nut_thickness']
        bolt_shank_lenght = bolt_klemmlaenge + 2 * bolts_sbs_data[bolt_to_create]['washer_thickness'] + 1.5 * bolts_sbs_data[bolt_to_create]['nut_thickness']

        #----------------- screw
        screw_solid = make_screw_solid(bolt_to_create, bolt_shank_lenght)
        #print(screw_solid)
        #print(type(screw_solid))

        #----------------- nut
        nut_solid = make_nut_solid(bolt_to_create)
        nut_trans = bolt_shank_lenght - 0.5 * bolts_sbs_data[bolt_to_create]['nut_thickness']
        translation = AllplanGeo.Matrix3D()
        translation.Translate(AllplanGeo.Vector3D(0, 0, -nut_trans))
        nut_solid = AllplanGeo.Transform(nut_solid, translation)

        #----------------- washers
        washer_solid = make_washer_solid(bolt_to_create)

        washer1_trans = nut_trans - bolts_sbs_data[bolt_to_create]['nut_thickness']
        translation = AllplanGeo.Matrix3D()
        translation.Translate(AllplanGeo.Vector3D(0, 0, -washer1_trans))
        washer1_solid = AllplanGeo.Transform(washer_solid, translation)

        washer2_trans = bolts_sbs_data[bolt_to_create]['washer_thickness']
        translation = AllplanGeo.Matrix3D()
        translation.Translate(AllplanGeo.Vector3D(0, 0, -washer2_trans))
        washer2_solid = AllplanGeo.Transform(washer_solid, translation)

        #----------------- CommonProperties
        com_prop = AllplanElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = bolt_color

        #------------------ draw solids
        self.model_ele_list.append(AllplanElements.ModelElement3D(com_prop, screw_solid))
        self.model_ele_list.append(AllplanElements.ModelElement3D(com_prop, nut_solid))
        self.model_ele_list.append(AllplanElements.ModelElement3D(com_prop, washer1_solid))
        self.model_ele_list.append(AllplanElements.ModelElement3D(com_prop, washer2_solid))
 

# screw
def make_screw_solid(bolt_to_create, bolt_shank_lenght):
    print('We gone build a screw: ', bolt_to_create)
    screw_diameter = bolts_sbs_data[bolt_to_create]['screw_diameter']
    head_width = bolts_sbs_data[bolt_to_create]['head_width']
    head_thickness = bolts_sbs_data[bolt_to_create]['head_thickness']

    #----------------- bolt_head
    bolt_head = make_hexagon_solid(head_width, head_thickness)

    #----------------- bolt_shank
    origin_bolt_shank = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, -bolt_shank_lenght),
                                                    AllplanGeo.Vector3D(0, 1, 0),
                                                    AllplanGeo.Vector3D(0, 0, 1))
    bolt_shank = AllplanGeo.BRep3D.CreateCylinder(origin_bolt_shank, 0.5 * screw_diameter,  bolt_shank_lenght)

    #------------------ union of bolt_head and bolt_shank
    err, screw = AllplanGeo.MakeUnion(bolt_head, bolt_shank)
    if GeometryValidate.polyhedron(err) and screw.IsValid():
        print('YEAH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
    return screw


# nut
def make_nut_solid(bolt_to_create):
    print('We gone build a nut: ', bolt_to_create)
    screw_diameter = bolts_sbs_data[bolt_to_create]['screw_diameter']
    nut_width = bolts_sbs_data[bolt_to_create]['head_width']
    nut_thickness = bolts_sbs_data[bolt_to_create]['nut_thickness']

    #----------------- nut_without_hole
    nut_without_hole = make_hexagon_solid(nut_width, nut_thickness)

    #----------------- hole
    origin = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, -nut_thickness),
                                                    AllplanGeo.Vector3D(0, 1, 0),
                                                    AllplanGeo.Vector3D(0, 0, 1))
    nut_hole = AllplanGeo.BRep3D.CreateCylinder(origin, 0.5 * screw_diameter,  3 * nut_thickness)

    #------------------ Subtraction
    err, nut = AllplanGeo.MakeSubtraction(nut_without_hole, nut_hole)
    if GeometryValidate.polyhedron(err) and nut.IsValid():
        print('YEAH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    return nut


# washer
def make_washer_solid(bolt_to_create):
    print('We gone build a washer: ', bolt_to_create)
    screw_diameter = bolts_sbs_data[bolt_to_create]['screw_diameter']
    washer_diameter = bolts_sbs_data[bolt_to_create]['washer_outer_diameter']
    washer_thickness = bolts_sbs_data[bolt_to_create]['washer_thickness']
    washer_hole_diameter = bolts_sbs_data[bolt_to_create]['washer_inner_diameter']

    #----------------- washer_without_hole
    origin = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, 0),
                                                    AllplanGeo.Vector3D(0, 1, 0),
                                                    AllplanGeo.Vector3D(0, 0, 1))
    washer_without_hole = AllplanGeo.BRep3D.CreateCylinder(origin, washer_diameter, washer_thickness)

    #----------------- hole
    origin = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, -washer_thickness),
                                                    AllplanGeo.Vector3D(0, 1, 0),
                                                    AllplanGeo.Vector3D(0, 0, 1))
    washer_hole = AllplanGeo.BRep3D.CreateCylinder(origin, 0.5 * washer_hole_diameter,  3 * washer_thickness)

    #------------------ Subtraction
    err, washer = AllplanGeo.MakeSubtraction(washer_without_hole, washer_hole)
    if GeometryValidate.polyhedron(err) and washer.IsValid():
        print('YEAH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    return washer


# helper
def make_hexagon_solid(a, t):
    import math
    origin = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, 0),
                                                    AllplanGeo.Vector3D(0, 1, 0),
                                                    AllplanGeo.Vector3D(0, 0, 1))

    d = a / math.sqrt(3)
    # a .. length one of the six edges
    # d .. inner hexagon diameter

    solid1 = AllplanGeo.BRep3D.CreateCuboid(origin, a, d, t)
    translation = AllplanGeo.Matrix3D()
    translation.Translate(AllplanGeo.Vector3D(0.5 * d, -0.5 * a, 0))
    solid1 = AllplanGeo.Transform(solid1, translation)

    rotation = AllplanGeo.Matrix3D()
    rotation_axis = AllplanGeo.Line3D(AllplanGeo.Point3D(0,0,0),AllplanGeo.Point3D(0,0,1))
    rotation_angle = AllplanGeo.Angle(math.pi / 3.0)
    rotation.Rotation(rotation_axis, rotation_angle)
    solid2 = AllplanGeo.Transform(solid1, rotation)

    rotation = AllplanGeo.Matrix3D()
    rotation_axis = AllplanGeo.Line3D(AllplanGeo.Point3D(0,0,0),AllplanGeo.Point3D(0,0,1))
    rotation_angle = AllplanGeo.Angle(math.pi * 2 / 3.0)
    rotation.Rotation(rotation_axis, rotation_angle)
    solid3 = AllplanGeo.Transform(solid1, rotation)

    # union of solids
    hexagon_solid = AllplanGeo.MakeUnion(solid1, solid2)[1]
    hexagon_solid = AllplanGeo.MakeUnion(hexagon_solid, solid3)[1]

    return hexagon_solid


# bolt data
bolts_sbs_data = {
                  'M5':{
                         'screw_diameter':5,
                         'head_width':8,
                         'head_thickness':4,
                         'nut_thickness':4,
                         'washer_thickness':2,
                         'washer_inner_diameter':5.3,
                         'washer_outer_diameter':10
                         },
                  'M6':{
                         'screw_diameter':6,
                         'head_width':10,
                         'head_thickness':4,
                         'nut_thickness':5,
                         'washer_thickness':2,
                         'washer_inner_diameter':6.4,
                         'washer_outer_diameter':12
                         },
                  'M8':{
                         'screw_diameter':8,
                         'head_width':13,
                         'head_thickness':6,
                         'nut_thickness':6.5,
                         'washer_thickness':4,
                         'washer_inner_diameter':8.4,
                         'washer_outer_diameter':16
                         },
                  'M10':{
                         'screw_diameter':10,
                         'head_width':17,
                         'head_thickness':7,
                         'nut_thickness':8,
                         'washer_thickness':4,
                         'washer_inner_diameter':11,
                         'washer_outer_diameter':21
                         },
                  'M12':{
                         'screw_diameter':12,
                         'head_width':19,
                         'head_thickness':8,
                         'nut_thickness':10,
                         'washer_thickness':4,
                         'washer_inner_diameter':14,
                         'washer_outer_diameter':24
                         },
                  'M16':{
                         'screw_diameter':16,
                         'head_width':24,
                         'head_thickness':10,
                         'nut_thickness':13,
                         'washer_thickness':6,
                         'washer_inner_diameter':18,
                         'washer_outer_diameter':30
                         },
                  'M20':{
                         'screw_diameter':20,
                         'head_width':30,
                         'head_thickness':13,
                         'nut_thickness':16,
                         'washer_thickness':8,
                         'washer_inner_diameter':22,
                         'washer_outer_diameter':37
                         },
                  'M24':{
                         'screw_diameter':24,
                         'head_width':36,
                         'head_thickness':15,
                         'nut_thickness':19,
                         'washer_thickness':8,
                         'washer_inner_diameter':26,
                         'washer_outer_diameter':44
                         },
                  'M27':{
                         'screw_diameter':27,
                         'head_width':41,
                         'head_thickness':17,
                         'nut_thickness':22,
                         'washer_thickness':8,
                         'washer_inner_diameter':30,
                         'washer_outer_diameter':50
                         },
                  'M30':{
                         'screw_diameter':30,
                         'head_width':46,
                         'head_thickness':19,
                         'nut_thickness':24,
                         'washer_thickness':8,
                         'washer_inner_diameter':33,
                         'washer_outer_diameter':56
                         }
                  }
