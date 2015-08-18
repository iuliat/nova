# Copyright 2014 Cloudbase Solutions SRL
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

"""
Unit tests for the Hyper-V utils factory.
"""

import mock

from nova import test
from nova.virt.hyperv import hostutils
from nova.virt.hyperv import utilsfactory
from nova.virt.hyperv import vmutils


class TestHyperVUtilsFactory(test.NoDBTestCase):

    @mock.patch.object(hostutils.HostUtils, 'get_windows_version')
    def test_get_class(self, mock_get_windows_version):
        mock_get_windows_version.return_value = '6.2'
        path = 'nova.virt.hyperv.hostutilsv2'
        module = __import__(path, globals(), locals(), ['hostutilsv2'], -1)
        expected_instance = getattr(module, 'HostUtilsV2')()

        instance = utilsfactory._get_class('hostutils')
        self.assertEqual(type(expected_instance), type(instance))

    @mock.patch.object(hostutils.HostUtils, 'get_windows_version')
    def test_get_class_not_found(self, mock_get_windows_version):
        mock_get_windows_version.return_value = '5.2'
        self.assertRaises(vmutils.HyperVException, utilsfactory._get_class,
                          'hostutils')
