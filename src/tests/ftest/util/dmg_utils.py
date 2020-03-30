#!/usr/bin/python
"""
  (C) Copyright 2018-2020 Intel Corporation.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  GOVERNMENT LICENSE RIGHTS-OPEN SOURCE SOFTWARE
  The Government's rights to use, modify, reproduce, release, perform, display,
  or disclose this software are subject to the terms of the Apache License as
  provided in Contract No. B609815.
  Any reproduction of computer software, computer software documentation, or
  portions thereof marked with this legend must also reproduce the markings.
"""
from __future__ import print_function

from getpass import getuser
from grp import getgrgid
from pwd import getpwuid
import re

from command_utils import \
    CommandWithParameters, FormattedParameter, CommandFailure, \
    CommandWithSubCommand


class DmgCommand(CommandWithSubCommand):
    """Defines a object representing a dmg command."""

    def __init__(self, path):
        """Create a dmg Command object.

        Args:
            path (str): path to the dmg command
        """
        super(DmgCommand, self).__init__("/run/dmg/*", "dmg", path)

        self.hostlist = FormattedParameter("-l {}")
        self.hostfile = FormattedParameter("-f {}")
        self.configpath = FormattedParameter("-o {}")
        self.insecure = FormattedParameter("-i", True)
        self.debug = FormattedParameter("-d", False)
        self.json = FormattedParameter("-j", False)

    def set_hostlist(self, manager):
        """Set the dmg hostlist parameter with the daos server/agent info.

        Use the daos server/agent access points port and list of hosts to define
        the dmg --hostlist command line parameter.

        Args:
            manager (SubprocessManager): daos server/agent process manager
        """
        self.hostlist.update(
            manager.get_config_value("access_points"), "dmg.hostlist")

    def get_sub_command_class(self):
        # pylint: disable=redefined-variable-type
        """Get the dmg sub command object based upon the sub-command."""
        if self.sub_command.value == "network":
            self.sub_command_class = self.NetworkSubCommand()
        elif self.sub_command.value == "pool":
            self.sub_command_class = self.PoolSubCommand()
        elif self.sub_command.value == "storage":
            self.sub_command_class = self.StorageSubCommand()
        elif self.sub_command.value == "system":
            self.sub_command_class = self.SystemSubCommand()
        else:
            self.sub_command_class = None

    class NetworkSubCommand(CommandWithSubCommand):
        """Defines an object for the dmg network sub command."""

        def __init__(self):
            """Create a dmg network subcommand object."""
            super(DmgCommand.NetworkSubCommand, self).__init__(
                "/run/dmg/network/*", "network")

        def get_sub_command_class(self):
            # pylint: disable=redefined-variable-type
            """Get the dmg network sub command object."""
            if self.sub_command.value == "scan":
                self.sub_command_class = self.ScanSubCommand()
            else:
                self.sub_command_class = None

        class ScanSubCommand(CommandWithParameters):
            """Defines an object for the dmg network scan command."""

            def __init__(self):
                """Create a dmg network scan command object."""
                super(
                    DmgCommand.NetworkSubCommand.ScanSubCommand, self).__init__(
                        "/run/dmg/network/scan/*", "scan")
                self.provider = FormattedParameter("-p {}", None)
                self.all = FormattedParameter("-a", False)

    class PoolSubCommand(CommandWithSubCommand):
        """Defines an object for the dmg pool sub command."""

        def __init__(self):
            """Create a dmg pool subcommand object."""
            super(DmgCommand.PoolSubCommand, self).__init__(
                "/run/dmg/pool/*", "pool")

        def get_sub_command_class(self):
            # pylint: disable=redefined-variable-type
            """Get the dmg pool sub command object."""
            if self.sub_command.value == "create":
                self.sub_command_class = self.CreateSubCommand()
            elif self.sub_command.value == "delete-acl":
                self.sub_command_class = self.DeleteAclSubCommand()
            elif self.sub_command.value == "destroy":
                self.sub_command_class = self.DestroySubCommand()
            elif self.sub_command.value == "get-acl":
                self.sub_command_class = self.GetAclSubCommand()
            elif self.sub_command.value == "list":
                self.sub_command_class = self.ListSubCommand()
            elif self.sub_command.value == "overwrite-acl":
                self.sub_command_class = self.OverwriteAclSubCommand()
            elif self.sub_command.value == "query":
                self.sub_command_class = self.QuerySubCommand()
            elif self.sub_command.value == "set-prop":
                self.sub_command_class = self.SetPropSubCommand()
            elif self.sub_command.value == "update-acl":
                self.sub_command_class = self.UpdateAclSubCommand()
            else:
                self.sub_command_class = None

        class CreateSubCommand(CommandWithParameters):
            """Defines an object for the dmg pool create command."""

            def __init__(self):
                """Create a dmg pool create command object."""
                super(
                    DmgCommand.PoolSubCommand.CreateSubCommand,
                    self).__init__(
                        "/run/dmg/pool/create/*", "create")
                self.group = FormattedParameter("--group={}", None)
                self.user = FormattedParameter("--user={}", None)
                self.acl_file = FormattedParameter("--acl-file={}", None)
                self.scm_size = FormattedParameter("--scm-size={}", None)
                self.nvme_size = FormattedParameter("--nvme-size={}", None)
                self.ranks = FormattedParameter("--ranks={}", None)
                self.nsvc = FormattedParameter("--nsvc={}", None)
                self.sys = FormattedParameter("--sys={}", None)

        class DeleteAclSubCommand(CommandWithParameters):
            """Defines an object for the dmg pool delete-acl command."""

            def __init__(self):
                """Create a dmg pool delete-acl command object."""
                super(
                    DmgCommand.PoolSubCommand.DeleteAclSubCommand,
                    self).__init__(
                        "/run/dmg/pool/delete-acl/*", "delete-acl")
                self.pool = FormattedParameter("--pool={}", None)
                self.principal = FormattedParameter("-p {}", None)

        class DestroySubCommand(CommandWithParameters):
            """Defines an object for the dmg pool destroy command."""

            def __init__(self):
                """Create a dmg pool destroy command object."""
                super(
                    DmgCommand.PoolSubCommand.DestroySubCommand,
                    self).__init__(
                        "/run/dmg/pool/destroy/*", "destroy")
                self.pool = FormattedParameter("--pool={}", None)
                self.sys_name = FormattedParameter("--sys-name={}", None)
                self.force = FormattedParameter("--force", False)

        class GetAclSubCommand(CommandWithParameters):
            """Defines an object for the dmg pool get-acl command."""

            def __init__(self):
                """Create a dmg pool get-acl command object."""
                super(
                    DmgCommand.PoolSubCommand.GetAclSubCommand,
                    self).__init__(
                        "/run/dmg/pool/get-acl/*", "get-acl")
                self.pool = FormattedParameter("--pool={}", None)

        class ListSubCommand(CommandWithParameters):
            """Defines an object for the dmg pool list command."""

            def __init__(self):
                """Create a dmg pool list command object."""
                super(
                    DmgCommand.PoolSubCommand.ListSubCommand,
                    self).__init__(
                        "/run/dmg/pool/list/*", "list")

        class OverwriteAclSubCommand(CommandWithParameters):
            """Defines an object for the dmg pool overwrite-acl command."""

            def __init__(self):
                """Create a dmg pool overwrite-acl command object."""
                super(
                    DmgCommand.PoolSubCommand.OverwriteAclSubCommand,
                    self).__init__(
                        "/run/dmg/pool/overwrite-acl/*", "overwrite-acl")
                self.pool = FormattedParameter("--pool={}", None)
                self.acl_file = FormattedParameter("-a {}", None)

        class QuerySubCommand(CommandWithParameters):
            """Defines an object for the dmg pool query command."""

            def __init__(self):
                """Create a dmg pool query command object."""
                super(
                    DmgCommand.PoolSubCommand.QuerySubCommand,
                    self).__init__(
                        "/run/dmg/pool/query/*", "query")
                self.pool = FormattedParameter("--pool={}", None)

        class SetPropSubCommand(CommandWithParameters):
            """Defines an object for the dmg pool set-prop command."""

            def __init__(self):
                """Create a dmg pool set-prop command object."""
                super(
                    DmgCommand.PoolSubCommand.SetPropSubCommand,
                    self).__init__(
                        "/run/dmg/pool/set-prop/*", "set-prop")
                self.pool = FormattedParameter("--pool={}", None)
                self.name = FormattedParameter("--name={}", None)
                self.value = FormattedParameter("--value={}", None)

        class UpdateAclSubCommand(CommandWithParameters):
            """Defines an object for the dmg pool update-acl command."""

            def __init__(self):
                """Create a dmg pool update-acl command object."""
                super(
                    DmgCommand.PoolSubCommand.UpdateAclSubCommand,
                    self).__init__(
                        "/run/dmg/pool/update-acl/*", "update-acl")
                self.pool = FormattedParameter("--pool={}", None)
                self.acl_file = FormattedParameter("-a {}", None)
                self.entry = FormattedParameter("-e {}", None)

    class StorageSubCommand(CommandWithSubCommand):
        """Defines an object for the dmg storage sub command."""

        def __init__(self):
            """Create a dmg storage subcommand object."""
            super(DmgCommand.StorageSubCommand, self).__init__(
                "/run/dmg/storage/*", "storage")

        def get_sub_command_class(self):
            # pylint: disable=redefined-variable-type
            """Get the dmg storage sub command object."""
            if self.sub_command.value == "format":
                self.sub_command_class = self.FormatSubCommand()
            elif self.sub_command.value == "prepare":
                self.sub_command_class = self.PrepareSubCommand()
            elif self.sub_command.value == "query":
                self.sub_command_class = self.QuerySubCommand()
            elif self.sub_command.value == "scan":
                self.sub_command_class = self.ScanSubCommand()
            elif self.sub_command.value == "set":
                self.sub_command_class = self.SetSubCommand()
            else:
                self.sub_command_class = None

        class FormatSubCommand(CommandWithParameters):
            """Defines an object for the dmg storage format command."""

            def __init__(self):
                """Create a dmg storage format command object."""
                super(
                    DmgCommand.StorageSubCommand.FormatSubCommand,
                    self).__init__(
                        "/run/dmg/storage/format/*", "format")
                self.reformat = FormattedParameter("--reformat", False)

        class PrepareSubCommand(CommandWithParameters):
            """Defines an object for the dmg storage format command."""

            def __init__(self):
                """Create a dmg storage prepare command object."""
                super(
                    DmgCommand.StorageSubCommand.PrepareSubCommand,
                    self).__init__(
                        "/run/dmg/storage/prepare/*", "prepare")
                self.pci_whitelist = FormattedParameter("-w {}", None)
                self.hugepages = FormattedParameter("-p {}", None)
                self.target_user = FormattedParameter("-u {}", None)
                self.nvme_only = FormattedParameter("-n", False)
                self.scm_only = FormattedParameter("-s", False)
                self.reset = FormattedParameter("--reset", False)
                self.force = FormattedParameter("-f", False)

        class QuerySubCommand(CommandWithSubCommand):
            """Defines an object for the dmg query format command."""

            def __init__(self):
                """Create a dmg storage query command object."""
                super(
                    DmgCommand.StorageSubCommand.QuerySubCommand,
                    self).__init__(
                        "/run/dmg/storage/query/*", "query")

            def get_sub_command_class(self):
                # pylint: disable=redefined-variable-type
                """Get the dmg pool sub command object."""
                if self.sub_command.value == "blobstore-health":
                    self.sub_command_class = self.BlobstoreHealthSubCommand()
                elif self.sub_command.value == "device-state":
                    self.sub_command_class = self.DeviceStateSubCommand()
                elif self.sub_command.value == "nvme-health":
                    self.sub_command_class = self.NvmeHealthSubCommand()
                elif self.sub_command.value == "smd":
                    self.sub_command_class = self.SmdSubCommand()
                else:
                    self.sub_command_class = None

            class BlobstoreHealthSubCommand(CommandWithParameters):
                """Defines a dmg storage query blobstore-health object."""

                def __init__(self):
                    """Create a dmg storage query blobstore-health object."""
                    super(
                        DmgCommand.StorageSubCommand.QuerySubCommand.
                        BlobstoreHealthSubCommand,
                        self).__init__(
                            "/run/dmg/storage/query/blobstore-health/*",
                            "blobstore-health")
                    self.devuuid = FormattedParameter("-u {}", None)
                    self.tgtid = FormattedParameter("-t {}", None)

            class DeviceStateSubCommand(CommandWithParameters):
                """Defines a dmg storage query device-state object."""

                def __init__(self):
                    """Create a dmg storage query device-state object."""
                    super(
                        DmgCommand.StorageSubCommand.QuerySubCommand.
                        DeviceStateSubCommand,
                        self).__init__(
                            "/run/dmg/storage/query/device-state/*",
                            "device-state")
                    self.devuuid = FormattedParameter("-u {}", None)

            class NvmeHealthSubCommand(CommandWithParameters):
                """Defines a dmg storage query nvme-health object."""

                def __init__(self):
                    """Create a dmg storage query nvme-health object."""
                    super(
                        DmgCommand.StorageSubCommand.QuerySubCommand.
                        NvmeHealthSubCommand,
                        self).__init__(
                            "/run/dmg/storage/query/nvme-health/*",
                            "nvme-health")

            class SmdSubCommand(CommandWithParameters):
                """Defines a dmg storage query smd object."""

                def __init__(self):
                    """Create a dmg storage query smd object."""
                    super(
                        DmgCommand.StorageSubCommand.QuerySubCommand.
                        SmdSubCommand,
                        self).__init__(
                            "/run/dmg/storage/query/smd/*",
                            "smd")
                    self.devices = FormattedParameter("-d", False)
                    self.pools = FormattedParameter("-p", False)

        class ScanSubCommand(CommandWithParameters):
            """Defines an object for the dmg storage scan command."""

            def __init__(self):
                """Create a dmg storage scan command object."""
                super(
                    DmgCommand.StorageSubCommand.ScanSubCommand,
                    self).__init__(
                        "/run/dmg/storage/scan/*", "scan")
                self.summary = FormattedParameter("-m", False)

        class SetSubCommand(CommandWithParameters):
            """Defines an object for the dmg storage set command."""

            def __init__(self):
                """Create a dmg storage set command object."""
                super(
                    DmgCommand.StorageSubCommand.SetSubCommand,
                    self).__init__(
                        "/run/dmg/storage/set/*", "set")
                self.nvme_faulty = FormattedParameter("nvme-faulty", False)

    class SystemSubCommand(CommandWithSubCommand):
        """Defines an object for the dmg system sub command."""

        def __init__(self):
            """Create a dmg system subcommand object."""
            super(DmgCommand.SystemSubCommand, self).__init__(
                "/run/dmg/system/*", "system")

        def get_sub_command_class(self):
            # pylint: disable=redefined-variable-type
            """Get the dmg system sub command object."""
            if self.sub_command.value == "leader-query":
                self.sub_command_class = self.LeaderQuerySubCommand()
            elif self.sub_command.value == "list-pools":
                self.sub_command_class = self.ListPoolsSubCommand()
            elif self.sub_command.value == "query":
                self.sub_command_class = self.QuerySubCommand()
            elif self.sub_command.value == "start":
                self.sub_command_class = self.StartSubCommand()
            elif self.sub_command.value == "stop":
                self.sub_command_class = self.StopSubCommand()
            else:
                self.sub_command_class = None

        class LeaderQuerySubCommand(CommandWithParameters):
            """Defines an object for the dmg system leader-query command."""

            def __init__(self):
                """Create a dmg system leader-query command object."""
                super(
                    DmgCommand.SystemSubCommand.LeaderQuerySubCommand,
                    self).__init__(
                        "/run/dmg/system/leader-query/*", "leader-query")

        class ListPoolsSubCommand(CommandWithParameters):
            """Defines an object for the dmg system list-pools command."""

            def __init__(self):
                """Create a dmg system list-pools command object."""
                super(
                    DmgCommand.SystemSubCommand.ListPoolsSubCommand,
                    self).__init__(
                        "/run/dmg/system/list-pools/*", "list-pools")

        class QuerySubCommand(CommandWithParameters):
            """Defines an object for the dmg system query command."""

            def __init__(self):
                """Create a dmg system query command object."""
                super(
                    DmgCommand.SystemSubCommand.QuerySubCommand,
                    self).__init__(
                        "/run/dmg/system/query/*", "query")
                self.rank = FormattedParameter("--rank={}")
                self.verbose = FormattedParameter("--verbose", False)

        class StartSubCommand(CommandWithParameters):
            """Defines an object for the dmg system start command."""

            def __init__(self):
                """Create a dmg system start command object."""
                super(
                    DmgCommand.SystemSubCommand.StartSubCommand,
                    self).__init__(
                        "/run/dmg/system/start/*", "start")

        class StopSubCommand(CommandWithParameters):
            """Defines an object for the dmg system stop command."""

            def __init__(self):
                """Create a dmg system stop command object."""
                super(
                    DmgCommand.SystemSubCommand.StopSubCommand,
                    self).__init__(
                        "/run/dmg/system/stop/*", "stop")
                self.force = FormattedParameter("--force", False)

    def _get_result(self):
        """Get the result from running the configured dmg command.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg command fails.

        """
        result = None
        try:
            result = self.run()
        except CommandFailure as error:
            raise CommandFailure("<dmg> command failed: {}".format(error))

        return result

    def storage_scan(self):
        """Get the result of the dmg storage scan command.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg storage scan command fails.

        """
        self.set_sub_command("storage")
        self.sub_command_class.set_sub_command("scan")
        return self._get_result()

    def storage_format(self):
        """Get the result of the dmg storage format command.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg storage format command fails.

        """
        self.set_sub_command("storage")
        self.sub_command_class.set_sub_command("format")
        return self._get_result()

    def storage_prepare(self, user=None, hugepages="4096", nvme=False,
                        scm=False, reset=False, force=True):
        """Get the result of the dmg storage format command.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg storage prepare command fails.

        """
        self.set_sub_command("storage")
        self.sub_command_class.set_sub_command("prepare")
        self.sub_command_class.sub_command_class.nvme_only.value = nvme
        self.sub_command_class.sub_command_class.scm_only.value = scm
        self.sub_command_class.sub_command_class.target_user.value = \
            getuser() if user is None else user
        self.sub_command_class.sub_command_class.hugepages.value = hugepages
        self.sub_command_class.sub_command_class.reset.value = reset
        self.sub_command_class.sub_command_class.force.value = force
        return self._get_result()

    def storage_query_smd(self, devices=True, pools=True):
        """Get the result of the 'dmg storage query smd' command.

        Args:
            devices (bool, optional): List all devices/blobstores stored in
                per-server metadata table. Defaults to True.
            pools (bool, optional): List all VOS pool targets stored in
                per-server metadata table. Defaults to True.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg storage prepare command fails.

        """
        self.set_sub_command("storage")
        self.sub_command_class.set_sub_command("query")
        self.sub_command_class.sub_command_class.set_sub_command("smd")
        self.sub_command_class. \
            sub_command_class.sub_command_class.devices.value = devices
        self.sub_command_class. \
            sub_command_class.sub_command_class.pools.value = pools
        return self._get_result()

    def storage_query_blobstore(self, devuuid, tgtid=None):
        """Get the result of the 'dmg storage query blobstore-health' command.

        Args:
            devuuid (str, optional): Device/Blobstore UUID to query.
                Defaults to None.
            tgtid (str, optional): VOS target ID to query. Defaults to None.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg storage prepare command fails.

        """
        self.set_sub_command("storage")
        self.sub_command_class.set_sub_command("query")
        self.sub_command_class. \
            sub_command_class.set_sub_command("blobstore-health")
        self.sub_command_class. \
            sub_command_class.sub_command_class.devuuid.value = devuuid
        self.sub_command_class. \
            sub_command_class.sub_command_class.tgtid.value = tgtid
        return self._get_result()

    def storage_query_device_state(self, devuuid):
        """Get the result of the 'dmg storage query device-state' command.

        Args:
            devuuid (str, optional): Device/Blobstore UUID to query.
                Defaults to None.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg storage prepare command fails.

        """
        self.set_sub_command("storage")
        self.sub_command_class.set_sub_command("query")
        self.sub_command_class. \
            sub_command_class.set_sub_command("device-state")
        self.sub_command_class. \
            sub_command_class.sub_command_class.devuuid.value = devuuid
        return self._get_result()

    def storage_query_nvme_health(self):
        """Get the result of the 'dmg storage query nvme-health' command.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg storage prepare command fails.

        """
        self.set_sub_command("storage")
        self.sub_command_class.set_sub_command("query")
        self.sub_command_class. \
            sub_command_class.set_sub_command("nvme-health")
        return self._get_result()

    def pool_create(self, scm_size, uid=None, gid=None, nvme_size=None,
                    target_list=None, svcn=None, group=None, acl_file=None):
        """Create a pool with the dmg command.

        The uid and gid method arguments can be specified as either an integer
        or a string.  If an integer value is specified it will be converted into
        the corresponding user/group name string.

        Args:
            scm_size (int): SCM pool size to create.
            uid (object, optional): User ID with privileges. Defaults to None.
            gid (object, otional): Group ID with privileges. Defaults to None.
            nvme_size (str, optional): NVMe size. Defaults to None.
            target_list (list, optional): a list of storage server unique
                identifiers (ranks) for the DAOS pool
            svcn (str, optional): Number of pool service replicas. Defaults to
                None, in which case 1 is used by the dmg binary in default.
            group (str, optional): DAOS system group name in which to create the
                pool. Defaults to None, in which case "daos_server" is used by
                default.
            acl_file (str, optional): ACL file. Defaults to None.

        Returns:
            CmdResult: an avocado CmdResult object containing the dmg command
                information, e.g. exit status, stdout, stderr, etc.

        Raises:
            CommandFailure: if the dmg pool create command fails.

        """
        self.set_sub_command("pool")
        self.sub_command_class.set_sub_command("create")
        self.sub_command_class.sub_command_class.user.value = \
            getpwuid(uid).pw_name if isinstance(uid, int) else uid
        self.sub_command_class.sub_command_class.group.value = \
            getgrgid(gid).gr_name if isinstance(gid, int) else gid
        self.sub_command_class.sub_command_class.scm_size.value = scm_size
        self.sub_command_class.sub_command_class.nvme_size.value = nvme_size
        if target_list is not None:
            self.sub_command_class.sub_command_class.ranks.value = ",".join(
                [str(target) for target in target_list])
        self.sub_command_class.sub_command_class.nsvc.value = svcn
        self.sub_command_class.sub_command_class.sys.value = group
        self.sub_command_class.sub_command_class.acl_file.value = acl_file
        return self._get_result()

    def pool_destroy(self, pool, force=True):
        """Destroy a pool with the dmg command.

        Args:
            pool (str): Pool UUID to destroy.
            force (bool, optional): Force removal of pool. Defaults to True.

        Returns:
            CmdResult: Object that contains exit status, stdout, and other
                information.

        Raises:
            CommandFailure: if the dmg pool destroy command fails.

        """
        self.set_sub_command("pool")
        self.sub_command_class.set_sub_command("destroy")
        self.sub_command_class.sub_command_class.pool.value = pool
        self.sub_command_class.sub_command_class.force.value = force
        return self._get_result()

    def pool_get_acl(self, pool):
        """Get the ACL for a given pool.

        Args:
            pool (str): Pool for which to get the ACL.

        Returns:
            CmdResult: Object that contains exit status, stdout, and other
                information.

        Raises:
            CommandFailure: if the dmg pool get-acl command fails.

        """
        self.set_sub_command("pool")
        self.sub_command_class.set_sub_command("get-acl")
        self.sub_command_class.sub_command_class.pool.value = pool
        return self._get_result()

    def pool_update_acl(self, pool, acl_file, entry):
        """Update the acl for a given pool.

        Args:
            pool (str): Pool for which to update the ACL.
            acl_file (str): ACL file to update
            entry (str): entry to be updated

        Returns:
            CmdResult: Object that contains exit status, stdout, and other
                information.

        Raises:
            CommandFailure: if the dmg pool update-acl command fails.

        """
        self.set_sub_command("pool")
        self.sub_command_class.set_sub_command("update-acl")
        self.sub_command_class.sub_command_class.pool.value = pool
        self.sub_command_class.sub_command_class.acl_file.value = acl_file
        self.sub_command_class.sub_command_class.entry.value = entry
        return self._get_result()

    def pool_overwrite_acl(self, pool, acl_file):
        """Overwrite the acl for a given pool.

        Args:
            pool (str): Pool for which to overwrite the ACL.
            acl_file (str): ACL file to update

        Returns:
            CmdResult: Object that contains exit status, stdout, and other
                information.

        Raises:
            CommandFailure: if the dmg pool overwrite-acl command fails.

        """
        self.set_sub_command("pool")
        self.sub_command_class.set_sub_command("overwrite-acl")
        self.sub_command_class.sub_command_class.pool.value = pool
        self.sub_command_class.sub_command_class.acl_file.value = acl_file
        return self._get_result()

    def pool_delete_acl(self, pool, principal):
        """Delete the acl for a given pool.

        Args:
            pool (str): Pool for which to delete the ACL.
            principal (str): principal to be deleted

        Returns:
            CmdResult: Object that contains exit status, stdout, and other
                information.

        Raises:
            CommandFailure: if the dmg pool delete-acl command fails.

        """
        self.set_sub_command("pool")
        self.sub_command_class.set_sub_command("delete-acl")
        self.sub_command_class.sub_command_class.pool.value = pool
        self.sub_command_class.sub_command_class.principal.value = principal
        return self._get_result()


