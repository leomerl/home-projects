// Provides encryption and decryption functions
// Use AES-256-GCM

import crypto from 'crypto';

// AES-256-GCM requires a 32-byte key and a 12-byte nonce (IV)
const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 12;
const TAG_LENGTH = 16;

export function encrypt(text: string, key: Buffer): string {
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv);

  const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();

  const result = Buffer.concat([iv, encrypted, tag]);
  return result.toString('base64');
}

export function decrypt(encrypted: string, key: Buffer): string {
  const data = Buffer.from(encrypted, 'base64');

  const iv = data.slice(0, IV_LENGTH);
  const tag = data.slice(data.length - TAG_LENGTH);
  const encryptedText = data.slice(IV_LENGTH, data.length - TAG_LENGTH);

  const decipher = crypto.createDecipheriv(ALGORITHM, key, iv);
  decipher.setAuthTag(tag);

  const decrypted = Buffer.concat([decipher.update(encryptedText), decipher.final()]);
  return decrypted.toString('utf8');
}

export function generateKey(): Buffer {
  return crypto.randomBytes(32);
}