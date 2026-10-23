const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '../..');
const base = 'b1275934fe1495769c37a3426387cab4062d0709';
const topics = ['area_volume','central_tendency','factorization','factorization_polynomials','inequality','law_of_indices','percentage','probability','quadrilaterals','triangle_centres'];
const scripts = ['shared/section-quiz.js', ...[['area_volume','area-volume'],['factorization','factorization'],['inequality','inequality'],['law_of_indices','law-of-indices'],['percentage','percentage'],['probability','probability']].map(([dir,name]) => `topics/${dir}/${name}-quiz.js`)];
function read(rel) { return fs.readFileSync(path.join(root, 'dashboard', rel), 'utf8').replace(/\r\n/g, '\n'); }
function original(rel) { return execFileSync('git', ['-c','safe.directory=' + root,'show',base + ':dashboard/' + rel], {cwd:root,encoding:'utf8'}).replace(/\r\n/g, '\n'); }
for (const topic of topics) {
  const rel = `topics/${topic}/index.html`, html = read(rel);
  assert.equal((html.match(/src="https:\/\/uni-education-elearning.pages.dev\/tracker\/uni-tracker.js/g)||[]).length, 1, rel);
  const restored = html.replace(/  <!-- Shared delivery tracker; content and quiz scoring remain owned by this page\. -->\n  <script defer src="https:\/\/uni-education-elearning.pages.dev\/tracker\/uni-tracker.js\?v=20261023-math-reconnect"><\/script>\n/, '');
  assert.equal(restored, original(rel), 'Content changed: ' + rel);
}
for (const rel of scripts) {
  const source = read(rel);
  new vm.Script(source, { filename: rel });
  const restored = source.replace(/^ *\/\/ (?:The topic page owns delivery after navigation away from the hub\.|Also deliver locally when this topic occupies the platform iframe\.)\n/gm, '').replace(/^ *if \(window.parent !== window\) window.postMessage\(payload, ['"]\*['"]\);\n/gm, '');
  assert.equal(restored, original(rel), 'Quiz/scoring changed: ' + rel);
  const relay = source.match(/if \(window.parent !== window\) window.postMessage\(payload, ['"]\*['"]\);\s*window.parent.postMessage\(payload, ['"]\*['"]\);/)[0];
  for (const embedded of [false,true]) {
    let local = 0, parent = 0;
    const window = {postMessage(){local++;}};
    window.parent = embedded ? {postMessage(){parent++;}} : window;
    vm.runInNewContext(relay, {window,payload:{type:'uniplus:quizAnswer',subject:'MATH'}});
    assert.equal(local,1,rel + ': local delivery');
    assert.equal(parent,embedded ? 1 : 0);
  }
}
console.log('PASS: 10 quiz loaders, 7 emitter syntax/relay checks; all original content and scoring preserved against production b127593.');

// Optional integration with the actual platform writer, using an offline fetch sink.
// node dashboard/scripts/test-live-tracker-reconnect.cjs <platform checkout>
async function integration(platform) {
  const {createHarness, settle} = require(path.resolve(platform, 'tools/tracker-harness.cjs'));
  for (const rel of scripts) {
    const source = read(rel);
    const match = source.match(/(?:var|const) payload = (\{\s*type: ['"]uniplus:quizAnswer['"][\s\S]*?\n\s*\});/);
    assert.ok(match, 'Missing actual payload: ' + rel);
    const relay = source.match(/if \(window.parent !== window\) window.postMessage\(payload, ['"]\*['"]\);\s*window.parent.postMessage\(payload, ['"]\*['"]\);/)[0];
    for (const picked of [0,1,undefined]) {
      const h = createHarness();
      h.login('offline-student', 'offline-token', 'MATH');
      const q = {id:1,type:'mc',stem:'offline fixture',choices:['A','B'],answer:0};
      const payload = vm.runInNewContext('(' + match[1] + ')', {
        q, userAnswerIdx:picked, picked, isCorrect:picked===0,
        activeSet:{idPrefix:'fixture-'},config:{quizId:'fixture',section:'JM31'},
      });
      const window = {postMessage(data){h.emit(data,'https://uni-s3-math.pages.dev');},parent:{postMessage(){}}};
      vm.runInNewContext(relay, {window,payload});
      await settle();
      assert.equal(h.requests.length,1,rel + ': exactly one write');
      const request = h.requests[0];
      assert.ok(request.url.includes('/math_quiz_attempts?on_conflict='));
      assert.equal(request.body.student_id,'offline-student');
      assert.equal(request.body.is_correct,picked===0);
      assert.equal(request.body.quiz_id,payload.quizId);
      assert.equal(request.body.question_id,payload.questionId);
      assert.ok(request.body.client_event_id);
      assert.equal(h.status().pending,0);
    }
  }
  console.log('PASS: 21 actual emitter/relay -> shared tracker -> mocked Supabase requests (correct, wrong, unanswered). No live records written.');
}
if (process.argv[2]) integration(process.argv[2]).catch(error => {console.error(error);process.exitCode=1;});
