def test_furla_title(browser):
    page = browser.new_page()
    page.goto('https://www.furla.com/gr/en/')
    title = page.title()
    assert "Furla" in title, f"Expected 'Furla' in title, but got '{title}'"

    print(f"Title of the page: {title}")
