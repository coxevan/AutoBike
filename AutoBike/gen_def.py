import maya.cmds as mc
import pymel.core as py


def set_text(text_field, **kwargs):
    selection = mc.ls(sl=True)[0]
    py.textField(text_field, e=True, tx=selection)


def get_text(text_field):
    file_name = py.textField(text_field, q=True, tx=True)
    return file_name


def file_dialogue(title, **kwargs):
    """
    Prompts the user with a file dialogue and returns the file path.
    If dir path is set to true, returns the directory instead of the full file path.
    Default values:
        dirpath = False
    """
    directory_bool = kwargs.setdefault('dirpath', False)

    file_path = mc.fileDialog(title=title)
    if directory_bool is True:
        file_path = '/'.join(file_path.split('/')[:-1])
    return file_path


def save_file(**kwargs):
    """
    Saves file to file path with specified extension.
    Only give ext, name and path parameters values if save_as parameter is True.
    Default values:
        ext = ''
        name = ''
        path = ''
        save_as = False

    """
    ext = kwargs.setdefault('ext', '')
    name = kwargs.setdefault('name', '')
    try:
        path, maya_ext = kwargs.setdefault('path', '').split('.')
    except:
        pass
    save_as = kwargs.setdefault('save_as', False)
    if save_as is True:
        mc.file(rename='%s%s%s' % (path, name, ext))
    try:
        mc.file(save=True, de=True, type='mayaBinary', f=True)
    except RuntimeError:
        mc.file(rename='untitled')
        mc.file(save=True, de=True, type='mayaBinary', f=True)


def import_file(filepath):
    mc.file(filepath, i=True, f=True)


def delete_namespaces():
    """
    Deletes all namespaces in the scene. No parameters required.
    """
    try:
        all_nodes = mc.ls()
        for node in all_nodes:
            name_space, new_name = node.split(':')
            mc.rename(node, new_name)
    except ValueError:
        pass


def set_attr(maya_object, attribute, set_to):
    """
    Sets attributes of object list to certain values.
    Example: set_attr(['pCube1', 'pSphere1'], ['tx', 'rz'], 4 )
        Sets the translate X and rotate Z of both pCube1 and pSphere1 to 4.
    """
    for i in range(0, len(maya_object)):
        for attr in attribute:
            mc.setAttr(maya_object[i] + '.' + attr, set_to)


def parent_constraint(driver_driven, **kwargs):
    """
    Creates a parent constraint between objects in a tuple. Allows for user to specify if maintain offset is applied.
    Default values:
        mo=False

    Example: parent_constraint([(pCube1, pSphere1), (pCube1, pCone1)], mo=True)
        Creates a parent constraint, pSphere1 is driven by pCube1. pCone1 is also driven by pCube1. Both have an offset.
    """
    offset_bool = kwargs.setdefault('mo', True)

    for i in range(0, len(driver_driven)):
        mc.parentConstraint(driver_driven[i][0], driver_driven[i][1], mo=offset_bool)