"""
Hello world template
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Elements as AllplanElements
import math


# Print some information
print('Load hexagonsolid.py')


# Method for checking the supported versions
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


# Method for element creation
def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
            tuple  with created elements, handles and (otional) reinforcement.
    """

    # Delete unused arguments
    del doc

    #----------------- input parameter
    diameter_anchor_char = build_ele.DiameterAnchorChar.value
    count_anchor = build_ele.CountAnchor.value
    height = build_ele.Height.value
    length = build_ele.Length.value
    column_head_cross_section = build_ele.ColumnHeadCrossSection.value
    column_width = build_ele.ColumnWidth.value
    column_length = build_ele.ColumnLength.value
    count_part = build_ele.CountPart.value
    print('\nInputvalues:')
    print(diameter_anchor_char)
    print(count_anchor)
    print(height)
    print(length)
    print(column_head_cross_section)
    print(column_width)
    print(column_length)
    print(count_part)
    print('\nSet diameter:')
    if diameter_anchor_char == 'X':
         diameter_anchor = 10
    elif diameter_anchor_char == 'A':
         diameter_anchor = 12
    elif diameter_anchor_char == 'B':
         diameter_anchor = 14
    elif diameter_anchor_char == 'C':
         diameter_anchor = 16
    elif diameter_anchor_char == 'G':
         diameter_anchor = 20
    elif diameter_anchor_char == 'J':
         diameter_anchor = 22
    elif diameter_anchor_char == 'O':
         diameter_anchor = 25
    elif diameter_anchor_char == 'P':
         diameter_anchor = 26
    elif diameter_anchor_char == 'T':
         diameter_anchor = 28
    elif diameter_anchor_char == 'U':
         diameter_anchor = 30
    print(diameter_anchor)

    ################################################
    print('\nStart Script')


    if column_head_cross_section == 'Rechteck':
        if count_part > 8:
            count_part = 8
        anko_placements = get_anko_placements(count_part, column_width, column_length)
        # print(anko_placements)

    my_list_of_ankoplus_parts = []
    rot = 0
    i = 0
    for part in range(count_part):
        i += 1
        if column_head_cross_section == 'Rund':
            rot = math.pi * 2.0 * i / count_part
            # print(rot)
            movex = 0.5 * column_width * math.cos(rot)
            movey = 0.5 * column_width * math.sin(rot)
        elif column_head_cross_section == 'Rechteck':
            # {i:[rot, movex, movey]}
            rot = anko_placements[i][0] * math.pi
            movex = anko_placements[i][1] * column_width
            movey = anko_placements[i][2] * column_length

        mytranslation = AllplanGeo.Matrix3D()
        mytranslation.Translate(AllplanGeo.Vector3D(movex, movey, 0))
        rotation_axis = AllplanGeo.Line3D(AllplanGeo.Point3D(0,0,0),AllplanGeo.Point3D(0,0,1))
        rotation_angle = AllplanGeo.Angle(rot)
        myrotation = AllplanGeo.Matrix3D()
        myrotation.Rotation(rotation_axis, rotation_angle)

        anko_part_solids = make_ankoplus_part(diameter_anchor, count_anchor, height, length)  # list of breps
        newsolids = []
        for brep in anko_part_solids:
            # print(brep)
            brep = AllplanGeo.Transform(brep, myrotation)
            brep = AllplanGeo.Transform(brep, mytranslation)
            # print(brep)
            newsolids.append(brep)
        # eine def die die solides der liste in der zeile darueber verschiebt
        model_ele_list = make_model_ele_list(newsolids)
        my_list_of_ankoplus_parts.append(model_ele_list)
    # count_part AnkoPlus am selben Ort !

    
    # ein ankoplus ohne groupping
    # anko_part_solids = make_ankoplus_part(diameter_anchor, count_anchor, height, length)
    # model_ele_list = make_model_ele_list(anko_part_solids)
    # return (model_ele_list, [])
    # we gone group the solids and return these group, see following lines



    #------------------ Define common properties, take global Allplan settings
    com_prop = AllplanElements.CommonProperties()
    com_prop.GetGlobalProperties()
    # print(com_prop)
    prop = AllplanElements.ElementGroupProperties()
    prop.Name = 'AnkoGroup'
    prop.ModifiableFlag = False
    prop.MacroSubType = AllplanElements.MacroSubType.eNOI_UseNoSpecialSubType
    # print(prop)

    anko_element_group = []
    for anko_plus_part_ele in my_list_of_ankoplus_parts:
        anko_element_group.append(AllplanElements.ElementGroupElement(com_prop, prop, anko_plus_part_ele))

    print('\n\nstarttesting move groups and list and allplan model types')

    #print(type(anko_element_group))
    #print(len(anko_element_group))
    #print('\n')
    
    #print(type(anko_element_group[0]))
    #objects = anko_element_group[0].GetElementGroupObjectList()
    #print(type(objects[0])) # yep here we are ModelElement3D !!!
    #print(len(objects))
    #print('\n')

    # ok jetzt brauch ich den solid (brep) aus dem ModelElement3D
    # geom_obj = objects[0].GetGeometryObject()
    # print(type(geom_obj))
    # print(geom_obj)
    # yep BRep3D

    #testobj = anko_element_group[0].GetElementGroupObjectList()[0].GetGeometryObject()
    #print(testobj)
    # yep BRep3D

    #mytranslation = AllplanGeo.Matrix3D()
    #mytranslation.Translate(AllplanGeo.Vector3D(100, 0, 0))
    #geom_obj = AllplanGeo.Transform(geom_obj, mytranslation)

    #print(anko_element_group[0].GetElementGroupObjectList()[0].GetGeometryObject())
    #anko_element_group[0].GetElementGroupObjectList()[0].GetGeometryObject() = AllplanGeo.Transform(anko_element_group[0].GetElementGroupObjectList()[0].GetGeometryObject(), mytranslation)
    #print(anko_element_group[0].GetElementGroupObjectList()[0].GetGeometryObject())
    # obiges funktioniert nicht, brep ist noch am selben ort siehe prints

    #for model_ele in objects:
    #    print(model_ele)
        
    # ich muss ein klares naming schaffen, was eine normale liste ist und was ein 
    # ModelElement3D
    # ElementGroupElement
    # Solid

    #print(type(my_list_of_ankoplus_parts))
    #print(len(my_list_of_ankoplus_parts))
    print('endtesting\n\n')
    
    return (anko_element_group, [])



    #print(anko_element_group2)
    #print(type(anko_element_group2))  # ElementGroupElement
    #mylist = AllplanElements.GetElementGroupObjectList(anko_element_group2)
    # komisch, gibt error, aber in API ist methode definiert ?!?
    
    # versuch elemente rausziehen verschieben 
    # http://pythonparts.allplan.com/2016-1/documentation.html

    
