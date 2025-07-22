import csv
import random

stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 2750,
    "MSFT": 330,
    "AMZN": 3500
}

portfolio = {}

def simulate_live_prices():
    for stock in stock_prices:
        # Randomly fluctuate price by ±5%
        change_percent = random.uniform(-0.05, 0.05)
        stock_prices[stock] = round(stock_prices[stock] * (1 + change_percent), 2)

def display_portfolio(sorted_by=None, filter_type=None):
    simulate_live_prices()  # Simulate live price before display
    print("\n📊 Portfolio Summary:")
    data_list = []

    total_investment = 0
    total_gain_loss = 0

    for stock, data in portfolio.items():
        current_price = stock_prices[stock]
        quantity = data["quantity"]
        buy_price = data["buy_price"]
        current_value = current_price * quantity
        gain_loss = (current_price - buy_price) * quantity
        total_investment += current_value
        total_gain_loss += gain_loss
        data_list.append((stock, quantity, buy_price, current_price, current_value, gain_loss))

    # Apply Sorting
    if sorted_by == "name":
        data_list.sort()
    elif sorted_by == "value":
        data_list.sort(key=lambda x: x[4], reverse=True)
    elif sorted_by == "gain":
        data_list.sort(key=lambda x: x[5], reverse=True)

    # Display with optional filter
    for stock, quantity, buy_price, current_price, value, gain_loss in data_list:
        if filter_type == "gain" and gain_loss <= 0:
            continue
        if filter_type == "loss" and gain_loss >= 0:
            continue
        print(f"{stock}: {quantity} shares | Buy @ ${buy_price} | Now @ ${current_price} | Value: ${value:.2f} | Gain/Loss: ${gain_loss:.2f}")

    overall_percent = (total_gain_loss / total_investment * 100) if total_investment else 0
    print(f"\n💰 Total Portfolio Value: ${total_investment:.2f} | Total Gain/Loss: ${total_gain_loss:.2f} ({overall_percent:.2f}%)")

def save_to_csv():
    with open("portfolio_summary.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Stock", "Quantity", "Buy Price", "Current Price", "Value", "Gain/Loss"])
        for stock, data in portfolio.items():
            current_price = stock_prices[stock]
            quantity = data["quantity"]
            buy_price = data["buy_price"]
            value = current_price * quantity
            gain_loss = (current_price - buy_price) * quantity
            writer.writerow([stock, quantity, buy_price, current_price, value, gain_loss])
    print("✅ Portfolio summary saved to 'portfolio_summary.csv'")

def save_session_history():
    with open("portfolio_log.txt", "a") as file:
        file.write("New Session:\n")
        for stock, data in portfolio.items():
            current_price = stock_prices[stock]
            quantity = data["quantity"]
            buy_price = data["buy_price"]
            value = current_price * quantity
            gain_loss = (current_price - buy_price) * quantity
            file.write(f"{stock}: {quantity} shares, Buy @ {buy_price}, Now @ {current_price}, Value: {value}, Gain/Loss: {gain_loss}\n")
        file.write("\n")
    print("✅ Session history saved to 'portfolio_log.txt'")

def update_or_remove_stock():
    choice = input("Do you want to (u)pdate or (r)emove a stock? ").lower()
    stock = input("Enter stock symbol: ").upper()
    if stock not in portfolio:
        print("❌ Stock not in portfolio.")
        return
    if choice == 'u':
        try:
            new_quantity = int(input("Enter new quantity: "))
            new_buy_price = float(input("Enter new buy price: "))
            portfolio[stock] = {"quantity": new_quantity, "buy_price": new_buy_price}
            print("✅ Stock updated.")
        except ValueError:
            print("❗ Invalid input.")
    elif choice == 'r':
        del portfolio[stock]
        print("✅ Stock removed.")
    else:
        print("❗ Invalid choice.")

def main():
    print("📈 Welcome to Supercharged Stock Portfolio Tracker")
    print("Available Stocks:", ", ".join(stock_prices.keys()))

    while True:
        stock = input("Enter stock symbol (or 'done' to finish): ").upper()
        if stock == 'DONE':
            break
        if stock not in stock_prices:
            print("❗ Stock not found.")
            continue
        try:
            quantity = int(input(f"Enter quantity for {stock}: "))
            buy_price = float(input(f"Enter your buying price for {stock}: "))
            portfolio[stock] = {"quantity": quantity, "buy_price": buy_price}
        except ValueError:
            print("❗ Invalid number. Try again.")

    while True:
        print("\n🔧 Options: [v]iew [s]ave [u]pdate/remove [f]ilter [q]uit")
        action = input("Choose an option: ").lower()

        if action == 'v':
            sort_choice = input("Sort by (name/value/gain/none): ").lower()
            filter_choice = input("Filter by (gain/loss/none): ").lower()
            display_portfolio(
                sorted_by=sort_choice if sort_choice in ["name", "value", "gain"] else None,
                filter_type=filter_choice if filter_choice in ["gain", "loss"] else None
            )
        elif action == 's':
            save_to_csv()
            save_session_history()
        elif action == 'u':
            update_or_remove_stock()
        elif action == 'f':
            search = input("Enter stock symbol to search: ").upper()
            if search in stock_prices:
                print(f"{search} is currently priced at ${stock_prices[search]}")
            else:
                print("❌ Stock not found.")
        elif action == 'q':
            print("👋 Exiting. Thanks for using the tracker.")
            break
        else:
            print("❗ Invalid option.")

if __name__ == "__main__":
    main()
