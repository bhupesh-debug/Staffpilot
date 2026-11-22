/**
 * Idempotency-key convention (see docs/API.md).
 *
 * Every money-adjacent POST must carry an `Idempotency-Key` header.
 * The server stores (key, organization_id, endpoint, request hash, response)
 * in `idempotency_keys` and replays the stored response for a repeat key
 * instead of executing the operation twice.
 */
import { createHash } from "crypto";

export function hashRequestBody(body: unknown): string {
  return createHash("sha256")
    .update(JSON.stringify(body ?? null))
    .digest("hex");
}

export function isValidIdempotencyKey(key: string | null | undefined): boolean {
  if (!key) return false;
  // UUID v4 (recommended) or any opaque token 8–128 chars.
  return /^[A-Za-z0-9._-]{8,128}$/.test(key);
}
