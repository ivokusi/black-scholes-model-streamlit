from matplotlib.colors import LinearSegmentedColormap
from black_scholes import BlackScholes
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np

# First section: Input text boxes
st.sidebar.header("Black Scholes Pricing Calculator")
S = st.sidebar.number_input("Underlying Price (in USD)", min_value=0.0, step=0.10)
K = st.sidebar.number_input("Strike Price (in USD)", min_value=0.0, step=0.10)
sigma = st.sidebar.number_input("Volatility (%)", min_value=0.0, step=0.10)
r = st.sidebar.number_input("Risk-Free Interest Rate (%)", min_value=0.0, step=0.10)
q = st.sidebar.number_input("Dividend Yield (optional) (%)", min_value=0.0, step=0.10)
T = st.sidebar.number_input("Time to Expiration (Yrs)", min_value=0.0, step=0.10)

call_price = "-"
put_price = "-"

st.subheader("Black Scholes Pricing Calculator")

if not S:
    st.error("Underlying Price Can't Be Zero")
elif not K:
    st.error("Strike Price Can't Be Zero")
elif not sigma:
    st.error("Volatility Can't Be Zero")
elif not r:
    st.error("Risk-Free Interest Rate Can't Be Zero")
elif not T:
    st.error("Time to Expiration Can't Be Zero")
else:

    call_price = f"${BlackScholes.call_price(S, K, sigma, r, T, q):.2f}"
    put_price = f"${BlackScholes.put_price(S, K, sigma, r, T, q):.2f}"

