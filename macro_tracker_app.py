import streamlit as st
import pandas as pd

# --- Streamlit page config ---
st.set_page_config(page_title="Macro Tracker", layout="centered")
st.title("🍽️ Lean Bulk Macro Tracker")

# --- Define macro goal presets based on weekly plan ---
presets = [
    {"Week":"Week 1",               "Dates":"Jun 24–30",       "Calories":1650, "Protein (g)":180, "Fat (g)":44, "Net Carbs (g)":125},
    {"Week":"Week 2",               "Dates":"Jul 1–7",         "Calories":1750, "Protein (g)":180, "Fat (g)":48, "Net Carbs (g)":130},
    {"Week":"Week 3",               "Dates":"Jul 8–14",        "Calories":1850, "Protein (g)":185, "Fat (g)":50, "Net Carbs (g)":137},
    {"Week":"Week 4",               "Dates":"Jul 15–21",       "Calories":1950, "Protein (g)":185, "Fat (g)":52, "Net Carbs (g)":145},
    {"Week":"Week 5",               "Dates":"Jul 22–28",       "Calories":2050, "Protein (g)":190, "Fat (g)":55, "Net Carbs (g)":152},
    {"Week":"Week 6",               "Dates":"Jul 29–Aug 4",    "Calories":2150, "Protein (g)":190, "Fat (g)":57, "Net Carbs (g)":160},
    {"Week":"Week 7",               "Dates":"Aug 5–11",        "Calories":2250, "Protein (g)":190, "Fat (g)":60, "Net Carbs (g)":167},
    {"Week":"Final Push (Week 8)",  "Dates":"Aug 12–18 (peak)","Calories":2300, "Protein (g)":190, "Fat (g)":62, "Net Carbs (g)":174},
    {"Week":"Custom",               "Dates":"-",               "Calories":None, "Protein (g)":None,"Fat (g)":None,"Net Carbs (g)":None}
]
presets_df = pd.DataFrame(presets).set_index("Week")

# --- Always-visible week selector ---
plan = st.selectbox(
    "Select your macro goal week:",
    presets_df.index.tolist(),
    index=1  # default = Week 2 (Jul 1–7)
)
selected = presets_df.loc[plan]
if plan == "Custom":
    st.subheader("➤ Enter Custom Macro Goals")
    cal_goal     = st.number_input("Calories",      min_value=0, value=1600)
    protein_goal = st.number_input("Protein (g)",   min_value=0, value=180)
    fat_goal     = st.number_input("Fat (g)",       min_value=0, value=44)
    carb_goal    = st.number_input("Net Carbs (g)", min_value=0, value=121)
else:
    cal_goal     = int(selected["Calories"])
    protein_goal = int(selected["Protein (g)"])
    fat_goal     = int(selected["Fat (g)"])
    carb_goal    = int(selected["Net Carbs (g)"])
    st.markdown(
        f"**Selected {plan} ({selected['Dates']})**:<br>"
        f"{cal_goal} kcal, {protein_goal}g P, {fat_goal}g F, {carb_goal}g C",
        unsafe_allow_html=True
    )

