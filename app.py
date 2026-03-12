import streamlit as st
import pandas as pd

st.set_page_config(page_title="XYZ Bank Dashboard", page_icon="🏦", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.main-title{
font-size:45px;
font-weight:bold;
color:#0E4D92;
text-align:center;
}

.card{
background-color:white;
padding:25px;
border-radius:15px;
box-shadow:0px 4px 12px rgba(0,0,0,0.1);
margin-bottom:20px;
}

.profile{
background-color:#0E4D92;
color:white;
padding:20px;
border-radius:15px;
text-align:center;
}

.stButton>button{
background-color:#0E4D92;
color:white;
border-radius:10px;
width:100%;
}

</style>
""", unsafe_allow_html=True)

# ---------- BANK CLASS ----------
class BankApplication:

    def __init__(self,name,account_number,age,mobile,balance):
        self.name=name
        self.account_number=account_number
        self.age=age
        self.mobile=mobile
        self.balance=balance
        self.history=[]

    def deposit(self,amount):
        self.balance+=amount
        self.history.append(("Deposit",amount))
        return f"₹{amount} Deposited Successfully"

    def withdraw(self,amount):
        if amount<=self.balance:
            self.balance-=amount
            self.history.append(("Withdraw",amount))
            return f"₹{amount} Withdraw Successful"
        else:
            return "Insufficient Balance"

    def update_mobile(self,new_mobile):
        self.mobile=new_mobile
        return "Mobile Updated"

# ---------- HEADER ----------
st.markdown('<p class="main-title">🏦 SBI Digital Banking Dashboard</p>',unsafe_allow_html=True)

# ---------- SESSION ----------
if "account" not in st.session_state:
    st.session_state.account=None

# ---------- SIDEBAR ----------
st.sidebar.title("🏦 Banking Menu")

menu=[
"Create Account",
"Dashboard",
"Deposit",
"Withdraw",
"Update Mobile"
]

choice=st.sidebar.radio("Select Option",menu)

# ---------- CREATE ACCOUNT ----------
if choice=="Create Account":

    st.subheader("Create New Account")

    col1,col2=st.columns(2)

    with col1:
        name=st.text_input("Name")
        age=st.number_input("Age",min_value=18)

    with col2:
        account=st.text_input("Account Number")
        mobile=st.text_input("Mobile Number")

    balance=st.number_input("Initial Balance",min_value=0)

    if st.button("Create Account"):
        st.session_state.account=BankApplication(name,account,age,mobile,balance)
        st.success("Account Created Successfully")


# ---------- DASHBOARD ----------
elif choice=="Dashboard":

    if st.session_state.account:

        user=st.session_state.account

        col1,col2=st.columns([1,3])

        # PROFILE CARD
        with col1:
            st.markdown(f"""
            <div class="profile">
            <h3>👤 {user.name}</h3>
            <p>Account: {user.account_number}</p>
            <p>📱 {user.mobile}</p>
            <p>Age: {user.age}</p>
            </div>
            """,unsafe_allow_html=True)

        # BALANCE CARD
        with col2:
            st.markdown(f"""
            <div class="card">
            <h2>💰 Current Balance</h2>
            <h1>₹{user.balance}</h1>
            </div>
            """,unsafe_allow_html=True)

        # TRANSACTION HISTORY
        if user.history:

            df=pd.DataFrame(user.history,columns=["Type","Amount"])

            st.subheader("Transaction History")
            st.dataframe(df,use_container_width=True)

            st.subheader("Transaction Chart")
            st.bar_chart(df["Amount"])

    else:
        st.warning("Create an account first")


# ---------- DEPOSIT ----------
elif choice=="Deposit":

    if st.session_state.account:

        amount=st.number_input("Enter Deposit Amount")

        if st.button("Deposit"):
            result=st.session_state.account.deposit(amount)
            st.success(result)

    else:
        st.warning("Create account first")


# ---------- WITHDRAW ----------
elif choice=="Withdraw":

    if st.session_state.account:

        amount=st.number_input("Enter Withdraw Amount")

        if st.button("Withdraw"):
            result=st.session_state.account.withdraw(amount)
            st.success(result)

    else:
        st.warning("Create account first")


# ---------- UPDATE MOBILE ----------
elif choice=="Update Mobile":

    if st.session_state.account:

        new_mobile=st.text_input("New Mobile Number")

        if st.button("Update"):
            result=st.session_state.account.update_mobile(new_mobile)
            st.success(result)

    else:
        st.warning("Create account first")