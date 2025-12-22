import streamlit as st
import pandas as pd
import requests

API_BASE = "http://127.0.0.1:8000"

def add_expense(user_id, name, amount, category, date):
    data = {
        "user_id": user_id,
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    }
    requests.post(f"{API_BASE}/expenses/", json=data)

def get_expenses(user_id):
    r = requests.get(f"{API_BASE}/expenses/{user_id}")
    return r.json() if r.status_code == 200 else []

def add_income(user_id, amount, date):
    data = {
        "user_id": user_id,
        "amount": amount,
        "date": date
    }
    requests.post(f"{API_BASE}/expenses/incomes/", json=data)

def get_incomes(user_id):
    r = requests.get(f"{API_BASE}/expenses/incomes/{user_id}")
    return r.json() if r.status_code == 200 else []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.title("Personal finance and budget management app")

menu = ["Login", "Register"] if not st.session_state.logged_in else ["Dashboard", "Troskovi", "Prihodi", "Logout"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        r = requests.post(f"{API_BASE}/auth/register", json={"username": username, "password": password})
        st.success("Registracija uspješna") if r.status_code == 200 else st.error(r.json()["detail"])

elif choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        r = requests.post(f"{API_BASE}/auth/login", json={"username": username, "password": password})
        if r.status_code == 200:
            data = r.json()
            st.session_state.logged_in = True
            st.session_state.username = data["username"]
            st.session_state.user_id = data["id"]
            st.rerun()
        else:
            st.error(r.json()["detail"])

elif choice == "Dashboard":
    expenses = get_expenses(st.session_state.user_id)
    incomes = get_incomes(st.session_state.user_id)

    total_spent = sum(e["amount"] for e in expenses)
    total_income = sum(i["amount"] for i in incomes)

    st.metric("Total Budget", total_income - total_spent)
    st.metric("Total Spent", total_spent)

    name = st.text_input("Naziv troška")
    amount = st.number_input("Iznos troška", min_value=0.0)
    category = st.selectbox("Kategorija", ["Hrana", "Prevoz", "Rezije", "Zabava"])
    date = st.date_input("Datum")
    if st.button("Dodaj trošak"):
        add_expense(st.session_state.user_id, name, amount, category, str(date))
        st.rerun()

    income_amount = st.number_input("Iznos prihoda", min_value=0.0)
    income_date = st.date_input("Datum prihoda")
    if st.button("Dodaj prihod"):
        add_income(st.session_state.user_id, income_amount, str(income_date))
        st.rerun()

elif choice == "Troskovi":
    data = get_expenses(st.session_state.user_id)
    if not data:
        st.info("Nema troškova")
    else:
        df = pd.DataFrame(data)
        df["year"] = pd.to_datetime(df["date"]).dt.year
        categories = ["Sve"] + sorted(df["category"].unique())
        cat = st.selectbox("Kategorija", categories)
        if cat != "Sve":
            df = df[df["category"] == cat]

        sort = st.selectbox("Sortiraj", ["Iznos ↑", "Iznos ↓", "Kategorija", "Godina"])
        if sort == "Iznos ↑":
            df = df.sort_values("amount")
        elif sort == "Iznos ↓":
            df = df.sort_values("amount", ascending=False)
        elif sort == "Kategorija":
            df = df.sort_values("category")
        elif sort == "Godina":
            df = df.sort_values("year")

        st.dataframe(df, use_container_width=True)

elif choice == "Prihodi":
    data = get_incomes(st.session_state.user_id)
    if not data:
        st.info("Nema prihoda")
    else:
        df = pd.DataFrame(data)
        df["year"] = pd.to_datetime(df["date"]).dt.year
        sort = st.selectbox("Sortiraj", ["Iznos ↑", "Iznos ↓", "Godina"])
        if sort == "Iznos ↑":
            df = df.sort_values("amount")
        elif sort == "Iznos ↓":
            df = df.sort_values("amount", ascending=False)
        elif sort == "Godina":
            df = df.sort_values("year")

        st.dataframe(df, use_container_width=True)

elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = None
    st.rerun()

if st.session_state.logged_in:
    st.success(f"Dobrodošao, {st.session_state.username}")
