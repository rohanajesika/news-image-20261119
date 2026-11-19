// The World in One Day — Thursday, 19 November 2026 (Node 22, stdlib only).
// The front page is composed offline by compose.py into entry.png beside
// this file; this program copies it to /output/entry.png and, before it
// does, proves the file is a whole image inside the competition's limits:
// PNG or JPEG by its first bytes, at most 1 MiB, at most 1024 by 1024 px.
// It writes the same bytes on every run: a copy, nothing generated here,
// so the two grader runs agree byte for byte.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

const source = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}

const isPng = bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e &&
  bytes[3] === 0x47 && bytes[4] === 0x0d && bytes[5] === 0x0a &&
  bytes[6] === 0x1a && bytes[7] === 0x0a;
const isJpeg = bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff;
if (!isPng && !isJpeg) {
  throw new Error('entry.png is neither PNG nor JPEG by its first bytes');
}

// Dimensions straight from the header, so a truncated file cannot slip by.
let width;
let height;
if (isPng) {
  if (bytes.length < 33 || bytes.readUInt32BE(12) !== 0x49484452) {
    throw new Error('PNG is missing its IHDR chunk');
  }
  width = bytes.readUInt32BE(16);
  height = bytes.readUInt32BE(20);
} else {
  let pos = 2;
  while (pos + 9 <= bytes.length) {
    if (bytes[pos] !== 0xff) throw new Error('JPEG segment out of sync');
    const marker = bytes[pos + 1];
    // Standalone markers (RSTn, SOI, EOI, TEM) carry no length field.
    if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd9)) {
      pos += 2;
      continue;
    }
    const len = bytes.readUInt16BE(pos + 2);
    if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 &&
        marker !== 0xc8 && marker !== 0xcc) {
      height = bytes.readUInt16BE(pos + 5);
      width = bytes.readUInt16BE(pos + 7);
      break;
    }
    pos += 2 + len;
  }
  if (width === undefined || height === undefined) {
    throw new Error('JPEG has no frame header');
  }
}
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`image is ${width}x${height}, over the 1024x1024 cap`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
const written = statSync(target).size;
if (written !== bytes.length) {
  throw new Error(`copied ${written} bytes, expected ${bytes.length}`);
}
console.log(`entry.png: ${isPng ? 'PNG' : 'JPEG'} ${width}x${height}, ` +
  `${bytes.length} bytes -> ${target}`);
