from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

class User:
    def __init__(self, user_id, name, email, mobile):
        self.id = user_id
        self.name = name
        self.email = email
        self.mobile = mobile

class BalanceSheet:
    def __init__(self):
        # balances[from_user][to_user] = amount
        self.balances = defaultdict(lambda: defaultdict(float))

    def add_transaction(self, paid_by, splits):
        for user, amount in splits.items():
            if user == paid_by:
                continue
            self.balances[user][paid_by] += amount

    def show_all_balances(self):
        found = False
        for user_from in self.balances:
            for user_to in self.balances[user_from]:
                amount = self.balances[user_from][user_to] - self.balances[user_to][user_from]
                if amount > 0.01:
                    found = True
                    print(f"{user_from} owes {user_to}: {round(amount, 2)}")
        if not found:
            print("No balances")

    def show_user_balance(self, user_id):
        found = False
        for user in self.balances:
            amount = self.balances[user][user_id] - self.balances[user_id][user]
            if user != user_id and amount > 0.01:
                found = True
                if amount > 0:
                    print(f"{user} owes {user_id}: {round(amount, 2)}")
                else:
                    print(f"{user_id} owes {user}: {round(-amount, 2)}")
        if not found:
            print("No balances")

class ExpenseManager:
    def __init__(self):
        self.users = {}
        self.sheet = BalanceSheet()

    def add_user(self, user_id, name, email, mobile):
        self.users[user_id] = User(user_id, name, email, mobile)

    def process_expense(self, tokens):
        paid_by = tokens[1]
        amount = float(tokens[2])
        count = int(tokens[3])
        users = tokens[4:4+count]
        split_type = tokens[4+count]
        split_data = tokens[5+count:]

        split_amounts = {}
        if split_type == "EQUAL":
            equal_amount = round(amount / count, 2)
            remaining = round(amount - equal_amount * (count - 1), 2)
            for i, user in enumerate(users):
                split_amounts[user] = remaining if i == 0 else equal_amount

        elif split_type == "EXACT":
            exacts = list(map(float, split_data))
            if round(sum(exacts), 2) != round(amount, 2):
                print("Invalid EXACT split")
                return
            split_amounts = dict(zip(users, exacts))

        elif split_type == "PERCENT":
            percents = list(map(float, split_data))
            if round(sum(percents), 2) != 100.0:
                print("Invalid PERCENT split")
                return
            for i in range(count):
                split_amounts[users[i]] = round(amount * percents[i] / 100, 2)

        else:
            print("Invalid split type")
            return

        self.sheet.add_transaction(paid_by, split_amounts)

    def show_balances(self):
        self.sheet.show_all_balances()

    def show_user_balance(self, user_id):
        self.sheet.show_user_balance(user_id)

def main():
    manager = ExpenseManager()

    # Predefine users
    manager.add_user("u1", "User1", "u1@email.com", "1234567890")
    manager.add_user("u2", "User2", "u2@email.com", "1234567891")
    manager.add_user("u3", "User3", "u3@email.com", "1234567892")
    manager.add_user("u4", "User4", "u4@email.com", "1234567893")

    print("Enter commands (type END to stop):")
    while True:
        try:
            line = input().strip()
            if line == "END":
                break
            elif line.startswith("SHOW"):
                tokens = line.split()
                if len(tokens) == 1:
                    manager.show_balances()
                elif len(tokens) == 2:
                    manager.show_user_balance(tokens[1])
            elif line.startswith("EXPENSE"):
                manager.process_expense(line.split())
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
