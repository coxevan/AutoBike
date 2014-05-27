import maya.cmds as mc
import pymel.core as py

import simple_sync_setup as ss
import gen_def as df
import mixamo_rig as mr
import bike_ui as bi


class GelUtil():
    file_path = ''

    def __init__(self):
        self.main_start_gui()

    def main_start_gui(self):
        window = 'Mixamo_util'
        window_title = 'GEL : Mixamo Rig Util'
        width_height = (200, 100)
        if py.window(window, exists=True):
            py.deleteUI(window, window=True)
        window_obj = py.window(window, title=window_title, widthHeight=width_height, sizeable=False)
        py.columnLayout('main_col', p=window)

        py.button('import', label='1) Find File Directory', width=width_height[0], command=py.Callback(self.set_file_directory))
        py.button('mixamo', label='2) Mixamo Rig', width=width_height[0], command=py.Callback(mr.MIXAMO_AutoControlRig_UI))
        py.button('simple_sync', label='3) Simple Sync Setup', width=width_height[0], command=py.Callback(ss.ChrisGui))
        py.button('rig', label='3) Bike Rig', width=width_height[0], command=py.Callback(bi.bike_start_gui))

        window_obj.show()

    def set_file_directory(self):
        GelUtil.file_path = df.file_dialogue('Find the file directory for the Character')
