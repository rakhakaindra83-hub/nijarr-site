from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome')
    page = browser.new_page(viewport={"width":1440,"height":900})
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto(Path(__file__).with_name('index.html').as_uri())
    page.wait_for_timeout(2800)
    assert page.locator('.night-city').count()==1, 'Night city background is missing'
    page.mouse.move(1300,200)
    page.wait_for_timeout(900)
    assert page.locator('.night-city').evaluate("e=>getComputedStyle(e).transform")!='none'
    assert page.locator('.cursor-glow').evaluate("e=>getComputedStyle(e).opacity")=='1'
    page.mouse.move(100,700)
    page.wait_for_timeout(900)
    first=page.locator('.night-city').evaluate("e=>getComputedStyle(e).transform")
    page.mouse.move(1300,100)
    page.wait_for_timeout(900)
    assert first!=page.locator('.night-city').evaluate("e=>getComputedStyle(e).transform")
    page.locator('.gallery-toggle').click()
    page.locator('.video').nth(1).click()
    assert page.locator('dialog').evaluate('e=>e.open')
    page.locator('dialog button').click()
    assert not page.locator('dialog iframe').get_attribute('src')
    assert page.locator('.carousel').evaluate("e=>e.classList.contains('paused')")
    page.evaluate("scrollTo({top:0,behavior:'instant'})")
    page.wait_for_timeout(1000)
    page.mouse.move(700,450)
    page.screenshot(path=str(Path(__file__).with_name('night-desktop.png')),full_page=False)
    assert not errors, errors
    mobile=browser.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True)
    tab=mobile.new_page(); tab.goto(Path(__file__).with_name('index.html').as_uri()); tab.wait_for_timeout(2800)
    assert tab.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Mobile overflow'
    assert tab.locator('.cursor-glow').count()==0
    tab.screenshot(path=str(Path(__file__).with_name('night-mobile.png')),full_page=True)
    reduced=browser.new_context(reduced_motion='reduce')
    tab=reduced.new_page(); tab.goto(Path(__file__).with_name('index.html').as_uri())
    assert tab.locator('.cursor-glow').count()==0
    assert tab.locator('.night-city').evaluate("e=>getComputedStyle(e).transform")=='none'
    assert tab.locator('.video-track').evaluate("e=>getComputedStyle(e).animationName")=='none'
    browser.close()
    print('PASS: city parallax, cursor, popup, gallery pause, mobile overflow, touch, reduced motion, no JS errors')