#########################################
# HELPER
def get_anko_placements(count_part, column_width, column_length):
    #{i:[rot, movex, movey]}
    anko_placements = {}
    if count_part <= 8:
        anko_placements[1] = [0.25, 0.5, 0.5]
        if count_part == 1:
            return anko_placements 
        anko_placements[2] = [0.50, 0.0, 0.5]
        if count_part == 2:
            return anko_placements 
        anko_placements[3] = [0.75, -0.5, 0.5]
        if count_part == 3:
            return anko_placements 
        anko_placements[4] = [1.00, -0.5, 0.0]
        if count_part == 4:
            return anko_placements 
        anko_placements[5] = [1.25, -0.5, -0.5]
        if count_part == 5:
            return anko_placements 
        anko_placements[6] = [1.50, 0.0, -0.5]
        if count_part == 6:
            return anko_placements 
        anko_placements[7] = [1.75, 0.5, -0.5]
        if count_part == 7:
            return anko_placements 
        anko_placements[8] = [2.00, 0.5, 0.0]
        if count_part == 8:
            return anko_placements 

def make_model_ele_list(anko_part_solids):
    #----------------- CommonProperties
    com_prop = AllplanElements.CommonProperties()
    com_prop.GetGlobalProperties()
    # print(com_prop)

    #------------------ draw solids
    model_ele_list = []
    for part in anko_part_solids:
        model_ele_list.append(AllplanElements.ModelElement3D(com_prop, part))
    # print(model_ele_list)
    # print(len(model_ele_list))
    # ist eine ganz normale liste von objekten des Typs ModelElement3D

    return model_ele_list

