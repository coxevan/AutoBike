import pymel.core as py
import maya.cmds as mc
import os

import main_ui as mi
import gen_def as df


class ChrisGui():
    def __init__(self):
        self.chris_start_gui()
        self.mesh = ''

    def chris_start_gui(self):
        window = 'face_rig_gui'
        window_title = 'Simple Sync Setup'
        if py.window(window, exists=True):
            py.deleteUI(window, window=True)
        window_obj = py.window(window, title=window_title, widthHeight=(300, 100), sizeable=False)
        py.columnLayout('prompt_column', p=window)
        py.button('face_placement_button', label='Create Locators', p='prompt_column', w=325, command=py.Callback(self.create_locators))
        py.rowLayout('deformer_row', p='prompt_column', numberOfColumns=2)
        py.button('deformer_export_placement_button', label='Export Mesh Weights',
                  p='deformer_row', w=160, command=py.Callback(self.export_deformer))
        py.button('deformer_import_placement_button', label='Import Mesh Weights',
                  p='deformer_row', w=160, command=py.Callback(self.import_deformer))
        py.frameLayout('fieldframe', p=window, l='Tell me what things are!')
        py.rowLayout('fieldrow', p='fieldframe', numberOfColumns=15)
        py.columnLayout('rt_eye', p='fieldrow')
        py.rowLayout('rt_row', p='rt_eye', numberOfColumns=2)
        py.button(label='>>', p='rt_row', command=py.Callback(df.set_text, 'rt_eye_text'))
        py.textField('rt_eye_text', tx='Right Eye', p='rt_row')

        py.columnLayout('lfeye', p='fieldrow')
        py.rowLayout('lfrow', p='lfeye', numberOfColumns=2)
        py.button(label='>>', p='lfrow', command=py.Callback(df.set_text, 'lfeye_text'))
        py.textField('lfeye_text', tx='Left Eye', p='lfrow')

        py.rowLayout('jaw_field_row', p='fieldframe', numberOfColumns=15)
        py.columnLayout('up_jaw', p='jaw_field_row')
        py.rowLayout('up_jaw_row', p='up_jaw', numberOfColumns=2)
        py.button(label='>>', p='up_jaw_row', command=py.Callback(df.set_text, 'up_jaw_text'))
        py.textField('up_jaw_text', tx='Up Teeth Group', p='up_jaw_row')

        py.columnLayout('low_jaw', p='jaw_field_row')
        py.rowLayout('low_jaw_row', p='low_jaw', numberOfColumns=2)
        py.button(label='>>', p='low_jaw_row', command=py.Callback(df.set_text, 'low_jaw_text'))
        py.textField('low_jaw_text', tx='Low Teeth Group', p='low_jaw_row')
        py.button(label='Create Rig', p='prompt_column', w=325, command=py.Callback(self.create_system))
        py.button(label='Save Rig', p='prompt_column', w=325, command=py.Callback(df.save_file))

        py.rowLayout('head_root_row', p='fieldframe', numberOfColumns=15)
        py.columnLayout('root', p='head_root_row')
        py.rowLayout('head_row', p='root', numberOfColumns=2)
        py.button(label='>>', p='head_row', command=py.Callback(df.set_text, 'head_text'))
        py.textField('head_text', tx='Head Root Joint', p='head_row')

        py.columnLayout('mesh_col', p='head_root_row')
        py.rowLayout('mesh_row', p='mesh_col', numberOfColumns=2)
        py.button(label='>>', p='mesh_row', command=py.Callback(df.set_text, 'mesh_text'))
        py.textField('mesh_text', tx='Skin Cluster', p='mesh_row')

        py.showWindow(window)

    def export_deformer(self):
        window = 'export_deformer_weights'
        window_title = 'What to do now!'
        if py.window(window, exists=True):
            py.deleteUI(window, window=True)
        window_obj = py.window(window, title=window_title, widthHeight=(300, 100), sizeable=False)
        py.columnLayout('prompt_column', p=window)
        py.text(' This tool cannot do everything for you! Sadly, you still must do the following for me before\
                \n we can import the deformer weights back on to the mesh!')
        py.text('\tSeparate the eyes, lower and upper jaws from the mesh.')
        py.text('\tMove the lower jaw parts and the upper jaw parts into groups')
        py.text('\tDelete your history on the resulting meshes!')
        py.text('\tImport the deformer weights.')

        window_obj.show()
        try:
            self.mesh = mc.ls(sl=True)[0]
            mc.deformerWeights(mi.GelUtil.file_path + ".xml", ex=True, shape="%sShape" % self.mesh)
        except:
            raise

    def import_deformer(self):
        if os.path.exists(mi.GelUtil.file_path + ".xml"):
            mc.deformerWeights(mi.GelUtil.file_path + ".xml", im=True, shape="%sShape" % self.mesh)
        else:
            mc.warning('No xml file exists for character.')

    def create_locators(self):
        """
        Creates locators near origin for positioning at the base of the head and jaw pivot, along with jaw tip.
        """
        mc.spaceLocator(n='cn_headroot_jnt_L')
        mc.spaceLocator(n='cn_low_jaw_jnt_L')
        mc.move(0, 2, 0)
        mc.spaceLocator(n='cn_low_jaw_tip_jnt_L')
        mc.move(0, 4, 0)

    def create_system(self):
        """
        Creates the system necessary for simple sync integration into rig.
        """
        mc.select(clear=True)
        bindjoints = []

        #Queries GUI text fields for their current values.
        rt_eye = py.textField('rt_eye_text', q=True, tx=True)
        lf_eye = py.textField('lfeye_text', q=True, tx=True)
        up_jaw = py.textField('up_jaw_text', q=True, tx=True)
        low_jaw = py.textField('low_jaw_text', q=True, tx=True)
        head = py.textField('head_text', q=True, tx=True)
        mesh = py.textField('mesh_text', q=True, tx=True)

        #Centers the pivot of the right and left eye
        py.xform(rt_eye, cp=True)
        py.xform(lf_eye, cp=True)

        #Queries the position of the left and right eye
        rt_eye_pivot = py.xform(rt_eye, q=True, rp=True, ws=True, a=True)
        lf_eye_pivot = py.xform(lf_eye, q=True, rp=True, ws=True, a=True)

        #creates right eye joint and appends it to the bindjoints list
        mc.joint(n='Right_eye_jnt', p=rt_eye_pivot)
        bindjoints.append(mc.joint(n='Right_U_eyelid_jnt', p=rt_eye_pivot))
        mc.parent(rt_eye, 'Right_eye_jnt')
        mc.select(clear=True)

        #creates left eye joint and appends it to the bindjoints list
        mc.joint(n='Left_eye_jnt', p=lf_eye_pivot)
        bindjoints.append(mc.joint(n='Left_U_eyelid_jnt', p=lf_eye_pivot))
        mc.parent(lf_eye, 'Left_eye_jnt')
        mc.parent('Left_eye_jnt', head)
        mc.select(clear=True)

        #makes cn_headroot_joint at the position of the locator/appends it to the bindjoints list.
        #Does the same for cn_low_jaw joint and low_jaw_tip joint.
        mc.joint(n='cn_headroot_jnt', p=(py.xform('cn_headroot_jnt_L', q=True, ws=True, a=True, t=True)))
        bindjoints.append(mc.joint(n='cn_low_jaw_jnt', p=(py.xform('cn_low_jaw_jnt_L', q=True, ws=True, a=True, t=True))))
        mc.joint(n='cn_low_jaw_tip_jnt', p=(py.xform('cn_low_jaw_tip_jnt_L', q=True, ws=True, a=True, t=True)))
        mc.select(clear=True)

        #parents the joints
        mc.parent('Right_eye_jnt', 'cn_headroot_jnt')
        mc.parent('Left_eye_jnt', 'cn_headroot_jnt')
        mc.parent(up_jaw, 'cn_headroot_jnt')
        mc.parent(low_jaw, 'cn_low_jaw_jnt')
        mc.parent('cn_headroot_jnt', head)

        #deletes locators and adds to influence
        mc.delete('cn_headroot_jnt_L', 'cn_low_jaw_jnt_L', 'cn_low_jaw_tip_jnt_L')
        mc.select(mesh)
        mc.skinCluster(mesh, edit=True, ai=bindjoints, wt=0)
        mc.select(clear=True)

chris_gui = ChrisGui()
