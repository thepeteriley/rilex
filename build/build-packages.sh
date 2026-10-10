#!/bin/bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")/.." && pwd)
STAGE="$ROOT/.build/rilex-defaults"
command -v dpkg-deb >/dev/null || { echo 'dpkg-deb is required.' >&2; exit 1; }
rm -rf -- "$STAGE"
mkdir -p "$STAGE/DEBIAN" "$STAGE/usr/bin" "$STAGE/usr/share/doc/rilex-defaults" "$ROOT/dist"
cp "$ROOT/packaging/rilex-defaults/DEBIAN/"* "$STAGE/DEBIAN/"
for tree in desktop/rootfs; do
 [[ ! -d "$ROOT/$tree" ]] || cp -a "$ROOT/$tree/." "$STAGE/"
done
for script in "$ROOT"/scripts/rilex-*; do
 [[ ! -f "$script" ]] || install -m755 "$script" "$STAGE/usr/bin/"
done
mkdir -p "$STAGE/etc/xdg/hypr" "$STAGE/etc/rilex/waybar" "$STAGE/etc/rilex/fuzzel" "$STAGE/etc/rilex/foot" "$STAGE/etc/xdg/mako" "$STAGE/etc/gtk-3.0" "$STAGE/usr/share/rilex/wallpapers" "$STAGE/usr/share/icons/hicolor/scalable/apps"
cp "$ROOT/desktop/hyprland/"* "$STAGE/etc/xdg/hypr/"
cp "$ROOT/desktop/waybar/"* "$STAGE/etc/rilex/waybar/"
cp "$ROOT/desktop/fuzzel/"* "$STAGE/etc/rilex/fuzzel/"
cp "$ROOT/desktop/terminal/foot.ini" "$STAGE/etc/rilex/foot/foot.ini"
cp "$ROOT/desktop/themes/mako.conf" "$STAGE/etc/xdg/mako/config"
cp "$ROOT/desktop/themes/gtk-settings.ini" "$STAGE/etc/gtk-3.0/settings.ini"
cp "$ROOT/desktop/wallpapers/rilex.svg" "$STAGE/usr/share/rilex/wallpapers/"
cp "$ROOT/desktop/themes/rilex-logo.svg" "$STAGE/usr/share/icons/hicolor/scalable/apps/rilex.svg"
mkdir -p "$STAGE/usr/share/rilex"
REVISION=${RILEX_SOURCE_REVISION:-$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || printf unknown)}
printf 'NAME=Rilex\nVERSION=0.1\nSOURCE_REVISION=%s\n' "$REVISION" > "$STAGE/usr/share/rilex/build-info"
printf '%s\n' "$REVISION" > "$ROOT/dist/source-revision.txt"
cp -a "$ROOT/docs/." "$STAGE/usr/share/doc/rilex-defaults/"
[[ ! -f "$ROOT/LICENSE" ]] || cp "$ROOT/LICENSE" "$STAGE/usr/share/doc/rilex-defaults/copyright"
find "$STAGE/etc" -type f -print 2>/dev/null | sed "s|$STAGE||" > "$STAGE/DEBIAN/conffiles" || true
chmod 755 "$STAGE/DEBIAN/preinst" "$STAGE/DEBIAN/postinst" "$STAGE/DEBIAN/postrm"
python3 "$ROOT/tests/test-config-paths.py" "$STAGE"
dpkg-deb --root-owner-group --build "$STAGE" "$ROOT/dist/rilex-defaults_0.1.0_all.deb"
