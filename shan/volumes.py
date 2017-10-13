from gi.repository import Gio


class Volume():
    """Represents a mountable volume."""

    def __init__(self, gvolume):
        self.gvolume = gvolume
        self.unix_id = self.gvolume.get_identifier('unix-device')
        self.uuid = self.gvolume.get_uuid()
        self.mount_point = self._get_mount_point()
        self.is_mounted = self.mount_point is not None
        self.parent_drive = self._get_parent_drive()
        self.name = self.gvolume.get_name()
        self.string_representation = self._get_str_representation()

    def _get_mount_point(self):
        """Return path to volume's mount point."""
        gmount = self.gvolume.get_mount()
        try:
            mount_point = gmount.get_default_location().get_path()
            return mount_point
        except AttributeError:
            return None

    def _get_parent_drive(self):
        """Return the name of the drive that the volume is a part of."""
        gdrive = self.gvolume.get_drive()
        try:
            drive_name = gdrive.get_name()
            return drive_name
        except AttributeError:
            return None

    def _get_str_representation(self):
        """Return a string representation for the TUI."""
        if self.is_mounted:
            mount_char = 'X'
            path = self.mount_point
        else:
            mount_char = 'O'
            path = self.unix_id

        str_ = '\t'.join([mount_char, path,
                          self.uuid, self.name])
        return str_


def get_volume_list():
    """Return a list of Volume objects."""
    gvolume_list = Gio.VolumeMonitor.get().get_volumes()
    return [Volume(gvolume) for gvolume in gvolume_list]


def get_str_volume_list():
    """Return a list of string representations of all volumes."""
    return [volume.string_representation for volume in get_volume_list()]
