import streamlit as st
import pandas as pd

# --- Streamlit page config ---
st.set_page_config(page_title="Macro Tracker", layout="centered")
st.title("🍽️ Lean Bulk Macro Tracker")

# --- Define macro goal presets based on weekly plan ---
presets = [
    {"Week": "Week 1", "Dates": "Jun 24–30",   "Calories": 1650, "Protein (g)": 180, "Fat (g)": 44, "Net Carbs (g)": 125},
    {"Week": "Week 2", "Dates": "Jul 1–7",     "Calories": 1750, "Protein (g)": 180, "Fat (g)": 48, "Net Carbs (g)": 130},
    {"Week": "Week 3", "Dates": "Jul 8–14",    "Calories": 1850, "Protein (g)": 185, "Fat (g)": 50, "Net Carbs (g)": 137},
    {"Week": "Week 4", "Dates": "Jul 15–21",   "Calories": 1950, "Protein (g)": 185, "Fat (g)": 52, "Net Carbs (g)": 145},
    {"Week": "Week 5", "Dates": "Jul 22–28",   "Calories": 2050, "Protein (g)": 190, "Fat (g)": 55, "Net Carbs (g)": 152},
    {"Week": "Week 6", "Dates": "Jul 29–Aug 4", "Calories": 2150, "Protein (g)": 190, "Fat (g)": 57, "Net Carbs (g)": 160},
    {"Week": "Week 7", "Dates": "Aug 5–11",    "Calories": 2250, "Protein (g)": 190, "Fat (g)": 60, "Net Carbs (g)": 167},
    {"Week": "Final Push (Week 8)", "Dates": "Aug 12–18 (peak)", "Calories": 2300, "Protein (g)": 190, "Fat (g)": 62, "Net Carbs (g)": 174},
    {"Week": "Custom",  "Dates": "-",          "Calories": None, "Protein (g)": None, "Fat (g)": None, "Net Carbs (g)": None}
]
presets_df = pd.DataFrame(presets).set_index("Week")

# --- Display presets table above menu ---
st.subheader("📑 Available Macro Goal Presets")
st.table(presets_df)

# --- User selects a plan ---
plan = st.selectbox("Select your macro goal week:", presets_df.index.tolist())
selected = presets_df.loc[plan]

# --- Assign macro goals ---
if plan == "Custom":
    st.subheader("➤ Enter Custom Macro Goals")
    cal_goal = st.number_input("Calories", min_value=0, value=1600)
    protein_goal = st.number_input("Protein (g)", min_value=0, value=180)
    fat_goal = st.number_input("Fat (g)", min_value=0, value=44)
    carb_goal = st.number_input("Net Carbs (g)", min_value=0, value=121)
else:
    cal_goal = int(selected["Calories"])
    protein_goal = int(selected["Protein (g)"])
    fat_goal = int(selected["Fat (g)"])
    carb_goal = int(selected["Net Carbs (g)"])
    st.markdown(f"**Selected {plan} ({selected['Dates']})**:<br>{cal_goal} kcal, {protein_goal}g P, {fat_goal}g F, {carb_goal}g C", unsafe_allow_html=True)

# --- Base food macro data ---
base_foods = [
    {"Item": "Fairlife Shake", "unit": "bottle", "P/unit": 30, "F/unit": 2.5, "C/unit": 4, "Fiber/unit": 0},
    {"Item": "Whole Egg",      "unit": "egg",    "P/unit": 6,  "F/unit": 5,   "C/unit": 0.5, "Fiber/unit": 0},
    {"Item": "Olive Oil",      "unit": "tbsp",   "P/unit": 0,  "F/unit": 14,  "C/unit": 0,   "Fiber/unit": 0},
    {"Item": "Feta Cheese",    "unit": "100g",   "P/unit": 14, "F/unit": 21,  "C/unit": 4,   "Fiber/unit": 0},
    {"Item": "Banana",         "unit": "100g",   "P/unit": 1.1,"F/unit": 0.3, "C/unit": 23,  "Fiber/unit": 2.6},
    {"Item": "Strawberries",   "unit": "100g",   "P/unit": 0.5,"F/unit": 0.2, "C/unit": 6,   "Fiber/unit": 2},
    {"Item": "Blueberries",    "unit": "100g",   "P/unit": 0.7,"F/unit": 0.3, "C/unit": 14,  "Fiber/unit": 2.5},
    {"Item": "Blackberries",   "unit": "100g",   "P/unit": 1.4,"F/unit": 0.5, "C/unit": 10,  "Fiber/unit": 5},
    {"Item": "Cracker",        "unit": "pc",     "P/unit": 0.2,"F/unit": 0.4, "C/unit": 2.2, "Fiber/unit": 0.2},
    {"Item": "Honey",          "unit": "tbsp",   "P/unit": 0.1,"F/unit": 0,   "C/unit": 17,  "Fiber/unit": 0},
    {"Item": "Cherries",       "unit": "100g",   "P/unit": 1.06,"F/unit": 0.2,"C/unit": 16,  "Fiber/unit": 2.1},
    {"Item": "Triscuit",       "unit": "pc",     "P/unit": 0.2,"F/unit": 0.4, "C/unit": 2.2, "Fiber/unit": 0}
]

