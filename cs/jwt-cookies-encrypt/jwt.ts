import jwt from 'jsonwebtoken';
import { encrypt, decrypt } from './crypto.js';

export interface JWTPayload {
  userId: number;
  role?: string;
  [key: string]: any;
}

export interface JWTOptions {
  expiresIn?: string | number;
  encryptToken?: boolean;
  encryptionKey?: Buffer;
}

if (!process.env.JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable must be set');
}
const DEFAULT_SECRET = process.env.JWT_SECRET as string;

export function generateJWT(payload: JWTPayload, options: JWTOptions = {}): string {
  const { expiresIn, encryptToken, encryptionKey } = options;

  const token = jwt.sign(
    payload,
    DEFAULT_SECRET,
    expiresIn !== undefined ? { expiresIn: expiresIn as any } : undefined
  );

  if (encryptToken) {
    if (!encryptionKey) throw new Error('Encryption key required for encrypted JWT');
    return encrypt(token, encryptionKey);
  }

  return token;
}

export function verifyJWT(token: string, options: JWTOptions = {}): JWTPayload {
  const { encryptToken, encryptionKey } = options;

  let decryptedToken = token;
  if (encryptToken) {
    if (!encryptionKey) throw new Error('Encryption key required to decrypt JWT');
    decryptedToken = decrypt(token, encryptionKey);
  }

  const payload = jwt.verify(decryptedToken, DEFAULT_SECRET) as JWTPayload;
  return payload;
}
