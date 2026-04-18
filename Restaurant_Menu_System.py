import sqlite3

# Connect DB
conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
""")

conn.commit()

# ---------------- FUNCTIONS ---------------- #

def add_category():
    name = input("Enter category name: ")
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        print("Category added.")
    except:
        print("Category already exists.")

def view_categories():
    cursor.execute("SELECT * FROM categories")
    for row in cursor.fetchall():
        print(row)

def add_item():
    name = input("Enter item name: ")
    price = float(input("Enter price: "))
    
    view_categories()
    category_id = int(input("Enter category ID: "))
    
    cursor.execute(
        "INSERT INTO menu_items (name, price, category_id) VALUES (?, ?, ?)",
        (name, price, category_id)
    )
    conn.commit()
    print("Item added.")

def view_items():
    cursor.execute("""
    SELECT menu_items.id, menu_items.name, menu_items.price, categories.name
    FROM menu_items
    JOIN categories ON menu_items.category_id = categories.id
    """)
    
    rows = cursor.fetchall()
    print("\n--- MENU ---")
    for r in rows:
        print(f"ID:{r[0]} | {r[1]} | ₹{r[2]} | {r[3]}")

def update_item():
    view_items()
    item_id = int(input("Enter item ID to update: "))
    new_price = float(input("Enter new price: "))
    
    cursor.execute(
        "UPDATE menu_items SET price=? WHERE id=?",
        (new_price, item_id)
    )
    conn.commit()
    print("Updated successfully.")

def delete_item():
    view_items()
    item_id = int(input("Enter item ID to delete: "))
    
    cursor.execute("DELETE FROM menu_items WHERE id=?", (item_id,))
    conn.commit()
    print("Deleted successfully.")

def delete_category():
    view_categories()
    cat_id = int(input("Enter category ID to delete: "))

    # Check if category has items
    cursor.execute("SELECT COUNT(*) FROM menu_items WHERE category_id=?", (cat_id,))
    count = cursor.fetchone()[0]

    if count > 0:
        print("⚠️ This category has menu items.")
        confirm = input("Delete all items under this category? (y/n): ")

        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM menu_items WHERE category_id=?", (cat_id,))
        else:
            print("Delete cancelled.")
            return

    cursor.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    conn.commit()
    print("Category deleted successfully.")

# ---------------- CLI ---------------- #

def menu():
    while True:
        print("\n--- RESTAURANT MENU SYSTEM ---")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Add Menu Item")
        print("4. View Menu")
        print("5. Update Item Price")
        print("6. Delete Item")
        print("7. Delete Category")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_category()
        elif choice == "2":
            view_categories()
        elif choice == "3":
            add_item()
        elif choice == "4":
            view_items()
        elif choice == "5":
            update_item()
        elif choice == "6":
            delete_item()
        elif choice == "7":
            delete_category()
        elif choice == "8":
            break
        else:
            print("Invalid choice.")

menu()

conn.close()