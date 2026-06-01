import streamlit as st
import csv
import os
import matplotlib.pyplot as plt

# --------------------------
# BANK DATABASE
# --------------------------
if "bank" not in st.session_state:

    st.session_state.bank = {

        1 : {
            "name" : "Rahul Sharma",
            "account_number" : 458921,
            "pin" : 1234,
            "balance" : 25000
        },

        2 : {
            "name" : "Priya Verma",
            "account_number" : 782145,
            "pin" : 5678,
            "balance" : 54000
        },

        3 : {
            "name" : "Amit Roy",
            "account_number" : 963258,
            "pin" : 4321,
            "balance" : 18000
        },

        4 : {
            "name" : "Sneha Das",
            "account_number" : 741852,
            "pin" : 8765,
            "balance" : 72000
        },

        5 : {
            "name" : "Arjun Sen",
            "account_number" : 159357,
            "pin" : 2468,
            "balance" : 31500
        }

    }

bank = st.session_state.bank

# --------------------------
# CSV FILE CREATION
# --------------------------

if os.path.exists("transactions.csv") == False:

    with open("transactions.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "Account",
            "Transaction",
            "Amount"
        ])

# --------------------------
# SESSION STATE
# --------------------------

if "login" not in st.session_state:

    st.session_state.login = False

if "customer" not in st.session_state:

    st.session_state.customer = 0

# --------------------------
# TITLE
# --------------------------

st.title("🏦 Advanced Banking App")

# --------------------------
# LOGIN
# --------------------------

if st.session_state.login == False:

    pin = st.number_input(
        "Enter PIN",
        step=1
    )

    if st.button("Login"):

        found = False

        for customer in bank:

            if bank[customer]["pin"] == pin:

                found = True

                st.session_state.login = True

                st.session_state.customer = customer

        if found == False:

            st.error("Invalid PIN")

# --------------------------
# AFTER LOGIN
# --------------------------

if st.session_state.login == True:

    c = st.session_state.customer

    st.success("Login Successful ✅")

    st.subheader(
        "Welcome " +
        bank[c]["name"]
    )

    st.write(
        "Account Number : ",
        bank[c]["account_number"]
    )

    # --------------------------
    # MENU
    # --------------------------

    option = st.selectbox(

        "Select Banking Service",

        [
            "Balance Enquiry",
            "Deposit Money",
            "Withdraw Money",
            "Fund Transfer",
            "Transaction History",
            "Deposit vs Withdrawal Chart"
        ]

    )

    # --------------------------
    # BALANCE ENQUIRY
    # --------------------------

    if option == "Balance Enquiry":

        st.subheader("💰 Account Balance")

        st.success(
            "Current Balance : ₹ " +
            str(bank[c]["balance"])
        )

    # --------------------------
    # DEPOSIT
    # --------------------------

    if option == "Deposit Money":

        st.subheader("💵 Deposit Money")

        deposit_amount = st.number_input(
            "Enter Deposit Amount",
            step=1
        )

        if st.button("Deposit"):

            bank[c]["balance"] = (

                bank[c]["balance"]
                + deposit_amount

            )

            # SAVE CSV

            with open("transactions.csv", "a", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    bank[c]["name"],
                    bank[c]["account_number"],
                    "Deposit",
                    deposit_amount
                ])

            st.success("Deposit Successful ✅")

            st.write(
                "Updated Balance : ₹",
                bank[c]["balance"]
            )

    # --------------------------
    # WITHDRAW
    # --------------------------

    if option == "Withdraw Money":

        st.subheader("🏧 Withdraw Money")

        withdraw_amount = st.number_input(
            "Enter Withdraw Amount",
            step=1
        )

        if st.button("Withdraw"):

            if withdraw_amount <= bank[c]["balance"]:

                bank[c]["balance"] = (

                    bank[c]["balance"]
                    - withdraw_amount

                )

                # SAVE CSV

                with open("transactions.csv", "a", newline="") as file:

                    writer = csv.writer(file)

                    writer.writerow([
                        bank[c]["name"],
                        bank[c]["account_number"],
                        "Withdrawal",
                        withdraw_amount
                    ])

                st.success("Withdrawal Successful ✅")

                st.write(
                    "Updated Balance : ₹",
                    bank[c]["balance"]
                )

            else:

                st.error("Insufficient Balance")

    # --------------------------
    # FUND TRANSFER
    # --------------------------

    if option == "Fund Transfer":

        st.subheader("🔁 Fund Transfer")

        target_account = st.number_input(
            "Enter Receiver Account Number",
            step=1
        )

        transfer_amount = st.number_input(
            "Enter Transfer Amount",
            step=1
        )

        if st.button("Transfer Money"):

            found = False

            for customer in bank:

                if bank[customer]["account_number"] == target_account:

                    found = True

                    if transfer_amount <= bank[c]["balance"]:

                        bank[c]["balance"] = (
                            bank[c]["balance"]
                            - transfer_amount
                        )

                        bank[customer]["balance"] = (
                            bank[customer]["balance"]
                            + transfer_amount
                        )

                        # SAVE CSV

                        with open("transactions.csv", "a", newline="") as file:

                            writer = csv.writer(file)

                            writer.writerow([
                                bank[c]["name"],
                                bank[c]["account_number"],
                                "Fund Transfer",
                                transfer_amount
                            ])

                        st.success("Fund Transfer Successful ✅")

                        st.write(
                            "Transferred To : ",
                            bank[customer]["name"]
                        )

                        st.write(
                            "Updated Balance : ₹",
                            bank[c]["balance"]
                        )

                    else:

                        st.error("Insufficient Balance")

            if found == False:

                st.error("Receiver Account Not Found")

    # --------------------------
    # TRANSACTION HISTORY
    # --------------------------

    if option == "Transaction History":

        st.subheader("📄 Transaction History")

        with open("transactions.csv", "r") as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) > 1:

                    if str(row[1]) == str(bank[c]["account_number"]):

                        st.write(row)

    # --------------------------
    # PIE CHART
    # --------------------------

    if option == "Deposit vs Withdrawal Chart":

        st.subheader("📊 Deposit vs Withdrawal Analysis")

        deposit_total = 0

        withdrawal_total = 0

        with open("transactions.csv", "r") as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) > 1:

                    if str(row[1]) == str(bank[c]["account_number"]):

                        if row[2] == "Deposit":

                            deposit_total += int(row[3])

                        if row[2] == "Withdrawal":

                            withdrawal_total += int(row[3])

        st.write("Total Deposit : ₹", deposit_total)

        st.write("Total Withdrawal : ₹", withdrawal_total)

        if deposit_total > 0 or withdrawal_total > 0:

            fig, ax = plt.subplots()

            ax.pie(
                [deposit_total, withdrawal_total],
                labels=["Deposit", "Withdrawal"],
                autopct="%1.1f%%"
            )

            st.pyplot(fig)

        else:

            st.warning("No Transactions Found")

    # --------------------------
    # LOGOUT
    # --------------------------

    if st.button("Logout"):

        st.session_state.login = False

        st.session_state.customer = 0

        st.rerun()
