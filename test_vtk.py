#!/usr/bin/env python

# This simple example shows how to do basic rendering and pipeline
# creation.
# https://vimeo.com/32232190

"""

"""


import vtk

def np2vtk(mat):
    if mat.shape == (4, 4):
        obj = vtk.vtkMatrix4x4()
        for i in range(4):
            for j in range(4):
                obj.SetElement(i, j, mat[i, j])
        return obj


class Link:
    def __init__(self):
        self.actor = None


class Revolute(Link):
    def __init__(self, a, r, transform=None):
        super().__init__()
        colors = vtk.vtkNamedColors()
        # Set the background color.
        # bkg = map(lambda x: x / 255.0, [26, 51, 102, 255])
        # colors.SetColor("BkgColor", *bkg)

        # This creates a polygonal cylinder model with eight circumferential
        # facets.
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetResolution(32)
        cylinder.SetHeight(a)
        cylinder.SetRadius(r)

        # The mapper is responsible for pushing the geometry into the graphics
        # library. It may also do color mapping, if scalars or other
        # attributes are defined.
        cylinderMapper = vtk.vtkPolyDataMapper()
        cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

        # The actor is a grouping mechanism: besides the geometry (mapper), it
        # also has a property, transformation matrix, and/or texture map.
        # Here we set its color and rotate it -22.5 degrees.
        cylinderActor = vtk.vtkActor()
        cylinderActor.SetMapper(cylinderMapper)
        cylinderActor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
        cylinderActor.RotateZ(-90.0)
        cylinderActor.SetPosition(a/2,0,0)
        # cylinderActor.RotateWXYZ(-90.0,0,0,1)
        # cylinderActor.RotateY(-45.0)

        self.actor = cylinderActor

        if transform:
            self.actor.SetUserTransform(transform)

        # print(self.actor.GetBounds())
        # print(self.actor, self.actor.GetActors())

    def rotate(self, angle):
        # self.actor.RotateZ(-90 + angle)
        pass


class Axes:
    def __init__(self, scale=1.0, label=0):
        axes_uni = vtk.vtkAxesActor()
        axes_uni.SetXAxisLabelText("x'")
        axes_uni.SetYAxisLabelText("y'")
        axes_uni.SetZAxisLabelText("z'")
        # axes_uni.SetTipTypeToSphere()
        axes_uni.SetShaftTypeToCylinder()
        axes_uni.SetTotalLength(scale, scale, scale)
        axes_uni.SetCylinderRadius(0.02)
        axes_uni.SetAxisLabels(label)
        self.actor = axes_uni


class vtkWindow:
    colors = vtk.vtkNamedColors()

    def __init__(self, width=300, height=300):
        # Set the background color.
        bkg = map(lambda x: x / 255.0, [26, 51, 102, 255])
        self.colors.SetColor("BkgColor", *bkg)

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(self.colors.GetColor3d("BkgColor"))
        self.ren.ResetCamera()

        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren)
        self.renWin.SetSize(width, height)

        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renWin)
        self.iren.Initialize()

    def start(self):
        self.renWin.Render()
        self.iren.Start()

    def AddActor(self, actor):
        self.ren.AddActor(actor)


def main():
    # colors = vtk.vtkNamedColors()
    # # Set the background color.
    # bkg = map(lambda x: x / 255.0, [26, 51, 102, 255])
    # colors.SetColor("BkgColor", *bkg)

    link = Revolute(3,0.5)

    t = vtk.vtkTransform()
    t.Translate(3,0,0)
    t.RotateZ(45)
    link1 = Revolute(5,0.5, t)

    ax0 = Axes(7)
    ax1 = Axes(7)

    # Create the graphics structure. The renderer renders into the render
    # window. The render window interactor captures mouse events and will
    # perform appropriate camera or actor manipulation depending on the
    # nature of the events.
    # ren = vtk.vtkRenderer()
    # renWin = vtk.vtkRenderWindow()
    # renWin.AddRenderer(ren)
    # iren = vtk.vtkRenderWindowInteractor()
    # iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren = vtkWindow()
    ren.AddActor(ax0.actor)
    ren.AddActor(link.actor)
    ren.AddActor(ax1.actor)
    ren.AddActor(link1.actor)
    ren.start()

    # ren.SetBackground(colors.GetColor3d("BkgColor"))
    # renWin.SetSize(300, 300)
    # renWin.SetWindowName('Cylinder')

    # # This allows the interactor to initalize itself. It has to be
    # # called before an event loop.
    # iren.Initialize()
    #
    # # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # # method on it.
    # ren.ResetCamera()
    # # ren.GetActiveCamera().Zoom(1.5)
    # renWin.Render()
    #
    # # Start the event loop.
    # iren.Start()


if __name__ == '__main__':
    main()
