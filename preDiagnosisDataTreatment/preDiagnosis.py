from __main__ import vtk, qt, ctk, slicer

#
# preDiagnosis
#

class preDiagnosis:
  def __init__(self, parent):
    parent.title = "preDiagnosis" # TODO make this more human readable by adding spaces
    parent.categories = ["Diagnosis"]
    parent.dependencies = []
    parent.contributors = ["Jean-Christophe Fillion-Robin (Kitware), Steve Pieper (Isomics)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc. and Steve Pieper, Isomics, Inc.  and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.
    self.parent = parent

#
# qpreDiagnosisWidget
#

class preDiagnosisWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "preDiagnosis Reload"
    self.layout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)


    # Collapsible button
    CollapsibleButton = ctk.ctkCollapsibleButton()
    CollapsibleButton.text = "Pre-diagnosis"
    self.layout.addWidget(CollapsibleButton)

    # Layout within the dummy collapsible button
    FormLayout = qt.QFormLayout(CollapsibleButton)

    # HelloWorld button
    preDiagButton = qt.QPushButton("Pre-diagnosis data treatment")
    preDiagButton.toolTip = "Divides the label map in analizable sub-sections"
    FormLayout.addWidget(preDiagButton)
    preDiagButton.connect('clicked(bool)', self.onPreDiagButtonClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.preDiagButton = preDiagButton

  def onPreDiagButtonClicked(self):
     #Creates an instance of the logic class
    self.pd=preDiagosisLogic()
    self.pd.divideLabelMap()
    self.pd.idIslandsEffect()

  def onReload(self,moduleName="preDiagnosis"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)
    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()

class preDiagosisLogic:

  #Initialize all instance variables
  def __init__(self, filename=None):
    import EditorLib
    editUtil = EditorLib.EditUtil.EditUtil()
  
    parameterNode = editUtil.getParameterNode()
    lm = slicer.app.layoutManager()
    paintEffect = EditorLib.PaintEffectOptions()
    paintEffect.setMRMLDefaults()
    paintEffect.__del__()
    sliceWidget = lm.sliceWidget('Red')
    self.paintTool = EditorLib.PaintEffectTool(sliceWidget)
    self.paintTool.radius = 30
    editUtil.setLabel(0)
    self.slicerLogic = sliceWidget.sliceLogic()
    self.editUtil = editUtil
  #divideLabelMap divides the current label map by painting slices with "background" so the label map
  #sub-sections can be analized in an easier way. This is done by using the paint effect from the editor module
  def divideLabelMap(self):
    self.slicerLogic.FitFOVToBackground(1821)
    for s in xrange(-100,0,5):
     print s
     self.slicerLogic.SetSliceOffset(s) 
     for x in xrange(140,175):
      for y in xrange(130,165):
       self.paintTool.paintAddPoint(x,y)
       self.paintTool.paintApply()
    self.slicerLogic.FitFOVToBackground(500)
  #Changes each label map sub-section to a difeferent label color so they can be analized separately. This
  #is done by using the identify label effect from the editor module 
  def idIslandsEffect(self):
    import EditorLib
    self.iOption = EditorLib.IdentifyIslandsEffectOptions()
    iOption = EditorLib.IdentifyIslandsEffectOptions()
    iTool = iOption.tools
    iEffect= iOption.logic
    iEffect.removeIslands()
    

  
