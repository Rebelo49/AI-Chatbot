"""
AI Chatbot — Portfolio Project
Interface web local com a API do Claude (Anthropic)
Corre em qualquer Python 3.6+

SETUP:
  1. Vai a https://console.anthropic.com e cria uma conta gratuita
  2. Gera uma API key em "API Keys"
  3. Cola a tua key na variável API_KEY abaixo
  4. Corre: python3 chatbot.py
"""

import json
import os
import webbrowser
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from datetime import datetime

PORT     = 8768
API_KEY  = "COLOCA_AQUI_A_TUA_API_KEY"   # ← substitui pela tua chave
MODEL    = "claude-haiku-4-5-20251001"    # modelo rápido e gratuito

HTML = r"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>🤖 AI Chatbot</title>
<style>
  :root{
    --bg:#1e1e2e;--surface:#2a2a3e;--accent:#a78bfa;--accent2:#c4b5fd;
    --text:#e2e8f0;--sub:#94a3b8;--border:#3f3f5a;--hover:#35354f;
    --user:#7c6af7;--bot:#2f2f45;--danger:#f87171;--success:#4ade80;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;height:100vh;display:flex;flex-direction:column}

  header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}
  header h1{font-size:20px;color:var(--accent2)}
  .status{font-size:12px;color:var(--sub);display:flex;align-items:center;gap:6px}
  .dot{width:8px;height:8px;border-radius:50%;background:var(--success)}

  .chat-area{flex:1;overflow-y:auto;padding:24px;display:flex;flex-direction:column;gap:16px}
  .chat-area::-webkit-scrollbar{width:4px}
  .chat-area::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}

  .msg{display:flex;gap:12px;max-width:80%;animation:fadeIn .3s ease}
  @keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
  .msg.user{align-self:flex-end;flex-direction:row-reverse}
  .msg.bot{align-self:flex-start}

  .avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;margin-top:2px}
  .msg.user .avatar{background:var(--user)}
  .msg.bot  .avatar{background:var(--bot);border:1px solid var(--border)}

  .bubble{padding:12px 16px;border-radius:16px;font-size:14px;line-height:1.6;max-width:100%}
  .msg.user .bubble{background:var(--user);color:white;border-bottom-right-radius:4px}
  .msg.bot  .bubble{background:var(--bot);border:1px solid var(--border);border-bottom-left-radius:4px}

  .bubble p{margin-bottom:8px}
  .bubble p:last-child{margin-bottom:0}
  .bubble code{background:#1e1e2e;padding:2px 6px;border-radius:4px;font-family:monospace;font-size:13px;color:var(--accent2)}
  .bubble pre{background:#1e1e2e;border:1px solid var(--border);border-radius:8px;padding:12px;overflow-x:auto;margin:8px 0}
  .bubble pre code{background:none;padding:0}

  .time{font-size:10px;color:var(--sub);margin-top:4px;padding:0 4px}
  .msg.user .time{text-align:right}

  .typing{display:none;align-self:flex-start}
  .typing-dots{display:flex;gap:4px;padding:14px 18px;background:var(--bot);border:1px solid var(--border);border-radius:16px;border-bottom-left-radius:4px}
  .typing-dots span{width:8px;height:8px;border-radius:50%;background:var(--sub);animation:bounce .8s infinite}
  .typing-dots span:nth-child(2){animation-delay:.15s}
  .typing-dots span:nth-child(3){animation-delay:.3s}
  @keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}

  .suggestions{display:flex;gap:8px;flex-wrap:wrap;padding:0 24px 12px}
  .sug-btn{background:var(--surface);border:1px solid var(--border);border-radius:20px;
    color:var(--sub);padding:6px 14px;font-size:12px;cursor:pointer;transition:all .2s}
  .sug-btn:hover{border-color:var(--accent);color:var(--accent)}

  .input-area{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;display:flex;gap:12px;align-items:flex-end;flex-shrink:0}
  textarea{flex:1;background:var(--hover);border:2px solid var(--border);border-radius:12px;
    color:var(--text);padding:12px 16px;font-size:14px;outline:none;resize:none;
    font-family:inherit;max-height:120px;line-height:1.5;transition:border-color .2s}
  textarea:focus{border-color:var(--accent)}
  .send-btn{background:var(--accent);color:white;border:none;border-radius:12px;
    width:46px;height:46px;font-size:20px;cursor:pointer;flex-shrink:0;transition:opacity .2s;display:flex;align-items:center;justify-content:center}
  .send-btn:hover{opacity:.85}
  .send-btn:disabled{opacity:.4;cursor:not-allowed}

  .clear-btn{background:none;border:1px solid var(--border);border-radius:8px;
    color:var(--sub);padding:8px 12px;font-size:12px;cursor:pointer;white-space:nowrap}
  .clear-btn:hover{border-color:var(--danger);color:var(--danger)}

  .welcome{text-align:center;color:var(--sub);padding:40px 20px}
  .welcome .icon{font-size:48px;margin-bottom:12px}
  .welcome h2{color:var(--accent2);margin-bottom:8px;font-size:18px}
  .welcome p{font-size:14px;line-height:1.6}
</style>
</head>
<body>

<header>
  <h1>🤖 AI Chatbot</h1>
  <div class="status"><div class="dot"></div> Claude — Online</div>
</header>

<div class="chat-area" id="chat">
  <div class="welcome">
    <div class="icon">🤖</div>
    <h2>Olá! Sou o teu assistente de IA</h2>
    <p>Podes perguntar-me qualquer coisa.<br/>Estou aqui para ajudar!</p>
  </div>
</div>

<div class="typing" id="typing">
  <div style="display:flex;gap:12px;align-items:flex-start">
    <div class="avatar">🤖</div>
    <div class="typing-dots"><span></span><span></span><span></span></div>
  </div>
</div>

<div class="suggestions" id="suggestions">
  <button class="sug-btn" onclick="sendSuggestion(this)">👋 Apresenta-te</button>
  <button class="sug-btn" onclick="sendSuggestion(this)">🐍 Explica Python</button>
  <button class="sug-btn" onclick="sendSuggestion(this)">💡 Dá-me uma ideia de projeto</button>
  <button class="sug-btn" onclick="sendSuggestion(this)">🌍 Conta-me uma curiosidade</button>
</div>

<div class="input-area">
  <button class="clear-btn" onclick="clearChat()">🗑 Limpar</button>
  <textarea id="input" rows="1" placeholder="Escreve uma mensagem…"
    onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"
    oninput="autoResize(this)"></textarea>
  <button class="send-btn" id="sendBtn" onclick="send()">➤</button>
</div>

<script>
let history = [];

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function now() {
  return new Date().toLocaleTimeString('pt-PT', {hour:'2-digit', minute:'2-digit'});
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function formatMsg(text) {
  // Code blocks
  text = text.replace(/```(\w*)\n?([\s\S]*?)```/g, (_,lang,code) =>
    `<pre><code>${escHtml(code.trim())}</code></pre>`);
  // Inline code
  text = text.replace(/`([^`]+)`/g, (_,c) => `<code>${escHtml(c)}</code>`);
  // Bold
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  // Line breaks
  text = text.split('\n').map(l => l ? `<p>${l}</p>` : '').join('');
  return text;
}

function addMsg(role, text) {
  const chat = document.getElementById('chat');
  const welcome = chat.querySelector('.welcome');
  if (welcome) welcome.remove();

  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = `
    <div class="avatar">${role === 'user' ? '👤' : '🤖'}</div>
    <div>
      <div class="bubble">${role === 'user' ? `<p>${escHtml(text)}</p>` : formatMsg(text)}</div>
      <div class="time">${now()}</div>
    </div>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function setLoading(v) {
  document.getElementById('typing').style.display = v ? 'flex' : 'none';
  document.getElementById('sendBtn').disabled = v;
  if (v) {
    const chat = document.getElementById('chat');
    chat.scrollTop = chat.scrollHeight;
  }
}

async function send() {
  const input = document.getElementById('input');
  const text  = input.value.trim();
  if (!text) return;

  input.value = '';
  input.style.height = 'auto';
  document.getElementById('suggestions').style.display = 'none';

  addMsg('user', text);
  history.push({role: 'user', content: text});
  setLoading(true);

  try {
    const r = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({messages: history})
    });
    const d = await r.json();
    setLoading(false);

    if (d.error) {
      addMsg('bot', '❌ Erro: ' + d.error);
      return;
    }

    addMsg('bot', d.reply);
    history.push({role: 'assistant', content: d.reply});
  } catch(e) {
    setLoading(false);
    addMsg('bot', '❌ Erro de ligação. Verifica se o servidor está a correr.');
  }
}

