from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome')
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(Path(__file__).with_name('index.html').as_uri())
    page.wait_for_timeout(1200)
    assert page.title() == 'Nijarr — Minecraft & Senyawa'
    assert page.locator('a[href="https://www.youtube.com/@NijarMC"]').count() == 2
    assert page.locator('.video-track > button:not([aria-hidden])').count() == 44
    assert page.locator('.gallery-toggle').count() == 1
    page.locator('.gallery-toggle').click()
    assert page.locator('.carousel').evaluate('(el)=>el.classList.contains("paused")')
    page.locator('.video-track > button').first.click()
    assert page.locator('#video-popup').evaluate('(el)=>el.open')
    assert 'NROraOaqPqg' in page.locator('#video-popup iframe').get_attribute('src')
    page.locator('#video-popup button').click()
    assert page.locator('#video-popup iframe').get_attribute('src') is None
    assert page.locator('.brand img').evaluate('(img)=>img.complete && img.naturalWidth > 0')
    assert page.locator('.featured').evaluate('(el)=>getComputedStyle(el).animationName') == 'arrival'
    page.mouse.move(700, 300)
    page.wait_for_timeout(500)
    assert page.locator('.cursor-glow').count() == 1
    assert page.locator('.cursor-glow').evaluate('(el)=>getComputedStyle(el).opacity') == '1'
    assert page.locator('.cursor-glow').evaluate('(el)=>getComputedStyle(el).pointerEvents') == 'none'
    assert page.locator('.cursor-glow').evaluate('(el)=>el.style.transform') == 'translate(700px, 300px)'
    page.evaluate("document.documentElement.dispatchEvent(new PointerEvent('pointerleave'))")
    page.wait_for_timeout(500)
    assert page.locator('.cursor-glow').evaluate('(el)=>getComputedStyle(el).opacity') == '0'
    page.locator('#videos').scroll_into_view_if_needed()
    page.wait_for_timeout(1000)
    assert not page.locator('.section-heading').evaluate('(el)=>el.classList.contains("pending")')
    page.screenshot(path=str(Path(__file__).with_name('desktop-check.png')), full_page=True)
    for width in (375, 760, 1440):
        page.set_viewport_size({"width": width, "height": 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
    page.emulate_media(reduced_motion='reduce')
    page.reload()
    assert page.locator('.pending').count() == 0
    assert page.locator('.featured').evaluate('(el)=>getComputedStyle(el).animationName') == 'none'
    assert not errors, errors
    browser.close()
print('PASS: channel/video links, logo, desktop/mobile overflow, reveal, reduced motion, no JS errors.')
