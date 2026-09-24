# Bundled software

The simulator JAR is the original LEGv8 Instruction Set Simulator 0.71 by
Kenneth Yun, University of California, San Diego. Its original copyright and
resources are retained. Packaging does not change its license or ownership.

The private runtime is built from Eclipse Temurin OpenJDK and Gluon OpenJFX.
Both projects use GPLv2 with the Classpath Exception (individual components
may have additional notices). The linked runtime retains its `legal` directory;
do not remove it from distributions.

- Temurin releases and matching source archives:
  https://github.com/adoptium/temurin25-binaries/releases
- OpenJDK source: https://github.com/openjdk/jdk25u
- OpenJFX source and licenses: https://github.com/openjdk/jfx25u
- Gluon builds: https://gluonhq.com/products/javafx/

BUILD-INFO.json records the actual Java build, JavaFX download and checksum,
and original simulator checksum. Keep the corresponding source archives and
license notices available when distributing these binaries; the linked project
pages identify their upstream source distributions.
