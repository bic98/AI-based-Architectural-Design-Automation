using System;
using System.Collections;
using System.Collections.Generic;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;
using System.IO;
using System.Linq;
using System.Data;
using System.Drawing;
using System.Reflection;
using System.Windows.Forms;
using System.Xml;
using System.Xml.Linq;
using System.Runtime.InteropServices;

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
  private void RunScript(Rectangle3d x, string space_size, string ratio, int y, out object a, out object A)
  {
    // Write your logic here
    string[] parts = space_size.Split(' ');
    // 면적에 따른 가능한 직사각형의 형태들
    List<List<Rectangle3d>> rec = new List<List<Rectangle3d>>();

    // 약수를 구함
    foreach(var i in parts){
      int num;
      if(int.TryParse(i, out num)){
        num *= (int) 1e6;
      }
      List<Tuple<int, int>> rowCol = divideNum(num);
      if(rowCol.Count > 0) // Ensure we have some factors
      {
        List<Rectangle3d> innerList = new List<Rectangle3d>();
        for(int k = 0; k < rowCol.Count; k++){
          var tuple = rowCol[k];
          Rectangle3d rect = new Rectangle3d(Plane.WorldXY, tuple.Item1, tuple.Item2);
          innerList.Add(rect);
        }
        rec.Add(innerList);
      }
    }



    //사각형 x의 크기
    int large_box = (int) (x.Width * x.Height);
    //비율에 맞는 개수 구하기
    List<int> small_box = new List<int>();
    int cnt = 0;
    //면적의 합
    int sum_space = 0;
    string[] ratio_space = ratio.Split(' ');
    for(int i = 0; i < ratio_space.Length; i++){
      int t;
      if(int.TryParse(ratio_space[i], out t)){
        small_box.Add(t);
      }
      int sz;
      if(int.TryParse(parts[i], out sz)){
        sz *= (int) 1e6;
      }
      sum_space += t * sz;
    }
    cnt = large_box / sum_space;
    int need_cnt = 0;
    for(int i = 0; i < small_box.Count; i++){
      small_box[i] *= cnt;
      need_cnt += small_box[i];
    }



    //백트래킹해서 모든 가능한 조합을 넣어보자.
    List<List<Rectangle3d>> ret = new List<List<Rectangle3d>>();
    List<Rectangle3d> temp = new List<Rectangle3d>();
    recur(0, ref rec, ref temp, ref ret, ref small_box);
    Print(ret[0].Count.ToString());

    List<Box> _boxes = new List<Box>();

    foreach(Rectangle3d rect in ret[y])
    {
      _boxes.Add(new Box {width = rect.Width, height = rect.Height});
    }
    _boxes.ForEach(b => b.area = (b.width * b.height));
    _boxes = _boxes.OrderByDescending(b => b.area).ToList();

    Node rootNode = new Node { width = x.Width, height = x.Height };
    rootNode.pos_x = x.Plane.Origin.X;
    rootNode.pos_y = x.Plane.Origin.Y;
    //Print(x.X.Min.ToString() + "-" + x.Y.Min.ToString());

    A = Pack(rootNode, _boxes);

    foreach (Box box in _boxes)
    {
      string positionx = box.position != null ? box.position.pos_x.ToString() : String.Empty;
      string positiony = box.position != null ? box.position.pos_y.ToString() : String.Empty;
      Print("X : " + positionx + "- Y  : " + positiony + "- W : " + box.width + "- H : " + box.height);
    }




    List<Rectangle3d> arrangedRects = ArrangeRectangles(ret, 10000.0, 20000.0);
    a = arrangedRects;
    DisplayAreaOnCenter(arrangedRects);
    double textHeight = 1200.0;  // 텍스트 높이 설정
    foreach (var rect in arrangedRects)
    {
      DisplayRectangleDimensions(rect, textHeight);
    }
  }

  // <Custom additional code> 
  //O(sqrt(n)) 약수구하는 알고리즘
  private List<Tuple<int, int>> divideNum(int n)
  {
    List<Tuple<int, int>> factors = new List<Tuple<int, int>>();
    for(int i = 3000; i * i <= n; i += 100)
    {
      if(n % i == 0){
        if(i * 2.5 < n / i) continue;
        if((n / i) % 100 == 50) continue;
        factors.Add(new Tuple<int, int>(i, n / i));
      }
    }
    return factors;
  }


  private void recur(int now, ref List<List<Rectangle3d>> rec, ref List<Rectangle3d> temp, ref List<List<Rectangle3d>> ret, ref List<int> small_box)
  {
    if(now == rec.Count){
      List<Rectangle3d> arr = new List<Rectangle3d>();
      for(int i = 0; i < small_box.Count; i++){
        for(int j = 0; j < small_box[i] - 2; j++){
          arr.Add(temp[i]);
        }
      }
      ret.Add(arr);
      return;
    }
    foreach (Rectangle3d i in rec[now]){
      temp.Add(i);
      recur(now + 1, ref rec, ref temp, ref ret, ref small_box);
      temp.RemoveAt(temp.Count - 1);
    }
  }

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
  private void DisplayAreaOnCenter(List<Rectangle3d> rectangles)
  {
    int id = 0;
    foreach (var rect in rectangles)
    {
      double area = rect.Area / 1000000;
      string name1 = area.ToString() + "m2";
      Plane rectPlane = rect.Plane;
      Plane centerPlane = new Plane(rect.Center, rectPlane.Normal);
      Rhino.RhinoDoc.ActiveDoc.Objects.AddText(name1, centerPlane, 1000.0, "Arial", true, false);
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

  public class Node {
    public Node rightNode;
    public Node bottomNode;
    public double pos_x;
    public double pos_y;
    public double width;
    public double height;
    public bool isOccupied;
  }

  public class Box {
    public double width;
    public double height;
    public double area;
    public Node position;
  }

  public List<Rectangle3d> Pack(Node rootNode, List<Box> _boxes)
  {
    List<Rectangle3d> nRects = new List<Rectangle3d>();
    foreach (Box box in _boxes)
    {
      var node = FindNode(rootNode, box.width, box.height);
      if (node != null)
      {
        box.position = SplitNode(node, box.width, box.height);
      }
      Point3d pt = new Point3d(box.position.pos_x, box.position.pos_y, 0);
      Plane pl = new Plane(pt, Vector3d.ZAxis);
      Rectangle3d nRect = new Rectangle3d(pl, box.width, box.height);
      nRects.Add(nRect);
    }
    return nRects;
  }

  public Node FindNode(Node rootNode, double boxWidth, double boxHeight)
  {
    if (rootNode.isOccupied){
      var nextNode = FindNode(rootNode.bottomNode, boxWidth, boxHeight);
      if (nextNode == null){
        nextNode = FindNode(rootNode.rightNode, boxWidth, boxHeight);
      }
      return nextNode;
    }
    else if (boxWidth <= rootNode.width && boxHeight <= rootNode.height){
      return rootNode;
    }
    else{
      return null;
    }
  }

  public Node SplitNode(Node node, double boxWidth, double boxHeight)
  {
    node.isOccupied = true;
    node.bottomNode = new Node { pos_y = node.pos_y, pos_x = node.pos_x + boxWidth, height = node.height, width = node.width - boxWidth };
    node.rightNode = new Node { pos_y = node.pos_y + boxHeight, pos_x = node.pos_x, height = node.height - boxHeight, width = boxWidth };
    return node;
  }
  // </Custom additional code> 
}
