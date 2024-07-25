import streamlit as st

# -------------Building Functions------------------

import numpy as np
# Use bash to download packages that are not already installed
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import streamlit.components.v1 as components


# Define Blackscholes option pricing formula

def blackScholes(S, K, r, T, volatility, type="c"):
    d1 = (np.log(S / K) + (r + volatility ** 2 / 2) * T) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    try:
        if type == "c":
            price = S * norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * norm.cdf(d2, 0, 1)
        elif type == "p":
            price = K * np.exp(-r * T) * norm.cdf(-d2, 0, 1) - S * norm.cdf(-d1, 0, 1)

        return price

    except:
        st.sidebar.error("Please enter all the parameters")


# ----------------- Option Greeks------------

# Define Delta Option Sensitivity
def optionDelta(S, K, r, T, volatility, type="c"):
    d1 = (np.log(S / K) + (r + (volatility ** 2) / 2)) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    try:
        if type == "c":
            delta = norm.cdf(d1, 0, 1)
        elif type == "p":
            delta = -norm.cdf(-d1, 0, 1)
        return delta
    except:
        st.sidebar.error("Please enter all the parameters")


# Define Gamma Option Sensitivity
def optionGamma(S, K, r, T, volatility):
    d1 = (np.log(S / K) + (r + (volatility ** 2) / 2)) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    try:
        gamma = norm.pdf(d1, 0, 1) / (S * volatility * np.sqrt(T))
    except:
        st.sidebar.error("Please enter all the parameters")
    return gamma


# Define Vega Option Sensitivity
def optionVega(S, K, r, T, volatility):
    d1 = (np.log(S / K) + (r + (volatility ** 2) / 2)) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    try:
        Vega = S * norm.pdf(d1, 0, 1) * T
    except:
        st.sidebar.error("Please enter all the parameters")
    return Vega


# Define Theta Option Sensitivity
def optionTheta(S, K, r, T, volatility, type="c"):
    d1 = (np.log(S / K) + (r + (volatility ** 2) / 2)) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    try:
        if type == "c":
            theta = -((S * norm.pdf(d1, 0, 1) * volatility) / (2 * np.sqrt(T))) - (
                        r * K * np.exp(-r * T) * norm.cdf(d2))
        elif type == "p":
            theta = -((S * norm.pdf(d1, 0, 1) * volatility) / (2 * np.sqrt(T))) + (
                        r * K * np.exp(-r * T) * norm.cdf(-d2))
        return theta
    except:
        st.sidebar.error("Please enter all the parameters")


# Define Rho Option Sensitivity
def optionRho(S, K, r, T, volatility, type="c"):
    d1 = (np.log(S / K) + (r + (volatility ** 2) / 2)) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    try:
        if type == "c":
            rho = K * T * np.exp(-r * T) * norm.cdf(d2)
        elif type == "p":
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        return rho
    except:
        st.sidebar.error("Please enter all the parameters")


# -----------Building the User Interface-------------------

st.title("Black Scholes Pricing Calculator")
st.write(
    "Samarth Bahukhandi"
)

st.markdown("<h2 align = 'center'> Option Greeks </h2>", unsafe_allow_html=True)

sidebar_title = st.sidebar.header(body="Blackscholes Parameters")

space = st.sidebar.header("")

r = st.sidebar.slider(label="Risk-Free Rate (Rf)", min_value=0.000,
                      max_value=1.000, value=0.30, step=0.01)

S = st.sidebar.number_input(label="Underlying Asset Price (s)", min_value=1.000,
                            value=30.000, step=0.100)

K = st.sidebar.number_input(label="Strike Price (K)", min_value=1.000,
                            value=50.000, step=0.100)

days_to_expiry = st.sidebar.number_input(label="Total Number of Days to Expire",
                                         min_value=1.000, value=200.000, step=1.000)

volatility = st.sidebar.slider(label="Volatility", min_value=0.000,
                               max_value=1.000, value=0.30, step=0.01)

option = st.sidebar.selectbox(label="Option Type", options=['Call', 'Put'])

# Choosing the type of option
type = ""

if option == "Call":
    type = "c"
elif option == "Put":
    type = "p"

# Choosing the date of expiry of option
T = days_to_expiry / 365

# -----------------------Adding Iterations--------------------------------

# Build the x-axis variable in list with given range
stock_price_x = [i for i in range(0, int(S) + 50)]

# Build BlackScholes list of option prices from specific x-stock prices
prices = [blackScholes(i, K, r, T, volatility, type) for i in stock_price_x]

delta = [optionDelta(i, K, r, T, volatility, type) for i in stock_price_x]

gamma = [optionGamma(i, K, r, T, volatility) for i in stock_price_x]

vega = [optionVega(i, K, r, T, volatility) for i in stock_price_x]

theta = [optionTheta(i, K, r, T, volatility, type) for i in stock_price_x]

rho = [optionRho(i, K, r, T, volatility, type) for i in stock_price_x]

# Building other Interface

col1, col2, col3, col4, col5 = st.columns(5)
col2.metric("Call Price", round(blackScholes(S, K, r, T, volatility, type="c"), 3))
col4.metric("Put Price", round(blackScholes(S, K, r, T, volatility, type="p"), 3))

cola, colb, colc, cold, cole = st.columns(5)
cola.metric("Delta Call", round(optionDelta(S, K, r, T, volatility, type="c"), 3))
colb.metric("Gamma", round(optionGamma(S, K, r, T, volatility), 3))
colc.metric("Vega", round(optionVega(S, K, r, T, volatility), 3))
cold.metric("Theta Call", round(optionTheta(S, K, r, T, volatility, type="c"), 3))
cole.metric("Rho Call", round(optionRho(S, K, r, T, volatility, type="c"), 3))

# ----------------------Building the Charting Layout-------------------------


sns.set_style("dark")
sns.color_palette("rocket")

fig1, ax1 = plt.subplots()
sns.lineplot(x=stock_price_x, y=prices, color="green")
ax1.set_title("Black Scholes Option Price")
ax1.set_xlabel("Asset Price")
ax1.set_ylabel("Option Price")

fig2, ax2 = plt.subplots()
sns.lineplot(x=stock_price_x, y=delta, color="red")
ax2.set_title("Delta")
ax2.set_xlabel("Asset Price")
ax2.set_ylabel("Delta")

fig3, ax3 = plt.subplots()
sns.lineplot(x=stock_price_x, y=gamma, color="blue")
ax3.set_title("Gamma")
ax3.set_xlabel("Asset Price")
ax3.set_ylabel("Gamma")

fig4, ax4 = plt.subplots()
sns.lineplot(x=stock_price_x, y=vega, color="orange")
ax4.set_title("Vega")
ax4.set_xlabel("Asset Price")
ax4.set_ylabel("Vega")

fig5, ax5 = plt.subplots()
sns.lineplot(x=stock_price_x, y=theta, color="yellow")
ax5.set_title("Theta")
ax5.set_xlabel("Asset Price")
ax5.set_ylabel("Theta")

fig6, ax6 = plt.subplots()
sns.lineplot(x=stock_price_x, y=rho, color="black")
ax6.set_title("Rho")
ax6.set_xlabel("Asset Price")
ax6.set_ylabel("Rho")

# Do a tight layout for parameters to fit within subplot
fig1.tight_layout()
fig2.tight_layout()
fig3.tight_layout()
fig4.tight_layout()
fig5.tight_layout()
fig6.tight_layout()

st.markdown("<h2 align = 'center'> Graph of the Greeks </h2>", unsafe_allow_html=True)


st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)
st.pyplot(fig4)
st.pyplot(fig5)
st.pyplot(fig6)
