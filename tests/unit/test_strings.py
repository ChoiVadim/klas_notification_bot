import pytest
from app.strings import Strings, Language


def test_string_get():
    # Test getting string with default language
    welcome_msg = Strings.get("test_string", Language.EN, name="Test User")
    assert "Welcome, Test User!" in welcome_msg

    # Test getting string with Korean language
    welcome_msg_ko = Strings.get("test_string", Language.KO, name="Test User")
    assert "환영합니다!" in welcome_msg_ko

    # Test getting string with Russian language
    welcome_msg_ru = Strings.get("test_string", Language.RU, name="Test User")
    assert "Добро пожаловать!" in welcome_msg_ru


def test_string_fallback():
    # Test fallback to English when translation not found
    msg = Strings.get("nonexistent_key", Language.KO)
    assert msg == Strings.get("nonexistent_key", Language.EN)
