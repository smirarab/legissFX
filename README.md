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
6. Under **Artifacts** on the run summary, download the packages you need.

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

The workflow is manually triggered: pushing commits does not start a build
or publish a release. Builds are unsigned previews; signing and macOS
notarization are separate steps before broad classroom distribution.

## Contents and local builds

- `legissFX071.jar`: original simulator binary, unchanged.
- `simulator-packaging/`: build script, pinned JavaFX downloads, checks, and student example.
- `.github/workflows/package-legv8.yml`: Windows, Linux, and both Mac build jobs.

See [the packaging guide](simulator-packaging/README.md) for local build commands,
validation details, signing considerations, and runtime updates. The build does
not require the recovered Java source, and no JDKs, dependency downloads, or
built application archives are committed to this repository.

The simulator retains its original copyright and ownership. See
[third-party notices](simulator-packaging/THIRD-PARTY.md) for bundled runtimes.
