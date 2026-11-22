import { describe, expect, it } from "vitest";
import {
  fromCents,
  lineTotal,
  marginAmount,
  marginPercent,
  money,
  sumMoney,
  toCents,
} from "../../src/lib/money";

describe("decimal money math (no floats, ever)", () => {
  it("computes margin dollars exactly: bill 95.00 − pay 65.00 = 30.00", () => {
    expect(marginAmount("95.0000", "65.0000")).toBe("30.0000");
  });

  it("computes margin percent exactly: (95 − 65) / 95 × 100", () => {
    // 30/95*100 = 31.578947... → 31.5789 at NUMERIC(19,4) precision
    expect(marginPercent("95.0000", "65.0000")).toBe("31.5789");
  });

  it("returns 0% margin when the bill rate is 0 (no division by zero)", () => {
    expect(marginPercent("0.0000", "0.0000")).toBe("0.0000");
  });

  it("multiplies rate × hours exactly (0.1 × 3 is not 0.30000000000000004)", () => {
    expect(lineTotal("0.1000", "3")).toBe("0.3000");
    expect(lineTotal("95.0000", "40")).toBe("3800.0000");
  });

  it("sums amounts exactly: 0.1 + 0.2 = 0.3, not 0.30000000000000004", () => {
    expect(sumMoney(["0.1000", "0.2000"])).toBe("0.3000");
  });

  it("rounds half-up to 4 decimals like NUMERIC(19,4)", () => {
    expect(money("10.12345")).toBe("10.1235");
    expect(money("10.12344")).toBe("10.1234");
  });

  it("converts to integer cents and back without float drift", () => {
    expect(toCents("95.0000")).toBe(9500);
    expect(fromCents(9500)).toBe("95.0000");
    expect(fromCents(toCents("19.99"))).toBe("19.9900");
  });
});
