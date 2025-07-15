# ⚙️ Configuration & DateTime Utilities

A clean and modular utility suite providing application configuration settings and handy date-time operations for Python projects. Perfect for centralizing constants and time-related tasks in your BankApp (or any other app)! 🕰️

---

## 📦 What’s Inside

1. **`Config` Class** — Manages application-wide settings:
   - **Title & Version**: `get_app_title()`, `get_app_version()` 🏷️
   - **Window Sizes**: Default, minimum, and maximum dimensions for UI layouts 📐
   - **Theme Settings**: Central place for theme mode & color (`DARK`/`LIGHT`, color themes) 🎨

2. **`DateTimeUtils` Class** — Static methods for retrieving formatted date & time:
   - **`get_current_time()`**: Returns current time (`HH:MM:SS`) ⏰
   - **`get_current_date()`**: Returns current date (`YYYY-MM-DD`) 📅
   - **`get_full_datetime()`**: Returns full timestamp (`YYYY-MM-DD HH:MM:SS`) 🗓️🕒

3. **`ThemeMode` Enum** — (Future-proof) Enum for theme modes: `DARK`, `LIGHT` 💡

---

## 🚀 Quick Start

1. **Add the file** to your project:
   ```bash
   BankApp/
   ├── Time_And_Config/
   │   └── time_and_config.py    # Contains Config & DateTimeUtils
   └── ...
   ```

2. **Import & Use**:
   ```python
   from Time_And_Config.time_and_config import Config, DateTimeUtils, ThemeMode

   title = Config.get_app_title()
   version = Config.get_app_version()
   default_size = Config.get_default_window_size()

   now_time = DateTimeUtils.get_current_time()
   today = DateTimeUtils.get_current_date()
   full = DateTimeUtils.get_full_datetime()

   theme = ThemeMode.DARK.value
   ```

---

## 🌟 Why Use These Utilities?

- **Centralized Configuration**: Change your app’s title, version, window parameters, and theme in one place.
- **Consistency**: Avoid magic strings/numbers scattered across your codebase.
- **Reusability**: Drop these utilities into any Python project for instant date-time and config management.
- **Future-Proof**: Easily extend `Config` with new settings or theme options as your app grows.

---

## 🔧 Code Highlights

### Configuration Class
```python
class Config:
    __APP_TITLE = "Bank Account Management System"
    __APP_VERSION = "1.0.0"
    __DEFAULT_WINDOW_SIZE = "1200x700"
    __MIN_WINDOW_SIZE = (800, 500)
    __MAX_WINDOW_SIZE = (1200, 900)
    __THEME_SETTINGS = {"mode": "#000000", "color_theme": "blue"}

    @classmethod
    def get_app_title(cls): return cls.__APP_TITLE
    ...
```

### DateTime Utilities
```python
class DateTimeUtils:
    @staticmethod
    def get_current_time():
        return datetime.datetime.now().strftime("%H:%M:%S")
```

---

## 🌱 Extending

- **Add New Configs**: Add more `__PRIVATE` class variables and corresponding getters.
- **Localization**: Extend `DateTimeUtils` to support different timezones or locales.
- **Enum Enhancements**: Use `ThemeMode` to automatically apply light/dark themes in your UI.

---
