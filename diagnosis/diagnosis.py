from __main__ import vtk, qt, ctk, slicer


#
# diagnosis
#

class diagnosis:
  def __init__(self, parent):
    parent.title = "Diagnostics" # TODO make this more human readable by adding spaces
    parent.categories = ["Diagnostics"]
    parent.dependencies = []
    parent.contributors = ["Ricardo Arcila (ICESI), Juan Ruiz (ICESI)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is a ang
    """
    parent.acknowledgementText = """
    Este modulo fue desarrollado como parte del desarrollo del proyecto de grado
""" # replace with organization, grant and thanks.
    self.parent = parent

#
# qdiagnosisWidget
#

class diagnosisWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.grayscaleNode = None
    self.labelNode = None
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    
    
    
    # Collapsible button
    dummyCollapsibleButton = ctk.ctkCollapsibleButton()
    dummyCollapsibleButton.text = "Parameters"
    self.layout.addWidget(dummyCollapsibleButton)

    # Layout within the dummy collapsible button
    dummyFormLayout = qt.QFormLayout(dummyCollapsibleButton)

    #LABEL VOLUME SELECTOR

    self.labelSelectorFrame = qt.QFrame()
    self.labelSelectorFrame.setLayout( qt.QHBoxLayout() )
    dummyFormLayout.addWidget( self.labelSelectorFrame )

    self.labelSelectorLabel = qt.QLabel()
    self.labelSelectorLabel.setText( "Label Map: " )
    dummyFormLayout.addWidget( self.labelSelectorLabel )

    self.labelSelector = slicer.qMRMLNodeComboBox()
    self.labelSelector.nodeTypes = ( "vtkMRMLScalarVolumeNode", "" )
    self.labelSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", "1" )
    # todo addAttribute
    self.labelSelector.selectNodeUponCreation = False
    self.labelSelector.addEnabled = False
    self.labelSelector.noneEnabled = True
    self.labelSelector.removeEnabled = False
    self.labelSelector.showHidden = False
    self.labelSelector.showChildNodeTypes = False
    self.labelSelector.setMRMLScene( slicer.mrmlScene )
    self.labelSelector.setToolTip( "Pick the label map to edit" )
    dummyFormLayout.addWidget( self.labelSelector )
    self.labelSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onLabelSelect)

    # the grayscale volume selector
    #
    self.grayscaleSelectorFrame = qt.QFrame(self.parent)
    self.grayscaleSelectorFrame.setLayout(qt.QHBoxLayout())
    dummyFormLayout.addWidget(self.grayscaleSelectorFrame)

    self.grayscaleSelectorLabel = qt.QLabel("Grayscale Volume: ", self.grayscaleSelectorFrame)
    self.grayscaleSelectorLabel.setToolTip( "Select the grayscale volume (background grayscale scalar volume node) for statistics calculations")
    dummyFormLayout.addWidget(self.grayscaleSelectorLabel)

    self.grayscaleSelector = slicer.qMRMLNodeComboBox(self.grayscaleSelectorFrame)
    self.grayscaleSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.grayscaleSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.grayscaleSelector.selectNodeUponCreation = False
    self.grayscaleSelector.addEnabled = False
    self.grayscaleSelector.removeEnabled = False
    self.grayscaleSelector.noneEnabled = True
    self.grayscaleSelector.showHidden = False
    self.grayscaleSelector.showChildNodeTypes = False
    self.grayscaleSelector.setMRMLScene( slicer.mrmlScene )
    # TODO: need to add a QLabel
    # self.grayscaleSelector.SetLabelText( "Master Volume:" )
    dummyFormLayout.addWidget(self.grayscaleSelector)
    self.grayscaleSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onGrayscaleSelect)
    
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "diagnosis Reload"
    self.layout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    
    

    # Calculate button
    self.calcButton = qt.QPushButton("Calculates")
    self.calcButton.toolTip = "Calculates the stenosis on the most patological slice"
    dummyFormLayout.addWidget(self.calcButton)
    self.calcButton.enabled = False
    self.calcButton.connect('clicked(bool)', self.onCalcButtonClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    #self.calcButton = calcButton

  def onCalcButtonClicked(self):
    print "Hello World !"
    LabelStatisticsLogic(self.grayscaleNode, self.labelNode)
    
  
    
  def onGrayscaleSelect(self, node):
    
    self.grayscaleNode = node
    self.calcButton.enabled = bool(self.grayscaleNode) and bool(self.labelNode)

  def onLabelSelect(self, node):
    self.labelNode = node
    self. calcButton.enabled = bool(self.grayscaleNode) and bool(self.labelNode)


  def onReload(self,moduleName="diagnosis"):
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
    

class LabelStatisticsLogic:
  """Implement the logic to calculate label statistics.
  Nodes are passed in as arguments.
  Results are stored as 'statistics' instance variable.
  """


  def getLabelsFromLabelMap(self, labelMapNode):
    if not labelMapNode:
      return
    accum = vtk.vtkImageAccumulate()
    accum.SetInput(labelMapNode.GetImageData())
    accum.UpdateWholeExtent()
    data = accum.GetOutput()
    data.Update()
    numBins = accum.GetComponentExtent()[1]
    nonZeroLabels = []
    for i in range(0, numBins + 1):
      numVoxels = data.GetScalarComponentAsDouble(i,0,0,0)
      
      if (numVoxels != 0):
        nonZeroLabels.append(i)
    return nonZeroLabels
  
  def __init__(self, grayscaleNode, labelNode, fileName=None):
    #import numpy

    self.keys = ("Index", "Count", "Volume mm^3", "Volume cc", "Min", "Max", "Mean", "StdDev")
    cubicMMPerVoxel = reduce(lambda x,y: x*y, labelNode.GetSpacing())
    ccPerCubicMM = 0.001
    

    #geting a set of labels from a label map
    
    labels = self.getLabelsFromLabelMap(labelNode)
    print "NON - ZERO     LABELS-----------------------------"
    print labels

    # TODO: progress and status updates
    # this->InvokeEvent(vtkLabelStatisticsLogic::StartLabelStats, (void*)"start label stats")
    
    self.labelStats = {}
    self.labelStats['Labels'] = []
   
    stataccum = vtk.vtkImageAccumulate()
    stataccum.SetInput(labelNode.GetImageData())
    
    stataccum.Update()
    lo = int(stataccum.GetMin()[0])
    
    hi = int(stataccum.GetMax()[0])


    aux1=999999999999999999999999999999999
    aux2=999999999999999999999999999999999

    for i in xrange(lo,hi+1):
      print i
      
      thresholder = vtk.vtkImageThreshold()
      thresholder.SetInput(labelNode.GetImageData())
      thresholder.SetInValue(1)
      thresholder.SetOutValue(0)
      thresholder.ReplaceOutOn()
      thresholder.ThresholdBetween(i,i)
      thresholder.SetOutputScalarType(grayscaleNode.GetImageData().GetScalarType())
      thresholder.Update()
      
      # this.InvokeEvent(vtkLabelStatisticsLogic::LabelStatsInnerLoop, (void*)"0.25");
      
      #  use vtk's statistics class with the binary labelmap as a stencil
      stencil = vtk.vtkImageToImageStencil()
      stencil.SetInput(thresholder.GetOutput())
      stencil.ThresholdBetween(1, 1)
      
      # this.InvokeEvent(vtkLabelStatisticsLogic::LabelStatsInnerLoop, (void*)"0.5")
      
      stat1 = vtk.vtkImageAccumulate()
      stat1.SetInput(grayscaleNode.GetImageData())
      stat1.SetStencil(stencil.GetOutput())
      stat1.Update()

      # this.InvokeEvent(vtkLabelStatisticsLogic::LabelStatsInnerLoop, (void*)"0.75")

      if stat1.GetVoxelCount() > 0:
        # add an entry to the LabelStats list
        self.labelStats["Labels"].append(i)
        self.labelStats[i,"Index"] = i
        self.labelStats[i,"Count"] = stat1.GetVoxelCount()
        print stat1.GetVoxelCount()
        self.labelStats[i,"Volume mm^3"] = self.labelStats[i,"Count"] * cubicMMPerVoxel
        self.labelStats[i,"Volume cc"] = self.labelStats[i,"Volume mm^3"] * ccPerCubicMM
        self.labelStats[i,"Min"] = stat1.GetMin()[0]
        self.labelStats[i,"Max"] = stat1.GetMax()[0]
        self.labelStats[i,"Mean"] = stat1.GetMean()[0]
        self.labelStats[i,"StdDev"] = stat1.GetStandardDeviation()[0]

        aux1= stat1.GetVoxelCount()
        if aux1 < aux2 :
          aux2 = aux1
    print "el menor"
    print aux2



        
        # end of the logics method
  
  
