# Updates
Use `sudo apt update` and `sudo apt upgrade` for Debian packages. Hyprland is
provided by official Trixie backports; updates for installed backport packages
follow Debian's backports policy. Read upgrade output before approving changes.
Do not enable Testing or Unstable archives.

Rilex defaults are a local Debian package. Version 0.1 has no hosted Rilex APT
repository or invented signing identity. Until that infrastructure exists,
maintainers build a versioned .deb from a reviewed tagged source revision and
publish it with signed release metadata. Users verify the maintainer signature
and SHA-256 before installing with `sudo apt install ./rilex-defaults_VERSION_all.deb`.
A checksum alone proves integrity, not publisher authenticity. Unsigned
third-party binaries must not be presented as verified Rilex updates.

Future infrastructure: publish separate suite/component indexes with aptly or
reprepro, sign Release/InRelease using an offline-controlled release key, ship
only its public key in a dedicated keyring package, and scope Signed-By to that
repository. Never commit private keys. CI builds cannot sign public releases
without an explicitly configured protected signing process. Debian sources and
security updates remain independent of this repository.
