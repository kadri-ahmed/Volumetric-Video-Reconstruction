#pragma once

#include <string>
#include <draco/io/mesh_io.h>
#include <draco/io/file_utils.h>
#include <draco/io/obj_encoder.h>
#include <draco/compression/encode.h>
#include <draco/compression/decode.h>
#include <iostream>
#include <filesystem>
#include <sstream>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>


namespace NarvisCompressionUtils
{

	/// <summary>
	/// concatenate string arguments into one string
	/// </summary>
	/// <typeparam name="...Args"></typeparam>
	/// <param name="...args"></param>
	/// <returns></returns>
	template<typename... Args>
	std::string stringFormat(Args const&... args)
	{
		std::ostringstream stream;
		using List = int[];
		(void)List {
			0, ((void)(stream << args), 0) ...
		};

		return stream.str();
	}

	/// <summary>
	/// compress one obj file to a draco file
	/// </summary>
	/// <param name="input"> path of input file </param>
	/// <param name="output"> path of output file </param>
	/// <param name="sequential"> specify whether to use SEQUENTIAL_ENCODING [=true] or EDGE_BREAKER_ENCODING [=false] </param>
	/// <returns></returns>
	bool convertObjToDrc(std::string input, std::string output, bool sequential);


	/// <summary>
	///  compress all obj files in the input directory
	///  to draco files saved in the output directory
	/// </summary>
	/// <param name="inputDir"> path of input directory </param>
	/// <param name="outputDir"> path of output directory </param>
	/// <param name="sequential"> specify whether to use SEQUENTIAL_ENCODING [=true] or EDGE_BREAKER_ENCODING [=false]</param>
	void compressData(std::string inputDir, std::string outputDir, bool sequential);


	/// compresses image to lower quality
	/// compression rate in [0..100]
	bool compressImage(std::string filepath, std::string outputPath, int compressionLevel);


	/// compress images in a directory
	/// compression rate in [0..100]
	bool compressImageSet(std::string inputDir, std::string outputDir, int compressionLevel);
}