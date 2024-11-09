using System;
using System.Collections;
using System.Collections.Generic;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;

using System.Linq;
using System.Runtime.InteropServices;


/// <summary>
/// This class will be instantiated on demand by the Script component.
/// </summary>
public class Script_Instance : GH_ScriptInstance
{
#region Utility functions
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
#endregion

#region Members
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
#endregion

  /// <summary>
  /// This procedure contains the user code. Input parameters are provided as regular arguments,
  /// Output parameters as ref arguments. You don't have to assign output parameters,
  /// they will have a default value.
  /// </summary>
  private void RunScript(Curve x, object y, ref object crvesL, ref object crvesR, ref object gcd)
  {
    var seg = x.DuplicateSegments();
    Curve reference = seg[0];
    Vector3d refV = reference.PointAtEnd - reference.PointAtStart;
    List<Curve> L = new List<Curve>{reference};
    List<Curve> R = new List<Curve>();
    for (int i = 1; i < seg.Length; i++)
    {
      var now = seg[i];
      var nowV = now.PointAtEnd - now.PointAtStart;
      double dotProduct = Math.Abs(Vector3d.Multiply(refV, nowV));
      if (dotProduct < 0.01) R.Add(now);
      else L.Add(now);
    }
    int w, h;
    w = (int) Math.Round(L[0].GetLength());
    Print(w.ToString());
    for (int i = 1; i < L.Count; i++)
    {
      w = Gcd(w, (int) Math.Round(L[i].GetLength()));
      Print((w.ToString()));
    }
    h = (int) R[0].GetLength();
    Print(h.ToString());
    for (int i = 1; i < R.Count; i++)
    {
      h = Gcd(h, (int) Math.Round(R[i].GetLength()));
      Print(h.ToString());
    }
    gcd = Gcd(w, h);

    crvesL = L;
    crvesR = R;
  }

  // <Custom additional code> 

  public int Gcd(int a, int b)
  {
    while (b != 0)
    {
      int temp = b;
      b = a % b;
      a = temp;
    }

    return Math.Abs(a);
  }
  // </Custom additional code> 
}