def get_pool_uuid_service_replicas_from_stdout(stdout_str):
    """Get Pool UUID and Service replicas from stdout.

    stdout_str is something like:
    Active connections: [wolf-3:10001]
    Creating DAOS pool with 100MB SCM and 0B NvMe storage (1.000 ratio)
    Pool-create command SUCCEEDED: UUID: 9cf5be2d-083d-4f6b-9f3e-38d771ee313f,
    Service replicas: 0
    This method makes it easy to create a test.

    Args:
        stdout_str (str): Output of pool create command.

    Returns:
        Tuple (str, str): Tuple that contains two items; Pool UUID and Service
            replicas if found. If not found, the tuple contains None.

    """
    # Find the following with regex. One or more of whitespace after "UUID:"
    # followed by one of more of number, alphabets, or -. Use parenthesis to
    # get the returned value.
    uuid = None
    svc = None
    match = re.search(r" UUID: (.+), Service replicas: (.+)", stdout_str)
    if match:
        uuid = match.group(1)
        svc = match.group(2)
    return uuid, svc


def query_smd_info(stdout_str):
    """Get storage query smd command information from stdout.

    Example output:
    boro-10:10001: connected
    SMD Device List:
    boro-10:10001:
            Device:
                    UUID: c2a1f8f6-fa89-4cda-b133-07f6fde9e868
                    VOS Target IDs: 0 1 2 3

    SMD Pool List:
    boro-10:10001:
            Pool:
                    UUID: b11ab5e3-0e2a-4858-b3bd-c4d572cc8b11
                    VOS Target IDs: 3 2 1 0
                    SPDK Blobs: 4294967296 4294967297 4294967298 4294967299

    Args:
    stdout_str (str): Output of dmg storage query create command.

    Returns:
        Dict (key, value): Dictionary that contains the contents query smd.
    """
    devs_pattern = r"""(?:\s+|\n|\r\n)([0-9a-zA-Z_-]+):\d+:
        (?:\s+|\n|\r\n)(?:\s+Device:)
        (?:\s+|\n|\r\n)\s+UUID:\s+([a-f0-9-]+)
        (?:\s+|\n|\r\n)\s+VOS\s+Target\s+IDs:\s+([\d+\s+]+\d+)"""

    pools_pattern = r"""(?:\s+|\n|\r\n)([0-9a-zA-Z_-]+):\d+:
        (?:\s+|\n|\r\n)(?:\s+Pool:)
        (?:\s+|\n|\r\n)\s+UUID:\s+([a-f0-9-]+)
        (?:\s+|\n|\r\n)\s+VOS\s+Target\s+IDs:\s+([\d+\s+]+\d+)
        (?:\s+|\n|\r\n)\s+SPDK\s+Blobs:\s+([\d+\s+]+\d+)"""

    info = []
    for pattern in devs_pattern, pools_pattern:
        try:
            info = re.findall(pattern, stdout_str, re.M | re.I | re.VERBOSE)
        except re.error as err:
            print("<regex> error: {}".format(err.args[0]))

    return info


