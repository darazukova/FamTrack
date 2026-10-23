from database import init_db, get_users, get_expenses, get_totals_by_category

init_db()

print("Пользователи:")
for row in get_users():
    print(" ", row)

print("\nИстория расходов:")
for row in get_expenses():
    print(" ", row)

print("\nРасходы по категориям:")
for name, total in get_totals_by_category():
    print(f"  {name}: {total:.2f}")