def make_ankoplus_part(diameter_anchor, count_anchor, height, length):
    anko_part_solids = []

    #----------------- bolt positions
    bolt_space = length / count_anchor
    bolt_positions = []
    for bp in range(count_anchor):
        bolt_position = 0.5 * bolt_space + bp * bolt_space
        bolt_positions.append(bolt_position)
    
    #----------------- bolt solids
    for bp in bolt_positions:
        translation = AllplanGeo.Matrix3D()
        translation.Translate(AllplanGeo.Vector3D(bp, 0, 0))
        bolt = make_double_head_bolt(diameter_anchor, height)
        bolt = AllplanGeo.Transform(bolt, translation)
        anko_part_solids.append(bolt)

    #----------------- base bars solid
    base_bars = make_two_basebars(diameter_anchor, length)
    anko_part_solids.append(base_bars)
    
    return anko_part_solids

def make_double_head_bolt(d, h):
    origin = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, 0),
                                                    AllplanGeo.Vector3D(0, 1, 0),
                                                    AllplanGeo.Vector3D(0, 0, 1))
    
    # head solid
    bolt_head = AllplanGeo.BRep3D.CreateCylinder(origin, 1.5 * d, 0.25 * d)

    # neck neck solid
    apex_point = AllplanGeo.Point3D(0, 0, 0.5 * d)
    translation = AllplanGeo.Matrix3D()
    translation.Translate(AllplanGeo.Vector3D(0, 0, (0.25 * d)))
    bolt_neck = AllplanGeo.Cone3D(origin, 1.5 * d, 0.5 * d, apex_point)
    bolt_neck = AllplanGeo.BRep3D.CreateCone(bolt_neck)  # convert to BRep3D
    bolt_neck = AllplanGeo.Transform(bolt_neck, translation)

    # shank solid
    translation = AllplanGeo.Matrix3D()
    translation.Translate(AllplanGeo.Vector3D(0, 0, (0.75 * d)))
    bolt_shank = AllplanGeo.BRep3D.CreateCylinder(origin, 0.5 * d, (0.5 * h - 0.75 * d))
    bolt_shank = AllplanGeo.Transform(bolt_shank, translation)
        
    # bolt bottom solid
    bolt_solid_bottom = AllplanGeo.MakeUnion(bolt_neck, bolt_head)[1]
    bolt_solid_bottom = AllplanGeo.MakeUnion(bolt_solid_bottom, bolt_shank)[1]

    # bolt top solid
    rotation = AllplanGeo.Matrix3D()
    rotation_axis = AllplanGeo.Line3D(AllplanGeo.Point3D(0,0,0),AllplanGeo.Point3D(1,0,0))
    rotation_angle = AllplanGeo.Angle(math.pi)
    rotation.Rotation(rotation_axis, rotation_angle)
    translation = AllplanGeo.Matrix3D()
    translation.Translate(AllplanGeo.Vector3D(0, 0, h))
    bolt_solid_top = AllplanGeo.Transform(bolt_solid_bottom, rotation)
    bolt_solid_top = AllplanGeo.Transform(bolt_solid_top, translation)

    # bolt solid
    bolt_solid = AllplanGeo.MakeUnion(bolt_solid_bottom, bolt_solid_top)[1]
    return bolt_solid

def make_two_basebars(d, l):
    bbd = 6.0  # base bar diameter
    origin = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, 0),
                                                AllplanGeo.Vector3D(0, 1, 0),
                                                AllplanGeo.Vector3D(0, 0, 1))
    # long base bar
    rotation = AllplanGeo.Matrix3D()
    rotation_axis = AllplanGeo.Line3D(AllplanGeo.Point3D(0,0,0),AllplanGeo.Point3D(0,1,0))
    rotation_angle = AllplanGeo.Angle(math.pi / 2)
    rotation.Rotation(rotation_axis, rotation_angle)
    translation = AllplanGeo.Matrix3D()
    translation.Translate(AllplanGeo.Vector3D(0, d, -(0.5 * bbd)))
    base_bar_long = AllplanGeo.BRep3D.CreateCylinder(origin, 0.5 * bbd, l + 40)
    base_bar_long = AllplanGeo.Transform(base_bar_long, rotation)
    base_bar_long = AllplanGeo.Transform(base_bar_long, translation)

    # short base bar
    translation = AllplanGeo.Matrix3D()
    translation.Translate(AllplanGeo.Vector3D(0, -d, -(0.5 * bbd)))
    base_bar_short = AllplanGeo.BRep3D.CreateCylinder(origin, 0.5 * bbd, l - 20)
    base_bar_short = AllplanGeo.Transform(base_bar_short, rotation)
    base_bar_short = AllplanGeo.Transform(base_bar_short, translation)

    # two base bars
    base_bar_solid = AllplanGeo.MakeUnion(base_bar_long, base_bar_short)[1]
    return base_bar_solid