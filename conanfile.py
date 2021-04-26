from conans import ConanFile, CMake, tools
import os

class RbdlJetConan(ConanFile):
    name = "rbdl_jet"
    version = "0.2"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "RBDL Library for dyros jet"
    # topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    def source(self):
        git = tools.Git(folder="rbdl-orb")
        git.clone("https://github.com/saga0619/rbdl-orb.git", "master")

    def build_requirements(self):
        self.build_requires("eigen/3.3.5@conan/stable")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_BUILD_TYPE"] = "Release"
        cmake.configure(source_folder="rbdl-orb", build_folder="build")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="rbdl-orb/include")
        self.copy("*.h", dst="include", src="build/include")
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", src="build", keep_path=False)
        

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