# --- Base foods (all units now 100g or explicit) ---
base_foods = [

    {"Item": "Fairlife Shake",               "unit": "bottle", "P/unit": 30,   "F/unit": 2.5,  "C/unit": 4,    "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Whole Egg",                    "unit": "egg",    "P/unit": 6,    "F/unit": 5,    "C/unit": 0.5,  "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Olive Oil",                    "unit": "tbsp",   "P/unit": 0,    "F/unit": 14,   "C/unit": 0,    "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Feta Cheese",                  "unit": "100g",   "P/unit": 14,   "F/unit": 21,   "C/unit": 4,    "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Banana",                       "unit": "100g",   "P/unit": 1.1,  "F/unit": 0.3,  "C/unit": 23,   "Fiber/unit": 2.6, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Strawberries",                 "unit": "100g",   "P/unit": 0.5,  "F/unit": 0.2,  "C/unit": 6,    "Fiber/unit": 2.0, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Blueberries",                  "unit": "100g",   "P/unit": 0.7,  "F/unit": 0.3,  "C/unit": 14,   "Fiber/unit": 2.5, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Blackberries",                 "unit": "100g",   "P/unit": 1.4,  "F/unit": 0.5,  "C/unit": 10,   "Fiber/unit": 5.0, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Cracker",                      "unit": "pc",     "P/unit": 0.2,  "F/unit": 0.4,  "C/unit": 2.2,  "Fiber/unit": 0.2, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Honey",                        "unit": "tbsp",   "P/unit": 0.1,  "F/unit": 0,    "C/unit": 17,   "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Cherries",                     "unit": "100g",   "P/unit": 1.06, "F/unit": 0.2,  "C/unit": 16,   "Fiber/unit": 2.1, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Triscuit",                     "unit": "pc",     "P/unit": 0.2,  "F/unit": 0.4,  "C/unit": 2.2,  "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Michelob Ultra",               "unit": "can",    "P/unit": 0.6,  "F/unit": 0,    "C/unit": 2.6,  "Fiber/unit": 0,   "Alc/unit": 12, "Cal/unit": 95},
    {"Item": "Dry Pasta",                    "unit": "100g",   "P/unit": 12.5, "F/unit": 1.8,  "C/unit": 75.0, "Fiber/unit": 5.4, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Yogurt",                       "unit": "100g",   "P/unit": 10.6, "F/unit": 0,    "C/unit": 2.9,  "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Tomato",                       "unit": "100g",   "P/unit": 0.9,  "F/unit": 0.2,  "C/unit": 3.9,  "Fiber/unit": 1.2, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Chicken Breast (raw)",         "unit": "100g",   "P/unit": 22.5, "F/unit": 2.6,  "C/unit": 0,    "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Chicken Thigh (raw)",          "unit": "100g",   "P/unit": 18.6, "F/unit": 7.9,  "C/unit": 0,    "Fiber/unit": 0,   "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Almonds",                      "unit": "100g",   "P/unit": 21,   "F/unit": 50,   "C/unit": 22,   "Fiber/unit": 13,  "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Pistachios (shelled)",         "unit": "100g",   "P/unit": 20,   "F/unit": 45,   "C/unit": 28,   "Fiber/unit": 10.3,"Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Pistachios (unshelled)",       "unit": "100g",   "P/unit": 9.8,  "F/unit": 22.1, "C/unit": 13.7, "Fiber/unit": 5.1, "Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Cucumber (raw, with peel)",    "unit": "100g",   "P/unit": 0.68, "F/unit": 0.11, "C/unit": 3.8,  "Fiber/unit": 0.52,"Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Romaine Lettuce (raw)",        "unit": "100g",   "P/unit": 1.18, "F/unit": 0,    "C/unit": 2.35, "Fiber/unit": 1.20,"Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Spring Mix (mesclun)",         "unit": "100g",   "P/unit": 2.35, "F/unit": 0,    "C/unit": 3.53, "Fiber/unit": 2.35,"Alc/unit": 0,  "Cal/unit": None},
    {"Item": "Avocado (flesh, raw)",         "unit": "100g",   "P/unit": 2,    "F/unit": 14.66,"C/unit": 8.53, "Fiber/unit": 6.7, "Alc/unit": 0,  "Cal/unit": None},


]

# --- Session state init ---
if "custom_foods" not in st.session_state: st.session_state.custom_foods = []
if "log"         not in st.session_state: st.session_state.log = []
if "next_id"     not in st.session_state: st.session_state.next_id = 1

foods_df = pd.DataFrame(base_foods + st.session_state.custom_foods)

# --- Macro Reference Table ---
st.subheader("📋 Macro Content per Unit")
ref_df = foods_df.copy()
ref_df["Net Carbs/unit"] = ref_df["C/unit"] - ref_df["Fiber/unit"]

def compute_cal_per_unit(r):
    if pd.notna(r["Cal/unit"]):
        return r["Cal/unit"]
    return r["P/unit"]*4 + r["F/unit"]*9 + r["Net Carbs/unit"]*4 + r["Alc/unit"]*7

ref_df["Calories per unit"] = ref_df.apply(compute_cal_per_unit, axis=1)

st.dataframe(
    ref_df.rename(columns={
        "Item":"Food", "unit":"Unit", "P/unit":"Protein (g)",
        "F/unit":"Fat (g)", "C/unit":"Carbs (g)", "Fiber/unit":"Fiber (g)",
        "Net Carbs/unit":"Net Carbs (g)", "Alc/unit":"Alcohol (g)",
        "Calories per unit":"Calories per unit"
    })[
        ["Food","Unit","Protein (g)","Fat (g)","Carbs (g)",
         "Fiber (g)","Net Carbs (g)","Alcohol (g)","Calories per unit"]
    ]
)

