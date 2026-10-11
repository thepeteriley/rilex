#!/usr/bin/env python3
"""Static checks supplement, and never replace, a destructive-test-disk VM installation."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'installer/rootfs/etc/calamares'

class InstallerConfiguration(unittest.TestCase):
    def test_installs_system_in_chroot(self):
        s = (BASE / 'settings.conf').read_text()
        self.assertIn('dont-chroot: false', s)
        self.assertIn('prompt-install: true', s)
        for name in ('partition', 'mount', 'unpackfs', 'fstab', 'users', 'bootloader', 'initramfs', 'umount'):
            self.assertIn('  - ' + name + '\n', s)
        self.assertLess(s.index('  - summary'), s.index('- exec:'))
        self.assertNotIn('  - bootloader-config\n', s)
        self.assertNotIn('  - sources-media\n', s)
        self.assertNotIn('  - sources-media-unmount\n', s)
        self.assertIn('  - sources-final\n', s)
    def test_installer_live_guard(self):
        s = (ROOT / 'installer/rootfs/usr/bin/rilex-install').read_text()
        self.assertIn('/run/live/medium', s)
        self.assertIn('sudo -n env', s)
        self.assertIn('xhost -si:localuser:root', s)
    def test_bootloader_platforms(self):
        s = (BASE / 'modules/bootloader.conf').read_text()
        self.assertIn('efiBootLoader: grub', s)
        self.assertIn('installEFIFallback: true', s)
    def test_installer_not_packaged_over_debian_files(self):
        s = (ROOT / 'build/build-packages.sh').read_text()
        self.assertNotIn('installer/rootfs', s)
        self.assertIn('"$ROOT/installer/rootfs/"', (ROOT / 'build/build-iso.sh').read_text())
    def test_partition_defaults_and_unverified_encryption(self):
        s = (BASE / 'modules/partition.conf').read_text()
        self.assertIn('enableLuksAutomatedPartitioning: false', s)
        self.assertIn('allowManualPartitioning: true', s)
        self.assertIn('mountPoint:         "/boot/efi"', s)
        self.assertIn('userSwapChoices:', s)
        self.assertIn('initialPartitioningChoice: none', s)
        self.assertIn('defaultFileSystemType:  "ext4"', s)
    def test_branding_requires_slideshow(self):
        s = (BASE / 'branding/rilex/branding.desc').read_text()
        self.assertIn('slideshow: show.qml', s)
        self.assertIn('slideshowAPI: 2', s)
        self.assertTrue((BASE / 'branding/rilex/show.qml').is_file())
    def test_no_credentials(self):
        for f in (ROOT / 'installer/rootfs').rglob('*'):
            if f.is_file():
                self.assertNotIn('password:', f.read_text())

if __name__ == '__main__':
    unittest.main()
