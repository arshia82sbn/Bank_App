from Logger.Log_manager import LogManager
from Time_And_Config.time_and_config import Config, DateTimeUtils
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image ,ImageTk
from Database.login_database import _Login, _data_base
import threading
import tkinter as tk
import time
import os

# Icon file paths (replace with actual paths)
logo_icon = os.path.join(os.path.dirname(__file__), "logo.png")
account_icon = os.path.join(os.path.dirname(__file__), "account.png")
menu_icon = os.path.join(os.path.dirname(__file__), "menu_icon.png")


class BankApp(ctk.CTk):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.resizable(0, 0)

        self.logger = LogManager().get_logger()
        self.title(Config.get_app_title())
        self.geometry(Config.get_default_window_size())
        self.minsize(*Config.get_min_window_size())
        self.maxsize(*Config.get_max_window_size())
        ctk.set_appearance_mode(Config.get_theme_settings()['mode'])

        logo_path = os.path.join(os.path.dirname(__file__), 'bank.png')
        logo_icon = ImageTk.PhotoImage(Image.open(logo_path))
        self.iconphoto(False, logo_icon)
        self.after(250, lambda: self.iconphoto(False, logo_icon))

        self._login = _Login()
        self.db = _data_base()
        self.datetime_util = DateTimeUtils()

        # Thread management variables
        self.active_threads = []
        self.thread_lock = threading.Lock()
        self.after_id = None
        self.login_after_id = None
        self.selected_row = None
        self.row_frames = []

        self.logger.info("Setting up the application")
        self.upper_frame = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color='#2E2E2E'
        )
        self.upper_frame.pack(side="top", fill="x", padx=10, pady=20)
        # Main frames for login UI
        self.menu_frame = ctk.CTkFrame(
            self,
            corner_radius=20,
            height=588,
            width=204,
            fg_color='#2E2E2E'
        )
        self.menu_frame.pack(side="right", fill="both", padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=20,
            width=955,
            height=588,
            fg_color='#2E2E2E'
        )
        self.main_frame.pack(side="right", fill="both", padx=10, pady=10, expand=True)
        self._create_upper_frame()
        self._create_login_ui()

    def _create_upper_frame(self):
        # Logo
        try:
            self.logo_icon_image = ctk.CTkImage(Image.open(logo_icon), size=(50, 50))
            self.logo_lbl = ctk.CTkLabel(
                self.upper_frame,
                image=self.logo_icon_image,
                text=' '
            )
            self.logo_lbl.pack(side="left", padx=10, pady=10)
        except Exception as e:
            self.logger.error(f"Error loading logo: {str(e)}")

        # Company name
        self.company_lbl = ctk.CTkLabel(
            self.upper_frame,
            text=Config.get_app_title(),
            text_color='white',
            font=('Arial', 24, 'bold')
        )
        self.company_lbl.pack(side="left", padx=0, pady=10)

        # Time label
        self.time_label = ctk.CTkLabel(
            self.upper_frame,
            text=f"{self.datetime_util.get_current_time()}",
            font=("Arial", 14, "bold"),
            fg_color="#2645C4",
            corner_radius=20
        )
        self.time_label.pack(side="right", padx=20, pady=10)

    def _create_login_ui(self):
        # Login page title
        self.login_title = ctk.CTkLabel(
            self.main_frame,
            text="Bank System Login",
            font=("Arial", 24, "bold"),
            text_color="#2645C4"
        )
        self.login_title.pack(pady=30)

        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Username",
            width=300,
            height=40,
            font=("Arial", 14)
        )
        self.username_entry.pack(pady=10)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Password",
            show="*",
            width=300,
            height=40,
            font=("Arial", 14)
        )
        self.password_entry.pack(pady=10)

        # Login button
        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="Login",
            command=self._login_btn_forward,
            fg_color="#2645C4",
            width=150,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.login_button.pack(pady=20)

        # Start updating time
        self.login_after_id = self.after(1000, self._update_login_clock)

    def _login_btn_forward(self):
        """Manage login using a Thread"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Disable buttons while processing
        self.login_button.configure(state="disabled")
        self.login_button.configure(text="Processing...")

        # Create Thread for login operation
        login_thread = threading.Thread(
            target=self._perform_login,
            args=(username, password),
            daemon=True
        )
        login_thread.start()

        # Track active Thread
        with self.thread_lock:
            self.active_threads.append(login_thread)

    def _perform_login(self, username, password):
        """Perform login operation in a separate Thread"""
        try:
            success = self._login.login_btn(username, password)
            # Return to main Thread to update UI
            self.after(0, self._handle_login_result, success)
        except Exception as e:
            self.logger.error(f"Login error: {str(e)}")
            self.after(0, self._show_message_box, 'Error', f'Login failed: {str(e)}', 'error')

    def _handle_login_result(self, success):
        """Process login result in main Thread"""
        # Re-enable buttons
        self.login_button.configure(state="normal")
        self.login_button.configure(text="Login")

        if success:
            try:
                self._show_message_box('Success', 'Login was successful', 'info')
                self._destroy_login_ui()
                self._create_main_ui()
            except Exception as e:
                self.logger.error(f"Error handling login result: {str(e)}")
        else:
            self.logger.warning("Login failed")
            self._show_message_box(
                'Login Failed',
                f'{"Username" if self._login.get_login_problem() == "Username" else "Password"} is incorrect',
                'error'
            )

    def _destroy_login_ui(self):
        """Destroy widgets related to login page"""
        try:
            if self.login_after_id:
                self.after_cancel(self.login_after_id)
                self.login_after_id = None

            # Remove main_frame widgets
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # Remove menu_frame widgets
            for widget in self.menu_frame.winfo_children():
                widget.destroy()
        except Exception as e:
            self.logger.error(f"Error destroying login UI: {str(e)}")

    def _create_main_ui(self):
        """Create main UI after successful login"""
        # Create icons
        try:
            self.account_icon_img = ctk.CTkImage(Image.open(account_icon), size=(25, 25))
            self.menu_icon_img = ctk.CTkImage(Image.open(menu_icon), size=(25, 25))
        except Exception as e:
            self.logger.error(f"Error loading icons: {str(e)}")
            self.account_icon_img = None
            self.menu_icon_img = None
        try:
            # User info button
            self.user_btn = ctk.CTkButton(
                self.menu_frame,
                text=self._login.get_username(),
                image=self.account_icon_img,
                fg_color="#2645C4",
                command=self._show_user_info,
                width=180,
                height=40,
                font=("Arial", 14, "bold")
            )
            self.user_btn.pack(pady=20, padx=10)

            # Search bar
            self.search_entry = ctk.CTkEntry(
                self.upper_frame,
                placeholder_text="Search by account number or national ID",
                width=300,
                height=35
            )
            self.search_entry.pack(side="left", padx=10)

            self.search_button = ctk.CTkButton(
                self.upper_frame,
                text="Search",
                command=self._search_accounts,
                fg_color="#2645C4",
                width=80,
                height=35
            )
            self.search_button.pack(side="left", padx=10)
        except Exception as e:
            self.logger.error(f"Error creating main UI: {str(e)}")
        try:
            # Create accounts table
            self._create_accounts_table()
        except Exception as e:
            self.logger.error(f'Create the table:{str(e)}')
        try:
            # Create menu buttons
            self._create_menu_buttons()
        except Exception as e:
            self.logger.error(f'Create the menu button:{str(e)}')
        try:
            # Start updating clock
            self.after_id = self.after(1000, self._update_clock)
        except Exception as e:
            self.logger.error(f"Error updating clock: {str(e)}")

    def _create_accounts_table(self):
        # Header
        column_names = ["Account Id", "National Code", "Full Name", "Opening Date", "State", "Balance"]
        customers = self.db.get_all_customers()
        rows = [list(row) for row in customers]

        # Clear previous
        self.row_frames.clear()

        # Header frame
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 0))
        for col_name in column_names:
            header_label = ctk.CTkLabel(
                self.header_frame,
                text=col_name,
                width=100,
                height=30,
                fg_color="#2645C4",
                text_color="white",
                corner_radius=5,
                anchor="center",
                font=("Arial", 12, "bold")
            )
            header_label.pack(side="left", expand=True, fill="x", padx=2)

        # Scroll area
        self.rows_container = ctk.CTkFrame(self.main_frame, fg_color="#2B2E2E")
        self.rows_container.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        canvas = ctk.CTkCanvas(self.rows_container, bg="#2B2E2E", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(self.rows_container, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ctk.CTkFrame(canvas, fg_color="#2B2E2E")
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        odd_bg = "#2E2E2E"
        even_bg = "#1F1F1F"

        # Rows
        for row_index, row_values in enumerate(rows):
            bg_color = odd_bg if (row_index % 2 == 0) else even_bg
            row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
            row_frame.pack(fill="x", expand=True, pady=2, padx=2)
            row_frame.original_bg = bg_color
            self.row_frames.append(row_frame)

            for cell_value in row_values:
                cell_label = ctk.CTkLabel(
                    row_frame,
                    text=f"{cell_value:^27}",
                    height=30,
                    text_color="white",
                    fg_color=bg_color,
                    anchor="center",
                    font=("Arial", 12)
                )
                cell_label.pack(side="left", expand=True, fill="x", padx=22)
                cell_label.bind("<Button-1>", lambda e, idx=row_index: self._select_row(idx))

            row_frame.bind("<Button-1>", lambda e, idx=row_index: self._select_row(idx))

        # Empty
        if not rows:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No customers to display.",
                text_color="white",
                fg_color="#2B2E2E",
                font=("Arial", 12, "italic")
            )
            no_data_label.pack(expand=True, pady=20)

    def add_row(self, data):
        row_frame = ctk.CTkFrame(self.scrollable_frame)
        row_frame.pack(side="left", fill="x", expand=True, pady=10)
        for items in data:
            for item in items:
                cell_label = ctk.CTkLabel(row_frame, text=item, anchor="center", font=("Arial", 11))
                cell_label.pack(side="left", fill="x", expand=True, padx=5)

    def _select_row(self, row_index):
        # Deselect previous
        if self.selected_row is not None and 0 <= self.selected_row < len(self.row_frames):
            prev_frame = self.row_frames[self.selected_row]
            prev_color = prev_frame.original_bg
            prev_frame.configure(fg_color=prev_color)
            for widget in prev_frame.winfo_children():
                widget.configure(fg_color=prev_color)

        # Select current
        self.selected_row = row_index
        selected_frame = self.row_frames[row_index]
        selected_color = "#3A71D1"
        selected_frame.configure(fg_color=selected_color)
        for widget in selected_frame.winfo_children():
            widget.configure(fg_color=selected_color)

    def _create_menu_buttons(self):
        # Buttons
        cfg = {"width": 180, "height": 40, "fg_color": "#2645C4", "font": ("Arial", 14)}
        buttons = [
            ("Create New Account", self._create_account),
            ("Edit Account", self._open_edit_account_dialog),
            ("Change Status Account", self._change_status_account),
            ("Withdraw Funds", self._open_withdraw_dialog),
            ("Deposit Funds", self._open_deposit_dialog),
            ("Add User", self._open_add_user_dialog),
            ("Delete User", self._delete_account),
            ("Logout", self._logout)
        ]
        for text, cmd in buttons:
            btn = ctk.CTkButton(self.menu_frame, text=text, command=cmd, **cfg)
            btn.pack(pady=5, padx=10)

    def _update_login_clock(self):
        # Update login time
        if hasattr(self, "time_label") and self.time_label.winfo_exists():
            new_time = self.datetime_util.get_current_time()
            self.time_label.configure(text=new_time)
            self.login_after_id = self.after(1000, self._update_login_clock)

    def _update_clock(self):
        # Update main time
        try:
            if hasattr(self, "time_label") and self.time_label.winfo_exists():
                new_time = self.datetime_util.get_current_time()
                self.time_label.configure(text=new_time)
        except tk.TclError:
            pass
        finally:
            if self.winfo_exists():
                self.after_id = self.after(1000, self._update_clock)

    def _search_accounts(self):
        # Search logic
        term = self.search_entry.get().strip()
        if not term:
            self._show_message_box("Error", "Please enter a search term", "warning")
            return

        self.logger.info(f"Search for: {term}")
        results = self.db.search_accounts(term)
        if not results:
            self._show_message_box("Info", f"No accounts found for '{term}'", "info")
            return

        # Clear old
        for frame in self.row_frames:
            frame.destroy()
        self.row_frames.clear()
        self.selected_row = None

        odd_bg = "#2E2E2E"
        even_bg = "#1F1F1F"

        # Display results
        for idx, vals in enumerate(results):
            bg_color = odd_bg if (idx % 2 == 0) else even_bg
            row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
            row_frame.pack(fill="x", expand=True, pady=2, padx=2)
            row_frame.original_bg = bg_color
            self.row_frames.append(row_frame)

            for cell in vals:
                cell_label = ctk.CTkLabel(
                    row_frame,
                    text=str(cell),
                    height=30,
                    text_color="white",
                    fg_color=bg_color,
                    anchor="center",
                    font=("Arial", 12)
                )
                cell_label.pack(side="left", expand=True, fill="x", padx=22)
                cell_label.bind("<Button-1>", lambda e, idx=idx: self._select_row(idx))

            row_frame.bind("<Button-1>", lambda e, idx=idx: self._select_row(idx))

    def _create_account(self):
        # Open create dialog
        try:
            dialog = ctk.CTkToplevel(self)
            dialog.title("Create New Account")
            dialog.geometry("400x300")
            dialog.grab_set()

            fields = [
                ("Account Number:", ctk.CTkEntry(dialog)),
                ("National ID:", ctk.CTkEntry(dialog)),
                ("First Name:", ctk.CTkEntry(dialog)),
                ("Last Name:", ctk.CTkEntry(dialog)),
                ("Account Type:", ctk.CTkComboBox(dialog, values=["Checking", "Savings", "Interest-Free Loan"]))
            ]
            for i, (lbl, widget) in enumerate(fields):
                ctk.CTkLabel(dialog, text=lbl).grid(row=i, column=0, padx=10, pady=5, sticky="e")
                widget.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            submit_btn = ctk.CTkButton(
                dialog,
                text="Submit Account",
                command=lambda: self._submit_new_account(fields[0][1].get(), fields[1][1].get(), dialog)
            )
            submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)
        except Exception as e:
            self.logger.error(f"Error creating new account: {e}")

    def _submit_new_account(self, account_number, national_id, dialog):
        # Submit new account
        if not account_number or not national_id:
            self._show_message_box("Error", "Please fill in all fields", "error")
            return

        self.logger.info(f"Create new account - Account Number: {account_number}, National ID: {national_id}")
        dialog.destroy()
        self._show_message_box("Success", "New account created successfully", "info")

    def _open_edit_account_dialog(self):
        # Open edit dialog
        if self.selected_row is None:
            self._show_message_box("Error", "Please select an account", "warning")
            return

        selected_data = self.db.get_all_customers()[self.selected_row]
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Account")
        dialog.geometry("400x300")
        dialog.grab_set()

        fields = [
            ("Account number:", ctk.CTkEntry(dialog)),
            ("Account name:", ctk.CTkEntry(dialog)),
            ("National ID:", ctk.CTkEntry(dialog)),
            ("Balance:", ctk.CTkEntry(dialog)),
        ]
        for i, (lbl, widget) in enumerate(fields):
            ctk.CTkLabel(dialog, text=lbl).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            widget.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        fields[0][1].insert(0, selected_data[0])
        fields[1][1].insert(0, selected_data[2])
        fields[2][1].insert(0, selected_data[1])
        fields[3][1].insert(0, selected_data[5])

        save_btn = ctk.CTkButton(
            dialog,
            text="Save Changes",
            command=lambda: self._edit_account({
                "Account number": fields[0][1].get(),
                "account name": fields[1][1].get(),
                "National ID": fields[2][1].get(),
                "Balance": fields[3][1].get()
            }, dialog)
        )
        save_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)

    def _edit_account(self, data, dialog):
        # Update account
        try:
            if not all(data.values()):
                self._show_message_box("Error", "Please fill in all fields", "cancel")
                return

            try:
                bal = str(data["Balance"])
                if int(bal.replace(",", "")) < 0:
                    raise ValueError("Balance cannot be negative")
            except ValueError as e:
                self._show_message_box("Error", str(e), "cancel")
                return

            success = self.db.update_account(
                account_number=data["Account number"],
                account_name=data["account name"],
                account_balance=bal,
                account_nationalcode=data["National ID"],
            )

            if success:
                self.logger.info(f"Edited account: {data['Account number']}")
                for child in self.main_frame.winfo_children():
                    child.destroy()
                self._show_message_box("Success", "Changes saved successfully", "info")
                self._create_accounts_table()
            else:
                self._show_message_box("Error", "Failed to update account", "cancel")

        except Exception as e:
            self.logger.error(f"Error editing account: {e}")
            self._show_message_box("Error", f"Failed to edit account: {e}", "cancel")

    def _change_status_account(self):
        # Toggle status
        idx = self.selected_row
        if idx is None:
            self._show_message_box("Error", "Please select an account", "warning")
            return

        if not self._question_messagebox("Confirm", "Are you sure you want to deactivate this account?"):
            return

        customers = self.db.get_all_customers()
        try:
            selected_row = customers[idx]
        except IndexError:
            self._show_message_box("Error", "Selected account not found", "error")
            return

        account_id = selected_row[0]
        success = self.db.deactivate_account(account_id)
        if success:
            self.logger.info(f"Account {account_id} deactivated")
            self._show_message_box("Success", "Account successfully deactivated", "info")
            for child in self.main_frame.winfo_children():
                child.destroy()
            self._create_accounts_table()
        else:
            self._show_message_box("Error", "Failed to deactivate account", "error")

    def _open_withdraw_dialog(self):
        # Withdraw dialog
        idx = self.selected_row
        if idx is None:
            self._show_message_box("Error", "Please select an account", "warning")
            return

        customers = self.db.get_all_customers()
        try:
            selected_row = customers[idx]
        except IndexError:
            self._show_message_box("Error", "Selected account not found", "error")
            return

        account_id = selected_row[0]
        current_balance = int(str(selected_row[5]).replace(",", ""))

        dialog = ctk.CTkToplevel(self)
        dialog.title("Withdraw Funds")
        dialog.geometry("400x300")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Withdrawal Amount:", font=("Arial", 14)).pack(pady=10)
        amount_entry = ctk.CTkEntry(dialog, placeholder_text="Enter amount", width=200, height=30, font=("Arial", 12))
        amount_entry.pack(pady=5)

        def on_withdraw():
            # Process withdrawal
            amt_text = amount_entry.get().strip()
            try:
                amount = int(amt_text.replace(",", ""))
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                if amount > current_balance:
                    self._show_message_box("Error", "Insufficient balance", "error")
                    return
            except ValueError:
                self._show_message_box("Error", "Please enter a valid amount", "error")
                return

            success = self.db.withdraw_account(account_id, amount)
            if success:
                self._show_message_box("Success", f"Withdrew {amount:,} successfully", "info")
                for child in self.main_frame.winfo_children():
                    child.destroy()
                self._create_accounts_table()
            else:
                self._show_message_box("Error", "Failed to withdraw funds", "error")

        ctk.CTkButton(
            dialog,
            text="Withdraw",
            fg_color="#2645C4",
            hover_color="#1A349F",
            width=120,
            height=35,
            font=("Arial", 12, "bold"),
            command=on_withdraw
        ).pack(pady=20)

    def _withdraw(self, amount, dialog):
        # Withdrawal without UI
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero")
        except ValueError:
            self._show_message_box("Error", "Please enter a valid amount", "cancel")
            return

        self.logger.info(f"Withdraw funds - Amount: {amount}")
        dialog.destroy()
        self._show_message_box("Success", "Funds withdrawn successfully", "info")

    def _open_deposit_dialog(self):
        # Deposit dialog
        idx = self.selected_row
        if idx is None:
            self._show_message_box("Error", "Please select an account", "warning")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Deposit Funds")
        dialog.geometry("400x200")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Deposit Amount:").pack(pady=10)
        amount_entry = ctk.CTkEntry(dialog)
        amount_entry.pack(pady=5)

        ctk.CTkButton(
            dialog,
            text="Deposit",
            command=lambda: self._deposit(amount_entry.get(), dialog)
        ).pack(pady=20)

    def _deposit(self, amount, dialog):
        # Perform deposit
        idx = self.selected_row
        if idx is None:
            self._show_message_box("Error", "Please select an account", "warning")
            return

        try:
            amt = int(str(amount).replace(",", ""))
            if amt <= 0:
                raise ValueError("Amount must be greater than zero")
        except ValueError:
            self._show_message_box("Error", "Please enter a valid amount", "error")
            return

        customers = self.db.get_all_customers()
        try:
            selected_row = customers[idx]
        except IndexError:
            self._show_message_box("Error", "Selected account not found", "error")
            return
        account_id = selected_row[0]

        success = self.db.deposit_account(account_id, amt)
        if not success:
            return

        self.logger.info(f"Deposit funds - Amount: {amt} into account {account_id}")
        self._show_message_box("Success", "Funds deposited successfully", "info")
        for child in self.main_frame.winfo_children():
            child.destroy()
        self._create_accounts_table()

    def _delete_account(self):
        # Delete account
        idx = self.selected_row
        if idx is None:
            self._show_message_box("Error", "Please select a user", "warning")
            return

        accounts = self.db.get_all_customers()
        try:
            selected_row = accounts[idx]
        except IndexError:
            self._show_message_box("Error", "Selected user not found", "cancel")
            return

        account_id = selected_row[0]
        if not self._question_messagebox("Confirm", f"Are you sure you want to delete user '{account_id}'?"):
            return

        success = self.db.delete_account(account_id)
        if success:
            self.logger.info(f"Deleted user: {account_id}")
            self._show_message_box("Success", "User deleted successfully", "info")
            for child in self.main_frame.winfo_children():
                child.destroy()
            self._create_accounts_table()
        else:
            self._show_message_box("Error", "Failed to delete user", "cancel")

    def _open_add_user_dialog(self):
        # Add user dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New User")
        dialog.geometry("400x250")
        dialog.grab_set()

        fields = [
            ("Username:", ctk.CTkEntry(dialog)),
            ("Password:", ctk.CTkEntry(dialog, show="*")),
            ("Full Name:", ctk.CTkEntry(dialog)),
            ("Role:", ctk.CTkComboBox(dialog, values=["Employee", "Branch Manager", "System Administrator"]))
        ]
        for i, (lbl, widget) in enumerate(fields):
            ctk.CTkLabel(dialog, text=lbl).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            widget.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        add_btn = ctk.CTkButton(
            dialog,
            text="Add User",
            command=lambda: self._add_user(fields[0][1].get(), fields[1][1].get(), dialog)
        )
        add_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)

    def _add_user(self, username, password, dialog):
        # Add user
        if not username or not password:
            self._show_message_box("Error", "Please fill in all fields", "error")
            return
        self.logger.info(f"Add new user - Username: {username}")
        dialog.destroy()
        self._show_message_box("Success", "New user added successfully", "info")

    def _delete_user(self):
        # Delete user
        idx = self.selected_row
        if idx is None:
            self._show_message_box("Error", "Please select a user", "warning")
            return

        employees = self.db.get_all_employees()
        try:
            selected_row = employees[idx]
        except IndexError:
            self._show_message_box("Error", "Selected user not found", "error")
            return

        username = selected_row[1]
        if not self._question_messagebox("Confirm", f"Are you sure you want to delete user '{username}'?"):
            return

        success = self.db.delete_user(username)
        if success:
            self.logger.info(f"Deleted user: {username}")
            self._show_message_box("Success", "User deleted successfully", "info")
            for child in self.main_frame.winfo_children():
                child.destroy()
            self._create_accounts_table()
        else:
            self._show_message_box("Error", "Failed to delete user", "error")

    def _show_user_info(self):
        # User info
        dialog = ctk.CTkToplevel(self)
        dialog.title("User Information")
        dialog.geometry("600x600")
        dialog.grab_set()

        info = f"Username: {self._login.get_username()}\nLogin Time: {self.datetime_util.get_current_time()}"
        ctk.CTkLabel(dialog, text=info, justify="left").pack(pady=20, padx=20)

        logout_btn = ctk.CTkButton(
            dialog,
            text="Logout",
            command=self._logout,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            corner_radius=20
        )
        logout_btn.pack(pady=10)

        if self._login.get_username() == "admin":
            add_user_btn = ctk.CTkButton(
                dialog,
                text="Add User",
                command=self._open_add_user_dialog,
                fg_color="#2ecc71",
                hover_color="#1abc9c"
            )
            add_user_btn.pack(pady=10)

            delete_user_btn = ctk.CTkButton(
                dialog,
                text="Delete User",
                fg_color="#d50000",
                command=self._delete_user,
                hover_color="#ff1515"
            )
            delete_user_btn.pack(pady=10)

            show_list_employee = ctk.CTkButton(
                dialog,
                text="Show List Employee",
                fg_color="#2645C4",
                command=self._create_employees_table
            )
            show_list_employee.pack(pady=10)

    def _create_employees_table(self):
        # Employees header
        column_names = ["Employee ID", "Username", "Old", "Full Name", "Position", "Branch Code"]
        employees = self.db.get_all_employees()
        rows = [[e[0], e[1], e[2], e[3], e[4], e[5]] for e in employees]

        # Clear previous
        if hasattr(self, "user_row_frames"):
            self.user_row_frames.clear()
        else:
            self.user_row_frames = []

        # Header frame
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2E")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        for col_name in column_names:
            lbl = ctk.CTkLabel(
                header_frame,
                text=col_name,
                width=100,
                height=30,
                fg_color="#2645C4",
                text_color="white",
                corner_radius=5,
                anchor="center",
                font=("Arial", 12, "bold")
            )
            lbl.pack(side="left", expand=True, fill="x", padx=2)

        # Scroll area
        rows_container = ctk.CTkFrame(self.main_frame, fg_color="#2B2E2E")
        rows_container.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        canvas = ctk.CTkCanvas(rows_container, bg="#2B2E2E", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(rows_container, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.user_scrollable_frame = ctk.CTkFrame(canvas, fg_color="#2B2E2E")
        self.user_scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.user_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        odd_bg = "#2E2E2E"
        even_bg = "#1F1F1F"

        # Rows
        for idx, vals in enumerate(rows):
            bg_color = odd_bg if (idx % 2 == 0) else even_bg
            row_frame = ctk.CTkFrame(self.user_scrollable_frame, fg_color=bg_color, corner_radius=5)
            row_frame.pack(fill="x", expand=True, pady=2, padx=2)
            row_frame.original_bg = bg_color
            self.user_row_frames.append(row_frame)

            for cell in vals:
                lbl = ctk.CTkLabel(
                    row_frame,
                    text=str(cell),
                    height=30,
                    text_color="white",
                    fg_color=bg_color,
                    anchor="center",
                    font=("Arial", 12)
                )
                lbl.pack(side="left", expand=True, fill="x", padx=22)
                lbl.bind("<Button-1>", lambda e, i=idx: self._select_user_row(i))

            row_frame.bind("<Button-1>", lambda e, i=idx: self._select_user_row(i))

        if not rows:
            no_data_label = ctk.CTkLabel(
                self.user_scrollable_frame,
                text="No employees to display.",
                text_color="white",
                fg_color="#2B2E2E",
                font=("Arial", 12, "italic")
            )
            no_data_label.pack(expand=True, pady=20)

        self.selected_user_row = None

    def _select_user_row(self, row_index):
        # Deselect prev
        if hasattr(self, "selected_user_row") and \
                self.selected_user_row is not None and \
                0 <= self.selected_user_row < len(self.user_row_frames):
            prev_frame = self.user_row_frames[self.selected_user_row]
            prev_color = prev_frame.original_bg
            prev_frame.configure(fg_color=prev_color)
            for widget in prev_frame.winfo_children():
                widget.configure(fg_color=prev_color)

        # Select new
        self.selected_user_row = row_index
        selected_frame = self.user_row_frames[row_index]
        selected_color = "#3A71D1"
        selected_frame.configure(fg_color=selected_color)
        for widget in selected_frame.winfo_children():
            widget.configure(fg_color=selected_color)

    def _logout(self):
        # Logout
        if self._question_messagebox("Confirm", "Are you sure you want to logout?"):
            self._login.login_status = False
            self._destroy_main_ui()
            self._create_login_ui()
            self.logger.info("User logged out")

    def _destroy_main_ui(self):
        # Clear UI
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        for widget in self.main_frame.winfo_children():
            widget.destroy()
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        if hasattr(self, "search_entry") and self.search_entry.winfo_exists():
            self.search_entry.destroy()
        if hasattr(self, "search_button") and self.search_button.winfo_exists():
            self.search_button.destroy()

    def _show_message_box(self, title, message, icon):
        # Message
        if icon == "error":
            icon = "cancel"
        CTkMessagebox(
            title=title,
            message=message,
            icon=icon.lower(),
            title_color="#2645C4",
            button_color="#2645C4",
            button_hover_color="#1A349F"
        )

    def _question_messagebox(self, title, message):
        # Confirm
        result = CTkMessagebox(
            title=title,
            message=message,
            icon="question",
            option_1="Yes",
            option_2="No",
            title_color="#2645C4",
            button_color="#2645C4",
            button_hover_color="#1A349F"
        ).get()
        return result == "Yes"

    def on_close(self):
        # Exit
        if self.login_after_id:
            self.after_cancel(self.login_after_id)
        if self.after_id:
            self.after_cancel(self.after_id)
        self._wait_for_threads()
        self.destroy()

    def _wait_for_threads(self, timeout=2.0):
        """Wait for active threads to finish"""
        start_time = time.time()
        for t in self.active_threads[:]:
            if t.is_alive():
                remaining = timeout - (time.time() - start_time)
                if remaining > 0:
                    t.join(remaining)
                if t.is_alive():
                    self.logger.warning(f"Thread {t.name} did not terminate")
            with self.thread_lock:
                if t in self.active_threads:
                    self.active_threads.remove(t)


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()
