import json

# Function to get email and token from user and save to accounts.json
def save_accounts():
    # Ask how many accounts the user wants to save
    num_accounts = int(input("How many accounts do you want to save? "))

    # Create an empty list to store the account data
    accounts = []

    # Loop to gather each account's details
    for i in range(num_accounts):
        print(f"\nAccount {i + 1}:")
        email = input("Enter your Email: ")
        token = input("Enter your Token: ")

        # Add the account data to the list
        accounts.append({
            "Email": email,
            "Token": token
        })

    # Save the data to accounts.json
    try:
        with open("accounts.json", "w") as file:
            json.dump(accounts, file, indent=4)
        print(f"\n{num_accounts} account(s) saved successfully!")
    except Exception as e:
        print(f"An error occurred while saving: {e}")

# Run the function to save the accounts
save_accounts()
