# Splitwise CLI App (Python)

This is a command-line based expense sharing application inspired by [Splitwise](https://www.splitwise.com/). It lets you split expenses among friends using different methods (EQUAL, EXACT, PERCENT), track balances, and check who owes whom — all from your terminal.

## 💡 Features

- Track shared expenses between multiple users
- Split bills using:
  - EQUAL
  - EXACT
  - PERCENT
- Show all outstanding balances
- Show balances for a specific user
- Automatic rounding to two decimal places

## 🧪 Sample Users

| ID  | Name   | Email           | Mobile      |
|-----|--------|------------------|-------------|
| u1  | User1  | u1@email.com     | 1234567890  |
| u2  | User2  | u2@email.com     | 1234567891  |
| u3  | User3  | u3@email.com     | 1234567892  |
| u4  | User4  | u4@email.com     | 1234567893  |

## 🚀 Getting Started

1. Clone the repository or copy the `main()` code to a Python file (e.g., `splitwise.py`).
2. Run it:
   ```bash
   python splitwise.py
   ```
3. Use commands like below to interact.

## 📌 Supported Commands

### 1. Add Expense
```
EXPENSE <paid_by> <amount> <num_users> <user_id_1> <user_id_2> ... <SPLIT_TYPE> [split_values...]
```

#### EQUAL Example
```
EXPENSE u1 1000 4 u1 u2 u3 u4 EQUAL
```

#### EXACT Example
```
EXPENSE u1 1250 2 u2 u3 EXACT 370 880
```

#### PERCENT Example
```
EXPENSE u4 1200 4 u1 u2 u3 u4 PERCENT 40 20 20 20
```

### 2. Show All Balances
```
SHOW
```

### 3. Show User Balances
```
SHOW <user_id>
```

### 4. Exit
```
END
```

## ✅ Example Session
```
SHOW
EXPENSE u1 1000 4 u1 u2 u3 u4 EQUAL
SHOW u1
EXPENSE u1 1250 2 u2 u3 EXACT 370 880
SHOW
EXPENSE u4 1200 4 u1 u2 u3 u4 PERCENT 40 20 20 20
SHOW u1
SHOW
END
```

## 🧱 Code Structure
- `User`: Represents a user
- `BalanceSheet`: Manages internal balances
- `ExpenseManager`: Orchestrates expenses and prints
- `main()`: CLI entry point for the program

## 📌 Optional Extensions
- Add passbook (transaction history)
- Allow SHARE splits (e.g., 2 people for one user)
- Simplify debts
- Store data in a database (e.g., SQLite)
- Support batch input via file

---

Built with ❤️ for fun and learning. Enjoy sharing expenses the hacker way!
