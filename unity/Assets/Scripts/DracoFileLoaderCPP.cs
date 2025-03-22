using UnityEngine;
using System.Runtime.InteropServices;

public class DracoFileLoaderCPP : MonoBehaviour
{
    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern void init();

    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int loadFile(string fileName);

    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int getVerticesCount();

    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int getFacesCount();

    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern bool copyData(Vector3[] vertices, int[] triangles, Vector2[] texCoordinates);
    
    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern long loadTexture(string filename);
    
    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern bool copyTexture(byte[] pixels);
    
    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern long getHeight();
    
    [DllImport("DracoCompressionPlugin", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern long getWidth();
}

