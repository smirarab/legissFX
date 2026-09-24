LEGv8 Instruction Set Simulator 0.71

Java and JavaFX are included. Do not install Java, change JAVA_HOME, or run the
JAR separately. The application uses its own runtime.

Mac: Extract the ZIP, then open LEGv8Simulator.app. You may move the app to
Applications. Select the aarch64 download for Apple Silicon (M-series chips),
or x64 for Intel Macs. See Apple menu > About This Mac.

Windows: Extract the entire ZIP, then open LEGv8Simulator/LEGv8Simulator.exe.
Keep all files in that folder together. This build targets Intel/AMD x64 PCs.

Linux: Extract the tar.gz, then run LEGv8Simulator/bin/LEGv8Simulator.
This build targets x64 Linux desktops with GTK 3 and a graphical session.
On Debian/Ubuntu, the GTK runtime is supplied by libgtk-3-0 or libgtk-3-0t64,
depending on the distribution. This is not an iPad, Android, or browser app.

Try File > Load Program and select examples/add-two-plus-two.a. Choose
Execute > Single Cycle Mode, then Execute > Run. The program adds 2 + 2,
prints 4 in the output panel, and leaves 4 in register X0. No data file is needed.
Reset/clear all before loading a different program.

These initial builds are unsigned previews. The OS may show a security warning;
contact your instructor for an approved/signed release if it blocks the app.
Do not disable system security. Report your OS version, computer model, and
the error message when requesting help.
