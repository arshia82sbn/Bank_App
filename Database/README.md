# 🏦 Bank Account & Employee Management System

Welcome to the **Bank Account & Employee Management System** — a robust Python application for handling customer accounts and employee records using SQLite, CustomTkinter, and modular design! 🚀

---

## 🌟 Key Features

- **🔐 Secure Login**: Validates users against the `employees` table (default admin: `admin/admin`).
- **🏢 Employee CRUD**: Create, read, search, and delete employee records with unique constraints.
- **💳 Customer Accounts**: Create, update, deactivate/reactivate, deposit, withdraw, and delete customer bank accounts.
- **📊 Transaction Logging**: Integrated with `LogManager` for audit trails and info logs.
- **🗓️ Timestamp Utilities**: Uses `DateTimeUtils` for consistent date-time formatting.
- **📦 Modular Structure**: Separated database logic (`_data_base`) and authentication (`_Login`).
- **💬 User Feedback**: Interactive pop-ups with `CTkMessagebox` for errors, confirmations, and status updates.

---

## 🛠️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/BankApp.git
   cd BankApp
   ```

2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   The database `bank_account.db` will auto-create in the project folder on first run, with the `employees` and `customers` tables.

5. **Run the Application**
   ```bash
   python main.py
   ```

---

## 📂 Project Structure

```bash
BankApp/
├── Time_And_Config/
│   └── time_and_config.py       # DateTimeUtils utility
├── Log_manager.py               # LogManager setup
├── bank_account.db              # SQLite database (auto-generated)
├── main.py                      # Application entry point (login & GUI setup)
├── database.py                  # `_data_base` class with all DB operations
├── auth.py                      # `_Login` class for authentication flow
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 💻 Code Highlights

### 1. `_data_base` Class
- **Initialization**: Creates `employees` table (with default `admin`) if missing. 📋
- **CRUD Operations**:
  - `add_employee`, `delete_user`, `get_all_employees`, `search_employees`
  - `create_account`, `update_account`, `deactivate_account`, `delete_account`
  - `deposit_account`, `withdraw_account` with balance checks 💰
  - `get_all_customers`, `search_accounts` with wildcard support 🔍

### 2. `_Login` Class
- **Login Flow**: `login_btn(username, password)` sets status, handles empty credentials, logs attempts 🔐
- **Status Accessors**: `get_login_status()`, `get_username()`, `get_login_problem()`

### 3. Error Handling & UX
- **CTkMessagebox** pop-ups for:
  - Missing data or invalid operations 🚫
  - Success confirmations ✅
  - Exceptions and rollbacks 💥
- **Logging**: All major actions use `LogManager` for traceability.

---

## 🚀 Getting Started

1. **Login Screen**: Enter your credentials (`admin` / `admin`).
2. **Dashboard**:
   - **Employees Tab**: Manage employee records.
   - **Customers Tab**: Manage bank accounts.
3. **Perform Operations**: Use intuitive buttons and forms to create, update, or remove records.
4. **Feedback**: Pop-ups guide you through success or error messages.

---

## 🛡️ Security & Best Practices

- **Password Storage**: Currently plain text — consider hashing (e.g., `bcrypt`) for production. 🔒
- **Input Validation**: SQL parameters are parameterized to prevent injection.
- **Error Logging**: All exceptions logged via `LogManager`.

---

## 🌱 Future Improvements

- 🔒 **Password Hashing**: Integrate secure hashing algorithms.
- 🤖 **Role-Based Access**: Differentiate admin and teller permissions.
- 📥 **Transaction History**: Track deposits/withdrawals per account.
- 🌐 **Web Interface**: Develop a Flask/Django front-end.
- 📊 **Reporting & Analytics**: Visualize account and employee stats.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📬 Contact

Built with ❤️ by **Arshia Saberian**. For questions or collaborations, email me at [Arshia82sbn@gmail.com](mailto:Arshia82sbn@gmail.com).

---
