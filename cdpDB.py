# -*- coding: mbcs -*-
from rsg.rsgGui import *

dialogBox = RsgDialog(title='CDP Concrete',
                      kernelModule='cdp_kernel',
                      kernelFunction='runCDP',
                      includeApplyBtn=False,
                      includeSeparator=True,
                      okBtnText='Create',
                      applyBtnText='Apply',
                      execDir=thisDir)

# Top-level fields
RsgTextField(p='DialogBox', fieldType='String', ncols=24, labelText='Model-Name',     keyword='model',   default='Model-1')
RsgTextField(p='DialogBox', fieldType='String', ncols=24, labelText='Material Name',  keyword='matname', default='C30')

# Group: Compression law
RsgGroupBox(name='grpComp', p='DialogBox', text='Compression law', layout='LAYOUT_FILL_X')
RsgComboBox(name='cmbCompLaw', p='grpComp', text='Compression law', keyword='form', default='Carreeira')
RsgListItem(p='cmbCompLaw', text='Carreeira')
RsgListItem(p='cmbCompLaw', text='Madrid')
RsgListItem(p='cmbCompLaw', text='SN1992')
RsgListItem(p='cmbCompLaw', text='Majewski')

# Group: Tension law
RsgGroupBox(name='grpTens', p='DialogBox', text='Tension law', layout='LAYOUT_FILL_X')
RsgComboBox(name='cmbTensLaw', p='grpTens', text='Tension formula', keyword='tensionlaw', default='EC2')
RsgListItem(p='cmbTensLaw', text='EC2')
RsgListItem(p='cmbTensLaw', text='fib2010')
RsgListItem(p='cmbTensLaw', text='ACI_SPLIT')
RsgListItem(p='cmbTensLaw', text='ACI_RUPTURE')
RsgListItem(p='cmbTensLaw', text='CUSTOM')
RsgTextField(p='grpTens', fieldType='Float', ncols=12, labelText='ft (MPa) if CUSTOM', keyword='ftcustom', default='2.0')

# Group: Key inputs
RsgGroupBox(name='grpKey', p='DialogBox', text='Key inputs', layout='LAYOUT_FILL_X')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='f_c (MPa)',          keyword='fc',     default='30.0')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='Density (tonne/mm^3)', keyword='density', default='2.4e-9')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText="Poisson's ratio (ν)",  keyword='meu',     default='0.20')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='Dilation angle (deg)', keyword='dil',     default='36')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='Excentricity',         keyword='exc',     default='0.1')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='fb0/fc0',              keyword='fb0fc0',  default='1.16')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='K (shape parameter)',  keyword='kshape',  default='0.667')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='Viscosity',            keyword='visc',    default='0.0')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='Tension recovery',     keyword='tr',      default='0.5')
RsgTextField(p='grpKey', fieldType='Float', ncols=12, labelText='Compression recovery', keyword='cr',      default='1.0')

dialogBox.show()
