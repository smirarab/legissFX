#!/usr/bin/env python3
"""Package the original simulator JAR with a private Java/JavaFX runtime.

Run on each target OS/architecture with Python 3.8+ and a Temurin 25 JDK.
No student-side Java installation is required. No recovered source is compiled.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NAME = "LEGv8Simulator"
PACKAGE_VERSION = "1.0.0"  # macOS requires a nonzero major; simulator stays 0.71.


def run(*args, **kwargs):
    print("+", " ".join(map(str, args)), flush=True)
    return subprocess.run(list(map(str, args)), check=True, **kwargs)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java-home", default=os.environ.get("JAVA_HOME"))
    parser.add_argument("--fx-archive", type=Path, help="Use an already downloaded, checksum-verified JavaFX JMOD zip")
    parser.add_argument("--work-dir", type=Path, default=Path(tempfile.gettempdir()) / "legv8-packaging-build",
                        help="Build outside cloud-synced folders to avoid macOS signing metadata errors")
    parser.add_argument("--installer", choices=["dmg", "pkg", "msi", "exe", "deb", "rpm"])
    args = parser.parse_args()
    if not args.java_home:
        parser.error("Set JAVA_HOME to a Temurin 25 JDK, or pass --java-home.")
    java_home = Path(args.java_home).resolve()
    system = {"Darwin": "mac", "Windows": "windows", "Linux": "linux"}[platform.system()]
    arch = {"arm64": "aarch64", "aarch64": "aarch64", "x86_64": "x64", "AMD64": "x64"}.get(platform.machine())
    target = f"{system}-{arch}"
    lock = json.loads((HERE / "dependencies.json").read_text())
    if target not in lock["javafx"]:
        parser.error(f"Unsupported build target: {target}. See README.md.")
    permitted = {"mac": {"dmg", "pkg"}, "windows": {"exe", "msi"}, "linux": {"deb", "rpm"}}
    if args.installer and args.installer not in permitted[system]:
        parser.error("Installer type must match the build operating system.")
    suffix = ".exe" if system == "windows" else ""
    def tool(name):
        return java_home / "bin" / (name + suffix)
    props = run(tool("java"), "-XshowSettings:properties", "-version", capture_output=True, text=True)
    print("\n".join(line for line in props.stderr.splitlines() if any(
        key in line for key in ["java.runtime.version =", "java.vendor =", "os.arch ="])))
    if "java.specification.version = 25" not in props.stderr or "Eclipse Adoptium" not in props.stderr:
        parser.error("Use Eclipse Temurin JDK 25, the tested redistributable runtime family.")
    if f"os.arch = {'amd64' if arch == 'x64' else 'aarch64'}" not in props.stderr and not (arch == "x64" and "os.arch = x86_64" in props.stderr):
        parser.error("The JDK architecture must match this Python process/build host.")
    original = ROOT / "legissFX071.jar"
    with zipfile.ZipFile(original) as jar:
        for required in ["legissFX/InstSetSim.class", "legissFX/legissFX.css", "legissFX/darkTheme.css"]:
            jar.getinfo(required)
    dep = lock["javafx"][target]
    archive = args.fx_archive or HERE / "downloads" / f"javafx-{target}.zip"
    if not archive.exists():
        archive.parent.mkdir(parents=True, exist_ok=True)
        partial = archive.with_suffix(".partial")
        print("Downloading", dep["url"], flush=True)
        with urllib.request.urlopen(dep["url"], timeout=120) as source, partial.open("wb") as out:
            shutil.copyfileobj(source, out)
        if sha256(partial) != dep["sha256"]:
            raise RuntimeError("JavaFX archive checksum mismatch; refusing to use download.")
        partial.replace(archive)
    if sha256(archive) != dep["sha256"]:
        raise RuntimeError("JavaFX archive checksum mismatch; refusing to build.")
    build_parent = args.work_dir.resolve()
    build_parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=target + "-", dir=build_parent))
    with zipfile.ZipFile(archive) as z:
        for member in z.namelist():
            resolved = (work / "fx" / member).resolve()
            try:
                resolved.relative_to((work / "fx").resolve())
            except ValueError:
                raise RuntimeError("Unsafe archive entry")
        z.extractall(work / "fx")
    jmods = next((work / "fx").rglob("javafx.controls.jmod")).parent
    runtime = work / "runtime"
    run(tool("jlink"), "--module-path", os.pathsep.join([str(java_home / "jmods"), str(jmods)]),
        "--add-modules", "javafx.controls,jdk.unsupported", "--strip-debug", "--no-header-files",
        "--no-man-pages", "--compress=zip-6", "--output", runtime)
    # Run simulator-engine checks using the exact linked runtime that will ship.
    classes = work / "checks"
    classes.mkdir()
    run(tool("javac"), "--system", runtime, "--add-modules", "javafx.controls", "-cp", original,
        "-d", classes, HERE / "checks" / "PackagingCheck.java")
    run(runtime / "bin" / ("java" + suffix), "--add-modules", "javafx.controls", "-cp",
        os.pathsep.join([str(classes), str(original)]), "legissFX.PackagingCheck",
        HERE / "examples", HERE / "checks" / "fixtures", timeout=60)
    inputs = work / "input"
    inputs.mkdir()
    shutil.copy2(original, inputs / original.name)
    run(tool("jpackage"), "--type", "app-image", "--name", NAME,
        "--app-version", PACKAGE_VERSION, "--vendor", "University of California, San Diego",
        "--description", "LEGv8 Instruction Set Simulator",
        "--input", inputs, "--main-jar", original.name, "--main-class", "legissFX.InstSetSim",
        "--runtime-image", runtime, "--java-options", "--add-modules=javafx.controls",
        "--java-options", "--enable-native-access=javafx.graphics", "--dest", work / "image")
    app = work / "image" / (NAME + (".app" if system == "mac" else ""))
    packaged_jar = next(app.rglob(original.name))
    if sha256(packaged_jar) != sha256(original):
        raise RuntimeError("Packaged simulator differs from original JAR")
    release = work / f"LEGv8-0.71-{target}"
    release.mkdir()
    shutil.move(str(app), release / app.name)
    app = release / app.name
    shutil.copy2(HERE / "STUDENT-README.txt", release / "START-HERE.txt")
    shutil.copytree(HERE / "examples", release / "examples")
    metadata = {
        "simulator_sha256": sha256(original), "target": target,
        "package_version": PACKAGE_VERSION,
        "java_version": run(tool("java"), "-version", capture_output=True, text=True).stderr,
        "javafx": dep,
        "javafx_version": lock["javafx_version"], "signed_for_distribution": False,
    }
    (release / "BUILD-INFO.json").write_text(json.dumps(metadata, indent=2))
    shutil.copy2(HERE / "THIRD-PARTY.md", release / "THIRD-PARTY.md")
    dest = HERE / "dist" / target
    dest.mkdir(parents=True, exist_ok=True)
    if system == "mac":
        output = dest / (release.name + ".zip")
        run("ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", release, output)
    else:
        fmt = "zip" if system == "windows" else "gztar"
        output = Path(shutil.make_archive(str(dest / release.name), fmt, root_dir=work, base_dir=release.name))
    outputs = [output]
    if args.installer:
        installer_dir = work / "installer"
        run(tool("jpackage"), "--type", args.installer, "--name", NAME,
            "--app-version", PACKAGE_VERSION, "--app-image", app, "--dest", installer_dir)
        for built in installer_dir.iterdir():
            shutil.copy2(built, dest / built.name)
            outputs.append(dest / built.name)
    (dest / "SHA256SUMS.txt").write_text("".join(f"{sha256(p)}  {p.name}\n" for p in outputs))
    print("\nBuilt:", *outputs, sep="\n")
    print("Unpacked application:", app)
    print("Unsigned development build. See README.md before public distribution.")


if __name__ == "__main__":
    main()
