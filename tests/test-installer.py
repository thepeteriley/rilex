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
    def test_no_credentials(self):
        for f in (ROOT / 'installer/rootfs').rglob('*'):
            if f.is_file():
                self.assertNotIn('password:', f.read_text())

if __name__ == '__main__':
    unittest.main()
