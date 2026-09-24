package legissFX;

import java.lang.reflect.Field;
import java.nio.file.Path;

/** Exercises the original bytecode, never compiled into the distributed app. */
public class PackagingCheck {
    private static long[] values(String field) throws Exception {
        Field f = LEGv8P.class.getDeclaredField(field);
        f.setAccessible(true);
        return (long[]) f.get(null);
    }

    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    public static void main(String[] args) throws Exception {
        Path examples = Path.of(args[0]);
        Path fixtures = Path.of(args[1]);
        check(InstSetSim.class.getResource("legissFX.css") != null, "Missing light theme");
        check(InstSetSim.class.getResource("darkTheme.css") != null, "Missing dark theme");
        for (boolean pipelined : new boolean[]{false, true}) {
            LEGv8P sim = new LEGv8P();
            sim.loadProg(fixtures.resolve("arithmetic.legv8").toString());
            sim.run(pipelined);
            long[] r = values("regFile");
            check(r[0] == 7 && r[1] == 5 && r[2] == 12 && r[3] == 12,
                "Arithmetic/load results, pipelined=" + pipelined);
            check(values("dataMem")[0] == 12, "Store result");
            check(!sim.getRegFileAsObservableList().isEmpty(), "Register display model");
            check(!sim.getDataMemAsObservableList(0).isEmpty(), "Memory display model");
            check(!sim.getStackAsObservableList(262136).isEmpty(), "Stack display model");
            System.out.println("PASS arithmetic, memory, display models; pipelined=" + pipelined);
        }
        LEGv8P sim = new LEGv8P();
        sim.loadProg(fixtures.resolve("arithmetic.legv8").toString());
        sim.addBreakpoint(2);
        sim.run(false);
        check(sim.getPC() == 2 && values("regFile")[2] == 0, "Breakpoint stops before ADD");
        sim.clearBreakpoint(2);
        sim.step(false);
        check(values("regFile")[2] == 12, "Step after breakpoint");
        System.out.println("PASS breakpoint and single step");
        sim = new LEGv8P();
        sim.resetOutput();
        sim.loadProg(examples.resolve("add-two-plus-two.a").toString());
        sim.run(false);
        check(values("regFile")[0] == 4, "2 + 2 must leave 4 in X0");
        check(sim.getOutput().trim().equals("4"), "Example must print 4");
        System.out.println("PASS student example: 2 + 2 prints 4");
    }
}
