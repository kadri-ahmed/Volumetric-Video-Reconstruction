# /usr/bin/python3
import os
from conans import ConanFile, CMake, tools


class Traact(ConanFile):
    
    name = "DracoCompressionPlugin"
    version = "0.0.1"    

    description = "Template to create a conan/cmake based dll for Unity3D"
    url = ""
    license = ""
    author = "Ahmed Kadri"

    generators = "cmake", "virtualrunenv"
    settings = "os", "compiler", "build_type", "arch"
    compiler = "cppstd"
    options = {        
        "with_tests": [True, False]
    }

    default_options = {        
        "with_tests": False
    }

    exports_sources = "src/*", "CMakeLists.txt"

    def requirements(self):
        if self.options.with_tests:
            self.requires("gtest/1.10.0")
        self.requires("draco/1.5.2@camposs/stable")  
        self.requires("opencv/4.5.5")
        self.requires("spdlog/1.11.0")      

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.verbose = True

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            cmake.definitions[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        cmake.configure()
        return cmake

    def configure(self):
        if self.options.with_tests:
            self.options['gtest'].shared = self.options.shared
        

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):        
        self.cpp_info.libs = tools.collect_libs(self)
