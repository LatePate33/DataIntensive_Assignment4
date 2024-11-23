import psycopg2
from pymongo import MongoClient

def connect_postgresql():
    try:
        conn = psycopg2.connect(
            database="Assignment4",
            user="postgres",
            password="P0stL4teSq!",
            host="localhost",
            port="5432"
        )
        print("Connected to PostgreSQL")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def connect_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        print("Connected to MongoDB")
        return client.Assignment4  # Updated to use the 'Assignment4' database
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# PostgreSQL: Read, Insert, Update, Delete
def pg_insert_product(conn, name, delivery_price, description):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Product (Name, DeliveryPrice, Description) VALUES (%s, %s, %s)",
            (name, delivery_price, description)
        )
        conn.commit()
        print("Data inserted into PostgreSQL")
    except Exception as e:
        print(f"Error inserting into PostgreSQL: {e}")

def pg_read_products(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product")
        rows = cursor.fetchall()
        print("PostgreSQL Data:")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error reading from PostgreSQL: {e}")

def pg_update_product(conn, product_id, name, delivery_price, description):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Product SET Name = %s, DeliveryPrice = %s, Description = %s WHERE Id = %s",
            (name, delivery_price, description, product_id)
        )
        conn.commit()
        print("Data updated in PostgreSQL")
    except Exception as e:
        print(f"Error updating PostgreSQL: {e}")

def pg_delete_product(conn, product_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Product WHERE Id = %s", (product_id,))
        conn.commit()
        print("Data deleted from PostgreSQL")
    except Exception as e:
        print(f"Error deleting from PostgreSQL: {e}")

# MongoDB: Read, Insert, Update, Delete
def mongo_insert_product(db, key, title, price, information):
    try:
        db.Product.insert_one({
            "Key": key,
            "Title": title,
            "Price": price,
            "Information": information
        })
        print("Data inserted into MongoDB")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")

def mongo_read_products(db):
    try:
        products = db.Product.find()
        print("MongoDB Data:")
        for product in products:
            print(product)
    except Exception as e:
        print(f"Error reading from MongoDB: {e}")

def mongo_update_product(db, key, title, price, information):
    try:
        db.Product.update_one(
            {"Key": key},
            {"$set": {"Title": title, "Price": price, "Information": information}}
        )
        print("Data updated in MongoDB")
    except Exception as e:
        print(f"Error updating MongoDB: {e}")

def mongo_delete_product(db, key):
    try:
        db.Product.delete_one({"Key": key})
        print("Data deleted from MongoDB")
    except Exception as e:
        print(f"Error deleting from MongoDB: {e}")

def compare_data(pg_conn, mongo_db):
    try:
        if pg_conn is None:
            print("PostgreSQL connection is not available.")
            return
        if mongo_db is None:
            print("MongoDB connection is not available.")
            return

        # Fetch data from PostgreSQL
        cursor = pg_conn.cursor()
        cursor.execute("SELECT Id, Name, DeliveryPrice, Description FROM Product")
        pg_data = cursor.fetchall()

        # Fetch data from MongoDB
        mongo_data = list(mongo_db.Product.find())

        print("\nComparing data between PostgreSQL and MongoDB...\n")
        for pg_row in pg_data:
            pg_key = str(pg_row[0])  # PostgreSQL key (Id) as string
            matching_mongo_doc = next(
                (doc for doc in mongo_data if doc.get("Key") == pg_key), None
            )
            if matching_mongo_doc:
                # Display matching data
                print(f"PostgreSQL: {pg_row}")
                print(f"MongoDB: {matching_mongo_doc}")
                print("-" * 50)
            else:
                print(f"No matching data in MongoDB for PostgreSQL Key: {pg_key}")
                print("-" * 50)
    except Exception as e:
        print(f"Error comparing data: {e}")

def main():
    pg_conn = connect_postgresql()
    mongo_db = connect_mongodb()

    while True:
        print("\nOptions:")
        print("1. View PostgreSQL Products")
        print("2. View MongoDB Products")
        print("3. Add Product to PostgreSQL")
        print("4. Add Product to MongoDB")
        print("5. Update Product in PostgreSQL")
        print("6. Update Product in MongoDB")
        print("7. Delete Product from PostgreSQL")
        print("8. Delete Product from MongoDB")
        print("9. Compare Data")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            if pg_conn:
                pg_read_products(pg_conn)
        elif choice == "2":
            if mongo_db is not None:
                mongo_read_products(mongo_db)
        elif choice == "3":
            name = input("Enter Name: ")
            price = float(input("Enter Delivery Price: "))
            description = input("Enter Description: ")
            if pg_conn:
                pg_insert_product(pg_conn, name, price, description)
        elif choice == "4":
            key = input("Enter Key: ")
            title = input("Enter Title: ")
            price = float(input("Enter Price: "))
            info = input("Enter Information: ")
            if mongo_db is not None:
                mongo_insert_product(mongo_db, key, title, price, info)
        elif choice == "5":
            product_id = int(input("Enter Product ID to Update: "))
            name = input("Enter Name: ")
            price = float(input("Enter Delivery Price: "))
            description = input("Enter Description: ")
            if pg_conn:
                pg_update_product(pg_conn, product_id, name, price, description)
        elif choice == "6":
            key = input("Enter Key to Update: ")
            title = input("Enter Title: ")
            price = float(input("Enter Price: "))
            info = input("Enter Information: ")
            if mongo_db is not None:
                mongo_update_product(mongo_db, key, title, price, info)
        elif choice == "7":
            product_id = int(input("Enter Product ID to Delete: "))
            if pg_conn:
                pg_delete_product(pg_conn, product_id)
        elif choice == "8":
            key = input("Enter Key to Delete: ")
            if mongo_db is not None:
                mongo_delete_product(mongo_db, key)
        elif choice == "9":
            if pg_conn and mongo_db is not None:
                compare_data(pg_conn, mongo_db)
            else:
                print("Both databases must be connected to compare data.")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

    if pg_conn:
        pg_conn.close()
    print("Goodbye!")

main()
