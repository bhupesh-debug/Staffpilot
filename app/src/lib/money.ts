/**
 * Decimal-safe money math — StaffPilot NEVER uses floats for money.
 *
 * All money is stored in PostgreSQL as NUMERIC(19,4) and computed here with
 * decimal.js. Amounts are passed around as decimal strings; conversion to
 * integer cents happens only at a payment-provider boundary (and StaffPilot
 * has no payment provider connected — see docs/ARCHITECTURE.md).
 */
import Decimal from "decimal.js";

Decimal.set({ precision: 28, rounding: Decimal.ROUND_HALF_UP });

export type Money = string; // decimal string, e.g. "125.5000"

export function toDecimal(value: string | number | Decimal): Decimal {
  return new Decimal(value);
}

/** Format a money value to 4 decimal places (matches NUMERIC(19,4)). */
export function money(value: string | number | Decimal): Money {
  return new Decimal(value).toFixed(4);
}

/** Format for display: 2 decimal places, e.g. "1,250.00" — display only. */
export function moneyDisplay(value: string | number | Decimal): string {
  return new Decimal(value).toFixed(2);
}

/** Gross margin dollars: bill − pay. */
export function marginAmount(billRate: Money, payRate: Money): Money {
  return money(new Decimal(billRate).minus(new Decimal(payRate)));
}

/** Gross margin percent: (bill − pay) / bill × 100. Returns 0 when bill is 0. */
export function marginPercent(billRate: Money, payRate: Money): Money {
  const bill = new Decimal(billRate);
  if (bill.isZero()) return money(0);
  return money(bill.minus(new Decimal(payRate)).dividedBy(bill).times(100));
}

/** Line total: rate × hours, exact decimal multiplication. */
export function lineTotal(rate: Money, hours: string | number): Money {
  return money(new Decimal(rate).times(new Decimal(hours)));
}

/** Sum a list of money amounts exactly. */
export function sumMoney(values: Money[]): Money {
  return money(values.reduce((acc, v) => acc.plus(new Decimal(v)), new Decimal(0)));
}

/** Convert a decimal-string amount to integer cents (provider boundary only). */
export function toCents(value: Money): number {
  return new Decimal(value).times(100).toDecimalPlaces(0).toNumber();
}

/** Convert integer cents back to a money string. */
export function fromCents(cents: number): Money {
  return money(new Decimal(cents).dividedBy(100));
}
