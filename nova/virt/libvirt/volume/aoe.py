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

from os_brick.initiator import connector
from oslo_config import cfg
from oslo_log import log as logging

from nova import utils
from nova.virt.libvirt.volume import volume as libvirt_volume

LOG = logging.getLogger(__name__)

volume_opts = [
    cfg.IntOpt('num_aoe_discover_tries',
               default=3,
               help='Number of times to rediscover AoE target to find volume'),
    ]

CONF = cfg.CONF
CONF.register_opts(volume_opts, 'libvirt')


class LibvirtAOEVolumeDriver(libvirt_volume.LibvirtBaseVolumeDriver):
    """Driver to attach AoE volumes to libvirt."""
    def __init__(self, connection):
        super(LibvirtAOEVolumeDriver,
              self).__init__(connection, is_block_dev=True)

        # Call the factory here so we can support
        # more than x86 architectures.
        self.connector = connector.InitiatorConnector.factory(
            'AOE', utils._get_root_helper(),
            device_scan_attempts=CONF.libvirt.num_aoe_discover_tries)

    def get_config(self, connection_info, disk_info):
        """Returns xml for libvirt."""
        conf = super(LibvirtAOEVolumeDriver,
                     self).get_config(connection_info, disk_info)

        conf.source_type = "block"
        conf.source_path = connection_info['data']['device_path']
        return conf

    def connect_volume(self, connection_info, mount_device):
        LOG.debug("Calling os-brick to attach AoE Volume")
        device_info = self.connector.connect_volume(connection_info['data'])
        LOG.debug("Attached AoE volume %s", device_info)

        connection_info['data']['device_path'] = device_info['path']

    def disconnect_volume(self, connection_info, disk_dev):
        """Detach the volume from instance_name."""

        LOG.debug("calling os-brick to detach AoE Volume %s",
                  connection_info)
        self.connector.disconnect_volume(connection_info['data'], None)
        LOG.debug("Disconnected AoE Volume %s", disk_dev)

        super(LibvirtAOEVolumeDriver,
              self).disconnect_volume(connection_info, disk_dev)
