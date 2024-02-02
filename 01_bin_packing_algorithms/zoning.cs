using System;
using System.Collections;
using System.Collections.Generic;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;

/// <summary>
/// This class will be instantiated on demand by the Script component.
/// </summary>
public class Script_Instance : GH_ScriptInstance
{
  /// <summary>Print a String to the [Out] Parameter of the Script component.</summary>
  /// <param name="text">String to print.</param>
  private void Print(string text) { /* Implementation hidden. */ }
  /// <summary>Print a formatted String to the [Out] Parameter of the Script component.</summary>
  /// <param name="format">String format.</param>
  /// <param name="args">Formatting parameters.</param>
  private void Print(string format, params object[] args) { /* Implementation hidden. */ }
  /// <summary>Print useful information about an object instance to the [Out] Parameter of the Script component. </summary>
  /// <param name="obj">Object instance to parse.</param>
  private void Reflect(object obj) { /* Implementation hidden. */ }
  /// <summary>Print the signatures of all the overloads of a specific method to the [Out] Parameter of the Script component. </summary>
  /// <param name="obj">Object instance to parse.</param>
  private void Reflect(object obj, string method_name) { /* Implementation hidden. */ }

  /// <summary>Gets the current Rhino document.</summary>
  private readonly RhinoDoc RhinoDocument;
  /// <summary>Gets the Grasshopper document that owns this script.</summary>
  private readonly GH_Document GrasshopperDocument;
  /// <summary>Gets the Grasshopper script component that owns this script.</summary>
  private readonly IGH_Component Component;
  /// <summary>
  /// Gets the current iteration count. The first call to RunScript() is associated with Iteration==0.
  /// Any subsequent call within the same solution will increment the Iteration count.
  /// </summary>
  private readonly int Iteration;

  /// <summary>
  /// This procedure contains the user code. Input parameters are provided as regular arguments,
  /// Output parameters as ref arguments. You don't have to assign output parameters,
  /// they will have a default value.
  /// </summary>
  private void RunScript(string x, double fontsize, out object rectangles)
  {
    string[] parts = x.Split('\n');
    List<List<Rectangle3d>> rectList2D = new List<List<Rectangle3d>>();
    List<string> nameSpace = new List<string>();
    foreach(var i in parts)
    {
      string[] j = i.Split(' ');
      string a = j[0];
      int b = 0;
      int u;
      if(int.TryParse(j[1], out u))
      {
        b = u * 1000000;
      }

      List<Tuple<int, int>> lists = divideNum(b);
      if(lists.Count > 0) // Ensure we have some factors
      {
        List<Rectangle3d> innerList = new List<Rectangle3d>();
        for(int k = 0; k < lists.Count; k++){
          var tuple = lists[k];
          Rectangle3d rect = new Rectangle3d(Plane.WorldXY, tuple.Item1, tuple.Item2);
          innerList.Add(rect);
          nameSpace.Add(a);
        }
        rectList2D.Add(innerList);
      }
    }
    List<Rectangle3d> arrangedRects = ArrangeRectangles(rectList2D, 10000.0, 20000.0);
    rectangles = arrangedRects;
    DisplayAreaOnCenter(arrangedRects, nameSpace, fontsize);
    double textHeight = fontsize;  // 텍스트 높이 설정
    foreach (var rect in arrangedRects)
    {
      DisplayRectangleDimensions(rect, textHeight);
    }
  }

  // <Custom additional code> 
  //가로 세로 뽑아내는 함수.
  private List<Tuple<int, int>> divideNum(int n)
  {
    List<Tuple<int, int>> factors = new List<Tuple<int, int>>();
    for(int i = 3000; i * i <= n; i += 50)
    {
      if(n % i == 0){
        if(i * 4 < n / i) continue;
        factors.Add(new Tuple<int, int>(i, n / i));
      }
    }
    return factors;
  }
  //2차원 평면을 1차원으로 바꾸고 정렬하기.
  private List<Rectangle3d> ArrangeRectangles(List<List<Rectangle3d>> rectList2D, double xSpacing, double ySpacing)
  {
    List<Rectangle3d> result = new List<Rectangle3d>();
    double yOffset = -rectList2D[0][0].Height + ySpacing;
    for (int i = 0; i < rectList2D.Count; i++)
    {
      double xOffset = 0.0;
      for (int j = 0; j < rectList2D[i].Count; j++)
      {
        Rectangle3d rect = rectList2D[i][j];
        Transform translation = Transform.Translation(xOffset, yOffset, 0);
        rect.Transform(translation);
        result.Add(rect);
        xOffset += rect.Width + xSpacing;
      }
      if( i + 1 < rectList2D.Count)
      {
        yOffset -= rectList2D[i + 1][0].Height + ySpacing;
      }
    }
    return result;
  }
  //면적을 적어보자.
  private void DisplayAreaOnCenter(List<Rectangle3d> rectangles, List<string> name, double fontsize)
  {
    int id = 0;
    foreach (var rect in rectangles)
    {
      double area = rect.Area / 1000000;
      string name1 = name[id] + "\n" + area.ToString() + "m2";
      Plane rectPlane = rect.Plane;
      Plane centerPlane = new Plane(rect.Center, rectPlane.Normal);
      Rhino.RhinoDoc.ActiveDoc.Objects.AddText(name1, centerPlane, fontsize, "Arial", true, false);
      id += 1;
    }
  }
  private void AddDimensionText(Point3d location, string text, double height, double rotationDegree = 0.0)
  {
    Plane textPlane = new Plane(location, Vector3d.ZAxis);

    if (Math.Abs(rotationDegree) > 0.01)
    {
      Transform rotation = Transform.Rotation(Rhino.RhinoMath.ToRadians(rotationDegree), textPlane.Normal, textPlane.Origin);
      textPlane.Transform(rotation);
    }

    Rhino.RhinoDoc.ActiveDoc.Objects.AddText(text, textPlane, height, "Arial", true, true);
  }

  private void DisplayRectangleDimensions(Rectangle3d rect, double textHeight)
  {

    Point3d midPointBottom = (rect.Corner(0) + rect.Corner(3)) * 0.5;
    Point3d midPointLeft = (rect.Corner(0) + rect.Corner(1)) * 0.5;

    AddDimensionText(midPointBottom, rect.Height.ToString(), textHeight, -90.0);
    AddDimensionText(midPointLeft, rect.Width.ToString(), textHeight);

  }



  // </Custom additional code> 
}
