import re

ansi_text = """ ██████╗  █████╗ ██████╗  ██████╗ ██╗
██╔════╝ ██╔══██╗██╔══██╗██╔════╝ ██║
██║  ███╗███████║██████╔╝██║  ███╗██║
██║   ██║██╔══██║██╔══██╗██║   ██║██║
╚██████╔╝██║  ██║██║  ██║╚██████╔╝██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝"""

lines = ansi_text.split("\n")
longest_line = max(len(line) for line in lines)

svg_header = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="250" viewBox="0 0 800 250">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#080b12;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#111827;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="blockColor" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:#1d4ed8" />
      <stop offset="100%" style="stop-color:#60a5fa" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <rect width="800" height="250" fill="url(#bg)" rx="0"/>
"""

svg_footer = """
  <!-- Subtitle -->
  <text x="400" y="185" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="14" fill="#9ca3af" letter-spacing="4">
    GARGI THAPA  /  <tspan fill="#38bdf8">AI &amp; BACKEND ENGINEER</tspan>  /  CHENNAI, INDIA
  </text>
  
  <!-- Decorative line -->
  <line x1="200" y1="205" x2="600" y2="205" stroke="#1e293b" stroke-width="1"/>
  
  <!-- Tech badges row -->
  <text x="400" y="232" text-anchor="middle" font-family="'Courier New', monospace" font-size="11" fill="#64748b" letter-spacing="2">
    FastAPI  ·  RAG + LLMs  ·  AWS Certified  ·  Docker + Redis  ·  Distributed Systems
  </text>
</svg>
"""

y_start = 50
line_height = 18
font_size = 18
char_width = 10.8 
total_width = longest_line * char_width
x_start = (800 - total_width) / 2

# For the blocks, we use the blue gradient.
blocks_svg = f'  <text font-family="Consolas, \'Courier New\', monospace" font-size="{font_size}" font-weight="bold" fill="url(#blockColor)" filter="url(#glow)" xml:space="preserve">\n'
# For the outlines, we use a darker matching cyan/blue.
outlines_svg = f'  <text font-family="Consolas, \'Courier New\', monospace" font-size="{font_size}" font-weight="bold" fill="#0284c7" xml:space="preserve">\n'

for i, line in enumerate(lines):
    y = y_start + i * line_height
    blocks_line = "".join(c if c == '█' else ' ' for c in line)
    outlines_line = "".join(' ' if c == '█' else c for c in line)
    
    blocks_svg += f'    <tspan x="{x_start}" y="{y}">{blocks_line}</tspan>\n'
    outlines_svg += f'    <tspan x="{x_start}" y="{y}">{outlines_line}</tspan>\n'

blocks_svg += '  </text>\n'
outlines_svg += '  </text>\n'

with open("assets/header.svg", "w", encoding="utf-8") as f:
    f.write(svg_header + blocks_svg + outlines_svg + svg_footer)

print("SVG Generated.")
