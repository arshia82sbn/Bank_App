# 📝 LogManager Utility for BankApp

A comprehensive **singleton**-based logging utility tailored for thread-safe, centralized logging in the BankApp. Harnesses Python's built-in `logging` module with custom formatting and concurrency protection! 🛡️

---

## 🚀 Key Highlights

- **🔒 Singleton Pattern**: Ensures only one `LogManager` instance throughout the application lifecycle.
- **🧵 Thread Safety**: Uses a `threading.Lock` to guard against race conditions during instantiation and initialization.
- **🎯 Custom Formatting**: Logs include timestamp, logger name, level, source file, line number, and message.
- **📣 Level Control**:
  - **Logger Level**: Set to `DEBUG` to capture all levels.
  - **Console Handler**: Defaults to `INFO` to avoid cluttering the console with overly verbose debug logs.
- **🔁 Idempotent Initialization**: Prevents duplicate handlers and reconfiguration on subsequent imports or uses.

---

## 📦 Installation & Usage

1. **Add `Log_manager.py` to Your Project**:
   ```bash
   BankApp/
   ├── Log_manager.py   # Contains LogManager singleton
   └── ...
   ```

2. **Import & Retrieve Logger**:
   ```python
   from Log_manager import get_logger

   logger = get_logger()
   logger.info("Application started")
   ```

3. **Log with Levels**:
   ```python
   logger.debug("Debugging details...")
   logger.info("Informational message")
   logger.warning("Warning! Check this out")
   logger.error("An error occurred", exc_info=True)
   logger.critical("Critical issue! Immediate action required")
   ```

---

## ⚙️ How It Works

1. **Instantiation (`__new__`)**
   - Checks if an instance exists; if not, acquires a lock and creates one.
   - Subsequent calls return the same instance.

2. **Initialization (`__init__`)**
   - Double-checked locking ensures the initialization block runs only once.
   - Configures:
     - A `Formatter` with pattern:  
       ```
       %(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s
       ```
     - A **console handler** at `INFO` level.
     - (Optional) Uncomment `FileHandler` to log to `bank_system.log` with UTF-8 encoding.

3. **Accessing the Logger**
   - Use `get_logger()` or `LogManager().get_logger()` anywhere in your code to fetch the centralized logger.

---

## 🌱 Extending & Customization

- **File Logging**:
  ```python
  file_handler = logging.FileHandler('bank_system.log', encoding='utf-8')
  file_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)
  ```

- **Log Level Adjustment**:
  ```python
  logger.setLevel(logging.WARNING)
  console_handler.setLevel(logging.ERROR)
  ```

- **Multiple Handlers**: Add handlers for rotating files, external systems, or HTTP endpoints.
- **Contextual Logging**: Integrate with `logging.LoggerAdapter` to inject request IDs or user IDs.

---
