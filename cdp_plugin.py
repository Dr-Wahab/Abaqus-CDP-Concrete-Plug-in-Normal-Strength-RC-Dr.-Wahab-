# -*- coding: mbcs -*-
# Safe registrar: registers only inside CAE GUI; otherwise no-op.
try:
    from abaqusGui import getAFXApp, Activator, AFXMode
    from abaqusConstants import ALL
    import os
    thisPath = os.path.abspath(__file__); thisDir = os.path.dirname(thisPath)
    toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
    toolset.registerGuiMenuButton(
        buttonText='CDP Concrete Creator V1',
        object=Activator(os.path.join(thisDir, 'cdpDB.py')),
        kernelInitString='import cdp_kernel',
        messageId=AFXMode.ID_ACTIVATE,
        icon=None,
        applicableModules=ALL,
        version='1.2f',
        author='CDP Creator',
        description='Create an Abaqus CDP material with selectable tensile formula (EC2, ACI, fib2010, Custom).',
        helpUrl=''
    )
except Exception:
    pass