function sendSuggestion(btn) {
  document.getElementById('input').value = btn.textContent.slice(2).trim();
  send();
}

function clearChat() {
  history = [];
  const chat = document.getElementById('chat');
  chat.innerHTML = `<div class="welcome">
    <div class="icon">🤖</div>
    <h2>Conversa reiniciada!</h2>
    <p>Podes começar uma nova conversa.</p>
  </div>`;
  document.getElementById('suggestions').style.display = 'flex';
}
</script>
</body>
</html>"""


# ── API ───────────────────────────────────────────────────────────────────────

def ask_claude(messages: list) -> str:
    payload = json.dumps({
        "model":      MODEL,
        "max_tokens": 1024,
        "system":     "És um assistente simpático e útil que responde sempre em português de Portugal. És conciso mas completo nas respostas.",
        "messages":   messages,
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data    = payload,
        headers = {
            "Content-Type":      "application/json",
            "x-api-key":         API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method = "POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())

    return data["content"][0]["text"]


# ── HTTP Handler ──────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path in ("/", "/index.html"):
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        if urlparse(self.path).path == "/api/chat":
            length   = int(self.headers.get("Content-Length", 0))
            body     = json.loads(self.rfile.read(length))
            messages = body.get("messages", [])

            if API_KEY == "COLOCA_AQUI_A_TUA_API_KEY":
                self.send_json({"error": "Adiciona a tua API key no ficheiro chatbot.py!"})
                return
            try:
                reply = ask_claude(messages)
                self.send_json({"reply": reply})
            except Exception as e:
                self.send_json({"error": str(e)})
        else:
            self.send_response(404); self.end_headers()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if API_KEY == "COLOCA_AQUI_A_TUA_API_KEY":
        print("\n  ⚠️  Atenção: Adiciona a tua API key no ficheiro!")
        print("  👉  Vai a https://console.anthropic.com e cria uma chave gratuita.\n")

    server = HTTPServer(("localhost", PORT), Handler)
    url    = f"http://localhost:{PORT}"
    print(f"  🤖  AI Chatbot")
    print(f"  🌐  A abrir em {url}")
    print(f"  ⛔  Para parar: Ctrl+C\n")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋  App encerrada!")
        server.shutdown()
