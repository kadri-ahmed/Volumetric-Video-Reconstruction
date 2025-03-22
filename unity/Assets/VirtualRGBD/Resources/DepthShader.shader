
Shader "Processing/DepthShader"
{
	SubShader
	{
		Pass
		{
			CGPROGRAM

			#pragma vertex vert
			#pragma fragment frag
			#include "UnityCG.cginc"

			uniform sampler2D _CameraDepthTexture;

			struct input
			{
				float4 vertex : POSITION;
				half2 uv : TEXCOORD0;
			};

			struct v2f
			{
				float4 vertex : SV_POSITION;
				half2 uv : TEXCOORD0;
			};


			v2f vert(input i)
			{
				v2f o;

				o.vertex = UnityObjectToClipPos(i.vertex);
				o.uv = i.uv;

				return o;
			}

			float4 frag(v2f i) : COLOR
			{
				// returned depth ranges from 0 to 1. 1 corresponds to the far-clipping plane
				return float4(1, 1, 1, 0) * Linear01Depth(UNITY_SAMPLE_DEPTH(tex2D(_CameraDepthTexture, i.uv)));
			}

			ENDCG
		}
	}
}