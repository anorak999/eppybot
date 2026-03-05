#!/usr/bin/env bash
set -euo pipefail

APP_NAME="eppybot"
VERSION="1.0.1"
ARCH="amd64"
WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKGROOT="$WORKDIR/build/deb/${APP_NAME}_${VERSION}_${ARCH}"
OUTDIR="$WORKDIR/dist-deb"

if [[ ! -f "$WORKDIR/eppybot.py" ]]; then
  echo "Error: missing application source at eppybot.py"
  exit 1
fi

rm -rf "$PKGROOT"
mkdir -p "$PKGROOT/DEBIAN"
mkdir -p "$PKGROOT/opt/eppybot"
mkdir -p "$PKGROOT/usr/bin"
mkdir -p "$PKGROOT/usr/share/applications"
mkdir -p "$PKGROOT/usr/share/pixmaps"

install -m 0644 "$WORKDIR/eppybot.py" "$PKGROOT/opt/eppybot/eppybot.py"
install -m 0644 "$WORKDIR/eppybot_icon.png" "$PKGROOT/usr/share/pixmaps/eppybot.png"
install -m 0644 "$WORKDIR/packaging/eppybot.desktop" "$PKGROOT/usr/share/applications/eppybot.desktop"

cat > "$PKGROOT/usr/bin/eppybot" <<'LAUNCHER'
#!/usr/bin/env bash
exec /usr/bin/python3 /opt/eppybot/eppybot.py "$@"
LAUNCHER
chmod 0755 "$PKGROOT/usr/bin/eppybot"

cat > "$PKGROOT/DEBIAN/control" <<CONTROL
Package: ${APP_NAME}
Version: ${VERSION}
Section: graphics
Priority: optional
Architecture: ${ARCH}
Maintainer: EppyBot Maintainers <maintainers@example.com>
Depends: python3, python3-tk, python3-pil, python3-pil.imagetk
Description: Professional Image Enhancement Suite
 Desktop image enhancement application with 4K upscaling.
CONTROL

cat > "$PKGROOT/DEBIAN/postinst" <<'POSTINST'
#!/usr/bin/env bash
set -e
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database /usr/share/applications || true
fi
POSTINST
chmod 0755 "$PKGROOT/DEBIAN/postinst"

cat > "$PKGROOT/DEBIAN/postrm" <<'POSTRM'
#!/usr/bin/env bash
set -e
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database /usr/share/applications || true
fi
POSTRM
chmod 0755 "$PKGROOT/DEBIAN/postrm"

mkdir -p "$OUTDIR"
OUTPUT_DEB="$OUTDIR/${APP_NAME}_${VERSION}_${ARCH}.deb"
dpkg-deb --root-owner-group --build "$PKGROOT" "$OUTPUT_DEB"

echo "Built: $OUTPUT_DEB"
