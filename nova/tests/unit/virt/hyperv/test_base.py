# Copyright 2014 Cloudbase Solutions Srl
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from nova import test
from nova.virt.hyperv import utilsfactory


class HyperVBaseTestCase(test.NoDBTestCase):
    def setUp(self):
        super(HyperVBaseTestCase, self).setUp()

        wmi_patcher = mock.patch('__builtin__.wmi', create=True)
        platform_patcher = mock.patch('sys.platform', 'win32')
        hostutils_patcher = mock.patch.object(utilsfactory, 'utils')

        platform_patcher.start()
        wmi_patcher.start()
        patched_hostutils = hostutils_patcher.start()

        patched_hostutils.get_windows_version.return_value = "6.2"

        self.addCleanup(wmi_patcher.stop)
        self.addCleanup(platform_patcher.stop)
        self.addCleanup(hostutils_patcher.stop)
