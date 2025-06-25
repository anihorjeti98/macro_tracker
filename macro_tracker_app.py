import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Food macro data with explicit unit field ---
food_data = [
    {"Item": "Fairlife Shake",    "unit": "bottle", "P/unit": 30,     "F/unit": 2.5,   "C/unit": 4,     "Fiber/unit": 0},
    {"Item": "Whole Egg",         "unit": "egg",    "P/unit": 6,      "F/unit": 5,     "C/unit": 0.5,   "Fiber/unit": 0},
    {"Item": "Olive Oil",         "unit": "tbsp",   "P/unit": 0,      "F/unit": 14,    "C/unit": 0,     "Fiber/unit": 0},
    {"Item": "Feta Cheese",       "unit": "100g",   "P/unit": 14,     "F/unit": 21,    "C/unit": 4,     "Fiber/unit": 0},
    {"Item": "Banana",            "unit": "100g",   "P/unit": 1.1,    "F/unit": 0.3,   "C/unit": 23,    "Fiber/unit": 2.6},
    {"Item": "Strawberries",      "unit": "100g",   "P/unit": 0.5,    "F/unit": 0.2,   "C/unit": 6,     "Fiber/unit": 2},
    {"Item": "Blueberries",       "unit": "100g",   "P/unit": 0.7,    "F/unit": 0.3,   "C/unit": 14,    "Fiber/unit": 2.5},
    {"Item": "Blackberries",      "unit": "100g",   "P/unit": 1.4,    "F/unit": 0.5,   "C/unit": 10,    "Fiber/unit": 5},
    {"Item": "Cracker",           "unit": "pc",     "P/unit": 0.2,    "F/unit": 0.4,   "C/unit": 2.2,   "Fiber/unit": 0.2},
    {"Item": "Honey",             "unit": "tbsp",   "P/unit": 0.1,    "F/unit": 0,     "C/unit": 17,    "Fiber/unit": 0},
    {"Item": "Cherries",          "unit": "100g",   "P/unit": 1.06,   "F/unit": 0.2,   "C/unit": 16,    "Fiber/unit": 2.1},
    {"Item": "Triscuit",          "unit": "pc",     "P/unit": 0.2,    "F/unit": 0.4,   "C/unit": 2.2,   "Fiber/unit": 0}
]

foods_df = pd.DataFrame(food_data)

# --- Page config ---
st.set_page_config(page_title="Macro Tracker", layout="centered")
st.title("🍽️ Lean Bulk Macro Tracker")

# --- Macro reference table ---
st.subheader("📋 Macro Content per Unit (per 'unit')")
ref_df = foods_df.copy()
ref_df["Net Carbs/unit"] = ref_df["C/unit"] - ref_df["Fiber/unit"]
# Calculate calories per macro per unit
ref_df["Cal from Protein/unit"] = ref_df["P/unit"] * 4
ref_df["Cal from Fat/unit"] = ref_df["F/unit"] * 9
ref_df["Cal from Net Carbs/unit"] = ref_df["Net Carbs/unit"] * 4
# Total calories per unit
ref_df["Calories/unit"] = ref_df["Cal from Protein/unit"] + ref_df["Cal from Fat/unit"] + ref_df["Cal from Net Carbs/unit"]
st.dataframe(ref_df.rename(columns={
    "Item": "Food",
    "unit": "Unit",
    "P/unit": "Protein_per_unit (g)",
    "F/unit": "Fat_per_unit (g)",
    "C/unit": "Carbs_per_unit (g)",
    "Fiber/unit": "Fiber_per_unit (g)",
    "Net Carbs/unit": "Net_Carbs_per_unit (g)",
    "Cal from Protein/unit": "Cal_from_Protein_per_unit (kcal)",
    "Cal from Fat/unit": "Cal_from_Fat_per_unit (kcal)",
    "Cal from Net Carbs/unit": "Cal_from_Net_Carbs_per_unit (kcal)",
    "Calories/unit": "Calories_per_unit (kcal)"
})[["Food","Unit","Protein_per_unit (g)","Fat_per_unit (g)","Carbs_per_unit (g)","Fiber_per_unit (g)","Net_Carbs_per_unit (g)","Cal_from_Protein_per_unit (kcal)","Cal_from_Fat_per_unit (kcal)","Cal_from_Net_Carbs_per_unit (kcal)","Calories_per_unit (kcal)"]])

# --- Sidebar: Macro goals ---
st.sidebar.header("🎯 Daily Macro Goals")
cal_goal = st.sidebar.number_input("Calories", 0, 10000, value=1600)
protein_goal = st.sidebar.number_input("Protein (g)", 0, 1000, value=180)
fat_goal = st.sidebar.number_input("Fat (g)", 0, 1000, value=44)
carb_goal = st.sidebar.number_input("Net Carbs (g)", 0, 1000, value=121)

# --- Initialize log state ---
if "log" not in st.session_state:
    st.session_state.log = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

# --- Input: add entries ---
st.subheader("➕ Log a Food Item")
choice = st.selectbox("Food", foods_df["Item"])
amt = st.number_input("Amount (in unit)", min_value=0.0, max_value=1000.0, step=0.1)
if st.button("Add to Log"):
    st.session_state.log.append({"id": st.session_state.next_id, "Item": choice, "Amount": amt})
    st.session_state.next_id += 1

# --- Display and edit log ---
log_df = pd.DataFrame(st.session_state.log)
if not log_df.empty:
    # Merge and calculate macros per entry
    def adjust_macro(val, unit):
        return val / 100 if unit == "100g" else val

    n_df = log_df.merge(foods_df, on="Item")
    for m in ["P", "F", "C", "Fiber"]:
        n_df[f"{m}_g"] = n_df.apply(lambda r: adjust_macro(r[f"{m}/unit"] * r["Amount"], r["unit"]), axis=1)
    n_df.rename(columns={"P_g":"Protein_g","F_g":"Fat_g","C_g":"Carbs_g","Fiber_g":"Fiber_g"}, inplace=True)
    n_df["Net_Carbs_g"] = n_df["Carbs_g"] - n_df["Fiber_g"]
    n_df["Calories"] = n_df["Protein_g"]*4 + n_df["Fat_g"]*9 + n_df["Net_Carbs_g"]*4

    # Show log
    st.subheader("📝 Current Log")
    st.dataframe(n_df[["id","Item","Amount","unit","Protein_g","Fat_g","Net_Carbs_g","Fiber_g","Calories"]])

    # Delete entry
    sel = st.selectbox("Select ID to delete", n_df["id"].tolist())
    if st.button("Delete Entry"):
        st.session_state.log = [e for e in st.session_state.log if e["id"] != sel]
        st.experimental_rerun()

    # Totals & remaining
    tot = n_df[["Protein_g","Fat_g","Net_Carbs_g","Fiber_g","Calories"]].sum()
    rem = pd.Series({
        "Protein_g": max(0, protein_goal - tot["Protein_g"]),
        "Fat_g": max(0, fat_goal - tot["Fat_g"]),
        "Net_Carbs_g": max(0, carb_goal - tot["Net_Carbs_g"]),
        "Fiber_g": "-",
        "Calories": max(0, cal_goal - tot["Calories"])
    })
    st.subheader("✅ Progress vs Goal")
    st.dataframe(pd.DataFrame({"Goal": [protein_go...
