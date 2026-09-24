# LEGv8 Instruction Set Simulator

Self-contained desktop packages for the original LEGv8 simulator 0.71 by
Kenneth Yun, University of California, San Diego. The original JAR and its
JavaFX interface are preserved. Each download includes its own Java and
JavaFX runtime, so students do not need to install either separately.

## Build all four platforms on GitHub

1. Open the **Actions** tab in this repository.
2. If GitHub asks to enable workflows, enable them.
3. Select **Package LEGv8 simulator** in the left sidebar.
4. Click **Run workflow**, select **master**, and click the green **Run workflow** button.
5. Open the new run and wait for its four jobs to finish.
6. After all four jobs succeed, **Create draft release** runs automatically.
7. Open **Releases**, review the draft and its attached downloads, and click
   **Publish release** when ready. Until publication, students cannot see the draft.

The build's **Artifacts** section also retains the packages for maintainer testing.

| Artifact | Student computer |
| --- | --- |
| `LEGv8-0.71-mac-aarch64-unsigned` | Apple Silicon Mac |
| `LEGv8-0.71-mac-x64-unsigned` | Intel Mac |
| `LEGv8-0.71-windows-x64-unsigned` | Intel/AMD Windows PC |
| `LEGv8-0.71-linux-x64-unsigned` | Intel/AMD Linux desktop |

GitHub wraps each artifact in a ZIP. Inside it is the student ZIP or tar.gz
and `SHA256SUMS.txt`. Distribute that inner student archive. Each includes
launch instructions and one simple example that adds 2 + 2 and prints 4.
No course exercise programs or data files are included.

The packaging workflow is manually triggered: pushing commits does not start a
build. Each successful build automatically prepares an unpublished draft release
with the four platform archives, a combined checksum file, and installation notes.
Builds are unsigned previews; signing and macOS
notarization are separate steps before broad classroom distribution.

## Create a release from an already completed build

1. Open **Actions > Create draft release > Run workflow**.
2. Select **master**. Leave **Build run ID** blank for the latest successful build,
   or enter the numeric ID from a packaging run's URL.
3. Click the green **Run workflow** button. No rebuild is needed.
4. After it succeeds, open **Releases** and review/publish the draft.

Draft tags use `v0.71-build-<run ID>` and refer to the exact commit that produced
the packages. All four packages and their checksums must be present and valid.
Rerunning release creation updates the same draft; it refuses to replace a
published release. Older builds can only be released while their Actions
artifacts remain available. Automatic release creation applies to successful
packaging runs that complete after the release workflow is installed.

## Contents and local builds

- `legissFX071.jar`: original simulator binary, unchanged.
- `simulator-packaging/`: build script, pinned JavaFX downloads, checks, and student example.
- `.github/workflows/package-legv8.yml`: Windows, Linux, and both Mac build jobs.
- `.github/workflows/release-legv8.yml`: draft releases from completed builds.

See [the packaging guide](simulator-packaging/README.md) for local build commands,
validation details, signing considerations, and runtime updates. The build does
not require the recovered Java source, and no JDKs, dependency downloads, or
built application archives are committed to this repository.

The simulator retains its original copyright and ownership. See
[third-party notices](simulator-packaging/THIRD-PARTY.md) for bundled runtimes.
