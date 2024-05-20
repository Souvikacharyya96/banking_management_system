import mysql.connector
import random

# Connect to MySQL
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Souvik@1996",
    auth_plugin="mysql_native_password"
)
cur_obj = conn_obj.cursor()

# Create a new database
try:
    cur_obj.execute("CREATE DATABASE IF NOT EXISTS bank_database")
    conn_obj.commit()
except mysql.connector.Error as err:
    print(f"Error1: {err}")
    conn_obj.rollback()

# Use the created database
try:
    cur_obj.execute("USE bank_database")
except mysql.connector.Error as err:
    print(f"Error2: {err}")
    conn_obj.rollback()

# Create a users table
cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id VARCHAR(50) PRIMARY KEY,
        full_name VARCHAR(50) NOT NULL,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        email_id VARCHAR(50) NOT NULL
    )
''')

# Create a user's personal details table
cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS personal_details (
        user_id VARCHAR(50) PRIMARY KEY NOT NULL,
        type_of_account VARCHAR(50) NOT NULL,
        account_no VARCHAR(50) NOT NULL,
        full_name VARCHAR(50) NOT NULL,
        email_id VARCHAR(50) NOT NULL,
        ph_number VARCHAR(50) NOT NULL,
        date_of_birth DATE NOT NULL,
        address VARCHAR(150) NOT NULL
    )
''')

# Create a user's professional details table
cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS professional_details (
        user_id VARCHAR(50) PRIMARY KEY NOT NULL,
        occupation VARCHAR(50) NOT NULL,
        job_sector VARCHAR(50) NOT NULL,
        income VARCHAR(50) NOT NULL
    )
''')

cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS account_details (
        user_id VARCHAR(50) PRIMARY KEY NOT NULL,
        account_no VARCHAR(50) NOT NULL,
        full_name VARCHAR(50) NOT NULL,
        balance DECIMAL(10,2) DEFAULT 0.0
    )
''')

cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS deposit_money (
        user_id VARCHAR(50) PRIMARY KEY NOT NULL,
        account_no VARCHAR(50) NOT NULL,
        full_name VARCHAR(50) NOT NULL,
        amount DECIMAL(10,2),
        date_of_deposit DATE NOT NULL 
    )
''')

cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS withdrawl_money (
        user_id VARCHAR(50) PRIMARY KEY NOT NULL,
        account_no VARCHAR(50) NOT NULL,
        full_name VARCHAR(50) NOT NULL,
        amount DECIMAL(10,2),
        date_of_withdrawl DATE NOT NULL 
    )
''')

# Create a transactions table
cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        sender_id VARCHAR(50) NOT NULL,
        receiver_id VARCHAR(50) NOT NULL,
        amount DECIMAL(10, 2),
        date_of_transaction DATE NOT NULL,
        FOREIGN KEY (sender_id) REFERENCES account_details(user_id),
        FOREIGN KEY (receiver_id) REFERENCES account_details(user_id)
    )
