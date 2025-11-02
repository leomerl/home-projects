import express from 'express';
import type { Request, Response } from 'express';
import { createCookie, readCookie } from './cookie.js';
import { generateKey } from './crypto.js';

const app = express();
app.use(express.json());

const encryptionKey = generateKey();

app.post('/login', (req: Request, res: Response) => {
  const { userId, role, cookieFlags } = req.body;

  if (!userId) return res.status(400).json({ error: 'userId required' });

  const cookieStr = createCookie(
    'jwt',
    { userId, role },
    {
      encryptToken: true,
      encryptionKey,
      expiresIn: '1h',
      flags: cookieFlags
    }
  );

  res.setHeader('Set-Cookie', cookieStr);
  return res.json({ message: 'Logged in, cookie set', cookie: cookieStr });
});

app.get('/protected', (req: Request, res: Response) => {
  const cookieHeader = req.headers.cookie || '';
  const result = readCookie(cookieHeader, 'jwt', { encryptToken: true, encryptionKey });

  if (!result) return res.status(401).json({ error: 'Invalid or missing cookie' });

  return res.json({ message: 'Access granted', payload: result.payload });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
