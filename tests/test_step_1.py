def test_furla_title(driver):
    title = driver.title
    print(title)
    assert "Furla" in title, f"Expected 'Furla' in title, but got '{title}'"