''')

def generate_user_id():
    return "".join(random.choices("0123", k = 4))

def generate_account_number():
    return "".join(random.choices("0123456789", k = 10))

# Function to store user's personal details
def personal_details(user_id, type_of_account, account_no, full_name, email_id, ph_number, date_of_birth, address):
    try:
        cur_obj.execute(
            "INSERT INTO personal_details (user_id, type_of_account, account_no, full_name, email_id, ph_number, date_of_birth, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (user_id, type_of_account, account_no, full_name, email_id, ph_number, date_of_birth, address))
        conn_obj.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

# Function to store user's professional details
def proffessional_details(user_id, occupation, job_sector, income):
    try:
        cur_obj.execute(
            "INSERT INTO professional_details (user_id, occupation, job_sector, income) VALUES (%s, %s, %s, %s)",
            (user_id, occupation, job_sector, income))
        conn_obj.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

# Function to see user's all details after inner joining personal details & professionalo details
def retrieve_user_details(user_id):
    try:
        cur_obj.execute("""
        SELECT * 
        FROM personal_details
        INNER JOIN professional_details
        ON personal_details.user_id = professional_details.user_id
        WHERE personal_details.user_id = %s
        """, (user_id,))
        result = cur_obj.fetchall()
        if result:
            print("USER ID: ", result[0][0])
            print("TYPE OF ACCOUNT: ", result[0][1])
            print("ACCOUNT NUMBER: ", result[0][2])
            print("FULL NAME: ", result[0][3])
            print("EMAIL ID: ", result[0][4])
            print("PHONE NUMBER: ", result[0][5])
            print("DATE OF BIRTH: ", result[0][6])
            print("ADDRESS.: ", result[0][7])
            print("OCCUPATION: ", result[0][9])
            print("JOB SECTOR: ", result[0][10])
            print("INCOME: ", result[0][11])
        else:
            print("USER NOT FOUND")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

#Define function update_data()
def update_data(user_id,ph_number):

    try:
        cur_obj.execute(f"UPDATE personal_details SET ph_number = %s WHERE user_id = %s", (ph_number, user_id))
        print("DETAILS HAVE BEEN UPDATED.")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

    try:
        cur_obj.execute(f"select * from personal_details WHERE user_id = %s", (user_id,))
        result1 = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

    # Print or process the retrieved data using list unpacking
    if result1:
        user_id, type_of_account, account_no, full_name, email_id, ph_number, date_of_birth, address = result1  # Unpacking the row into variables
        # Print data in proper sequence using f-strings
        print(f"DATA FOR USER: '{full_name}'")
        print("----------------------------------")
        print(f"USER ID: {user_id}")
        print(f"ACCOUNT TYPE: {type_of_account}")
        print(f"ACCOUNT NUMBER: {account_no}")
        print(f"STUDENT NAME: {full_name}")
        print(f"EMAIL ID: {email_id}")
        print(f"PHONE NUMBER: {ph_number}")
        print(f"DATE OF BIRTH: {date_of_birth}")
        print(f"ADDRESS: {address}")
    else:
        print("NO USER FOUND WITH THE PROVIDED NAME.")

# Creating a function for User's account details
def account_details(user_id, full_name, account_no, balance):
    try:
        cur_obj.execute(
            "INSERT INTO account_details (user_id, full_name, account_no, balance) VALUES (%s, %s, %s, %s)",
            (user_id, full_name, account_no, balance))
        conn_obj.commit()
        print("ACCOUNT DETAILS UPLOADED SUCCESSFULY.")
    except mysql.connector.Error as err:
        print(f"Error creating account details: {err}")
        conn_obj.rollback()

# Creating a function to deposit money
def deposit_money(user_id, account_no, full_name, amount, date_of_deposit):
    try:
        # Check user's balance
        cur_obj.execute("SELECT balance FROM account_details WHERE user_id = %s", (user_id,))
        user_balance = cur_obj.fetchone()[0]

        if user_balance >= 0:
            cur_obj.execute("UPDATE account_details SET balance = balance + %s WHERE user_id = %s", (amount, user_id))

            cur_obj.execute(
                "INSERT INTO deposit_money (user_id, account_no, full_name, amount, date_of_deposit) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount = amount + %s",
                (user_id, account_no, full_name, amount, date_of_deposit, amount))
            conn_obj.commit()
            print("DEPOSIT SUCCESSFUL")
            print(f"AVAILABLE BALANCE: {user_balance + Decimal(str(amount))}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

# Creating a function to withdraw money
def withdrawl_money(user_id, account_no, full_name, amount, date_of_withdrawl):
    try:
        # Check user's balance
        cur_obj.execute("SELECT balance FROM account_details WHERE user_id = %s", (user_id,))
        user_balance = cur_obj.fetchone()[0]

        if user_balance >= amount:
            cur_obj.execute("UPDATE account_details SET balance = balance - %s WHERE user_id = %s", (amount, user_id))

            cur_obj.execute(
                "INSERT INTO withdrawl_money (user_id, account_no, full_name, amount, date_of_withdrawl) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount = amount + %s",
                (user_id, account_no, full_name, amount, date_of_withdrawl, amount))
            conn_obj.commit()
            print("WITHDRAWAL SUCCESSFUL")
            print(f"AVAILABLE BALANCE: {user_balance - Decimal(str(amount))}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()


# Creating a function to transfer money
def transfer_money(sender_id, receiver_id, amount, date_of_transaction):
    try:
        # Check sender's balance
        cur_obj.execute("SELECT balance FROM account_details WHERE user_id = %s", (sender_id,))
        sender_balance = cur_obj.fetchone()[0]

        # If sender has sufficient balance, proceed with the transfer
        if sender_balance >= amount:
            # Update sender's balance
            cur_obj.execute("UPDATE account_details SET balance = balance - %s WHERE user_id = %s", (amount, sender_id))

            # Update receiver's balance
            cur_obj.execute("UPDATE account_details SET balance = balance + %s WHERE user_id = %s", (amount, receiver_id))

            # Insert a new transaction record
            cur_obj.execute("INSERT INTO transactions (sender_id, receiver_id, amount, date_of_transaction) VALUES (%s, %s, %s, %s)",
                            (sender_id, receiver_id, amount, date_of_transaction))

            conn_obj.commit()
            print("TRANSFERED SUCCESSFUL")
        else:
            print("INSUFFICIENT FUNDS")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

# Creating a function to check User's account balance
def check_balance(user_id,account_no):
    try:
        cur_obj.execute("SELECT * FROM account_details WHERE user_id = %s AND account_no = %s", (user_id, account_no,))
        user = cur_obj.fetchall()
        if user:
            print("YOUR ACCOUNT BALANCE: ", user[0][3])
        else:
            print("YOU HAVE ENTERED WRONG USER ID & ACCOUNT NO")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

# Creating a function to see User's transaction history
def transaction_history(user_id):
    try:
        cur_obj.execute("SELECT * FROM transactions WHERE sender_id = %s", (user_id,))
        user = cur_obj.fetchall()
        if user:
            print("|", "SENDER".center(15), "|".center(15), "RECIEVER".center(15), "|".center(15), "AMOUNT".center(15),
                  "|".center(15), "DATE OF TRANSACTION".center(15), "|".center(15))
            print(" ".center(5), user[0][1], " ".center(24), user[0][2], " ".center(21), user[0][3], " ".center(20),
                  user[0][4])
        else:
            print(" ")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

def deposit_withdrawl_history(user_id):
    try:
        cur_obj.execute("SELECT * FROM deposit_money WHERE user_id = %s", (user_id,))
        user = cur_obj.fetchall()
        if user:
            print("|", "USER ID".center(15), "|".center(15), "ACCOUNT NUMBER".center(15), "|".center(15), "FULL NAME".center(15),
                  "|".center(15), "DATE OF DEPOSIT".center(15), "|".center(15) ,"AMOUNT".center(15), "|".center(15))
            print(" ".center(5), user[0][0], " ".center(20), user[0][1], " ".center(19), user[0][2], " ".center(18),
                  user[0][4], " ".center(18), user[0][3])
        else:
            print("YOU HAVE ENTERED WRONG USER ID")

        cur_obj.execute("SELECT * FROM withdrawl_money WHERE user_id = %s", (user_id,))
        user = cur_obj.fetchall()
        if user:
            print("|", "USER ID".center(15), "|".center(15), "ACCOUNT NUMBER".center(15), "|".center(15),
                  "FULL NAME".center(15),
                  "|".center(15), "DATE OF WITHDRAWL".center(15), "|".center(15), "AMOUNT".center(13), "|".center(15))
            print(" ".center(5), user[0][0], " ".center(20), user[0][1], " ".center(19), user[0][2], " ".center(18),
                  user[0][4], " ".center(18), user[0][3])
        else:
            print("YOU HAVE ENTERED WRONG USER ID")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

# Function to register a new user
def register_user(user_id, full_name, username, password, email_id):
    try:
        cur_obj.execute("INSERT INTO users (user_id, full_name, username, password, email_id) VALUES (%s, %s, %s, %s, %s)", (user_id, full_name, username, password, email_id))
        conn_obj.commit()
        print("USER REGISTERED SUCCESSFULY.")
        # Retrieve the user_id of the newly inserted user
        cur_obj.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        result = cur_obj.fetchone()

        if result:
            user_id = result[0]
            print(f"YOUR REGISTERED USER ID: UIC{user_id}")
            print("\nNOW UPLOAD YOUR PERSONAL DETAILS AND PROFESSIONAL DETAILS WITH YOUR REGISTERED USER NAME & PASSWORD(USE THE ABOVE MENTIONED USER ID TO UPLOAD YOUR DETAILS).")
            # User Details Upload Menu
            while True:
                print("\nCHOOSE THE RIGHT OPTION BETWEEN (1 TO 4): ")
                print("1. CREATE YOUR BANK ACCOUNT")
                print("2. CHECK YOUR DETAILS")
                print("3. UPDATE YOUR DETAILS(ONLY PHONE NUMBER)")
                print("4. LOGOUT")

                option = input("\nPLEASE SELECT RIGHT OPTION IN BETWEEN (1/2/3/4): ")

                if option == "1":
                    print("\nENTER YOUR BASIC DETAILS:- ")
                    print("\n1. SAVING ACCOUNT")
                    print("2. SALARY ACCOUNT")
                    option = input("\nPLEASE SELECT RIGHT OPTION IN BETWEEN 1 OR 2 TO UPLOAD YOUR DETAILS: ")

                    if option == "1":
                        user_id = input("\nENTER YOUR USER ID: ")
                        try:
                            cur_obj.execute("SELECT * FROM personal_details WHERE user_id = %s", (user_id,))
                            result1 = cur_obj.fetchall()

                            if result1:
                                print("THIS USER ID IS USED BEFORE")
                                break
                            else:
                                print(" ")

                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if user_id.startswith("UIC"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        type_of_account = "SAVING ACCOUNT"

                        account_no = generate_account_number()

                        full_name = input("ENTER FULL NAME: ")
                        try:
                            cur_obj.execute("SELECT * FROM personal_details WHERE full_name = %s", (full_name,))
                            result = cur_obj.fetchall()

                            if result:
                                print("THIS NAME IS USED BEFORE")
                                break
                            else:
                                print(" ")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if type(full_name) == str and full_name.isupper():
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        email_id = input("ENTER YOUR EMAIL ID: ")
                        try:
                            cur_obj.execute("SELECT * FROM personal_details WHERE email_id = %s", (email_id,))
                            result = cur_obj.fetchall()

                            if result:
                                print("THIS EMAIL ID IS USED BEFORE")
                                break
                            else:
                                print(" ")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if email_id.find("@") != -1 and email_id.endswith(".com"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break
                        ph_number = input("ENTER YOUR PHONE NUMBER: ")
                        try:
                            cur_obj.execute("SELECT * FROM personal_details WHERE ph_number = %s", (ph_number,))
                            result = cur_obj.fetchall()

                            if result:
                                print("THIS PHONE NUMBER IS USED BEFORE")
                                break
                            else:
                                print(" ")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if len(ph_number) == 10 and ph_number[0] == "6" or ph_number[0] == "7" or ph_number[0] == "8" or \
                                ph_number[0] == "9":
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        date_of_birth = input("ENTER YOUR DATE OF BIRTH(FORMAT - YYYY-MM-DD): ")

                        address = input("\nENTER YOUR PERMANENT ADDRESS(WITHIN 150 WORDS & ALL IN CAPITAL LETTER): ")
                        if len(address) < 151 and address.isupper() == True:
                            print(" ")
                        else:
                            print("ADDRESS IS NOT OK")
                            break

                        print("USER'S PERSONAL DETAILS UPLOADED SUCCESFULLY....")
                        personal_details(user_id, type_of_account, account_no, full_name, email_id, ph_number,
                                         date_of_birth, address)

                        print("\nNOW, PLEASE UPLOAD YOUR PROFESSIONAL DETAILS:")
                        user_id = input("\nENTER YOUR USER ID: ")
                        try:
                            cur_obj.execute("SELECT * FROM professional_details WHERE user_id = %s", (user_id,))
                            result1 = cur_obj.fetchall()

                            if result1:
                                print("THIS USER ID IS USED BEFORE")
                                break
                            else:
                                print(" ")

                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if user_id.startswith("UIC"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break
                        occupation = input("ENTER YOUR OCCUPATION: ")
                        job_sector = input("\n\nENTER YOUR JOB SECTOR(PRIVATE/GOVT./NA): ")
                        if job_sector == "PRIVATE" or "GOVT." or "NA":
                            print(" ")
                        else:
                            print("NOT OK")
                        income = input("\nENTER INCOME (YEARLY): ")
                        print("\nUSER'S PROFESSIONAL DETAILS UPLOADED SUCCESFULLY....")
                        print(f"\nYOUR ACCOUNT NUMBER: {account_no}")
                        print("NOW, GO TO YOUR LOGIN PAGE TO DEPOSIT MONEY/WITHDRAWL MONEY/TRANSFER MONEY")
                        proffessional_details(user_id, occupation, job_sector, income)

                    elif option == "2":
                        user_id = input("\nENTER YOUR USER ID: ")
                        try:
                            cur_obj.execute("SELECT * FROM personal_details WHERE user_id = %s", (user_id,))
                            result1 = cur_obj.fetchall()

                            if result1:
                                print("THIS USER ID IS USED BEFORE")
                                break
                            else:
                                print(" ")

                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if user_id.startswith("UIC"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        type_of_account = "SALARY ACCOUNT"

                        account_no = generate_account_number()

                        full_name = input("ENTER FULL NAME: ")
                        try:
                            cur_obj.execute("SELECT * FROM personal_details WHERE full_name = %s", (full_name,))
                            result = cur_obj.fetchall()

                            if result:
                                print("THIS NAME IS USED BEFORE")
                                break
                            else:
                                print(" ")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if type(full_name) == str and full_name.isupper():
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        email_id = input("ENTER YOUR EMAIL ID: ")
                        try:
                            cur_obj.execute("SELECT * FROM personal_details WHERE email_id = %s", (email_id,))
                            result = cur_obj.fetchall()

                            if result:
                                print("THIS EMAIL ID IS USED BEFORE")
                                break
                            else:
                                print(" ")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if email_id.find("@") != -1 and email_id.endswith(".com"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break
                        ph_number = input("ENTER YOUR PHONE NUMBER: ")
                        try:
                            cur_obj.execute("SELECT * FROM personal_details WHERE ph_number = %s", (ph_number,))
                            result = cur_obj.fetchall()

                            if result:
                                print("THIS PHONE NUMBER IS USED BEFORE")
                                break
                            else:
                                print(" ")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if len(ph_number) == 10 and ph_number[0] == "6" or ph_number[0] == "7" or ph_number[0] == "8" or \
                                ph_number[0] == "9":
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        date_of_birth = input("ENTER YOUR DATE OF BIRTH(FORMAT - YYYY-MM-DD): ")

                        address = input("\nENTER YOUR PERMANENT ADDRESS(WITHIN 150 WORDS & ALL IN CAPITAL LETTER): ")
                        if len(address) < 151 and address.isupper() == True:
                            print(" ")
                        else:
                            print("ADDRESS IS NOT OK")
                            break

                        print("USER'S PERSONAL DETAILS UPLOADED SUCCESFULLY....")
                        personal_details(user_id, type_of_account, account_no, full_name, email_id, ph_number,
                                         date_of_birth, address)

                        print("\nNOW, PLEASE UPLOAD YOUR PROFESSIONAL DETAILS:")
                        user_id = input("\nENTER YOUR USER ID: ")
                        try:
                            cur_obj.execute("SELECT * FROM professional_details WHERE user_id = %s", (user_id,))
                            result1 = cur_obj.fetchall()

                            if result1:
                                print("THIS USER ID IS USED BEFORE")
                                break
                            else:
                                print(" ")

                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if user_id.startswith("UIC"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break
                        occupation = input("ENTER YOUR OCCUPATION: ")
                        job_sector = input("\n\nENTER YOUR JOB SECTOR(PRIVATE/GOVT.): ")
                        if job_sector == "PRIVATE" or "GOVT.":
                            print(" ")
                        else:
                            print("NOT OK")
                        income = input("\nENTER INCOME (YEARLY): ")
                        print("\nUSER'S PROFESSIONAL DETAILS UPLOADED SUCCESFULLY....")
                        print(f"\nYOUR ACCOUNT NUMBER: {account_no}")
                        print("NOW, GO TO YOUR LOGIN PAGE TO DEPOSIT MONEY/WITHDRAWL MONEY/TRANSFER MONEY")
                        proffessional_details(user_id, occupation, job_sector, income)
                    else:
                        print("INVALID OPTION")
                elif option == "2":
                    user_id_to_fetch = input("ENTER YOUR USER ID TO SEE YOUR ALL DETAILS: ")
                    retrieve_user_details(user_id_to_fetch)
                elif option == "3":
                    user_id = input("ENTER USER ID:")
                    ph_number = input("ENTER NEW PHONE NUMBER:")
                    update_data(user_id, ph_number)
                elif option == "4":
                    print("LOGOUT DONE SUCCESSFULY")
                    break
                else:
                    print("INVALID OPTION")
        else:
            print("USER ID NOT AVAILABLE")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

# Function to authenticate an existing user
#Giving options to upload user's details
def existing_user(username, password):
    cur_obj.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur_obj.fetchall()
    if user:
        print("\nLOGIN SUCCESSFUL.")
        while True:
            print("\n1. CREATE ACCOUNT")
            print("2. TRANSFER MONEY")
            print("3. LOGOUT")

            option = input("\nCHOOSE YOUR OPTION IN (1/2/3): ")

            if option == "1":
                # User Details Upload Menu
                while True:
                    print("\nCHOOSE THE RIGHT OPTION BETWEEN (1 TO 4): ")
                    print("1. CREATE YOUR BANK ACCOUNT")
                    print("2. CHECK YOUR DETAILS")
                    print("3. UPDATE YOUR DETAILS(ONLY PHONE NUMBER)")
                    print("4. LOGOUT")

                    option = input("\nPLEASE SELECT RIGHT OPTION IN BETWEEN (1/2/3/4): ")

                    if option == "1":
                        print("\nENTER YOUR BASIC DETAILS:- ")
                        print("\n1. SAVING ACCOUNT")
                        print("2. SALARY ACCOUNT")
                        option = input("\nPLEASE SELECT RIGHT OPTION IN BETWEEN 1 OR 2 TO UPLOAD YOUR DETAILS: ")

                        if option == "1":
                            user_id = input("\nENTER YOUR USER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM personal_details WHERE user_id = %s", (user_id,))
                                result1 = cur_obj.fetchall()

                                if result1:
                                    print("THIS USER ID IS USED BEFORE")
                                    break
                                else:
                                    print(" ")

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if user_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break

                            type_of_account = "SAVING ACCOUNT"

                            account_no = generate_account_number()

                            full_name = input("ENTER FULL NAME: ")
                            try:
                                cur_obj.execute("SELECT * FROM personal_details WHERE full_name = %s", (full_name,))
                                result = cur_obj.fetchall()

                                if result:
                                    print("THIS NAME IS USED BEFORE")
                                    break
                                else:
                                    print(" ")
                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if type(full_name) == str and full_name.isupper():
                                print(" ")
                            else:
                                print("NOT OK")
                                break

                            email_id = input("ENTER YOUR EMAIL ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM personal_details WHERE email_id = %s", (email_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print("THIS EMAIL ID IS USED BEFORE")
                                    break
                                else:
                                    print(" ")
                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if email_id.find("@") != -1 and email_id.endswith(".com"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            ph_number = input("ENTER YOUR PHONE NUMBER: ")
                            try:
                                cur_obj.execute("SELECT * FROM personal_details WHERE ph_number = %s", (ph_number,))
                                result = cur_obj.fetchall()

                                if result:
                                    print("THIS PHONE NUMBER IS USED BEFORE")
                                    break
                                else:
                                    print(" ")
                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if len(ph_number) == 10 and ph_number[0] == "6" or ph_number[0] == "7" or ph_number[
                                0] == "8" or ph_number[0] == "9":
                                print(" ")
                            else:
                                print("NOT OK")
                                break

                            date_of_birth = input("ENTER YOUR DATE OF BIRTH(FORMAT - YYYY-MM-DD): ")

                            address = input(
                                "\nENTER YOUR PERMANENT ADDRESS(WITHIN 150 WORDS & ALL IN CAPITAL LETTER): ")
                            if len(address) < 151 and address.isupper() == True:
                                print(" ")
                            else:
                                print("ADDRESS IS NOT OK")
                                break

                            print("USER'S PERSONAL DETAILS UPLOADED SUCCESFULLY....")
                            personal_details(user_id, type_of_account, account_no, full_name, email_id, ph_number,
                                             date_of_birth, address)

                            print("\nNOW, PLEASE UPLOAD YOUR PROFESSIONAL DETAILS:")
                            user_id = input("\nENTER YOUR USER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM professional_details WHERE user_id = %s", (user_id,))
                                result1 = cur_obj.fetchall()

                                if result1:
                                    print("THIS USER ID IS USED BEFORE")
                                    break
                                else:
                                    print(" ")

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if user_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            occupation = input("ENTER YOUR OCCUPATION: ")
                            job_sector = input("\n\nENTER YOUR JOB SECTOR(PRIVATE/GOVT./NA): ")
                            if job_sector == "PRIVATE" or "GOVT." or "NA":
                                print(" ")
                            else:
                                print("NOT OK")
                            income = input("\nENTER INCOME (YEARLY): ")
                            print("\nUSER'S PROFESSIONAL DETAILS UPLOADED SUCCESFULLY....")
                            print(f"\nYOUR ACCOUNT NUMBER: {account_no}")
                            print("NOW, GO TO YOUR LOGIN PAGE TO DEPOSIT MONEY/WITHDRAWL MONEY/TRANSFER MONEY")
                            proffessional_details(user_id, occupation, job_sector, income)

                        elif option == "2":
                            user_id = input("\nENTER YOUR USER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM personal_details WHERE user_id = %s", (user_id,))
                                result1 = cur_obj.fetchall()

                                if result1:
                                    print("THIS USER ID IS USED BEFORE")
                                    break
                                else:
                                    print(" ")

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if user_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break

                            type_of_account = "SALARY ACCOUNT"

                            account_no = generate_account_number()

                            full_name = input("ENTER FULL NAME: ")
                            try:
                                cur_obj.execute("SELECT * FROM personal_details WHERE full_name = %s", (full_name,))
                                result = cur_obj.fetchall()

                                if result:
                                    print("THIS NAME IS USED BEFORE")
                                    break
                                else:
                                    print(" ")
                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if type(full_name) == str and full_name.isupper():
                                print(" ")
                            else:
                                print("NOT OK")
                                break

                            email_id = input("ENTER YOUR EMAIL ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM personal_details WHERE email_id = %s", (email_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print("THIS EMAIL ID IS USED BEFORE")
                                    break
                                else:
                                    print(" ")
                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if email_id.find("@") != -1 and email_id.endswith(".com"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            ph_number = input("ENTER YOUR PHONE NUMBER: ")
                            try:
                                cur_obj.execute("SELECT * FROM personal_details WHERE ph_number = %s", (ph_number,))
                                result = cur_obj.fetchall()

                                if result:
                                    print("THIS PHONE NUMBER IS USED BEFORE")
                                    break
                                else:
                                    print(" ")
                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if len(ph_number) == 10 and ph_number[0] == "6" or ph_number[0] == "7" or ph_number[
                                0] == "8" or ph_number[0] == "9":
                                print(" ")
                            else:
                                print("NOT OK")
                                break

                            date_of_birth = input("ENTER YOUR DATE OF BIRTH(FORMAT - YYYY-MM-DD): ")

                            address = input(
                                "\nENTER YOUR PERMANENT ADDRESS(WITHIN 150 WORDS & ALL IN CAPITAL LETTER): ")
                            if len(address) < 151 and address.isupper() == True:
                                print(" ")
                            else:
                                print("ADDRESS IS NOT OK")
                                break

                            print("USER'S PERSONAL DETAILS UPLOADED SUCCESFULLY....")
                            personal_details(user_id, type_of_account, account_no, full_name, email_id, ph_number,
                                             date_of_birth, address)

                            print("\nNOW, PLEASE UPLOAD YOUR PROFESSIONAL DETAILS:")
                            user_id = input("\nENTER YOUR USER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM professional_details WHERE user_id = %s", (user_id,))
                                result1 = cur_obj.fetchall()

                                if result1:
                                    print("THIS USER ID IS USED BEFORE")
                                    break
                                else:
                                    print(" ")

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if user_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            occupation = input("ENTER YOUR OCCUPATION: ")
                            job_sector = input("\n\nENTER YOUR JOB SECTOR(PRIVATE/GOVT.): ")
                            if job_sector == "PRIVATE" or "GOVT.":
                                print(" ")
                            else:
                                print("NOT OK")
                            income = input("\nENTER INCOME (YEARLY): ")
                            print("\nUSER'S PROFESSIONAL DETAILS UPLOADED SUCCESFULLY....")
                            print(f"\nYOUR ACCOUNT NUMBER: {account_no}")
                            print("NOW, GO TO YOUR LOGIN PAGE TO DEPOSIT MONEY/WITHDRAWL MONEY/TRANSFER MONEY")
                            proffessional_details(user_id, occupation, job_sector, income)
                        else:
                            print("INVALID OPTION")
                    elif option == "2":
                        user_id_to_fetch = input("ENTER YOUR USER ID TO SEE YOUR ALL DETAILS: ")
                        retrieve_user_details(user_id_to_fetch)
                    elif option == "3":
                        user_id = input("ENTER USER ID:")
                        ph_number = input("ENTER NEW PHONE NUMBER:")
                        update_data(user_id, ph_number)
                    elif option == "4":
                        print("LOGOUT DONE SUCCESSFULY")
                        break
                    else:
                        print("INVALID OPTION")
            elif option == "2":
                # Transaction Menu
                print("\nCHOOSE RIGHT OPTION TO COMPLETE YOUR TRANSACTION")

                while True:
                    print("\n1. UPLOAD YOUR ACCOUNT DETAILS")
                    print("2. MAKE YOUR TRANSACTION")
                    print("3. TRANSACTION HISTORY")
                    print("4. CHECK BALANCE")
                    print("5. EXIT")

                    option = input("\nENTER YOUR OPTION BETWEEN 1/2/3/4: ")

                    if option == '1':
                        user_id = input("\nENTER YOUR VALIDATE USER ID: ")
                        if user_id.startswith("UIC"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        account_no = input("ENTER YOUR ACCOUNT NO: ")
                        if len(account_no) == 10:
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        full_name = input("ENTER YOUR FULL NAME(IN CAPITAL LETTERS): ")
                        if full_name.isupper() == True:
                            print(" ")
                        else:
                            print("NOT OK")
                            break

                        balance = 0.0
                        account_details(user_id, full_name, account_no, balance)

                    elif option == '2':
                        print("\nTRANSACTION MENU:")
                        print("1. DEPOSIT")
                        print("2. WITHDRAW")
                        print("3. TRANSFER MONEY")
                        print("4. CHECK BALANCE")
                        print("5. EXIT")

                        user_choice = input("ENTER YOUR CHOICE BETWEEN(1/2/3/4): ")

                        if user_choice == '1':
                            user_id = input("\nENTER YOUR USER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE user_id = %s", (user_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("USER ID IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if user_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            account_no = input("ENTER YOUR ACCOUNT NO: ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE account_no = %s", (account_no,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("ACCOUNT NUMBER IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if len(account_no) == 10:
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            full_name = input("ENTER YOUR FULL NAME(IN CAPITAL LETTERS): ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE full_name = %s", (full_name,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("THIS NAME IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if full_name.isupper() == True:
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            amount = float(input("\nENTER AMOUNT TO DEPOSIT: "))
                            date_of_deposit = input("\nENTER THE DATE(YYYY-MM-DD): ")
                            deposit_money(user_id, account_no, full_name, amount, date_of_deposit)
                        elif user_choice == '2':
                            user_id = input("\nENTER YOUR USER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE user_id = %s", (user_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("USER ID IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if user_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            account_no = input("ENTER YOUR ACCOUNT NO: ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE account_no = %s", (account_no,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("ACCOUNT NUMBER IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if len(account_no) == 10:
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            full_name = input("ENTER YOUR FULL NAME(IN CAPITAL LETTERS): ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE full_name = %s", (full_name,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("THIS NAME IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if full_name.isupper() == True:
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            amount = float(input("\nENTER AMOUNT TO WITHDRAWL: "))
                            date_of_withdrawl = input("\nENTER THE DATE(YYYY-MM-DD): ")
                            withdrawl_money(user_id, account_no, full_name, amount, date_of_withdrawl)
                        elif user_choice == '3':
                            sender_id = input("\nENTER YOUR USER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE user_id = %s", (sender_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("USER ID IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if sender_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            receiver_id = input("ENTER RECEIVER USER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE user_id = %s", (receiver_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("USER ID IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if receiver_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            amount = float(input("\nENTER THE AMOUNT YOU WANT TO TRANSFER: "))
                            date_of_transaction = input("\nENTER THE DATE(YYYY-MM-DD): ")
                            transfer_money(sender_id, receiver_id, amount, date_of_transaction)
                        elif user_choice == '4':
                            user_id = input("\nENTER YOUR USER ID TO CHECK BALANCE: ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE user_id = %s", (user_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("USER ID IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if user_id.startswith("UIC"):
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            account_no = input("ENTER YOUR ACCOUNT NO: ")
                            try:
                                cur_obj.execute("SELECT * FROM account_details WHERE account_no = %s", (account_no,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("ACCOUNT NUMBER IS NOT AVAILABLE")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            if len(account_no) == 10:
                                print(" ")
                            else:
                                print("NOT OK")
                                break
                            check_balance(user_id, account_no)
                        elif option == '5':
                            print("EXIT OUT SUCCESSFULY.")
                            break
                        else:
                            print("INVALID CHOICE. PLEASE ENTER VALID OPTION.")
                    elif option == '3':
                        user_id = input("\nENTER YOUR USER ID TO SEE YOUR TRANSACTION: ")
                        try:
                            cur_obj.execute("SELECT * FROM account_details WHERE user_id = %s", (user_id,))
                            result = cur_obj.fetchall()

                            if result:
                                print(" ")
                            else:
                                print("USER ID IS NOT AVAILABLE")
                                break

                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if user_id.startswith("UIC"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break
                        deposit_withdrawl_history(user_id)
                        transaction_history(user_id)
                    elif option == "4":
                        user_id = input("\nENTER YOUR USER ID TO CHECK BALANCE: ")
                        try:
                            cur_obj.execute("SELECT * FROM account_details WHERE user_id = %s", (user_id,))
                            result = cur_obj.fetchall()

                            if result:
                                print(" ")
                            else:
                                print("USER ID IS NOT AVAILABLE")
                                break

                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if user_id.startswith("UIC"):
                            print(" ")
                        else:
                            print("NOT OK")
                            break
                        account_no = input("ENTER YOUR ACCOUNT NO: ")
                        try:
                            cur_obj.execute("SELECT * FROM account_details WHERE account_no = %s", (account_no,))
                            result = cur_obj.fetchall()

                            if result:
                                print(" ")
                            else:
                                print("ACCOUNT NUMBER IS NOT AVAILABLE")
                                break

                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
                            conn_obj.rollback()
                        if len(account_no) == 10:
                            print(" ")
                        else:
                            print("NOT OK")
                            break
                        check_balance(user_id, account_no)
                    elif option == '5':
                        print("EXIT OUT SUCCESSFULY.")
                        break
                    else:
                        print("PLEASE ENTER VALID OPTION.")
            elif option == "3":
                print("\nLOGGED OUT SUCCESSFULY")
                break
            else:
                print("INVALID OPTION")
        return True
    else:
        print("LOGIN FAILED. INVALID USER NAME OR PASSWORD.")
        return False

def genaration_pin():
    return "".join(random.choices("0123", k=4))

def forgot_password(username, password):
    try:
        cur_obj.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur_obj.fetchall()
        if user:
            #Update Password
            cur_obj.execute(f"UPDATE users SET password = %s WHERE username = %s", (password, username,))
            print("\nNEW PASSWORD UPDATE SUCCESSFULY")
            print(f"YOUR NEW PASSWORD: {password}")
            conn_obj.commit()
        else:
            print("ENTERED WRONG USERNAME")
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

# LOGIN Menu
while True:
    print("HELLO, USER".center(50))
    print("WELCOME TO YOUR UIC BANK ONLINE REGISTRATION & LOGIN PAGE".center(50))
    print("\nPLEASE CONFIRM: \nARE YOU A NEW USER OR AN EXISTING USER?")
    print("\nCHOOSE THE RIGHT OPTION BETWEEN 1 & 2:")
    print("1. REGISTER A NEW USER")
    print("2. LOGIN")
    print("3. FORGET PASSWORD")
    print("4. LOGOUT")

    action = input("\nPLEASE SELECT THE OPTION: ")

    if action == "1":
        def validate_input(full_name, username, password, email_id):
            if not (full_name.isupper() == True):
                print("FULL NAME IS IN WRONG FORMAT, PLEASE CHECK")
                return False
            if not (username.find("@") != -1 and username.istitle() and len(username) < 17):
                print("USERNAME IS WRONG, PLEASE CHECK")
                return False
            elif not(len(password) <= 8 and password.istitle()):
                print("PASSWORD IS WRONG, PLEASE CHECK")
                return False
            elif not (email_id.find("@") != -1 and email_id.endswith(".com")):
                print("EMAIL ID IS WRONG, PLEASE CHECK")
                return False
            return True

        user_id = generate_user_id()
        full_name = input("\nENTER YOUR FULL NAME(IN CAPITAL LETTERS): ")
        username = input("\nENTER USER NAME(FORMAT: Limit - 15 Characters(Alphabet, Special Character only '@', Numbers are allowed), EX- 'Souvik@1996'): ")
        try:
            cur_obj.execute("SELECT * FROM users WHERE username = %s", (username,))
            result = cur_obj.fetchall()

            if result:
                print("THIS USERNAME IS USED BEFORE")
                break
            else:
                print(" ")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn_obj.rollback()
        password = input("\nENTER NEW PASSWORD(FORMAT: Limit - 8 Characters(Only Alphabet & Numbers), EX- 'Suvo1996'): ")
        try:
            cur_obj.execute("SELECT * FROM users WHERE password = %s", (password,))
            result = cur_obj.fetchall()

            if result:
                print("THIS PASSWORD IS USED BEFORE")
                break
            else:
                print(" ")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn_obj.rollback()
        email_id = input("\nENTER YOUR EMAIL ID: ")

        if validate_input(full_name, username, password, email_id):
            # Check for duplicate username and password in the database
            try:
                cur_obj.execute("SELECT username, password FROM users WHERE full_name = %s OR username = %s OR password = %s OR email_id = %s",(full_name, username, password, email_id))
                result7 = cur_obj.fetchall()

                if result7:
                    print("THIS USER NAME OR PASSWORD CANNOT BE UPLOADED (USED)")
                else:
                    print("USERNAME & PASSWORD IS ACCEPTED")
                    print(f"\nYOUR REGISTERED USER NAME: {username} AND PASSWORD: {password}")
                    register_user(user_id, full_name, username, password, email_id)

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn_obj.rollback()
        else:
            print("PLEASE CHECK USER NAME OR PASSWORD")
    elif action == "2":
        attempt = 3
        while attempt > 0:
            username = input("\nENTER EXISTING USERNAME(FORMAT: Limit - 16 Characters(Alphabet, Special Character only '@', Numbers are allowed), EX- 'Souvik@1996'): ")
            password = input("\nENTER EXISTING PASSWORD(FORMAT: Limit - 8 Characters(Only Alphabet & Numbers), EX- 'Suvo1996'): ")

            if existing_user(username, password):
                break

            attempt -= 1
            print(f'YOU HAVE {attempt} ATTEMPTS REMAINING.')
    elif action == "3":
        pin = genaration_pin()
        print(f"OTP: {pin}")
        otp = input("\nENTER OTP TO RESET PASSWORD: ")
        if otp == pin:
            username = input("\nENTER YOUR USERNAME: ")
            password = input("ENTER YOUR NEW PASSWORD(FORMAT: Limit - 8 Characters(Only Alphabet & Numbers), (FORMAT: Limit - 8 Characters(Only Alphabet & Numbers), EX- 'Suvo1996')- 'Suvo1996'): ")
            try:
                cur_obj.execute("SELECT * FROM users WHERE password = %s", (password,))
                result = cur_obj.fetchall()
                if result:
                    print("THIS PASSWORD IS USED BEFORE")
                    break
                else:
                    print(" ")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn_obj.rollback()
            if len(password) <= 8:
                print(" ")
            else:
                print("NOT OK")
                break
            forgot_password(username, password)
        else:
            print("YOU HAVE ENTERED WRONG OTP")
    elif action == "4":
        print("LOGGED OUT")
        break
    else:
        print("INVALID OPTION.")

# Close the cursor and connection
conn_obj.close()