import vtk

def setOpacity(opacityTransferFunction):
    opacityTransferFunction.AddPoint(-4931.54, 1.0)
    opacityTransferFunction.AddPoint(101.815, 0.002)
    opacityTransferFunction.AddPoint(2594.97, 0.0)

def setColor(colorTransferFunction):
    colorTransferFunction.AddRGBPoint(-4931.54, 0, 1, 1)
    colorTransferFunction.AddRGBPoint(-2508.95, 0, 0, 1)
    colorTransferFunction.AddRGBPoint(-1873.9, 0, 0, 0.5)
    colorTransferFunction.AddRGBPoint(-1027.16, 1, 0, 0)
    colorTransferFunction.AddRGBPoint(-298.031, 1, 0.4, 0)
    colorTransferFunction.AddRGBPoint(2594.97, 1, 1, 0)

# Loading 3D data provided
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_3D.vti')
reader.Update()

# Create instances of vtkColorTransferFunction andd setting values
colorTransferFunction = vtk.vtkColorTransferFunction()
setColor(colorTransferFunction)


# Create instances of vtkPiecewiseFunction and setting values
opacityTransferFunction = vtk.vtkPiecewiseFunction()
setOpacity(opacityTransferFunction)

# vtkSmartVolumeMapper() class to perform the volume rendering
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Using vtkOutlineFilter to add an outline to the volume rendered data
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.GetProperty().SetColor(0.0, 0.0, 0.0)
outlineActor.SetMapper(outlineMapper)

# Createing volume Property
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.SetAmbient(0.5)
volumeProperty.SetDiffuse(0.5)
volumeProperty.SetSpecular(0.5)
# setting default shade off
volumeProperty.ShadeOff()


volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Enable phong shading if user desires
phong_shading = input("Want Phong shading? (yes/no): ").lower()
if phong_shading == 'yes':
    volumeProperty.ShadeOn()

# Creating renderer and render window
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(1000, 1000)

# Creating render window interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Adding volume and outline actors to the renderer
renderer.AddVolume(volume)
renderer.AddActor(outlineActor)
renderer.SetBackground(1, 1, 1)

# Starting interaction
renderWindow.Render()
renderWindowInteractor.Start()