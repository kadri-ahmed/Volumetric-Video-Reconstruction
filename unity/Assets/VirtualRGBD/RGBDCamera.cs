using System;
using UnityEngine;
using UnityEngine.SceneManagement;

[RequireComponent(typeof(Camera)), ExecuteInEditMode]
public class RGBDCamera : MonoBehaviour
{
    private Material DepthMaterial;
    private Camera _Camera;

    public RenderTexture ColorFrame;
    public RenderTexture DepthFrame;
    private Matrix4x4 CapturePosition = Matrix4x4.identity;

    public float maxDistanceThresholdDepth = 0.02f;
    public int Layer = 0;
    public bool RenderPointCloud = false;
    private bool IsInstantiated
    {
        get
        {
            return _Depth2BufferComputeShader != null && ProceduralMat != null && _args != null && DepthFrame != null && ColorFrame != null;
        }
    }
    // To be used for rendering the view to the unity viewport
    public Material ProceduralMat;

    // Compute buffer shared between Compute buffer and rendering material ProceduralMat
    private ComputeBuffer _args;
    private ComputeBuffer _ib; // index buffer
    private ComputeBuffer _ub; // uv coordinates buffer
    private ComputeBuffer _vb; // vertex buffer

    private ComputeShader _Depth2BufferComputeShader;
    private int KernelID = 0;

    private readonly int Height = 576;
    private readonly int Width = 640;

    private void Awake()
    {
        Initiate();
    }

    private void Initiate()
    {
        Screen.SetResolution(Width, Height, FullScreenMode.FullScreenWindow);

        // Step 1 : Instantiate Depthmap and Colormap
        DepthMaterial = new Material(Shader.Find("Processing/DepthShader"));
        _Camera = GetComponent<Camera>();
        _Camera.depthTextureMode = DepthTextureMode.Depth;

        if (DepthFrame == null)
        {
            //DepthFrame = new RenderTexture((int)_Camera.sensorSize.x, (int)_Camera.sensorSize.y, 24);
            DepthFrame = new RenderTexture(Width, Height, 24);
        }
        else
        {
            DepthFrame.Release();
            /*DepthFrame.width = (int)_Camera.sensorSize.x;
            DepthFrame.height = (int)_Camera.sensorSize.y;*/
            DepthFrame.width = Width;
            DepthFrame.height = Height;
        }
        DepthFrame.name = "DepthImage";
        DepthFrame.Create();

        if(ColorFrame == null)
        {
            //ColorFrame = new RenderTexture((int)_Camera.sensorSize.x, (int)_Camera.sensorSize.y, 24);
            ColorFrame = new RenderTexture(Width, Height, 24);
        }else
        {
            ColorFrame.Release();
            /*ColorFrame.width = (int)_Camera.sensorSize.x;
            ColorFrame.height = (int)_Camera.sensorSize.y;*/
            ColorFrame.width = Width;
            ColorFrame.height = Height;
            
        }
        ColorFrame.name = "ColorImage";
        ColorFrame.Create();

        int size = DepthFrame.width * DepthFrame.height;

        _Depth2BufferComputeShader = UnityEngine.Object.Instantiate(Resources.Load("Depth2Buffer") as ComputeShader);
        KernelID = _Depth2BufferComputeShader.FindKernel("Compute");

        _Depth2BufferComputeShader.SetInt("_DepthWidth", DepthFrame.width);
        _Depth2BufferComputeShader.SetInt("_DepthHeight", DepthFrame.height);

        _args = new ComputeBuffer(4, sizeof(int), ComputeBufferType.IndirectArguments);
        _ib = new ComputeBuffer(size * 6, sizeof(int));
        _ub = new ComputeBuffer(size, 2 * sizeof(float));
        _vb = new ComputeBuffer(size, 3 * sizeof(float));

        int[] args = new int[] { size * 6, 2, 0, 0 };
        _args.SetData(args);

        // Set Kernel variables
        _Depth2BufferComputeShader.SetBuffer(KernelID, "vertices", _vb);
        _Depth2BufferComputeShader.SetBuffer(KernelID, "uv", _ub);
        _Depth2BufferComputeShader.SetBuffer(KernelID, "triangles", _ib);

        ProceduralMat = new Material(Shader.Find("MedP/Buffer2Mesh"));
        ProceduralMat.SetBuffer("vertices", _vb);
        ProceduralMat.SetBuffer("uv", _ub);
        ProceduralMat.SetBuffer("triangles", _ib);

        ProceduralMat.mainTexture = ColorFrame;
        
    }


    private void UpdatePointcloud()
    {
        if (!IsInstantiated) Initiate();

        if(RenderPointCloud)
        {
            int numthreads = 8;

            _Depth2BufferComputeShader.SetFloat("_focalLength", (DepthFrame.height / 2.0f) / Mathf.Tan(_Camera.fieldOfView / 2 * 0.0174533f));
            _Depth2BufferComputeShader.SetFloat("_nearPlane", _Camera.nearClipPlane);
            _Depth2BufferComputeShader.SetFloat("_farPlane", _Camera.farClipPlane);
            _Depth2BufferComputeShader.SetFloat("_maxDistThreshold", maxDistanceThresholdDepth);

            _Depth2BufferComputeShader.SetMatrix("_Transform", CapturePosition);

            _Depth2BufferComputeShader.SetTexture(KernelID, "_DepthTex", DepthFrame);

            _Depth2BufferComputeShader.Dispatch(KernelID, DepthFrame.width / numthreads, DepthFrame.height / numthreads, 1);

            Graphics.DrawProceduralIndirect(ProceduralMat, new Bounds(transform.position, Vector3.one * _Camera.farClipPlane * 2), MeshTopology.Triangles, _args,
                castShadows: UnityEngine.Rendering.ShadowCastingMode.Off, receiveShadows: false, layer: Layer);
            //Graphics.DrawProcedural(ProceduralMat, new Bounds(transform.position, Vector3.one * _Camera.farClipPlane), MeshTopology.Triangles, DepthFrame.width * DepthFrame.height * 6, layer: Layer);
        }
        
        _args.Dispose();
        _ib.Dispose();
        _ub.Dispose();
        _vb.Dispose();
    }

    private void Update()
    {
        UpdatePointcloud();
    }
    
    private void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        DepthMaterial.SetFloat("nearPlane", _Camera.nearClipPlane);
        DepthMaterial.SetFloat("farPlane", _Camera.farClipPlane);

        // "When OnRenderImage finishes, Unity expects that the destination render
        // texture is the active render target. Generally, a Graphics.Blit or manual
        // rendering into the destination texture should be the last rendering operation."
        // So your last blit should use the destination texture.
        
        Graphics.Blit(source, ColorFrame);
        Graphics.Blit(source, DepthFrame, DepthMaterial);
        Graphics.Blit(source, destination, DepthMaterial);

        CapturePosition = Matrix4x4.TRS(transform.position, transform.rotation, Vector3.one);
    }


}
