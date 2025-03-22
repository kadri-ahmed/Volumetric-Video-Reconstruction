#include "compressionutils.h"

namespace fs = std::filesystem;

namespace NarvisCompressionUtils
{

	bool convertObjToDrc(std::string inputOBJ, std::string outputDRC, bool sequential)
	{
		auto isMeshRead(draco::ReadMeshFromFile(inputOBJ));
		if (isMeshRead.ok())
		{
			const auto& mesh = isMeshRead.value();
			draco::ExpertEncoder encoder{ *mesh };
			encoder.SetAttributeQuantization(draco::GeometryAttribute::POSITION, 16);  // Position quantization.
			encoder.SetAttributeQuantization(draco::GeometryAttribute::TEX_COORD, 15);  // Tex-coord 0 quantization.
			encoder.SetAttributeQuantization(draco::GeometryAttribute::NORMAL, 14);  // Tex-coord 1 quantization.
			encoder.SetTrackEncodedProperties(true);

			if (sequential) {
				encoder.SetEncodingMethod(draco::MESH_SEQUENTIAL_ENCODING);  // sequential order
			}
			else {
				encoder.SetEncodingMethod(draco::MESH_EDGEBREAKER_ENCODING); // reversed order
			}

			draco::EncoderBuffer buffer;
			encoder.EncodeToBuffer(&buffer);

			std::cout << stringFormat("Encoded vertices = ", encoder.num_encoded_points(), " , faces = ", encoder.num_encoded_faces()) << std::endl;
			auto attr = mesh->GetNamedAttribute(draco::GeometryAttribute::TEX_COORD);
			std::cout << stringFormat("texture coordinates = ", mesh->num_faces()) << std::endl;

			return draco::WriteBufferToFile(buffer.data(), buffer.size(), outputDRC);
		}
		else
		{
			throw new std::runtime_error("Error: failed to read mesh");
		}
		return false;
	}



	void compressData(std::string inputDir, std::string outputDir, bool sequential)
	{
		for (const auto& entry : fs::directory_iterator(inputDir))
		{
			auto inputOBJ = entry.path();
			auto outputDRCName = entry.path().filename();
			outputDRCName.replace_extension(".drc");
			inputOBJ /= "Data\\Model\\Model.obj";
			std::filesystem::path outputDRC{ outputDir };
			outputDRC /= outputDRCName;
			bool success = convertObjToDrc(inputOBJ.string(), outputDRC.string(), sequential);
			if (success) {
				std::cout << stringFormat("Compressed ", inputOBJ.string()) << std::endl;
			}
			else {
				std::cout << stringFormat("Error: Failed to compress ", inputOBJ.string()) << std::endl;
			}
		}

	}

	bool compressImage(std::string filepath, std::string outputPath, int compressionLevel)
	{
		auto img = cv::imread(filepath);
		cv::imwrite(outputPath, img, { cv::IMWRITE_JPEG_QUALITY, compressionLevel });
		return true;
	}

	bool compressImageSet(std::string inputDir, std::string outputDir, int compressionLevel)
	{
		for (const auto& entry : fs::directory_iterator(inputDir))
		{
			auto inputImage = entry.path();
			inputImage /= "Data\\Model\\Model_0.jpg";
			auto img = cv::imread(inputImage.string());
			auto outputImageName = entry.path().filename();
			std::filesystem::path outputImage{ outputDir };
			outputImageName.replace_extension(".jpg");
			outputImage /= outputImageName;
			bool success = cv::imwrite(outputImage.string(), img, { cv::IMWRITE_JPEG_QUALITY, 0 });
			if (success) {
				std::cout << stringFormat("Compressed ", inputImage.string()) << std::endl;
			}
			else {
				std::cout << stringFormat("Error: Failed to compress ", inputImage.string()) << std::endl;
				return false;
			}
		}
		return true;
	}
}