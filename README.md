# LEGv8 Instruction Set Simulator

Use this app to run LEGv8 assembly programs. This simulator was created by Kenneth Yun, University of California, San Diego. We just package it here for ease of use with newer machines. 

## 1. Download

Open the **[Releases page](https://github.com/smirarab/legissFX/releases)** and
choose the newest release. Under **Assets**, click
the file for your computer:

| Your computer | File to download |
| --- | --- |
| Mac with an Apple M-series chip (M1, M2, etc.) | `LEGv8-0.71-mac-aarch64.zip` |
| Mac with an Intel processor | `LEGv8-0.71-mac-x64.zip` |
| Windows PC with an Intel or AMD processor | `LEGv8-0.71-windows-x64.zip` |
| Linux computer with an Intel or AMD processor | `LEGv8-0.71-linux-x64.tar.gz` |

**Not sure which Mac you have?** Open the Apple menu → **About This Mac**.
Look for an Apple chip name or an Intel processor.

You only need one file. Ignore **Source code** and **SHA256SUMS.txt**.
The app does not run on an iPad or phone.

## 2. Open the app

### Mac

1. Double-click the downloaded ZIP file to extract it.
2. Open the extracted folder.
3. Double-click **LEGv8Simulator.app** (Finder may show it as **LEGv8Simulator**).

You can drag the app into **Applications** if you want to keep it there.

### Windows

1. Right-click the downloaded ZIP file and choose **Extract All**.
2. Open the extracted folder, then the **LEGv8Simulator** folder inside it.
3. Double-click **LEGv8Simulator.exe** (Windows may hide the `.exe` ending).

Keep the whole folder together. Moving just the `.exe` file will break the app.

### Linux

1. Extract the downloaded `.tar.gz` file using your archive manager.
2. Open a terminal in the extracted folder.
3. Run:

   ```sh
   ./LEGv8Simulator/bin/LEGv8Simulator
   ```

Keep the whole folder together. A desktop environment with GTK 3.20 or newer
is required; if you see a missing-library error, ask us for help and we will make an effort.

## 3. Try a simple program

1. In the simulator, choose **File → Load Program**.
2. In the download's **examples** folder, select **add-two-plus-two.a**.
3. Choose **Execute → Single Cycle Mode**, then **Execute → Run**.

The program adds **2 + 2**. You should see **4** in the output panel and in
register **X0**. No data file is needed for this example.

## FAQ

### My computer shows a security warning. How do I open the app?

These downloads are not yet digitally signed. Follow the steps below only for
this simulator downloaded from our [Releases page](https://github.com/smirarab/legissFX/releases),
when you trust the download.

**Mac:** Right-click (or Control-click) **LEGv8Simulator.app**, choose **Open**,
and confirm **Open** if offered. On newer macOS versions, this may not be enough:

1. Try opening the app once, then dismiss the warning.
2. Open **Apple menu → System Settings → Privacy & Security**.
3. Scroll to the security section and click **Open Anyway** next to the message
   about LEGv8Simulator.
4. Confirm **Open** and enter your Mac password or use Touch ID if asked.

See [Apple's instructions](https://support.apple.com/en-us/102445).

**Windows:** If you see **Windows protected your PC** when opening
**LEGv8Simulator.exe**:

1. Click **More info**.
2. Check that the app shown is **LEGv8Simulator.exe**. The publisher may be listed
   as **Unknown publisher** because the app is unsigned.
3. Click **Run anyway**.

See [Microsoft's explanation of this warning](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation).

**No Open Anyway or Run anyway button?** A school-managed computer or Windows
Smart App Control may prevent exceptions. Contact your instructor or IT support;
you do not need to turn off your computer's security protection. If the message
specifically reports malware or a damaged file, stop and report that message
instead of following these steps.

### Do I need to install Java or JavaFX?

No. Both are included in the download. Extract the whole archive and open the
app using the steps above.

---

Original simulator by Kenneth Yun, University of California, San Diego.
For build and release instructions, see the [developer guide](DEVELOPMENT.md).
