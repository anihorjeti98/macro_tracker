import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Streamlit page config ---
st.set_page_config(page_title="Macro Tracker", layout="centered")
st.title("🍽️ Lean Bulk Macro Tracker")

# --- Base food macro data with explicit unit field ---
base_foods = [
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

# --- Session state ---
if "custom_foods" not in st.session_state:
    st.session_state.custom_foods = []
if "log" not in st.session_state:
    st.session_state.log = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

# --- Combine foods ---
foods_df = pd.DataFrame(base_foods + st.session_state.custom_foods)

# --- Sidebar: Custom food entry ---
st.sidebar.header("➕ Add Custom Food")
with st.sidebar.expander("Custom Food Entry", expanded=False):
    new_name = st.text_input("Food Name")
    new_unit = st.selectbox("Unit", ["100g", "g", "pc", "tbsp", "cup", "oz"], key="new_unit")
    new_p = st.number_input("Protein per unit (g)", min_value=0.0, key="new_p")
    new_f = st.number_input("Fat per unit (g)", min_value=0.0, key="new_f")
    new_c = st.number_input("Carbs per unit (g)", min_value=0.0, key="new_c")
    new_fiber = st.number_input("Fiber per unit (g)", min_value=0.0, key="new_fiber")
    if st.button("Add Food to Menu"):
        st.session_state.custom_foods.append({
            "Item": new_name,
            "unit": new_unit,
            "P/unit": new_p,
            "F/unit": new_f,
            "C/unit": new_c,
            "Fiber/unit": new_fiber
        })
        st.experimental_rerun()

# --- Sidebar: Macro Goals and Reset Logs ---
st.sidebar.header("🎯 Daily Macro Goals")
cal_goal = st.sidebar.number_input("Calories", min_value=0, value=1600)
protein_goal = st.sidebar.number_input("Protein (g)", min_value=0, value=180)
fat_goal = st.sidebar.number_input("Fat (g)", min_value=0, value=44)
carb_goal = st.sidebar.number_input("Net Carbs (g)", min_value=0, value=121)
if st.sidebar.button("Reset Log"):
    st.session_state.log = []
    st.session_state.next_id = 1
    st.experimental_rerun()

# --- Macro Reference Table ---
st.subheader("📋 Macro Content per Unit")
ref_df = foods_df.copy()
ref_df["Net Carbs/unit"] = ref_df["C/unit"] - ref_df["Fiber/unit"]
ref_df["Calories per unit"] = (
    ref_df["P/unit"]*4 + ref_df["F/unit"]*9 + ref_df["Net Carbs/unit"]*4
)
st.dataframe(ref_df.rename(columns={
    "Item": "Food", "unit":"Unit",
    "P/unit":"Protein (g)", "F/unit":"Fat (g)",
    "C/unit":"Carbs (g)", "Fiber/unit":"Fiber (g)",
    "Net Carbs/unit":"Net Carbs (g)",
    "Calories per unit":"Calories per unit"
})[["Food","Unit","Protein (g)","Fat (g)","Carbs (g)","Fiber (g)","Net Carbs (g)","Calories per unit"]])

# --- Log Input ---
st.subheader("➕ Log a Food Item")
choice = st.selectbox("Food", foods_df["Item"])
amt = st.number_input("Amount (in unit)", min_value=0.0, step=0.1)
if st.button("Add to Log"):
    st.session_state.log.append({"id": st.session_state.next_id, "Item": choice, "Amount": amt})
    st.session_state.next_id += 1
    st.experimental_rerun()

# --- Display and Manage Log ---
log_df = pd.DataFrame(st.session_state.log)
if not log_df.empty:
    def adjust(val, unit):
        return val/100 if unit=="100g" else val
    n_df = log_df.merge(foods_df, on="Item")
    for m in ["P","F","C","Fiber"]:
        n_df[f"{m}_g"] = n_df.apply(lambda r: adjust(r[f"{m}/unit"]*r["Amount"], r["unit"]), axis=1)
    n_df.rename(columns={"P_g":"Protein_g","F_g":"Fat_g","C_g":"Carbs_g","Fiber_g":"Fiber_g"}, inplace=True)
    n_df["Net_Carbs_g"] = n_df["Carbs_g"] - n_df["Fiber_g"]
    n_df["Calories"] = n_df["Protein_g"]*4 + n_df["Fat_g"]*9 + n_df["Net_Carbs_g"]*4

    st.subheader("📝 Current Log")
    st.dataframe(n_df[["id","Item","Amount","unit","Protein_g","Fat_g","Net_Carbs_g","Fiber_g","Calories"]])

    sel = st.selectbox("Select ID to delete", options=n_df["id"].tolist())
    if st.button("Delete Entry"):
        st.session_state.log = [e for e in st.session_state.log if e["id"]!=sel]
        st.experimental_rerun()

    tot = n_df[["Protein_g","Fat_g","Net_Carbs_g","Fiber_g","Calories"]].sum()
    rem = pd.Series({
        "Protein_g":max(0, protein_goal-tot["Protein_g"]),
        "Fat_g":max(0, fat_goal-tot["Fat_g"]),
        "Net_Carbs_g":max(0, carb_goal-tot["Net_Carbs_g"]),
        "Fiber_g":"-",
        "Calories":max(0, cal_goal-tot["Calories"])
    })
    st.subheader("✅ Progress vs Goal")
    progress_df = pd.DataFrame({"Goal":[protein_goal,fat_goal,carb_goal,"-",cal_goal],"Consumed":tot,"Remaining":rem},
                               index=["Protein_g","Fat_g","Net_Carbs_g","Fiber_g","Calories"])
    st.dataframe(progress_df)

    pie = pd.Series({"Protein":tot["Protein_g"]*4,"Fat":tot["Fat_g"]*9,"Net Carbs":tot["Net_Carbs_g"]*4})
    st.subheader("🍰 Macro Breakdown")
    fig,ax = plt.subplots()
    ax.pie(pie, labels=pie.index, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)
else:
    st.info("Add some food to begin tracking.")