def query_blobstore_info(stdout_str):
    """Get storage query smd command information from stdout.

    Example output:
        boro-10:10001: connected
        Blobstore Health Data:
        boro-10:10001:
            Device UUID: c2a1f8f6-fa89-4cda-b133-07f6fde9e868
            Read errors: 0
            Write errors: 0
            Unmap errors: 0
            Checksum errors: 0
            Device Health:
                    Error log entries: 0
                    Media errors: 0
                    Temperature: 287
                    Temperature: OK
                    Available Spare: OK
                    Device Reliability: OK
                    Read Only: OK
                    Volatile Memory Backup: OK

    Args:
    stdout_str (str): Output of dmg storage query create command.

    Returns:
        Dict (key, value): Dictionary that contains the contents query smd.
    """
    pattern = r"""^([0-9a-zA-Z_-]+):\d+:
        (?:\s+|\n|\r\n)\s+Device\s+UUID:\s+([a-f0-9-]+)
        (?:\s+|\n|\r\n)\s+Read\s+errors:\s+([0-9]+)
        (?:\s+|\n|\r\n)\s+Write\s+errors:\s+([0-9]+)
        (?:\s+|\n|\r\n)\s+Unmap\s+errors:\s+([0-9]+)
        (?:\s+|\n|\r\n)\s+Checksum\s+errors:\s+([0-9]+)
        (?:\s+|\n|\r\n)\s+[0-9a-zA-Z_-]+\s+[0-9a-zA-Z_-]+:
        (?:\s+|\n|\r\n)\s+Error\s+log\s+entries:\s+([0-9]+)
        (?:\s+|\n|\r\n)\s+Media\s+errors:\s+([0-9]+)
        (?:\s+|\n|\r\n)\s+Temperature:\s+([0-9]+)
        (?:\s+|\n|\r\n)\s+Temperature:\s+([A-Z]+)
        (?:\s+|\n|\r\n)\s+Available\s+Spare:\s+([A-Z]+)
        (?:\s+|\n|\r\n)\s+Device\s+Reliability:\s+([A-Z]+)
        (?:\s+|\n|\r\n)\s+Read\s+Only:\s+([A-Z]+)
        (?:\s+|\n|\r\n)\s+Volatile\s+Memory\s+Backup:\s+([A-Z]+)"""
    info = []
    try:
        info = re.findall(pattern, stdout_str, re.M | re.I | re.VERBOSE)
    except re.error as err:
        print("<regex> error: {}".format(err.args[0]))
    return info


