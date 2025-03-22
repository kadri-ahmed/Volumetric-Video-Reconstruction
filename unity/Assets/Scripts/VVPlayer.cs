using System;
using System.IO;
using UnityEngine;
using UnityEngine.Rendering;

public class VVPlayer : MonoBehaviour
{
    // Paths 
    private static readonly string TestDataDir = Path.Combine(Environment.CurrentDirectory, "..\\testdata\\ALLDATA");
    public string ColorImagePathFormat = "Data\\Model\\Model_0.jpg";
    public string DracoFilesPath = Path.Combine(TestDataDir, "stryker-compressed");
    public string TextureFilesPath = Path.Combine(TestDataDir, "stryker-texture");
    
    // Parameters
    public int SceneCount;
    public int CurrentIndex = 0;
    public bool PlayInReverse = false;
    
    // Components
    private Mesh mesh;
    private Texture2D currentTexture;
    private MeshFilter _meshFilter;
    private MeshRenderer _meshRenderer;

    private void Awake()
    {
        DirectoryInfo inputDir = new DirectoryInfo(DracoFilesPath);
        SceneCount = inputDir.GetFiles().Length;
        _meshFilter = gameObject.GetComponent<MeshFilter>();
        _meshRenderer = gameObject.GetComponent<MeshRenderer>();
        DracoFileLoaderCPP.init();
    }
    
    private bool LoadNext()
    {
        // check if obj file exists
        string meshFile = Path.Combine(DracoFilesPath, $"camera05-{CurrentIndex:D6}.drc");
        if (!File.Exists(meshFile))
        {
            Debug.LogErrorFormat("Mesh file does not exist. Filepath {0}", meshFile);
            return false;
        }
    
        // load texture 
        string textureFile =  Path.Combine(TextureFilesPath, $"camera05-{CurrentIndex:D6}.jpg");
        if (!currentTexture.LoadImage(File.ReadAllBytes(textureFile)))
        {
            Debug.LogErrorFormat("Couldn't load texture image. Filepath {0}", meshFile);
            return false;
        }

        // load draco file
        var status = DracoFileLoaderCPP.loadFile(meshFile);
        if (status != 0)
        {
            Debug.LogErrorFormat("Couldn't load drc file. Filepath {0}", meshFile);
            return false;
        }
        mesh.Clear();
        mesh.indexFormat = IndexFormat.UInt32;
        var verticesCount = DracoFileLoaderCPP.getVerticesCount();
        var facesCount = DracoFileLoaderCPP.getFacesCount();
        var vertices = new Vector3[verticesCount];
        var triangles = new int[facesCount * 3];
        var texCoordinates = new Vector2[verticesCount];
        
        DracoFileLoaderCPP.copyData(vertices, triangles,texCoordinates);
        mesh.vertices = vertices;
        mesh.triangles = triangles;
        mesh.uv = texCoordinates;
        mesh.RecalculateNormals();
        _meshFilter.mesh = mesh;
        _meshRenderer.material.mainTexture = currentTexture;
        
        if (PlayInReverse)
        {
            CurrentIndex--;
        }
        else
        {
            CurrentIndex++;
        }
        
        return true;
    }
    
    void Start()
    {
        Application.targetFrameRate = 60;
        mesh = new Mesh();
        currentTexture = new Texture2D(2, 2);
    }

    void Update()
    {
        if ( !PlayInReverse && CurrentIndex < SceneCount - 1)
        {
            LoadNext();
        }

        if (PlayInReverse && CurrentIndex > 0)
        {
            LoadNext();
        }
    }
}
