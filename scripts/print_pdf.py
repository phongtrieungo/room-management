"""Print review HTML; does not approve readings or produce billing amounts."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    source, target = map(Path, sys.argv[1:])
    if target.exists():
        raise SystemExit(f'Refusing to overwrite {target}')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(source.resolve().as_uri(), wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        page.pdf(path=str(target), prefer_css_page_size=True,
                 print_background=True, display_header_footer=False, scale=1)
        browser.close()

if __name__ == '__main__':
    main()
