import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).parent

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <title>SkillFolio — Nexora Tech Workspace</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen p-6">
  <div class="max-w-5xl mx-auto space-y-6">
    <div class="flex justify-between items-center border-b border-slate-800 pb-4">
      <div>
        <h1 class="text-2xl font-bold text-emerald-400">SkillFolio</h1>
        <p class="text-sm text-slate-400">Nexora Tech • TASK-001: The Broken Billing API</p>
      </div>
      <span id="mentor-badge" class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
        AI Mentor: UNLOCKED (Round 1)
      </span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-4">
        <h2 class="font-semibold text-lg" id="task-title">Round 1: Fix the Discount Bug</h2>
        <p class="text-sm text-slate-300" id="task-desc">
          Customers are being overcharged! Fix <code>calculate_discount</code> so <b>gold</b> gets 20% off and <b>silver</b> gets 10% off.
        </p>
        <div id="mentor-box" class="p-3 rounded-lg bg-slate-800 text-xs text-slate-300">
          <b>AI Mentor Hint:</b> Check line 15—the discount is currently being added to <code>price</code> instead of subtracted.
        </div>
        <button id="next-round-btn" onclick="triggerRound2()" class="hidden w-full py-2 px-4 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-sm">
          Simulate Changed Requirement →
        </button>
      </div>

      <div class="md:col-span-2 space-y-4">
        <textarea id="editor" rows="16" class="w-full font-mono text-sm bg-slate-900 text-emerald-200 p-4 rounded-xl border border-slate-700 focus:outline-none"></textarea>
        <div class="flex gap-3">
          <button onclick="runCode()" class="px-5 py-2.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm">
            Run Hidden Tests (pytest)
          </button>
        </div>
        <pre id="output" class="bg-slate-900 p-4 rounded-xl border border-slate-800 text-xs text-slate-300 overflow-x-auto whitespace-pre-wrap">Click "Run Hidden Tests" to verify your fix...</pre>
      </div>
    </div>

    <div id="evidence-card" class="hidden bg-emerald-950/40 border border-emerald-500/40 p-5 rounded-xl space-y-2">
      <h3 class="text-lg font-bold text-emerald-300">Verified SkillFolio Evidence Record</h3>
      <p class="text-sm text-slate-300">Candidate passed Round 1 (Bug Fix) AND adapted unaided in Round 2 with AI Mentor Locked.</p>
      <p class="text-xs text-emerald-400 font-mono">STATUS: VERIFIED • BACKEND PYTHON • ADAPTIVE DEBUGGING</p>
    </div>
  </div>

  <script>
    let currentRound = 1;
    fetch('/api/starter').then(r => r.json()).then(d => document.getElementById('editor').value = d.code);

    async function runCode() {
      const code = document.getElementById('editor').value;
      const out = document.getElementById('output');
      out.textContent = "Running tests...";
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ code, round_num: currentRound })
      });
      const data = await res.json();
      out.textContent = data.output;
      if (data.passed && currentRound === 1) {
        document.getElementById('next-round-btn').classList.remove('hidden');
      } else if (data.passed && currentRound === 2) {
        document.getElementById('evidence-card').classList.remove('hidden');
      }
    }

    function triggerRound2() {
      currentRound = 2;
      document.getElementById('next-round-btn').classList.add('hidden');
      document.getElementById('mentor-badge').textContent = "AI Mentor: LOCKED (Round 2)";
      document.getElementById('mentor-badge').className = "px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/40";
      document.getElementById('task-title').textContent = "Round 2: Changed Requirement!";
      document.getElementById('task-desc').innerHTML = "Product Manager update: If <code>is_promo=True</code>, apply an <b>extra 5% discount</b> on top of the tier-discounted price.";
      document.getElementById('mentor-box').innerHTML = "<b class='text-rose-400'>AI Mentor Locked:</b> Prove you understand your code without AI help.";
      document.getElementById('output').textContent = "Round 2 active. Update your code and run hidden tests.";
    }
  </script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/starter":
            code = (BASE_DIR / "task_001.py").read_text(encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"code": code}).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())

    def do_POST(self):
        if self.path == "/api/run":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            (BASE_DIR / "student_code.py").write_text(data["code"], encoding="utf-8")
            test_file = "tests_round1.py" if data["round_num"] == 1 else "tests_round2.py"
            runner = f"import {test_file[:-3]} as t\nfor fn in [getattr(t, f) for f in dir(t) if f.startswith('test_')]:\n    fn()\nprint('ALL HIDDEN TESTS PASSED!')"
            res = subprocess.run([sys.executable, "-c", runner], cwd=BASE_DIR, capture_output=True, text=True)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"passed": res.returncode == 0, "output": res.stdout + res.stderr}).encode())

if __name__ == "__main__":
    print("SkillFolio running on http://127.0.0.1:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
