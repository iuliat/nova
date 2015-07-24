# Copyright 2015 Cloudbase Solutions Srl
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

from nova.virt.hyperv import vmutilsv2


class VMUtils10(vmutilsv2.VMUtilsV2):

    _VIRTUAL_SYSTEM_SUBTYPE_GEN2 = 'Microsoft:Hyper-V:SubType:2'

    def set_secure_boot(self, vs_data, config_secure_boot):
        if config_secure_boot['os'] == 'windows':
            vs_data.SecureBootEnabled = config_secure_boot['secure_boot']
        elif config_secure_boot['os'] == 'linux':
                uefi_data = self._conn.Msvm_VirtualSystemSettingData(
                    ElementName="MicrosoftUEFICertificateAuthority")[0]
                SecureBootId = uefi_data.SecureBootTemplateId
                vs_data.SecureBootTemplateId = SecureBootId
                vs_data.SecureBootEnabled = config_secure_boot['secure_boot']
