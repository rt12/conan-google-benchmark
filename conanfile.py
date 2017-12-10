from conans import ConanFile, CMake, tools
import shutil

class GoogleBenchmarkConan(ConanFile):
    name = 'benchmark'
    version = '1.3.0'
    description = 'A microbenchmark support library.'
    url = 'http://github.com/rt12/conan-google-benchmark'
    license = 'https://github.com/google/benchmark/blob/v1.3.0/LICENSE'
    settings = 'arch', 'build_type', 'compiler', 'os'
    options = { 
	'enable_lto': [True, False], 
        'enable_exceptions': [True, False],
	}
    default_options = "enable_lto=False", "enable_exceptions=True"
    generators = 'cmake'

    def source(self):
        archive_url = 'https://github.com/google/benchmark/archive/v{!s}.tar.gz'.format(self.version)
        tools.get(archive_url, sha256='f19559475a592cbd5ac48b61f6b9cedf87f0b6775d1443de54cfe8f53940b28d')
        shutil.move('benchmark-{!s}'.format(self.version), 'benchmark')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir='./benchmark', build_dir="./")
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            cmake.definitions['BENCHMARK_' + option_name.upper()] = 'ON' if activated else 'OFF'
        cmake.definitions['BENCHMARK_USE_LIBCXX'] = 'ON' if self.settings.compiler.libcxx else 'OFF'
        cmake.install()

    def package(self):
        # already packaged by cmake.install()
        pass

    def package_info(self):
        # let consuming projects know what library name is used for linking
        self.cpp_info.libs = [self.name]
        if self.settings.os == 'Linux':
            self.cpp_info.libs.extend(['pthread', 'rt'])
        if self.settings.os == 'Windows':
            self.cpp_info.libs.append('shlwapi')

