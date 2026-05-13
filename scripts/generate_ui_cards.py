import os
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

# Tokyo Night Palette
BG       = "#0f1117"
CARD_BG  = "#161b22"
BORDER   = "#21262d"
TEXT     = "#c9d1d9"
DIM      = "#8b949e"
ACCENT   = "#58a6ff"
GREEN    = "#3fb950"
ORANGE   = "#d29922"
CYAN     = "#39d353"

def badge(x, y, text, border_color, text_color):
    width = len(text) * 7 + 24
    return f'''
    <g transform="translate({x}, {y})">
      <rect width="{width}" height="24" rx="4" fill="{BG}" stroke="{border_color}" stroke-width="1"/>
      <text x="{width/2}" y="16" text-anchor="middle" font-family="Consolas, 'Courier New', monospace" font-size="11" font-weight="bold" fill="{text_color}">{text}</text>
    </g>
    ''', width + 10

def render_tech_stack():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="260" viewBox="0 0 800 260">
  <rect width="800" height="260" rx="10" fill="{BG}"/>
  
  <!-- AI & ML -->
  <g class="card" transform="translate(10, 10)">
    <rect width="385" height="115" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="20" y="30" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="{TEXT}">AI &amp; ML</text>
    {badge(20, 45, "RAG Systems", "#1f6feb", "#58a6ff")[0]}
    {badge(125, 45, "OpenAI API", "#1f6feb", "#58a6ff")[0]}
    {badge(220, 45, "FAISS", "#1f6feb", "#58a6ff")[0]}
    {badge(20, 75, "LLM Pipelines", "#1f6feb", "#58a6ff")[0]}
    {badge(135, 75, "Vector Search", "#1f6feb", "#58a6ff")[0]}
  </g>

  <!-- Backend & APIs -->
  <g class="card" transform="translate(405, 10)">
    <rect width="385" height="115" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="20" y="30" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="{TEXT}">Backend &amp; APIs</text>
    {badge(20, 45, "FastAPI", "#238636", "#3fb950")[0]}
    {badge(100, 45, "Flask", "#238636", "#3fb950")[0]}
    {badge(170, 45, "async Python", "#238636", "#3fb950")[0]}
    {badge(20, 75, "WebSockets", "#238636", "#3fb950")[0]}
    {badge(115, 75, "JWT / OAuth2", "#238636", "#3fb950")[0]}
  </g>

  <!-- Databases & Cache -->
  <g class="card" transform="translate(10, 135)">
    <rect width="385" height="115" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="20" y="30" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="{TEXT}">Databases &amp; Cache</text>
    {badge(20, 45, "PostgreSQL", "#8957e5", "#bc8cff")[0]}
    {badge(115, 45, "Redis", "#8957e5", "#bc8cff")[0]}
    {badge(180, 45, "Redis Streams", "#8957e5", "#bc8cff")[0]}
    {badge(20, 75, "SQL", "#8957e5", "#bc8cff")[0]}
  </g>

  <!-- Infrastructure -->
  <g class="card" transform="translate(405, 135)">
    <rect width="385" height="115" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="20" y="30" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="{TEXT}">Infrastructure</text>
    {badge(20, 45, "Docker", "#9e6a03", "#d29922")[0]}
    {badge(90, 45, "AWS EC2/S3", "#9e6a03", "#d29922")[0]}
    {badge(185, 45, "GitHub Actions", "#9e6a03", "#d29922")[0]}
    {badge(20, 75, "Prometheus", "#9e6a03", "#d29922")[0]}
    {badge(115, 75, "Grafana", "#9e6a03", "#d29922")[0]}
    {badge(190, 75, "Linux", "#9e6a03", "#d29922")[0]}
  </g>
