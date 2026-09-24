# Distributing LEGv8 0.71 without student-side Java setup

This packages `../legissFX071.jar` unchanged. It does not compile the recovered
Java files. The original JAR already contains both CSS themes. It runs with a
private, reduced Eclipse Temurin 25 runtime containing OpenJFX 25.0.4.
No system Java is installed or changed, and students need neither a JDK nor
JavaFX. The runtime contains only modules needed by the application.
The native package version is 1.0.0 because macOS rejects a zero major version;
the simulator itself remains version 0.71 with its original title and bytecode.

The JAR is portable, but JavaFX and Java contain OS/CPU-specific native code.
Build four separate downloads: Apple Silicon Mac, Intel Mac, Windows x64,
and Linux x64. These share the same simulator bytecode and behavior. iPad,
Windows ARM native, and Linux ARM builds are outside this initial setup.

## Build locally

Install/download Python 3.8+ and **Eclipse Temurin JDK 25**, matching the host
architecture. The locally tested build is **25.0.4.1+1**. The workflow selects
the latest available Temurin 25 patch and records its exact version in each
artifact's BUILD-INFO.json; JavaFX downloads are pinned by version and checksum.
The JDK can simply be unpacked into a development directory; it need not be
installed system-wide. Only the maintainer needs these tools.

```sh
python3 simulator-packaging/build.py --java-home /path/to/temurin-25
```

On macOS the Java home is inside the extracted JDK at `Contents/Home`.
On Windows use `python` and a quoted Windows path to the JDK. Alternatively,
set `JAVA_HOME` and omit the argument. Builds must run on their target OS and
architecture; this is not a cross-compiling script.

The script downloads the matching JavaFX JMOD archive from Gluon and checks
its SHA-256 against `dependencies.json`. An existing archive can be supplied
with `--fx-archive`; it must match the same checksum. The locked JavaFX hashes
were recorded from the official HTTPS downloads, not independently signed
checksum manifests. The local Temurin archive was checked against the checksum
published by the Adoptium release API.

It links the runtime, compiles a small external test harness against the original
JAR, and checks arithmetic, loads/stores, breakpoints, stepping, and both execution
modes using that linked runtime. The test classes are not shipped. It then creates
a native application launcher with `jpackage`, checks that the packaged JAR is
byte-for-byte identical, and creates a ZIP (Mac/Windows) or tar.gz (Linux).
Legal notices from the linked modules remain inside the runtime.

Outputs are in `simulator-packaging/dist/<platform>/`, alongside SHA256SUMS.txt.
The unpacked app remains under the unique build directory reported at completion.
By default this is in the OS temporary directory, outside cloud-synced folders
that can attach Finder metadata and interfere with macOS signing. Override it
with `--work-dir` if needed.
Build directories are retained for diagnostics and may be removed when no longer
needed. Student directions and an example program are included in the archive.

Optional installers: append `--installer dmg` on Mac, `--installer msi` on
Windows, or `--installer deb` on Debian/Ubuntu. Windows installer generation
requires the WiX toolset supported by the selected JDK; Linux packaging requires
the relevant native packaging tools. The default portable archives avoid those
extra installer-tool dependencies.

## Build all four platforms

The local `.github/workflows/package-legv8.yml` defines a manually triggered
GitHub Actions build matrix. In a repository containing the original JAR,
this folder, and the workflow, run **Actions > Package LEGv8 simulator > Run
workflow**. Download the four artifacts after they pass. Nothing here uploads
the repository or publishes a release automatically. A separate release workflow
prepares an unpublished draft after all four builds succeed. The first remote
four-platform build completed successfully; GUI validation is still needed on
Windows, Intel Mac, and Linux.

Use a simulator-only repository if course materials should remain private.
Each artifact contains the student archive and its checksum. Distribute the
inner archive, not the entire GitHub artifact wrapper.

For student distribution, use the draft release described in the repository's
[developer guide](../DEVELOPMENT.md). **Create draft release** can also be started manually to reuse a
completed build without rebuilding. It verifies each downloaded archive against
its build checksum and combines the four manifests into one SHA256SUMS.txt.
Only you publish the draft; the automation never publishes it.

## Before handing out to the class

These are unsigned preview builds. The local macOS ad-hoc signature produced
by packaging is not a trusted Developer ID signature. For a smooth download
experience, sign and notarize the macOS application with an institutional Apple
Developer ID, then package/staple it using Apple's supported process. Windows
code signing is also recommended; a signature alone does not guarantee that
SmartScreen has established reputation. Signing credentials are not configured
or assumed by this build. Do not tell students to disable system security.

Test each download on its intended OS with no system Java installed, including
opening a program, loading data, run/step, breakpoints, both execution modes,
themes, scrolling, and save-output. The automated checks verify selected engine
behavior, not complete GUI compatibility or every instruction. Linux needs a
desktop session and GTK 3.20+ supplied by the distribution; test on the oldest
Linux version the course intends to support. Likewise, establish minimum Mac
and Windows versions through validation of the chosen runtime distributions.

The original JAR's existing bugs remain. For example, the recovered source shows
that canceling Load Program dereferences the file before checking for null.
Keeping the JAR unchanged deliberately separates packaging from simulator fixes.

## Local validation results (September 23, 2026)

Built on Apple Silicon macOS 15.7.3, using Temurin 25.0.4.1+1 and OpenJFX
25.0.4. The compressed student archive is approximately 38 MiB. The native
launcher started without reporting errors. Computer-use permissions were not
available, so manual GUI interaction and appearance have **not** been verified.

- Synthetic arithmetic/load/store test: passes in single-cycle and pipelined modes.
- Breakpoint and single-step test: passes in single-cycle mode.
- Bundled `add-two-plus-two.a`: X0 is 4 and printed output is `4` in single-cycle mode.
- Both original stylesheets and register/memory/stack display models are present.
- Packaged JAR checksum equals the input JAR checksum.

Earlier checks with the original JAR observed duplicate printed output in
pipelined mode. The student instructions use single-cycle mode. Packaging
preserves the original simulator bytecode and does not fix this behavior.

The examples folder contains only a simple 2 + 2 program. Course exercises
and their data files are excluded. The synthetic memory test is kept under
checks/fixtures and is not included in student downloads.