def query_device_state_info(stdout_str):
    """Get storage query smd command information from stdout.

    Example output:
        boro-10:10001: connected
            Device State Info:
            boro-10:10001:
                    Device UUID: c2a1f8f6-fa89-4cda-b133-07f6fde9e868
                    State: NORMAL

    Args:
    stdout_str (str): Output of dmg storage query create command.

    Returns:
        Dict (key, value): Dictionary that contains the contents query smd.
    """
    pattern = r"""^([0-9a-zA-Z_-]+):\d+:
        (?:\s+|\n|\r\n)\s+Device\s+UUID:\s+([a-f0-9-]+)
        (?:\s+|\n|\r\n)\s+State:\s+([a-zA-Z]+)"""
    info = []
    try:
        info = re.findall(pattern, stdout_str, re.MULTILINE | re.VERBOSE)
    except re.error as err:
        print("<regex> error: {}".format(err.args[0]))
    return info


# ************************************************************************
# *** External usage should be replaced by DmgCommand.storage_format() ***
# ************************************************************************
def storage_format(path, hosts, insecure=True):
    """Execute format command through dmg tool to servers provided.

    Args:
        path (str): path to tool's binary
        hosts (list): list of servers to run format on.
        insecure (bool): toggle insecure mode

    Returns:
        Avocado CmdResult object that contains exit status, stdout information.

    """
    # Create and setup the command
    dmg = DmgCommand(path)
    dmg.insecure.value = insecure
    dmg.hostlist.value = hosts

    try:
        result = dmg.storage_format()
    except CommandFailure as details:
        print("<dmg> command failed: {}".format(details))
        return None

    return result
