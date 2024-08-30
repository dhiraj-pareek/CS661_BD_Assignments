import vtk
import numpy as np

#Reading data file
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("tornado3d_vector.vti")
reader.Update()
data = reader.GetOutput()

# Taking Seed Location in Input
seed_location = [float(x) for x in input("Enter seed location (x y z): ").split()]
seed_location=np.array(seed_location)

# Initialising Step Size and Number of Steps
step_size = 0.05
max_steps = 1000

# Function to get Velocity at query point
def get_velocity(point):
    points = vtk.vtkPoints()
    # print(point)
    points.InsertNextPoint(point[0], point[1], point[2])
    pointsPoly = vtk.vtkPolyData()
    pointsPoly.SetPoints(points)
    probe = vtk.vtkProbeFilter()
    probe.SetSourceData(data)
    probe.SetInputData(pointsPoly)
    probe.Update()

    return np.array(probe.GetOutput().GetPointData().GetArray("vectors"))[0]

# Function to find RK4 Integration until 1000 steps
def rk4(seed_location,step_size,max_steps):
    l=[seed_location]
    i=0
    while i<max_steps:
        
        k1=step_size*get_velocity(seed_location)
        k2=step_size*get_velocity(seed_location+k1/2)
        k3=step_size*get_velocity(seed_location+k2/2)
        k4=step_size*get_velocity(seed_location+k3)
        next_point=seed_location+(k1+2*k2+2*k3+k4)/6
        bounds=data.GetBounds()
        
        if not ((bounds[0] <= next_point[0] <= bounds[1] and bounds[2] <= next_point[1] <= bounds[3] and bounds[4] <= next_point[2] <= bounds[5])):
            break
        l.append(next_point)
        seed_location=next_point
        i=i+1
    return l

# Finding Forward and backward Points and combining them
forward_stream=rk4(seed_location,step_size,max_steps)
backward_stream=rk4(seed_location,-1*step_size,max_steps)[::-1][:-1]
streamline=[]
for i in backward_stream:
    streamline.append(i)
for i in forward_stream:
    streamline.append(i)

# Creating vtp file
polyline = vtk.vtkPolyLine()
size=len(streamline)
polyline.GetPointIds().SetNumberOfIds(size)
for i in range(size):
    polyline.GetPointIds().SetId(i, i)

cells = vtk.vtkCellArray()
cells.InsertNextCell(polyline)

points = vtk.vtkPoints()

for point in streamline:
    points.InsertNextPoint(point)

polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(cells)

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('streamline.vtp')
writer.SetInputData(polydata)
writer.Write()

