Shader "MedP/Buffer2Mesh"{

	Properties
	{
		[NoScaleOffset] _MainTex("Texture", 2D) = "white" {}
		[Enum(UnityEngine.Rendering.CompareFunction)] _ZTest("ZTest", Float) = 4
	}

		SubShader
		{
			Tags{ "RenderType" = "Opaque" "Queue" = "Geometry" }
			ZTest[_ZTest]
			Pass
			{
				CGPROGRAM

				#include "UnityCG.cginc"
				#pragma vertex vert
				#pragma fragment frag
				#pragma exclude_renderers gles
				sampler2D _MainTex;

		//Buffer interface for compute buffers
		StructuredBuffer<float3> vertices;
		StructuredBuffer<float2> uv;
		StructuredBuffer<int> triangles;

		struct appdata
		{
			uint vertex_id: SV_VertexID;
		};

		struct v2f
		{
			float4 vertex : SV_POSITION;
			float2 uv : TEXCOORD0;
			float4 posWorld : TEXCOORD1;
		};

		//the vertex shader function
		v2f vert(appdata v) {
			v2f o;

			// Read triangle from compute buffer
			int positionID = triangles[v.vertex_id];

			if (positionID >= 0)
			{
				o.uv = uv[positionID];
				float4 rawVertex = float4(vertices[positionID], 1);
				o.posWorld = mul(unity_ObjectToWorld, rawVertex);
				o.vertex = UnityObjectToClipPos(rawVertex);
			}


			return o;
		}


		fixed4 frag(v2f i) : SV_TARGET
		{
			return tex2D(_MainTex, i.uv);
		}

		ENDCG
	}


		}
			Fallback "Diffuse"
}
