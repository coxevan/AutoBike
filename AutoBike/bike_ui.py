import maya.cmds as mc
import pymel.core as py

import gen_def as df
import main_ui as mi
reload(df)


def bike_start_gui():
    nodes = mc.ls()
    if 'Character' in nodes:
        window = 'bike_ui'
        window_title = 'NIH/NASA Bike Rigger'
        width_height = (300, 100)
        if py.window(window, exists=True):
            py.deleteUI(window, window=True)
        window_obj = py.window(window, title=window_title, widthHeight=width_height, sizeable=False)
        py.columnLayout('main_col', p=window)
        py.button('import', label='1) Import the bike', width=width_height[0], command=py.Callback(import_bike))
        py.text('2) Place the character on the bike.')
        py.radioButtonGrp('gender_radio', label='Gender', labelArray2=['Male', 'Female'], numberOfRadioButtons=2)
        py.button('rig', label='3) Connect the Character and Save', width=width_height[0], command=py.Callback(rig_bike))

        window_obj.show()
    else:
        mc.warning('Character node not found! Cannot start bike rig without a Character node!')


def import_bike():
    bike_path = df.file_dialogue('Find the correct gender bike!')
    df.import_file(bike_path)
    df.delete_namespaces()
    df.set_attr(['RightHand_Options', 'LeftHand_Options', 'RightFoot_Options', 'LeftFoot_Options'], ['FK_IK'], 1)


def rig_bike():
    """
    Sets up constraints necessary for the character to be connected to the bikes.
    Also creates a male node for the male bike.
    Saves the scene to the file directory provided
    """
    if py.radioButtonGrp('gender_radio', q=True, sl=True) == 1:
        df.parent_constraint([('rt_hand_grp', 'RightHand_IK_CTRL'), ('lf_hand_grp', 'LeftHand_IK_CTRL'),
                              ('rt_foot_locator', 'RightFoot_IK_CTRL'), ('lf_foot_locator', 'LeftFoot_IK_CTRL')])
        df.save_file(save_as=True, ext='_bike', path=mi.GelUtil.file_path)
        mc.select(cl=True)
        mc.group(em=True, n='male')
        mc.parent('Character', 'male')

    elif py.radioButtonGrp('gender_radio', q=True, sl=True) == 2:
        df.parent_constraint([('rt_hand_ctrl_null', 'RightHand_IK_CTRL'), ('lf_hand_ctrl_null', 'LeftHand_IK_CTRL'),
                              ('rt_foot_ctrl_null', 'RightFoot_IK_CTRL'), ('lf_foot_ctrl_null', 'LeftFoot_IK_CTRL')])
        df.save_file(save_as=True, ext='_bike', path=mi.GelUtil.file_path)
    else:
        mc.warning('Must select a gender!')