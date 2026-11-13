const fs = require('node:fs');
const path = require('node:path');

const root = path.join(__dirname, '..');
const readText = (relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8');
const readBase64 = (relativePath) => fs.readFileSync(path.join(root, relativePath)).toString('base64');
const fonts = readText('assets/geist.css')
  .replace('GEIST_CYRILLIC', readBase64('assets/geist-cyrillic.woff2'))
  .replace('GEIST_LATIN', readBase64('assets/geist-latin.woff2'));
const manning = 'https://manning-content.s3.amazonaws.com/download/d/5d0f2b3-4591-4648-a869-6dafc6f38310/sample_ch01_Trask2_Grokking_Deep-Learning_corr_January06.pdf';
const html = readText('src/reading-room.html')
  .replace('FONT_STYLES', () => fonts)
  .replace('NOTEBOOK_PDF', readBase64('assets/grokking-deep-learning-chapter-1.pdf'))
  .replace('CHAPTER_TEMPLATES', () => readText('src/technical-chapters.html'))
  .replaceAll('MANNING_URL', manning);

fs.writeFileSync(path.join(root, 'index.html'), html);
