#include "CompressionUtils.h"
#include "DracoFileLoader.h"

char* getCmdOption(char** begin, char** end, const std::string& option)
{
	char** itr = std::find(begin, end, option);
	if (itr != end && ++itr != end)
	{
		return *itr;
	}
	return 0;
}

bool cmdOptionExists(char** begin, char** end, const std::string& option)
{
	return std::find(begin, end, option) != end;
}

const std::string help = "[Usage] -h : show the help message\n"
" \t--mesh : mesh compression will be chosen\n"
" \t--texture : texture compression will be used\n"
" \t-f : file compression will be used\n"
" \t-d : directory compression will be used\n"
" \t--sequential : when mesh compression is chosen, specify 1 for sequential and 0 for edgebreaker encoding\n"
" \t--quality : when texture compression is chosen, specify compression level from 0 (lowest) to 100 (highest) image quality\n"
" \t-i : specify input path\n"
" \t-o : specify output path\n";



/// Specify InputDir and OutputDir in the command line args
int main(int argc, char* argv[])
{
	if (cmdOptionExists(argv, argv + argc, "-h") || cmdOptionExists(argv, argv + argc, "--help"))
	{
		std::cout << help << std::endl;
		return 0;
	}
	if (cmdOptionExists(argv, argv + argc, "--mesh"))
	{
		if (cmdOptionExists(argv, argv + argc, "-f"))
		{
			if (!cmdOptionExists(argv, argv + argc, "-i") || !cmdOptionExists(argv, argv + argc, "-o") || !cmdOptionExists(argv, argv + argc, "--sequential"))
			{
				throw new std::runtime_error("no input or output specified");
			}

			NarvisCompressionUtils::convertObjToDrc(getCmdOption(argv, argv + argc, "-i"), getCmdOption(argv, argv + argc, "-o"), std::atoi(getCmdOption(argv, argv + argc, "--sequential")));
			return 0;
		}
		if (cmdOptionExists(argv, argv + argc, "-d"))
		{
			if (!cmdOptionExists(argv, argv + argc, "-i") || !cmdOptionExists(argv, argv + argc, "-o") || !cmdOptionExists(argv, argv + argc, "--sequential"))
			{
				throw new std::runtime_error("no input or output specified");
			}
			NarvisCompressionUtils::compressData(getCmdOption(argv, argv + argc, "-i"), getCmdOption(argv, argv + argc, "-o"), std::atoi(getCmdOption(argv, argv + argc, "--sequential")));
			return 0;
		}
	}
	if (cmdOptionExists(argv, argv + argc, "--texture"))
	{
		if (cmdOptionExists(argv, argv + argc, "-f"))
		{
			if (!cmdOptionExists(argv, argv + argc, "-i") || !cmdOptionExists(argv, argv + argc, "-o") || !cmdOptionExists(argv, argv + argc, "--compression"))
			{
				throw new std::runtime_error("no input or output specified");
			}

			NarvisCompressionUtils::compressImage(getCmdOption(argv, argv + argc, "-i"), getCmdOption(argv, argv + argc, "-o"), std::atoi(getCmdOption(argv, argv + argc, "--compression")));
			return 0;
		}
		if (cmdOptionExists(argv, argv + argc, "-d"))
		{
			if (!cmdOptionExists(argv, argv + argc, "-i") || !cmdOptionExists(argv, argv + argc, "-o") || !cmdOptionExists(argv, argv + argc, "--compression"))
			{
				throw new std::runtime_error("no input or output specified");
			}
			NarvisCompressionUtils::compressImageSet(getCmdOption(argv, argv + argc, "-i"), getCmdOption(argv, argv + argc, "-o"), std::atoi(getCmdOption(argv, argv + argc, "--compression")));
			return 0;
		}
	}

	throw new std::runtime_error("no file type specified for compression");
	return 0;
}