# --- Session state for custom foods and log ---
if "custom_foods" not in st.session_state:
    st.session_state.custom_foods = []
if "log" not in st.session_state:
    st.session_state.log = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

foods_df = pd.DataFrame(base_foods + st.session_state.custom_foods)

# --- Macro Reference Table (Menu) ---
st.subheader("📋 Macro Content per Unit")
ref_df = foods_df.copy()
ref_df["Net Carbs/unit"] = ref_df["C/unit"] - ref_df["Fiber/unit"]
ref_df["Calories per unit"] = ref_df["P/unit"]*4 + ref_df["F/unit"]*9 + ref_df["Net Carbs/unit"]*4
st.dataframe(
    ref_df.rename(columns={
        "Item":"Food","unit":"Unit",
        "P/unit":"Protein (g)","F/unit":"Fat (g)",
        "C/unit":"Carbs (g)","Fiber/unit":"Fiber (g)",
        "Net Carbs/unit":"Net Carbs (g)","Calories per unit":"Calories per unit"
    })[["Food","Unit","Protein (g)","Fat (g)","Carbs (g)","Fiber (g)","Net Carbs (g)","Calories per unit"]]
)

# --- Add Custom Food ---
st.subheader("➕ Add a Custom Food to Menu")
new_name = st.text_input("Food Name for Menu", key="new_name")
new_unit = st.selectbox("Unit", ["100g","g","pc","tbsp","cup","oz"], key="menu_unit")
new_p = st.number_input("Protein per unit (g)", min_value=0.0, key="menu_p")
new_f = st.number_input("Fat per unit (g)", min_value=0.0, key="menu_f")
new_c = st.number_input("Carbs per unit (g)", min_value=0.0, key="menu_c")
new_fiber = st.number_input("Fiber per unit (g)", min_value=0.0, key="menu_fiber")
if st.button("Add to Menu", key="add_menu_button"):
    st.session_state.custom_foods.append({"Item": new_name, "unit": new_unit, "P/unit": new_p, "F/unit": new_f, "C/unit": new_c, "Fiber/unit": new_fiber})

# --- Log Input ---
st.subheader("➕ Log a Food Item")
choice = st.selectbox("Food to Log", foods_df["Item"])
amt = st.number_input("Amount (in unit)", min_value=0.0, step=0.1, key="log_amt")
if st.button("Add to Log", key="add_log_button"):
    st.session_state.log.append({"id": st.session_state.next_id, "Item": choice, "Amount": amt})
    st.session_state.next_id += 1

# --- Display and Manage Log ---
if st.session_state.log:
    log_df = pd.DataFrame(st.session_state.log)
    def adjust(val, unit): return val/100 if unit=="100g" else val
    n_df = log_df.merge(foods_df, on="Item")
    for m in ["P","F","C","Fiber"]:
        n_df[f"{m}_g"] = n_df.apply(lambda r: adjust(r[f"{m}/unit"]*r["Amount"], r["unit"]), axis=1)
    n_df.rename(columns={"P_g":"Protein_g","F_g":"Fat_g","C_g":"Carbs_g","Fiber_g":"Fiber_g"}, inplace=True)
    n_df["Net_Carbs_g"] = n_df["Carbs_g"] - n_df["Fiber_g"]
    n_df["Calories"] = n_df["Protein_g"]*4 + n_df["Fat_g"]*9 + n_df["Net_Carbs_g"]*4

    st.subheader("📝 Current Log")
    st.dataframe(n_df[["id","Item","Amount","unit","Protein_g","Fat_g","Net_Carbs_g","Fiber_g","Calories"]])

    sel = st.selectbox("Select ID to delete", options=n_df["id"].tolist(), key="del_id")
    if st.button("Delete Entry", key="del_entry_button"):
        st.session_state.log = [e for e in st.session_state.log if e["id"]!=sel]
    # Reset log under delete
    if st.button("Reset Log", key="reset_log_button"):
        st.session_state.log = []
        st.session_state.next_id = 1

    tot = n_df[["Protein_g","Fat_g","Net_Carbs_g","Fiber_g","Calories"]].sum()
    rem = pd.Series({"Protein_g": max(0, protein_goal - tot["Protein_g"]), "Fat_g": max(0, fat_goal - tot["Fat_g"]), "Net_Carbs_g": max(0, carb_goal - tot["Net Carbs_g"]), "Fiber_g": "-", "Calories": max(0, cal_goal - tot["Calories"])})