st.markdown(
    f"""
    <div style="display: flex; flex-direction: row; align-items: center; justify-content: space-around; width: 100%;">
        <div style="background-color:#39ff14; padding: 20px; border-radius: 10px; width: 45%; text-align: center;">
            <h3 style="color:black; margin: 0;">CALL Value</h3>
            <h1 style="color:black; margin: 10px 0;">{call_price}</h1>
        </div>
        <div style="background-color:#ff073a; padding: 20px; border-radius: 10px; width: 45%; text-align: center;">
            <h3 style="color:black; margin: 0;">PUT Value</h3>
            <h1 style="color:black; margin: 10px 0;">{put_price}</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Heatmap Parameters")

columns = ["Underlying Price (in USD)", "Strike Price (in USD)", "Volatility (%)", "Risk-Free Interest Rate (%)", "Dividend Yield (%)", "Time to Expiration (Yrs)"]

x_col = st.selectbox("X-axis", columns)
columns.remove(x_col)
y_col = st.selectbox("Y-axis", columns)
columns.append(x_col)

# Second section: heatmap parameter (%)
st.sidebar.header("Heatmap Parameters")
x_min = st.sidebar.number_input(f"{x_col} Min", min_value=0.0, step=0.10)
x_max = st.sidebar.number_input(f"{x_col} Max", min_value=x_min, step=0.10)
y_min = st.sidebar.number_input(f"{y_col} Min", min_value=0.0, step=0.10)
y_max = st.sidebar.number_input(f"{y_col} Max", min_value=y_min, step=0.10)

# Third section: Input boxes for call and put prices
st.sidebar.header("Threshold")
call_price = st.sidebar.number_input("Purchase Call Price (in USD)", min_value=0.0, step=0.10)
put_price = st.sidebar.number_input("Purchase Put Price (in USD)", min_value=0.0, step=0.10)

if not x_min:
    st.error(f"{x_col} Min Can't be Zero")
elif not x_max:
    st.error(f"{x_col} Max Can't be Zero")
elif x_min == x_max:
    st.error(f"{x_col} Min and Max Can't be Equal")
elif not y_min:
    st.error(f"{y_col} Min Can't be Zero")
elif not y_min:
    st.error(f"{y_col} Max Can't be Zero")
elif y_min == y_max:
    st.error(f"{y_col} Min and Max Can't be Equal")
elif not call_price:
    st.error("Call Price Can't be Zero")
elif not put_price:
    st.error("Put Price Can't be Zero")


else:

    if st.button("Generate Heatmap"):

        n = 10

        x_vals = np.linspace(x_min, x_max, n)
        y_vals = np.linspace(y_min, y_max, n)

        heatmap_call = [[0] * n for _ in range(n)]
        heatmap_put = [[0] * n for _ in range(n)]

        for i, x_val in enumerate(x_vals):

            S = x_val if x_col == "Underlying Price (in USD)" else S
            K = x_val if x_col == "Strike Price (in USD)" else K
            sigma = x_val if x_col == "Volatility (%)" else sigma
            r = x_val if x_col == "Risk-Free Interest Rate (%)" else r
            q = x_val if x_col == "Dividend Yield (%)" else q
            T = x_val if x_col == "Time to Expiration (Yrs)" else T

            for j, y_val in enumerate(y_vals):

                S = y_val if y_col == "Underlying Price (in USD)" else S
                K = y_val if y_col == "Strike Price (in USD)" else K
                sigma = y_val if y_col == "Volatility (%)" else sigma
                r = y_val if y_col == "Risk-Free Interest Rate (%)" else r
                q = y_val if y_col == "Dividend Yield (%)" else q
                T = y_val if y_col == "Time to Expiration (Yrs)" else T

                heatmap_call[i][j] = BlackScholes.call_price(S, K, sigma, r, T, q)
                heatmap_put[i][j] = BlackScholes.put_price(S, K, sigma, r, T, q)

        heatmap_call = np.array(heatmap_call)
        heatmap_put = np.array(heatmap_put)

        # Create a custom colormap with neon red, neon yellow, and neon green
        colors = ["#ff073a", "#ffff00", "#39ff14"]  # Red, yellow, green
        cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

        col1, col2 = st.columns(2)

        with col1:

            # Plotting the heatmap with a custom dark background
            plt.figure(figsize=(10, 8))
            
            ax = sns.heatmap(heatmap_call, cmap=cmap, center=call_price, cbar=True, annot=True, fmt=".2f", linewidths=.5, linecolor='black')
            ax.set_title("Call Option Price", color="white")

            # Customizing the plot to have the specific dark background color
            background_color = (14/255, 17/255, 23/255)  # RGB values converted to 0-1 scale
            ax.set_facecolor(background_color)
            plt.gcf().set_facecolor(background_color)

            # Adjust the color of the annotations to be readable on the dark background
            for text in ax.texts:
                text.set_color(background_color)

            # Customizing the colorbar to match the theme
            cbar = ax.collections[0].colorbar
            cbar.ax.yaxis.set_tick_params(color="white")
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color="white")

            # Set the x-axis and y-axis labels using the variables x_col and y_col
            ax.set_xlabel(x_col, color="white")
            ax.set_ylabel(y_col, color="white")

            # Set the tick positions using np.linspace and customize their color
            ax.set_xticklabels([f'{tick:.2f}' for tick in x_vals], color="white")
            ax.set_yticklabels([f'{tick:.2f}' for tick in y_vals], color="white")

            # Display the plot in Streamlit
            st.pyplot(plt)
        
        with col2:

            # Plotting the heatmap with a custom dark background
            plt.figure(figsize=(10, 8))
            
            ax = sns.heatmap(heatmap_put, cmap=cmap, center=put_price, cbar=True, annot=True, fmt=".2f", linewidths=.5, linecolor='black')
            ax.set_title("Put Option Price", color="white")

            # Customizing the plot to have the specific dark background color
            background_color = (14/255, 17/255, 23/255)  # RGB values converted to 0-1 scale
            ax.set_facecolor(background_color)
            plt.gcf().set_facecolor(background_color)

            # Adjust the color of the annotations to be readable on the dark background
            for text in ax.texts:
                text.set_color(background_color)

            # Customizing the colorbar to match the theme
            cbar = ax.collections[0].colorbar
            cbar.ax.yaxis.set_tick_params(color="white")
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color="white")
            cbar.set_label('Option Price', rotation=270, labelpad=20, color="white")

            # Set the x-axis and y-axis labels using the variables x_col and y_col
            ax.set_xlabel(x_col, color="white")
            ax.set_ylabel(y_col, color="white")

            # Set the tick positions using np.linspace and customize their color
            ax.set_xticklabels([f'{tick:.2f}' for tick in x_vals], color="white")
            ax.set_yticklabels([f'{tick:.2f}' for tick in y_vals], color="white")

            # Display the plot in Streamlit
            st.pyplot(plt)

        st.info("Green is Undervalued and Red is Overvalued")

    else:
        
        st.write("Waiting To Generate Heatmap...")
