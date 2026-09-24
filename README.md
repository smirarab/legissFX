# LEGv8 Instruction Set Simulator

Use this app to run LEGv8 assembly programs. This simulator was created by Kenneth Yun, University of California, San Diego. We just package it here for ease of use with newer machines. 

## 1. Download

Open the **[Releases page](https://github.com/smirarab/legissFX/releases)** and
choose the newest release recommended by your instructor. Under **Assets**, click
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
is required; if you see a missing-library error, ask your instructor for help.

## 3. Try a simple program

1. In the simulator, choose **File → Load Program**.
2. In the download's **examples** folder, select **add-two-plus-two.a**.
3. Choose **Execute → Single Cycle Mode**, then **Execute → Run**.

The program adds **2 + 2**. You should see **4** in the output panel and in
register **X0**. No data file is needed for this example.

## Need help?

These downloads are not yet digitally signed, so your computer may block the
app or show a security warning. If that happens, contact your instructor with
your computer type, operating system version, and a screenshot of the message.
You do not need to install a different version of Java.

---

Original simulator by Kenneth Yun, University of California, San Diego.
For build and release instructions, see the [developer guide](DEVELOPMENT.md).
