import re

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# Replace TECH.STACK table
readme = re.sub(
    r'<h3><code>// TECH\.STACK</code></h3>.*?</table>', 
    '<h3><code>// TECH.STACK</code></h3>\n\n<div align="center">\n<img src="assets/tech_stack.svg?v=1" alt="Tech Stack" width="800"/>\n</div>', 
    readme, 
    flags=re.DOTALL
)

# Replace EXPERIENCE.LOG table
readme = re.sub(
    r'<h3><code>// EXPERIENCE\.LOG</code></h3>.*?</table>', 
    '<h3><code>// EXPERIENCE.LOG</code></h3>\n\n<div align="center">\n<img src="assets/experience.svg?v=1" alt="Experience Log" width="800"/>\n</div>', 
    readme, 
    flags=re.DOTALL
)

# Replace PROJECTS table
readme = re.sub(
    r'<h3><code>// PROJECTS</code></h3>.*?</table>', 
    '<h3><code>// PROJECTS</code></h3>\n\n<div align="center">\n<a href="https://github.com/gaaarrrgiiiiiiiiiii?tab=repositories">\n<img src="assets/projects.svg?v=1" alt="Projects" width="800"/>\n</a>\n</div>', 
    readme, 
    flags=re.DOTALL
)

# Replace CERTIFICATIONS table
readme = re.sub(
    r'<h3><code>// CERTIFICATIONS</code></h3>.*?</table>', 
    '<h3><code>// CERTIFICATIONS</code></h3>\n\n<div align="center">\n<img src="assets/certifications.svg?v=1" alt="Certifications" width="800"/>\n</div>', 
    readme, 
    flags=re.DOTALL
)

# Replace CONNECT table
readme = re.sub(
    r'<h3><code>// CONNECT</code></h3>.*?</table>', 
    '<h3><code>// CONNECT</code></h3>\n\n<div align="center">\n<a href="https://www.linkedin.com/in/gargi-thapa-089767294/">\n<img src="assets/connect.svg?v=1" alt="Connect" width="800"/>\n</a>\n</div>', 
    readme, 
    flags=re.DOTALL
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)
