import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Food macro data ---
food_data = [
    {"Item": "Fairlife Shake",    "P/unit": 30,     "F/unit": 2.5,   "C/unit": 4,     "Fiber/unit": 0},
    {"Item": "Whole Egg",         "P/unit": 6,      "F/unit": 5,     "C/unit": 0.5,   "Fiber/unit": 0},
    {"Item": "Olive Oil (tbsp)",  "P/unit": 0,      "F/unit": 14,    "C/unit": 0,     "Fiber/unit": 0},
    {"Item": "Feta Cheese (28g)", "P/unit": 4,      "F/unit": 6,     "C/unit": 1,     "Fiber/unit": 0},
    {"Item": "Banana (g)",        "P/unit": 0.011,  "F/unit": 0.003, "C/unit": 0.23,  "Fiber/unit": 0.026},
    {"Item": "Strawberries (g)",  "P/unit": 0.005,  "F/unit": 0.002, "C/unit": 0.06,  "Fiber/unit": 0.02},
    {"Item": "Blueberries (g)",   "P/unit": 0.007,  "F/unit": 0.003, "C/unit": 0.14,  "Fiber/unit": 0.025},
    {"Item": "Blackberries (g)",  "P/unit": 0.014,  "F/unit": 0.005, "C/unit": 0.10,  "Fiber/unit": 0.05},
    {"Item": "Crackers (pc)",     "P/unit": 0.16,   "F/unit": 0.8,   "C/unit": 2,     "Fiber/unit": 0.2},
    {"Item": "Honey (tbsp)",      "P/unit": 0.1,    "F/unit": 0,     "C/unit": 17,    "Fiber/unit": 0},
    {"Item": "Cherries (g)",      "P/unit": 0.0106, "F/unit": 0.002, "C/unit": 0.16,  "Fiber/unit": 0.021},
    {"Item": "Triscuit (pc)",     "P/unit": 0.2,    "F/unit": 0.4,   "C/unit": 2.2,   "Fiber/unit": 0}
]

foods_df = pd.DataFrame(food_data)

# --- Set page config ---
st.set_page_config(page_title="Macro Tracker", layout="centered")
st.title("🍽️ Lean Bulk Macro Tracker")

# --- Sidebar: Set Macro Goals ---
st.sidebar.header("Daily Macro Goals")
cal_goal = st.sidebar.number_input("Calories", 1600, 4000, value=1600)
protein_goal = st.sidebar.number_input("Protein (g)", 0, 300, value=180)
fat_goal = st.sidebar.number_input("Fat (g)", 0, 200, value=44)
carb_goal = st.sidebar.number_input("Net Carbs (g)", 0, 400, value=121)

# --- Tracker session state ---
if "log" not in st.session_state:
    st.session_state.log = []

# --- Input Section ---
st.subheader("📥 Log a Food Item")
food = st.selectbox("Food Item", foods_df["Item"])
amount = st.number_input("Amount (g, pc, or tbsp)", 0.0, 1000.0, step=1.0)
if st.button("Add to Log"):
    st.session_state.log.append({"Item": food, "Amount": amount})

# --- Display Table ---
log_df = pd.DataFrame(st.session_state.log)
if not log_df.empty:
    merged = log_df.merge(foods_df, on="Item")
    merged["Protein_g"] = merged["Amount"] * merged["P/unit"]
    merged["Fat_g"] = merged["Amount"] * merged["F/unit"]
    merged["Carbs_g"] = merged["Amount"] * merged["C/unit"]
    merged["Fiber_g"] = merged["Amount"] * merged["Fiber/unit"]
    merged["Net_Carbs_g"] = merged["Carbs_g"] - merged["Fiber_g"]
    merged["Calories"] = merged["Protein_g"] * 4 + merged["Fat_g"] * 9 + merged["Net_Carbs_g"] * 4

    st.subheader("📊 Current Log")
    st.dataframe(merged[["Item", "Amount", "Protein_g", "Fat_g", "Net_Carbs_g", "Fiber_g", "Calories"]])

    totals = merged[["Protein_g", "Fat_g", "Net_Carbs_g", "Fiber_g", "Calories"]].sum()
    remaining = pd.Series({
        "Protein_g": max(0, protein_goal - totals["Protein_g"]),
        "Fat_g": max(0, fat_goal - totals["Fat_g"]),
        "Net_Carbs_g": max(0, carb_goal - totals["Net_Carbs_g"]),
        "Fiber_g": "-",
        "Calories": max(0, cal_goal - totals["Calories"])
    })

    st.subheader("✅ Progress vs Goal")
    progress_df = pd.DataFrame({
        "Goal": [protein_goal, fat_goal, carb_goal, "-", cal_goal],
        "Consumed": totals,
        "Remaining": remaining
    }, index=["Protein_g", "Fat_g", "Net_Carbs_g", "Fiber_g", "Calories"])

    st.dataframe(progress_df)

    # Pie chart for macros
    macro_pie = pd.Series({
        "Protein": totals["Protein_g"] * 4,
        "Fat": totals["Fat_g"] * 9,
        "Net Carbs": totals["Net_Carbs_g"] * 4
    })

    st.subheader("🧬 Macro Breakdown")
    fig, ax = plt.subplots()
    ax.pie(macro_pie, labels=macro_pie.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Current % of Calories from Macros")
    st.pyplot(fig)

else:
    st.info("Add some food to begin tracking.")
