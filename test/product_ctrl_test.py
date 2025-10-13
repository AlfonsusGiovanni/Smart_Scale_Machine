# Product Control Algorithm Testing

from lib import product_control as pctl

def main():
    pctl.Myproduct.load_products()
    while True:
        print("=== Product Control Menu ===")
        print("1. View products")
        print("2. Add product")
        print("3. Delete product")
        print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            print(" ")
            print("\n=== Product List ===")
            for i, p in enumerate(pctl.Myproduct.product_list, start=1):
                print(f"{i}. {p['name']} | Price: Rp{p['price']:.2f}")
            print("====================\n")
            print(" ")

        elif choice == "2":
            try:
                name = input("Enter product name: ").strip()
                price = float(input("Enter price: "))

            except ValueError:
                print("⚠️ Invalid input. Please enter numeric values for price and stock.\n")
                return
            
            pctl.Myproduct.add_product(name, price)

        elif choice == "3":
            target = input("Enter product number or name to delete: ").strip()
            pctl.Myproduct.delete_product(product_num=target)

        elif choice == "4":
            print("💾 Exiting... Goodbye!")
            break

        else:
            print("⚠️ Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()