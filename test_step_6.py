import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


def test_furla_title(browser):
    page = browser.new_page()
    page.goto('https://www.furla.com/gr/en/')
    title = page.title()
    assert "Furla" in title, f"Expected 'Furla' in title, but got '{title}'"

    print(f"Title of the page: {title}")
