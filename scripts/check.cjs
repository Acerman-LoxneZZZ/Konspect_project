const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { pathToFileURL } = require('node:url');
const { chromium, devices } = require('playwright');

const root = path.join(__dirname, '..');
const screenshots = path.join(root, 'test-results');

async function check() {
  const url = process.env.READING_QA_URL || pathToFileURL(path.join(root, 'index.html')).href;
  fs.mkdirSync(screenshots, { recursive: true });
  const browser = await chromium.launch({ headless: true, executablePath: process.env.POLYA_CHROME });
  try {
    const desktop = await browser.newPage({ viewport: { width: 1440, height: 960 }, permissions: ['clipboard-read', 'clipboard-write'] });
    const errors = [];
    desktop.on('pageerror', (error) => errors.push(error.message));
    await desktop.goto(url);
    await desktop.evaluate(() => document.fonts.ready);
    await desktop.screenshot({ path: path.join(screenshots, 'library.png') });
    await desktop.getByRole('searchbox').fill('Траск');
    await desktop.getByRole('link', { name: /Грокаем глубокое обучение/ }).click();
    await desktop.getByRole('heading', { name: 'Оглавление' }).waitFor();
    await desktop.screenshot({ path: path.join(screenshots, 'outline.png') });
    assert.equal(await desktop.getByRole('link', { name: 'С чего начать', exact: true }).count(), 0);
    await desktop.getByRole('link', { name: /Открыть конспект.*Введение/ }).click();
    await desktop.getByRole('heading', { name: 'Как выглядит задача прогнозирования' }).waitFor();
    await desktop.getByRole('heading', { name: 'Дополнительный пример · время в дороге' }).waitFor();
    await desktop.screenshot({ path: path.join(screenshots, 'reader.png') });
    const download = desktop.waitForEvent('download');
    await desktop.getByRole('link', { name: 'PDF', exact: true }).click();
    assert.deepEqual(fs.readFileSync(await (await download).path()), fs.readFileSync(path.join(root, 'assets/grokking-deep-learning-chapter-1.pdf')));
    await desktop.getByRole('textbox', { name: 'Мои заметки' }).fill('Заметка ко всей главе');
    await desktop.reload();
    assert.equal(await desktop.getByRole('textbox', { name: 'Мои заметки' }).inputValue(), 'Заметка ко всей главе');
    await desktop.getByRole('link', { name: 'Оглавление', exact: true }).click();
    await desktop.getByRole('link', { name: /Открыть конспект.*Прямое распространение/ }).click();
    await desktop.locator('#topic-forward .code-example').waitFor();
    await desktop.screenshot({ path: path.join(screenshots, 'code.png') });
    assert.equal(await desktop.locator('output').first().innerText(), '2.0\n4.5');
    await desktop.getByRole('button', { name: 'Копировать' }).first().click();
    if (url.startsWith('http')) {
      await desktop.getByRole('button', { name: 'Скопировано' }).waitFor();
      const clipboard = await desktop.evaluate(() => navigator.clipboard.readText());
      assert.equal(clipboard.replaceAll('\r\n', '\n'), await desktop.locator('.code-example code').first().textContent());
    }
    const code = await desktop.locator('.code-example').evaluateAll((blocks) => blocks.map((block) => [block.querySelector('code').textContent, block.dataset.result]));
    await desktop.getByRole('link', { name: /Дальше: градиентный спуск/ }).click();
    await desktop.getByRole('heading', { name: 'Градиентный спуск', exact: true }).waitFor();
    code.push(...await desktop.locator('.code-example').evaluateAll((blocks) => blocks.map((block) => [block.querySelector('code').textContent, block.dataset.result])));
    for (const [snippet, expected] of code) {
      const result = spawnSync(process.env.POLYA_PYTHON || 'python', ['-c', snippet], { encoding: 'utf8' });
      assert.equal(result.status, 0, result.stderr);
      assert.equal(result.stdout.trim().replaceAll('\r\n', '\n'), expected);
    }
    const printed = await desktop.pdf({ preferCSSPageSize: true, printBackground: true });
    assert.equal(printed.subarray(0, 4).toString(), '%PDF');
    await desktop.getByRole('link', { name: 'Оглавление', exact: true }).click();
    await desktop.getByRole('link', { name: 'Цикл обучения на Python', exact: true }).waitFor();
    await desktop.screenshot({ path: path.join(screenshots, 'multi-outline.png') });
    await desktop.getByRole('link', { name: 'Цикл обучения на Python', exact: true }).click();
    await desktop.waitForFunction(() => Math.abs(document.querySelector('#topic-training').getBoundingClientRect().top - 80) < 2);
    await desktop.screenshot({ path: path.join(screenshots, 'training.png') });
    await desktop.getByRole('link', { name: 'Оглавление', exact: true }).click();
    await desktop.locator('summary', { hasText: 'Как учатся машины' }).click();
    await desktop.getByRole('button', { name: 'Разбить на темы' }).click();
    const field = desktop.getByRole('textbox', { name: 'Одна тема на строку' });
    await field.fill((await field.inputValue()) + '\nМой пример');
    await desktop.getByRole('button', { name: 'Сохранить', exact: true }).click();
    await desktop.getByRole('link', { name: 'Мой пример' }).click();
    await desktop.getByRole('textbox', { name: 'Мои заметки' }).fill('Моя проверочная заметка');
    await desktop.reload();
    assert.equal(await desktop.getByRole('textbox', { name: 'Мои заметки' }).inputValue(), 'Моя проверочная заметка');
    await desktop.goto(url);
    await desktop.getByRole('button', { name: 'Добавить', exact: true }).click();
    await desktop.getByRole('textbox', { name: 'Название' }).fill('Моя новая книга');
    await desktop.getByRole('dialog').getByRole('button', { name: 'Добавить' }).click();
    await desktop.getByRole('heading', { name: 'Моя новая книга' }).waitFor();
    assert.deepEqual(errors, []);

    const mobile = await browser.newPage({ ...devices['iPhone 13'], viewport: { width: 390, height: 844 } });
    await mobile.goto(url);
    await mobile.getByRole('link', { name: /Грокаем глубокое обучение/ }).click();
    await mobile.getByRole('link', { name: /Открыть конспект.*Введение/ }).click();
    await mobile.getByRole('heading', { name: 'Как выглядит задача прогнозирования' }).waitFor();
    await mobile.evaluate(() => document.fonts.ready);
    await mobile.screenshot({ path: path.join(screenshots, 'mobile.png'), scale: 'css' });
    assert.equal(await mobile.evaluate(() => document.documentElement.scrollWidth), 390);
    await mobile.getByRole('link', { name: 'Оглавление', exact: true }).click();
    await mobile.getByRole('heading', { name: 'Оглавление' }).waitFor();
    assert.equal(await mobile.evaluate(() => document.documentElement.scrollWidth), 390);
    await mobile.locator('summary', { hasText: 'Градиентный спуск' }).click();
    await mobile.getByRole('link', { name: 'Цикл обучения на Python', exact: true }).click();
    await mobile.locator('#topic-training .code-example').waitFor();
    await mobile.waitForFunction(() => Math.abs(document.querySelector('#topic-training').getBoundingClientRect().top - 72) < 2);
    await mobile.screenshot({ path: path.join(screenshots, 'mobile-code.png'), scale: 'css' });
    assert.equal(await mobile.evaluate(() => document.documentElement.scrollWidth), 390);
  } finally {
    await browser.close();
  }
}

check().then(() => console.log('Verified chapters, executable examples, topics, saved notes, PDF and mobile.')).catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
