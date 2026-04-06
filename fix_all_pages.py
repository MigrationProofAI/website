"""
Run this script from the root of your migrationproof repo:
    python fix_all_pages.py

It will:
1. Update the nav on all pages to include Diagnostic + Sample Report + logo
2. Replace "14 minutes" and similar time claims with "minutes, not months"
3. Update footer links consistently
"""

import os
import re

# The correct nav HTML
NEW_NAV = '''<header class="topbar"><div class="container topbar-inner">
    <a class="brand" href="/"><div class="brand-mark"><img src="/images/mp-icon.png" alt="MP" style="width:100%;height:100%;object-fit:cover"></div><div><div>Migration Proof</div><div class="muted" style="font-size:0.8rem;font-weight:500">Maths, not art</div></div></a>
    <nav class="nav"><a href="/diagnostic/">Diagnostic</a><a href="/sample-report/">Sample Report</a><a href="/blog/">Articles</a><a href="/about/">About</a><a href="mailto:hello@migrationproof.io">Contact</a><button class="toggle" id="themeToggle" type="button">Light mode</button></nav>
  </div></header>'''

NEW_FOOTER_LINKS = '<div class="footer-links"><a href="/">Home</a><a href="/diagnostic/">Diagnostic</a><a href="/sample-report/">Sample Report</a><a href="/blog/">Articles</a><a href="/about/">About</a></div>'

# Nav patterns to find and replace
NAV_PATTERNS = [
    # Old nav without diagnostic/sample-report (articles pages, about, blog index)
    r'<nav class="nav">.*?</nav>',
]

# Time claim patterns to replace
TIME_REPLACEMENTS = [
    ('fourteen minutes', 'minutes, not months'),
    ('14 minutes', 'minutes, not months'),
    ('in under twenty minutes', 'in minutes, not months'),
    ('under twenty minutes', 'minutes, not months'),
    ('in under 20 minutes', 'in minutes, not months'),
    ('Results in under twenty minutes', 'Results in minutes, not months'),
]

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Fix nav - replace the entire nav element
    nav_match = re.search(r'<nav class="nav">.*?</nav>', content, re.DOTALL)
    if nav_match:
        old_nav = nav_match.group()
        new_nav = '<nav class="nav"><a href="/diagnostic/">Diagnostic</a><a href="/sample-report/">Sample Report</a><a href="/blog/">Articles</a><a href="/about/">About</a><a href="mailto:hello@migrationproof.io">Contact</a><button class="toggle" id="themeToggle" type="button">Light mode</button></nav>'
        if old_nav != new_nav:
            content = content.replace(old_nav, new_nav)
            changes.append('nav updated')
    
    # Fix brand mark - replace MP text with image
    if '<div class="brand-mark">MP</div>' in content:
        content = content.replace(
            '<div class="brand-mark">MP</div>',
            '<div class="brand-mark"><img src="/images/mp-icon.png" alt="MP" style="width:100%;height:100%;object-fit:cover"></div>'
        )
        changes.append('logo updated')
    
    # Fix footer links
    old_footer_patterns = [
        '<div class="footer-links"><a href="/">Home</a><a href="/blog/">Articles</a><a href="/about/">About</a></div>',
        '<div class="footer-links"><a href="/">Home</a><a href="/blog/">All articles</a><a href="mailto:hello@migrationproof.io">hello@migrationproof.io</a></div>',
        '<div class="footer-links"><a href="#top">Top</a><a href="/blog/">Articles</a><a href="/about/">About</a><a href="mailto:hello@migrationproof.io">Contact</a></div>',
    ]
    for old_footer in old_footer_patterns:
        if old_footer in content:
            content = content.replace(old_footer, NEW_FOOTER_LINKS)
            changes.append('footer updated')
            break
    
    # Fix time claims
    for old_text, new_text in TIME_REPLACEMENTS:
        if old_text.lower() in content.lower():
            content = re.sub(re.escape(old_text), new_text, content, flags=re.IGNORECASE)
            changes.append(f'time claim fixed: "{old_text}"')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✓ {filepath}: {", ".join(changes)}')
        return True
    else:
        print(f'  - {filepath}: no changes needed')
        return False

# Find all HTML files
count = 0
for root, dirs, files in os.walk('.'):
    # Skip .git directory
    if '.git' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            if fix_file(filepath):
                count += 1

print(f'\nDone. {count} files updated.')
