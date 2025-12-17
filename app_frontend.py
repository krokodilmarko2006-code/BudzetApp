import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/auth"

def add_expense(user_id, name, amount, category, date):
    data = {
        "user_id": user_id,
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    }
    response = requests.post(f"{API_URL.replace('/auth','')}/expenses/", json=data)
    return response.json()

def get_expenses(user_id):
    response = requests.get(f"{API_URL.replace('/auth','')}/expenses/{user_id}")
    if response.status_code == 200:
        return response.json()
    return []

def add_income(user_id, amount, date):
    data = {
        "user_id": user_id,
        "amount": amount,
        "date": date
    }
    response = requests.post(f"{API_URL.replace('/auth','')}/expenses/incomes/", json=data)
    return response.json()

def get_incomes(user_id):
    response = requests.get(f"{API_URL.replace('/auth','')}/expenses/incomes/{user_id}")
    if response.status_code == 200:
        return response.json()
    return []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.title("Personal finance and budget management app")

if st.session_state.logged_in:
    menu = ["Dashboard", "Logout"]
else:
    menu = ["Login", "Register"]

choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Register novi korisnik")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        data = {"username": username, "password": password}
        response = requests.post(f"{API_URL}/register", json=data)
        if response.status_code == 200:
            st.success("Registracija uspešna!")
        else:
            st.error(response.json()["detail"])

elif choice == "Login":
    st.subheader("Login korisnika")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        data = {"username": username, "password": password}
        response = requests.post(f"{API_URL}/login", json=data)
        if response.status_code == 200:
            data = response.json()
            st.session_state.logged_in = True
            st.session_state.username = data["username"]
            st.session_state.user_id = data["id"]
            st.success("Uspješno ste prijavljeni!")
            st.rerun()
        else:
            st.error(response.json()["detail"])

elif choice == "Dashboard" and st.session_state.logged_in:
    st.subheader("Dashboard")

    expenses = get_expenses(st.session_state.user_id)
    incomes = get_incomes(st.session_state.user_id)

    total_spent = sum([e["amount"] for e in expenses])
    total_income = sum([i["amount"] for i in incomes])
    total_budget = total_income - total_spent

    st.metric("Total Budget", total_budget)
    st.metric("Total Spent", total_spent)

    st.subheader("Dodaj trošak")
    expense_name = st.text_input("Naziv troška", key="expense_name")
    expense_amount = st.number_input("Iznos", min_value=0.0, key="expense_amount")
    expense_category = st.selectbox("Kategorija", ["Hrana", "Prevoz", "Rezije", "Zabava"], key="expense_cat")
    expense_date = st.date_input("Datum", key="expense_date")

    if st.button("Dodaj trošak"):
        add_expense(
            st.session_state.user_id,
            expense_name,
            expense_amount,
            expense_category,
            str(expense_date)
        )
        st.success(f"Dodat trošak: {expense_name} {expense_amount} KM")
        st.rerun()

    st.subheader("Dodaj prihod")
    income_amount = st.number_input("Iznos prihoda", min_value=0.0, key="income_amount")
    income_date = st.date_input("Datum prihoda", key="income_date_input")

    if st.button("Dodaj prihod"):
        add_income(
            st.session_state.user_id,
            income_amount,
            str(income_date)
        )
        st.success(f"Dodat prihod: {income_amount} KM")
        st.rerun()

    st.subheader("Troškovi")
    if expenses:
        st.table(expenses)
    else:
        st.info("Nema troškova")

    st.subheader("Prihodi")
    if incomes:
        st.table(incomes)
    else:
        st.info("Nema prihoda")

elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = None
    st.success("Odjavljeni ste")
    st.rerun()

if st.session_state.logged_in:
    st.success(f"Dobrodošao, {st.session_state.username}")
