// dllmain.cpp : Defines the entry point for the DLL application.

#include <iostream>
#include "Unity/IUnityInterface.h"
#include "DracoFileloader.h"

std::unique_ptr<DracoFileLoader> dracoFileLoader;


extern "C" UNITY_INTERFACE_EXPORT void  UNITY_INTERFACE_API  init()
{
	dracoFileLoader = std::make_unique<DracoFileLoader>();
}

extern "C" UNITY_INTERFACE_EXPORT int UNITY_INTERFACE_API loadFile(char* fileName)
{
	return dracoFileLoader->loadFile(fileName);
}
extern "C" UNITY_INTERFACE_EXPORT int  UNITY_INTERFACE_API getVerticesCount()
{
	return dracoFileLoader->getVerticesCount();
}


extern "C" UNITY_INTERFACE_EXPORT int  UNITY_INTERFACE_API getFacesCount()
{
	return dracoFileLoader->getFacesCount(); // mul by 3
}


extern "C" UNITY_INTERFACE_EXPORT bool  UNITY_INTERFACE_API copyData(Vector3 * vertices, int* indices, Vector2 * texCoordinates)
{
	return dracoFileLoader->copyData(vertices, indices, texCoordinates);
}

extern "C" UNITY_INTERFACE_EXPORT long UNITY_INTERFACE_API getWidth()
{
	return dracoFileLoader->getWidth();
}

extern "C" UNITY_INTERFACE_EXPORT long UNITY_INTERFACE_API getHeight()
{
	return dracoFileLoader->getHeight();
}

extern "C" UNITY_INTERFACE_EXPORT size_t UNITY_INTERFACE_API loadTexture(char* fileName)
{
	return dracoFileLoader->loadTexture(fileName);
}

extern "C" UNITY_INTERFACE_EXPORT bool UNITY_INTERFACE_API copyTexture(char* buffer)
{
	return dracoFileLoader->copyTexture(buffer);
}


