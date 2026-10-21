// HTML を1コマずつ撮って mp4（映像のみ）にする。時間は render(ms) で決めるので、ずれない。
// 使い方: node render.js <dir> <id> [fps=60] [ms=10000]
const {chromium} = require('playwright');
const {spawn} = require('child_process');
const path = require('path');
(async () => {
  const [dir, id, fpsS, msS] = process.argv.slice(2);
  const fps = +(fpsS || 60), total = +(msS || 10000), n = Math.round(total / 1000 * fps);
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'}).catch(() => chromium.launch());
  const p = await b.newPage({viewport: {width: 1080, height: 1920}});
  await p.goto('file://' + path.resolve(dir, id + '.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', '-r', String(fps),
    path.resolve(dir, id + '_v.mp4')], {stdio: ['pipe', 'inherit', 'inherit']});
  for (let i = 0; i < n; i++) {
    await p.evaluate(ms => window.render(ms), i * 1000 / fps);
    const buf = await p.screenshot({type: 'jpeg', quality: 98});
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
