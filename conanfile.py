from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os, shutil, glob

class GoogleBenchmarkConan(ConanFile):
    name = 'benchmark'
    version = '1.3.0'
    description = 'A microbenchmark support library.'
    url = 'http://github.com/rt12/conan-google-benchmark'
    license = 'https://github.com/google/benchmark/blob/v1.1.0/LICENSE'
    settings = 'arch', 'build_type', 'compiler', 'os'
    options = { 
	'enable_lto': [True, False], 
        'enable_exceptions': [True, False],
	}
    default_options = """
enable_lto=False
enable_exceptions=True
    """
    generators = 'cmake'

    def source(self):
        archive_url = 'https://github.com/google/benchmark/archive/v{!s}.zip'.format(self.version)
        tools.download(archive_url, 'benchmark.zip')
        # tools.check_sha256('benchmark.zip', '3f5321836cf531e621e0187ccbb1d836cd909994ed00c102a41385cbc1254e4e')
        tools.unzip('benchmark.zip')
        os.unlink('benchmark.zip')
        shutil.move('benchmark-{!s}'.format(self.version), 'benchmark')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir='./benchmark', build_dir="./")
        print (cmake.command_line)
        cmake.build()

    def package(self):
        self.copy(pattern='*.h', dst='include', src='include')
        self.copy(pattern='*{!s}*'.format(self.name), dst='lib', src='lib', keep_path=False)
        self.copy(pattern='conan_run.log', dst='.', keep_path=False)

    def package_info(self):
        # let consuming projects know what library name is used for linking
        self.cpp_info.libs = [self.name]
        if self.settings.os == 'Linux':
            self.cpp_info.libs.extend(['pthread', 'rt'])
        if self.settings.os == 'Windows':
            self.cpp_info.libs.append('shlwapi')

