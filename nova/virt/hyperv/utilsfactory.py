# Copyright 2013 Cloudbase Solutions Srl
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

from nova.i18n import _
from nova.virt.hyperv import hostutils
from nova.virt.hyperv import hostutilsv2
from nova.virt.hyperv import livemigrationutils
from nova.virt.hyperv import networkutils
from nova.virt.hyperv import networkutilsv2
from nova.virt.hyperv import pathutils
from nova.virt.hyperv import vhdutils
from nova.virt.hyperv import vhdutilsv2
from nova.virt.hyperv import vmutils
from nova.virt.hyperv import vmutilsv2
from nova.virt.hyperv import vmutilsv3
from nova.virt.hyperv import volumeutils
from nova.virt.hyperv import volumeutilsv2
import os


utils = hostutils.HostUtils()

class_utils = {
    'hostutils': {'HostUtils': {'min_version': '6.0', 'max_version': '6.2'},
                  'HostUtilsV2': {'min_version': '6.2',
                                  'max_version': None}},
    'livemigrationutils': {'LiveMigrationUtils': {'min_version': '6.0',
                                                  'max_version': 'None'}},
    'networkutils': {'NetworkUtils': {'min_version': '6.0',
                                      'max_version': '6.2'},
                     'NetworkUtilsV2': {'min_version': '6.2',
                                        'max_version': None}},
    'pathutils': {'PathUtils': {'min_version': '6.0', 'max_version': None}},
    'vmutils': {'VMUtils': {'min_version': '6.0', 'max_version': '6.2'},
                'VMUtilsV2': {'min_version': '6.2', 'max_version': '10'},
                'VMUtilsV3': {'min_version': '10', 'max_version': None}},
    'vhdutils': {'VHDUtils': {'min_version': '6.0', 'max_version': '6.2'},
                 'VHDUtilsV2': {'min_version': '6.2', 'max_version': None}},
    'volumeutils': {'VolumeUtils': {'min_version': '6.0',
                                    'max_version': '6.2'},
                    'VolumeUtilsV2': {'min_version': '6.2',
                                      'max_version': None}},
    'rdpconsoleutils': {'RDPConsoleUtils': {'min_version': '6.0',
                                            'max_version': '6.2'},
                        'RDPConsoleUtilsV2': {'min_version': '6.2',
                                              'max_version': None}},
}


def _get_class(current_class):
    windows_version = utils.get_windows_version()

    if current_class not in class_utils:
        raise vmutils.HyperVException(_('Class does not exist.'))

    existing_classes = class_utils.get(current_class)
    for class_variant in existing_classes.keys():
        version = existing_classes.get(class_variant)
        if (version['min_version'] <= windows_version and
                (version['max_version'] is None or
                 windows_version < version['max_version'])):
            found_class = class_variant
            break
    if found_class is None:
        raise Exception("Class is not found for windows version: %s"
                        % windows_version)
        return

    module_name = found_class.lower()
    module = globals()[module_name]
    instance = getattr(module, found_class)()
    return instance


def get_vmutils(host='.'):
    return _get_class(current_class='vmutils')


def get_vhdutils():
    return _get_class(current_class='vhdutils')


def get_networkutils():
    return _get_class(current_class='networkutils')


def get_hostutils():
    return _get_class(current_class='hostutils')


def get_pathutils():
    return _get_class(current_class='pathutils')


def get_volumeutils():
    return _get_class(current_class='volumeutils')


def get_livemigrationutils():
    return _get_class(current_class='livemigrationutils')


def get_rdpconsoleutils():
    return _get_class(current_class='rdpconsoleutils')
