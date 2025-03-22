#pragma once

#include <draco/io/mesh_io.h>
#include <draco/io/file_utils.h>
#include <draco/io/obj_encoder.h>
#include "draco/compression/encode.h"
#include "draco/compression/decode.h"
#include "Unity/IUnityInterface.h"
#include <memory>
#include <thread>
#include <fmt/format.h>
#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>



struct Vector3 { float x, y, z; };
struct Vector2 { float u, v; };


class DracoFileLoader
{
public:
	/// <summary>
	/// Decode draco file to get all infos
	/// </summary>
	/// <param name="fileName"> path to draco file </param>
	/// <returns>error code or success [= 0 ]</returns>
	int loadFile(char* fileName);

	/// <summary>
	/// returns the number of vertices that construct the mesh
	/// </summary>
	/// <returns></returns>
	int getVerticesCount();

	/// <summary>
	/// retuns the number of faces that construct the mesh
	/// </summary>
	/// <returns></returns>
	int getFacesCount();

	/// <summary>
	/// copies all data from the mesh into the respective array
	/// </summary>
	/// <param name="vertices"></param>
	/// <param name="indices"></param>
	/// <param name="texCoordinates"></param>
	/// <returns> success or failure </returns>
	bool copyData(Vector3* vertices, int* indices, Vector2* texCoordinates);

	/// <summary>
	/// Load image file to get texture image information
	/// </summary>
	/// <param name="fileName"> path to draco file </param>
	/// <returns> returns size in bytes </returns>
	size_t loadTexture(char* fileName);

	/// <summary>
	/// Copy image pixel values to buffer which be already initialized
	/// </summary>
	/// <param name="buffer"></param>
	/// <returns></returns>
	bool copyTexture(char* buffer);

	long getWidth();

	long getHeight();

private:

	std::unique_ptr<draco::Mesh> mesh_;
	std::unique_ptr<cv::Mat> texture_;
	size_t textureSize_;
};