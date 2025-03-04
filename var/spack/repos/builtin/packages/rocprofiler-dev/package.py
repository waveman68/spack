# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RocprofilerDev(CMakePackage):
    """ROCPROFILER library for AMD HSA runtime API extension support"""

    homepage = "https://github.com/ROCm-Developer-Tools/rocprofiler"
    git      = "https://github.com/ROCm-Developer-Tools/rocprofiler.git"
    url      = "https://github.com/ROCm-Developer-Tools/rocprofiler/archive/refs/tags/rocm-5.1.3.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']
    libraries = ['librocprofiler64']

    version('5.1.3', sha256='eca7be451c7bf000fd9c75683e7f5dfbed32dbb385b5ac685d2251ee8c3abc96')
    version('5.1.0', sha256='4a1c6ed887b0159392406af8796508df2794353a4c3aacc801116044fb4a10a5')
    version('5.0.2', sha256='48f58c3c16dd45fead2086f89a175f74636e81bc2437e30bb6e9361b1083e71d')
    version('5.0.0', sha256='2ed521f400e4aafd17405c2f9ad2fb3b906a982d3767b233122d9c2964c3245f')
    version('4.5.2', sha256='baa59826f8fb984993c03d05e2e3cdf0b830b08f8056b18ba206dfbaa367aca9')
    version('4.5.0', sha256='9b47b086d28fc831dbe0f83ec7e4640057b97edc961f2f050a0968633f32a06b')
    version('4.3.1', sha256='c6f5fa192c9cdb32553d24ed5c847107d312042e39fa3dd17c83e237c9542a2d', deprecated=True)
    version('4.3.0', sha256='3b876a0e601d2c6ae56ddf2a6027afe45b3533f4445b0c2da748d020b6b00cf2', deprecated=True)
    version('4.2.0', sha256='c5888eda1404010f88219055778cfeb00d9c21901e172709708720008b1af80f', deprecated=True)
    version('4.1.0', sha256='2eead5707016da606d636b97f3af1c98cb471da78659067d5a77d4a2aa43ef4c', deprecated=True)
    version('4.0.0', sha256='e9960940d1ec925814a0e55ee31f5fc2fb23fa839d1c6a909f72dd83f657fb25', deprecated=True)
    version('3.10.0', sha256='fbf5ce9fbc13ba2b3f9489838e00b54885aba92336f055e8b03fef3e3347071e', deprecated=True)
    version('3.9.0', sha256='f07ddd9bf2f86550c8d243f887e9bde9d4f2ceec81ecc6393012aaf2a45999e8', deprecated=True)
    version('3.8.0', sha256='38ad3ac20f60f3290ce750c34f0aad442354b1d0a56b81167a018e44ecdf7fff', deprecated=True)
    version('3.7.0', sha256='d3f03bf850cbd86ca9dfe6e6cc6f559d8083b0f3ea4711d8260b232cb6fdd1cc', deprecated=True)
    version('3.5.0', sha256='c42548dd467b7138be94ad68c715254eb56a9d3b670ccf993c43cd4d43659937', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0', '5.1.3']:
        depends_on('hsakmt-roct@' + ver, when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, when='@' + ver)
        depends_on('rocminfo@' + ver, when='@' + ver)
        depends_on('roctracer-dev-api@' + ver, when='@' + ver)

    depends_on('numactl', type='link', when='@4.3.1')

    # See https://github.com/ROCm-Developer-Tools/rocprofiler/pull/50
    patch('fix-includes.patch')

    def patch(self):
        filter_file('${HSA_RUNTIME_LIB_PATH}/../include',
                    '${HSA_RUNTIME_LIB_PATH}/../include ${HSA_KMT_LIB_PATH}/..\
                     /include', 'test/CMakeLists.txt', string=True)

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r'lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)',
                          lib)
        if match:
            ver = '{0}.{1}.{2}'.format(int(match.group(1)),
                                       int(match.group(2)),
                                       int(match.group(3)))
        else:
            ver = None
        return ver

    def cmake_args(self):
        return [
            self.define(
                'PROF_API_HEADER_PATH',
                self.spec['roctracer-dev-api'].prefix.roctracer.inc.ext
            ),
            self.define('ROCM_ROOT_DIR', self.spec['hsakmt-roct'].prefix.include)
        ]
