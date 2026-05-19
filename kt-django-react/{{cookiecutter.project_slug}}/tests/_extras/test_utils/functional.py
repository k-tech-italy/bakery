def ui_login(sb, frontend_url, test_user):
    """Log in to the application via the browser UI."""
    sb.open(f"{frontend_url}/login")
    sb.type("input#username", test_user.username)
    sb.type("input#password", test_user._raw_password)
    sb.click('button[type="submit"]')
    sb.wait_for_element(".app-content", timeout=10)
