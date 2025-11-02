import { generateJWT, verifyJWT } from './jwt.js';
import type { JWTOptions, JWTPayload } from './jwt.js';

export interface CookieFlags {
  httpOnly?: boolean;
  secure?: boolean;
  sameSite?: 'Strict' | 'Lax' | 'None';
  maxAge?: number;
  path?: string;
  refreshable?: boolean;
  audit?: boolean;
}

export interface Cookie {
  name: string;
  value: string;
  flags: CookieFlags;
}

export function createCookie(
  name: string,
  payload: JWTPayload,
  jwtOptions: JWTOptions & { flags?: CookieFlags }
): string {
  const { flags = {}, encryptToken, encryptionKey, expiresIn } = jwtOptions;

  const jwtOpts: JWTOptions = {};
  if (encryptToken !== undefined) jwtOpts.encryptToken = encryptToken;
  if (encryptionKey !== undefined) jwtOpts.encryptionKey = encryptionKey;
  if (expiresIn !== undefined) jwtOpts.expiresIn = expiresIn;

  const token = generateJWT(payload, jwtOpts);

  const parts = [`${name}=${token}`];

  if (flags.httpOnly) parts.push('HttpOnly');
  if (flags.secure) parts.push('Secure');
  if (flags.sameSite) parts.push(`SameSite=${flags.sameSite}`);
  if (flags.maxAge) parts.push(`Max-Age=${flags.maxAge}`);
  if (flags.path) parts.push(`Path=${flags.path}`);

  return parts.join('; ');
}


export function parseCookies(cookieHeader: string): Record<string, string> {
  const result: Record<string, string> = {};
  if (!cookieHeader) return result;

  const cookies = cookieHeader.split(';');
  cookies.forEach((cookie) => {
    const [key, ...val] = cookie.trim().split('=');
    if (key) {
      result[key] = val.join('=');
    }
  });

  return result;
}

export function readCookie(
  cookieHeader: string,
  name: string,
  jwtOptions: JWTOptions
): { payload: JWTPayload } | null {
  const cookies = parseCookies(cookieHeader);
  const token = cookies[name];
  if (!token) return null;

  try {
    const payload = verifyJWT(token, jwtOptions);
    return { payload };
  } catch (err) {
    console.error('Invalid or expired JWT:', err);
    return null;
  }
}