</svg>'''
    with open(ASSETS / "tech_stack.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def render_experience():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="350" viewBox="0 0 800 350">
  <rect width="800" height="350" rx="10" fill="{BG}"/>
  
  <rect x="10" y="10" width="780" height="330" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
  
  <!-- DappaSol -->
  <text x="30" y="45" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="700" fill="{TEXT}">AI Infrastructure Engineer Intern</text>
  <text x="770" y="45" text-anchor="end" font-family="Consolas, 'Courier New', monospace" font-size="12" fill="{DIM}">Dec 2025 – Jan 2026</text>
  <text x="30" y="65" font-family="'Segoe UI', sans-serif" font-size="12" fill="{DIM}">DappaSol</text>
  <circle cx="40" cy="85" r="3" fill="{ACCENT}"/>
  <text x="55" y="90" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">FastAPI + FAISS + OpenAI Embeddings — 89% retrieval precision@5 across 500K+ indexed docs</text>
  <circle cx="40" cy="110" r="3" fill="{ACCENT}"/>
  <text x="55" y="115" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">Async ingestion pipeline with per-tenant namespace isolation; sub-800ms P95 for NY enterprise client</text>

  <line x1="30" y1="135" x2="770" y2="135" stroke="{BORDER}" stroke-width="1"/>

  <!-- Ericsson -->
  <text x="30" y="165" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="700" fill="{TEXT}">Software Engineering Intern</text>
  <text x="770" y="165" text-anchor="end" font-family="Consolas, 'Courier New', monospace" font-size="12" fill="{DIM}">Jun – Aug 2025</text>
  <text x="30" y="185" font-family="'Segoe UI', sans-serif" font-size="12" fill="{DIM}">Ericsson</text>
  <circle cx="40" cy="205" r="3" fill="{GREEN}"/>
  <text x="55" y="210" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">Concurrent Python ETL pipelines — 40% reduction in manual ingestion overhead</text>
  <circle cx="40" cy="230" r="3" fill="{GREEN}"/>
  <text x="55" y="235" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">Modular Flask microservices with structured logging across 3+ backend service modules</text>

  <line x1="30" y1="255" x2="770" y2="255" stroke="{BORDER}" stroke-width="1"/>

  <!-- Citi -->
  <text x="30" y="285" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="700" fill="{TEXT}">Bridge Trainee — Fintech Backend</text>
  <text x="770" y="285" text-anchor="end" font-family="Consolas, 'Courier New', monospace" font-size="12" fill="{DIM}">Mar 2026</text>
  <text x="30" y="305" font-family="'Segoe UI', sans-serif" font-size="12" fill="{DIM}">Citi</text>
  <circle cx="40" cy="325" r="3" fill="{ORANGE}"/>
  <text x="55" y="330" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">Enterprise fintech systems, secure dev practices &amp; AI in financial services</text>
</svg>'''
    with open(ASSETS / "experience.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def render_projects():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="230" viewBox="0 0 800 230">
  <rect width="800" height="230" rx="10" fill="{BG}"/>
  
  <!-- AegisFlow -->
  <g class="card" transform="translate(10, 10)">
    <rect width="385" height="210" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="20" y="35" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="700" fill="{ACCENT}">⚙ AegisFlow</text>
    
    <text x="20" y="65" font-family="Consolas, 'Courier New', monospace" font-size="11" fill="{DIM}">FastAPI · Redis Streams · PostgreSQL</text>
    <text x="20" y="80" font-family="Consolas, 'Courier New', monospace" font-size="11" fill="{DIM}">Docker · AWS</text>
    
    <text x="20" y="115" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">Distributed async task orchestration engine.</text>
    <text x="20" y="135" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">Exactly-once execution, circuit breakers,</text>
    <text x="20" y="155" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">exponential-backoff DLQ, JWT REST API.</text>
    
    {badge(20, 175, "2400+ tasks/min", "#238636", "#3fb950")[0]}
    {badge(155, 175, "P95 22ms", "#238636", "#3fb950")[0]}
    {badge(245, 175, "50 workers", "#238636", "#3fb950")[0]}
  </g>

  <!-- CortexGate -->
  <g class="card" transform="translate(405, 10)">
    <rect width="385" height="210" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="20" y="35" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="700" fill="{ACCENT}">🛡 CortexGate</text>
    
    <text x="20" y="65" font-family="Consolas, 'Courier New', monospace" font-size="11" fill="{DIM}">FastAPI · Redis · PostgreSQL · JWT</text>
    <text x="20" y="80" font-family="Consolas, 'Courier New', monospace" font-size="11" fill="{DIM}">Docker · AWS</text>
    
    <text x="20" y="115" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">Multi-tenant API gateway with Redis</text>
    <text x="20" y="135" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">caching, dynamic upstream failover,</text>
    <text x="20" y="155" font-family="'Segoe UI', sans-serif" font-size="13" fill="{TEXT}">per-tenant rate limiting, usage metering.</text>
    
    {badge(20, 175, "99.9% uptime", "#238636", "#3fb950")[0]}
    {badge(130, 175, "38% cache wins", "#238636", "#3fb950")[0]}
    {badge(255, 175, "31% latency", "#238636", "#3fb950")[0]}
  </g>
</svg>'''
    with open(ASSETS / "projects.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def render_certifications():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="90" viewBox="0 0 800 90">
  <rect width="800" height="90" rx="10" fill="{BG}"/>
  
  <g class="card" transform="translate(10, 10)">
    <rect width="385" height="70" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="192.5" y="30" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="{TEXT}">🏅 AWS Certified AI Practitioner</text>
    <text x="192.5" y="50" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="12" fill="{DIM}">Amazon Web Services · 2026</text>
  </g>

  <g class="card" transform="translate(405, 10)">
    <rect width="385" height="70" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="192.5" y="30" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="{TEXT}">🏅 AWS Certified Cloud Practitioner</text>
    <text x="192.5" y="50" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="12" fill="{DIM}">Amazon Web Services · 2026</text>
  </g>
</svg>'''
    with open(ASSETS / "certifications.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def render_connect():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="90" viewBox="0 0 800 90">
  <rect width="800" height="90" rx="10" fill="{BG}"/>
  
  <g class="card" transform="translate(10, 10)">
    <rect width="385" height="70" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="30" y="30" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="{TEXT}">📧 email</text>
    <text x="30" y="55" font-family="'Segoe UI', sans-serif" font-size="13" fill="{ACCENT}">gargith24@gmail.com</text>
  </g>

  <g class="card" transform="translate(405, 10)">
    <rect width="385" height="70" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="30" y="30" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="{TEXT}">🔗 linkedin</text>
    <text x="30" y="55" font-family="'Segoe UI', sans-serif" font-size="13" fill="{ACCENT}">linkedin.com/in/gargi-thapa-089767294</text>
  </g>
</svg>'''
    with open(ASSETS / "connect.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    render_tech_stack()
    render_experience()
    render_projects()
    render_certifications()
    render_connect()
    print("UI SVGs generated successfully.")
