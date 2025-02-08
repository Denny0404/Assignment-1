from user import Database, UserService

def main():
    db = Database('users.db')
    user_service = UserService(db)
    
    while True:
        action = input("Choose action: 'get', 'create', 'update', 'delete' (or 'exit' to quit): ").strip().lower()
        if action == 'exit':
            break

        elif action == 'get':
            user_id = int(input("Enter user ID: "))
            user_data, status_code = user_service.get_user(user_id)
            print(f"Response: {user_data} (Status Code: {status_code})")
            
        elif action == 'create':
            name = input("Enter user name: ")
            age = int(input("Enter user age: "))
            user_data, status_code = user_service.create_user(name, age)
            print(f"Response: {user_data} (Status Code: {status_code})")

        elif action == 'update':
            user_id = int(input("Enter user ID to update: "))
            name = input("Enter new name: ")
            age = int(input("Enter new age: "))
            user_data, status_code = user_service.update_user(user_id, name, age)
            print(f"Response: {user_data} (Status Code: {status_code})")

        elif action == 'delete':
            user_id = int(input("Enter user ID to delete: "))
            user_data, status_code = user_service.delete_user(user_id)
            print(f"Response: {user_data} (Status Code: {status_code})")

        else:
            print("Invalid action. Please type 'get', 'create', 'update', or 'delete'.")

if __name__ == '__main__':
    main()
