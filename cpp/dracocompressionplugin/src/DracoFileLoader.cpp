
#include "dracofileloader.h"

//spd log

int DracoFileLoader::loadFile(char* fileName)
{
	std::vector<char> data;

	bool status = draco::ReadFileToBuffer(fileName, &data);
	if (!status)
	{
		return 10;
	}
	draco::DecoderBuffer buffer;
	buffer.Init(data.data(), data.size());

	draco::Decoder decoder;

	auto geom_type = draco::Decoder::GetEncodedGeometryType(&buffer);
	if (geom_type.ok() && geom_type.value() == draco::TRIANGULAR_MESH) {
		auto mesh = decoder.DecodeMeshFromBuffer(&buffer);
		if (!mesh.ok())
			return 20;
		else
		{
			mesh_ = std::move(mesh).value();
			return 0;
		}
	}
	else {
		return 30;
	}
}


int DracoFileLoader::getVerticesCount()
{
	return mesh_->num_points();
}

int DracoFileLoader::getFacesCount()
{
	return mesh_->num_faces();
}



bool DracoFileLoader::copyData(Vector3* vertices, int* indices, Vector2* texCoordinates)
{
	float vector[3];

	auto attr = mesh_->GetNamedAttribute(draco::GeometryAttribute::POSITION);
	if (attr == NULL) return false;
	switch (attr->data_type())
	{
	case draco::DataType::DT_FLOAT32:
		if (attr->num_components() != 3)
		{
			spdlog::error("Error: Invalid number of components in compressed mesh position attribute");
			return false;
		}
		if (attr->byte_stride() > 16)
		{
			spdlog::error("Error: Attribute byte stride is too long");
			return false;
		}
		for (draco::AttributeValueIndex v{ 0 }; v < mesh_->num_points(); v++)
		{
			attr->ConvertValue<float>(v, vector);
			vertices[v.value()].x = vector[0];
			vertices[v.value()].y = vector[1];
			vertices[v.value()].z = vector[2];
		}
		break;
	default:
		spdlog::error("Error: Invalid data type in compressed mesh position attribute");
		return false;
		break;
	}

	// Load triangle indices in clockwise winding order
	for (draco::FaceIndex t{ 0 }; t < mesh_->num_faces(); ++t)
	{
		auto x = mesh_->face(t);
		indices[t.value() * 3] = attr->mapped_index(mesh_->face(t)[0]).value();		// BL
		indices[t.value() * 3 + 1] = attr->mapped_index(mesh_->face(t)[1]).value();	// TL
		indices[t.value() * 3 + 2] = attr->mapped_index(mesh_->face(t)[2]).value();	// BR
	}

	// Load uv coordinates
	attr = mesh_->GetNamedAttribute(draco::GeometryAttribute::TEX_COORD);
	if (attr == NULL) return false;
	switch (attr->data_type())
	{
	case draco::DataType::DT_FLOAT32:
		if (attr->num_components() != 2)
		{
			spdlog::error("Error: Invalid number of components in compressed mesh position attribute");
			return false;
		}
		if (attr->byte_stride() > 16)
		{
			spdlog::error("Error: Attribute byte stride is too long");
			return false;
		}
		for (draco::AttributeValueIndex v{ 0 }; v < attr->size(); v++)
		{
			attr->ConvertValue<float>(v, vector);
			texCoordinates[v.value()].u = vector[0];
			texCoordinates[v.value()].v = vector[1];
		}
		break;
	default:
		spdlog::error("Error: Invalid data type in compressed mesh position attribute");
		return false;
		break;
	}
	return false;

}

size_t DracoFileLoader::loadTexture(char* fileName)
{
	if (texture_)
	{
		texture_.release();
	}
	texture_ = std::make_unique<cv::Mat>(cv::imread(std::string(fileName), cv::IMREAD_COLOR));
	if (texture_->empty())
	{
		spdlog::error("Could not read the image: ", fileName);
		return 1;
	}
	textureSize_ = texture_->step[0] * texture_->rows;
	return textureSize_;
}

bool DracoFileLoader::copyTexture(char* buffer)
{
	if (texture_->empty())
	{
		spdlog::error("There is no texture loaded");
		return false;
	}
	auto pixels = texture_->data;
	for (size_t i = 0; i < textureSize_; ++i)
	{
		buffer[i] = pixels[i];
	}
	return true;
}

long DracoFileLoader::getWidth()
{
	return texture_->cols;
}

long DracoFileLoader::getHeight()
{
	return texture_->rows;
}
