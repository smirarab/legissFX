#!/usr/bin/env python3
"""Verify four CI artifacts before preparing assets for an unpublished release."""
import hashlib
import os
from pathlib import Path
import shutil
import sys

TARGETS = ("mac-aarch64", "mac-x64", "windows-x64", "linux-x64")


def prepare(source, destination):
    packages = []
    for target in TARGETS:
        folder = source / f"LEGv8-0.71-{target}-unsigned"
        extension = "tar.gz" if target == "linux-x64" else "zip"
        name = f"LEGv8-0.71-{target}.{extension}"
        package = folder / name
        checksum = folder / "SHA256SUMS.txt"
        if not package.is_file() or not checksum.is_file():
            raise ValueError(f"Missing package or checksum for {target}")
        rows = [line.split() for line in checksum.read_text().splitlines() if line.strip()]
        if len(rows) != 1 or len(rows[0]) != 2 or rows[0][1] != name:
            raise ValueError(f"Unexpected checksum manifest for {target}")
        digest = hashlib.sha256()
        with package.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        actual = digest.hexdigest()
        if rows[0][0] != actual:
            raise ValueError(f"Checksum mismatch for {target}")
        packages.append((package, actual))
    # Create output only once every required input has passed validation.
    destination.mkdir(parents=True, exist_ok=False)
    for package, _ in packages:
        shutil.copyfile(package, destination / package.name)
    (destination / 'SHA256SUMS.txt').write_text(''.join(
        f'{digest}  {package.name}\n' for package, digest in packages))
    return packages


if __name__ == '__main__':
    packages = prepare(Path(sys.argv[1]), Path(sys.argv[2]))
    repo = os.environ['GH_REPO']
    run_id = os.environ['BUILD_RUN_ID']
    sha = os.environ['BUILD_SHA']
    Path('release-notes.md').write_text(f'''Self-contained LEGv8 Instruction Set Simulator 0.71.

Java and JavaFX are bundled. No separate Java installation is needed.

| Download | Computer |
| --- | --- |
| `LEGv8-0.71-mac-aarch64.zip` | Apple Silicon Mac (M-series) |
| `LEGv8-0.71-mac-x64.zip` | Intel Mac |
| `LEGv8-0.71-windows-x64.zip` | Intel/AMD Windows PC |
| `LEGv8-0.71-linux-x64.tar.gz` | Intel/AMD Linux desktop with GTK 3.20+ |

Download your platform archive from **Assets**, extract it, and follow
`START-HERE.txt`. Use the platform archive, not GitHub's automatic Source code
downloads. The sole student example adds 2 + 2 and prints 4 in single-cycle mode.
`SHA256SUMS.txt` contains checksums for all four archives.

These are **unsigned builds**; macOS notarization and Windows signing have not
been configured. The simulator JAR and GUI are unchanged. Automated engine
checks passed; successful CI does not replace GUI testing on each platform.

Build: [{run_id}](https://github.com/{repo}/actions/runs/{run_id})
Source commit: `{sha}`

Maintainer: review these packages before clicking **Publish release**.
''')
    print(f'Prepared {len(packages)} verified packages and combined checksums.')
