# Rilex packages

`build/build-packages.sh` builds `dist/rilex-defaults_0.1.0_all.deb` with Debian's `dpkg-deb`. It contains desktop defaults, original artwork, welcome helpers, and documentation. Files under `/etc` are Debian conffiles, preserving administrator edits on upgrade; per-user settings belong under `$XDG_CONFIG_HOME`.

The package is generated from the tracked `desktop`, `scripts` and `docs` source trees. The live-build overlay (Calamares settings, password locking and live autologin) is deliberately not in this package. Calamares removes its live autologin configuration and installer launchers from the installed target.

Hyprland is not custom compiled: the compositor, portal and locker are pinned official Debian trixie-backports packages in `config/hooks/live/0200-hyprland.hook.chroot`. APT validates Debian archive signatures and the package hashes covered by those signatures. Their Debian package copyright and source information remain installed. No testing or unstable suite is configured. Backports dependencies are resolved by APT using the explicit backports target for that transaction; the base kernel remains stable.

This is a repeatable build recipe, not a claim of bit-identical artifacts. Debian security and stable updates move over time. Each build records installed package versions under `/usr/share/rilex/package-manifest.tsv`. Publishing fully frozen rebuilds would require retaining the signed repository metadata and package payloads, or a reviewed Debian snapshot policy.

A Rilex update repository is not deployed by 0.1. Update Rilex defaults only using a downloaded Debian package after checking its hash against a release manifest from the authenticated GitHub release channel; `sudo apt install ./rilex-defaults_VERSION_all.deb` handles installation. A checksum alone is not a signature. Production signing/deployment must use an operator-owned archive key and signed Release/InRelease metadata; no fictional key identity or private key is included here. Debian security updates continue through Debian's normal signed APT repositories.