# --- Add Custom Food to Menu ---
st.subheader("➕ Add a Custom Food to Menu")
with st.form("menu_form", clear_on_submit=True):
    name    = st.text_input("Food Name", key="menu_name")
    unit    = st.selectbox("Unit", ["100g","g","pc","tbsp","cup","oz","can"], key="menu_unit")
    p       = st.number_input("Protein per unit (g)", min_value=0.0, key="menu_p")
    f       = st.number_input("Fat per unit (g)",     min_value=0.0, key="menu_f")
    c       = st.number_input("Carbs per unit (g)",   min_value=0.0, key="menu_c")
    fiber   = st.number_input("Fiber per unit (g)",   min_value=0.0, key="menu_fiber")
    alc     = st.number_input("Alcohol per unit (g)", min_value=0.0, key="menu_alc")
    cal_man = st.number_input("Calories per unit (label)", min_value=0.0, key="menu_cal")
    if st.form_submit_button("Add to Menu"):
        st.session_state.custom_foods.append({
            "Item":       name,
            "unit":       unit,
            "P/unit":     p,
            "F/unit":     f,
            "C/unit":     c,
            "Fiber/unit": fiber,
            "Alc/unit":   alc,
            "Cal/unit":   (cal_man if cal_man > 0 else None)
        })

# --- Log a Food Item ---
st.subheader("➕ Log a Food Item")
with st.form("log_form", clear_on_submit=True):
    choice = st.selectbox("Food to Log", foods_df["Item"], key="log_choice")
    amt    = st.number_input("Amount (in unit)", min_value=0.0, step=0.1, key="log_amt")
    if st.form_submit_button("Add to Log"):
        st.session_state.log.append({
            "id":     st.session_state.next_id,
            "Item":   choice,
            "Amount": amt
        })
        st.session_state.next_id += 1

# --- Display & Manage Log ---
if st.session_state.log:
    log_df = pd.DataFrame(st.session_state.log)

    def adjust(val, unit):
        return val/100 if unit == "100g" else val

    n_df = log_df.merge(foods_df, on="Item")
    for m in ["P","F","C","Fiber","Alc"]:
        n_df[f"{m}_g"] = n_df.apply(
            lambda r: adjust(r[f"{m}/unit"] * r["Amount"], r["unit"]), axis=1
        )
    n_df.rename(columns={
        "P_g":"Protein_g","F_g":"Fat_g",
        "C_g":"Carbs_g","Fiber_g":"Fiber_g","Alc_g":"Alcohol_g"
    }, inplace=True)
    n_df["Net_Carbs_g"] = n_df["Carbs_g"] - n_df["Fiber_g"]

    def entry_calories(r):
        if pd.notna(r["Cal/unit"]):
            return r["Cal/unit"] * r["Amount"]
        return r["Protein_g"]*4 + r["Fat_g"]*9 + r["Net_Carbs_g"]*4 + r["Alcohol_g"]*7

    n_df["Calories"] = n_df.apply(entry_calories, axis=1)

    st.subheader("📝 Current Log")
    st.dataframe(n_df[[
        "id","Item","Amount","unit",
        "Protein_g","Fat_g","Net_Carbs_g","Fiber_g","Alcohol_g","Calories"
    ]])

    sel = st.selectbox("Select ID to delete", options=n_df["id"].tolist(), key="del_id")
    if st.button("Delete Entry", key="del_entry_button"):
        st.session_state.log = [e for e in st.session_state.log if e["id"] != sel]
    if st.button("Reset Log", key="reset_log_button"):
        st.session_state.log, st.session_state.next_id = [], 1

    tot = n_df[["Protein_g","Fat_g","Net_Carbs_g","Calories"]].sum()
    rem = pd.Series({
        "Protein_g":   max(0, protein_goal   - tot["Protein_g"]),
        "Fat_g":       max(0, fat_goal       - tot["Fat_g"]),
        "Net_Carbs_g": max(0, carb_goal      - tot["Net_Carbs_g"]),
        "Calories":    max(0, cal_goal       - tot["Calories"])
    })
    st.subheader("✅ Progress vs Goal")
    progress_df = pd.DataFrame({
        "Goal":      [protein_goal, fat_goal, carb_goal, cal_goal],
        "Consumed":  [tot["Protein_g"], tot["Fat_g"], tot["Net_Carbs_g"], tot["Calories"]],
        "Remaining": [rem["Protein_g"],  rem["Fat_g"],  rem["Net_Carbs_g"],  rem["Calories"]]
    }, index=["Protein_g","Fat_g","Net_Carbs_g","Calories"])
    st.dataframe(progress_df)
else:
    st.info("Add some food to begin tracking.")
