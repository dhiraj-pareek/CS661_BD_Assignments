## Import VTK
import vtk

## Load data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

##taking input isovalue
contourValue=int(input("Enter isoContour Value:"))

def getPointX(pid1,pid2):
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    x=(val1-contourValue)/(val1-val2)* (data.GetPoint(pid2)[0]-data.GetPoint(pid1)[0]) + data.GetPoint(pid1)[0]
    return (x,data.GetPoint(pid2)[1],data.GetPoint(pid2)[2])

def getPointY(pid1,pid2):
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    y=(val1-contourValue)/(val1-val2)* (data.GetPoint(pid2)[1]-data.GetPoint(pid1)[1]) + data.GetPoint(pid1)[1]
    return (data.GetPoint(pid2)[0],y,data.GetPoint(pid2)[2])
    
## Query how many cells the dataset has
numCells = data.GetNumberOfCells()
points=vtk.vtkPoints()
lines=vtk.vtkCellArray()

for i in range(0,numCells):
    cell = data.GetCell(i)
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(1)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(2)
    dataArr = data.GetPointData().GetArray('Pressure')
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    val3 = dataArr.GetTuple1(pid3)
    val4 = dataArr.GetTuple1(pid4)
    
    point=[pid1,pid2,pid3,pid4]
    values=[val1,val2,val3,val4]
    lr_points=[]
    for i in range(4):
        if (values[i]>contourValue)^(values[(i+1)%4]>contourValue):
            if data.GetPoint(point[i])[1]==data.GetPoint(point[(i+1)%4])[1]:
                lr_points.append(getPointX(point[i],point[(i+1)%4]))
            else:
                lr_points.append(getPointY(point[i],point[(i+1)%4]))
    
         
    while(len(lr_points)):
        p1=points.InsertNextPoint(lr_points[0])
        p2=points.InsertNextPoint(lr_points[1])
        lr_points=lr_points[2:]
        templine=vtk.vtkLine()
        templine.GetPointIds().SetId(0,p1)
        templine.GetPointIds().SetId(1,p2)
        lines.InsertNextCell(templine)

    
polydata=vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(lines)

writer=vtk.vtkXMLPolyDataWriter()
writer.SetFileName("op.vtp")
writer.SetInputData(polydata)
writer.Write()