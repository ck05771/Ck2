import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

# ── Global CSS: Warm Earthy Professional ──────────────────────────────────────
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* Root variables — blue palette */
:root {
    --bg:            #EEF3FB;
    --bg-alt:        #E0EAF7;
    --surface:       #F5F8FF;
    --surface-2:     #E8F0FA;
    --border:        #C5D5EE;
    --border-strong: #A0BADE;
    --text-primary:  #1A3A6E;
    --text-secondary:#3B68B0;
    --accent:        #1D5CC8;
    --accent-light:  #DDEAFC;
    --accent-2:      #2B8AC4;
    --success:       #1A6E50;
    --warning:       #A06010;
    --danger:        #A83232;
    --radius:        12px;
    --shadow:        0 2px 12px rgba(26,58,110,0.10);
}

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

.stApp { background: var(--bg); }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3.5rem 4rem 3.5rem;
    max-width: 1240px;
}

/* Title area — editorial serif display */
h1 {
    font-family: 'Instrument Serif', Georgia, serif !important;
    font-size: 2rem !important;
    font-weight: 400 !important;
    letter-spacing: -0.01em;
    color: var(--text-primary) !important;
    margin-bottom: 0.1rem !important;
    line-height: 1.2 !important;
}

h2 {
    font-family: 'Instrument Serif', Georgia, serif !important;
    font-size: 1.35rem !important;
    font-weight: 400 !important;
    letter-spacing: -0.01em;
    color: var(--text-primary) !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0.5rem !important;
    margin-bottom: 1.2rem !important;
}

h3 {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: 0.01em;
}

/* Sidebar — warm toned */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 0.84rem;
    color: var(--text-secondary);
    padding: 0.45rem 0;
    transition: color 0.15s;
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--accent) !important;
}

/* Metric cards — warm shadow */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.4rem !important;
    box-shadow: var(--shadow);
    border-top: 3px solid var(--accent) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.7rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
[data-testid="stMetricValue"] {
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 2rem;
    font-weight: 400;
    color: var(--accent);
}
[data-testid="stMetricDelta"] { font-size: 0.8rem; }

/* Tables */
[data-testid="stTable"] table, .stDataFrame table {
    font-size: 0.82rem;
    border-collapse: collapse;
    width: 100%;
    background: var(--surface);
    border-radius: var(--radius);
    overflow: hidden;
}

[data-testid="stTable"] thead th, .stDataFrame thead th {
    background: var(--bg-alt) !important;
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.7rem 1rem !important;
    border-bottom: 2px solid var(--border-strong) !important;
}

[data-testid="stTable"] tbody td, .stDataFrame tbody td {
    padding: 0.6rem 1rem !important;
    border-bottom: 1px solid var(--border) !important;
    color: var(--text-primary);
    font-family: 'DM Mono', monospace;
    font-size: 0.79rem;
    background: var(--surface);
}

[data-testid="stTable"] tbody tr:nth-child(even) td,
.stDataFrame tbody tr:nth-child(even) td {
    background: var(--surface-2) !important;
}

[data-testid="stTable"] tbody tr:hover td,
.stDataFrame tbody tr:hover td {
    background: var(--accent-light) !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent);
    color: #FAF7F4;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.3rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.18s ease;
    letter-spacing: 0.02em;
    box-shadow: 0 1px 4px rgba(29,92,200,0.3);
}
.stButton > button:hover {
    background: #154FA8;
    box-shadow: 0 3px 12px rgba(29,92,200,0.35);
    transform: translateY(-1px);
}

/* Alerts */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: var(--radius) !important;
    font-size: 0.84rem !important;
}
.stSuccess { border-left: 4px solid var(--success) !important;  background: #EDF5F0 !important; border: 1px solid #C4DDD0 !important; }
.stInfo    { border-left: 4px solid var(--accent) !important;   background: var(--accent-light) !important; border: 1px solid #E0C9B5 !important; }
.stWarning { border-left: 4px solid var(--warning) !important;  background: #FDF5DC !important; border: 1px solid #E8D68A !important; }
.stError   { border-left: 4px solid var(--danger) !important;   background: #FAEAEA !important; border: 1px solid #E0B0B0 !important; }

/* Expander */
details {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 0.3rem 0.5rem !important;
    background: var(--surface);
    box-shadow: var(--shadow);
}
summary { font-size: 0.85rem; font-weight: 600; color: var(--text-primary); }

/* Divider */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* Forms */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    border: 1px solid var(--border-strong) !important;
    border-radius: 8px !important;
    font-size: 0.84rem !important;
    font-family: 'DM Sans', sans-serif !important;
    background: var(--surface) !important;
    color: var(--text-primary) !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(29,92,200,0.12) !important;
}

/* Section header stripe */
.section-badge {
    display: inline-block;
    background: var(--accent);
    color: #FAF7F4;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Matplotlib style ──────────────────────────────────────────────────────────
PALETTE = ["#1D5CC8", "#2B8AC4", "#3BA8D8", "#A83232", "#5A72D0", "#0E9E8A"]
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DM Sans", "Helvetica Neue", "Arial"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": True,
    "axes.grid": True,
    "grid.color": "#C5D5EE",
    "grid.linewidth": 0.7,
    "grid.alpha": 0.7,
    "axes.facecolor": "#F5F8FF",
    "figure.facecolor": "#F5F8FF",
    "axes.labelcolor": "#3B68B0",
    "xtick.color": "#3B68B0",
    "ytick.color": "#3B68B0",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.titlesize": 12,
    "axes.titleweight": "600",
    "axes.titlepad": 16,
    "axes.edgecolor": "#C5D5EE",
    "figure.dpi": 120,
})

# ── Data ──────────────────────────────────────────────────────────────────────
def load_data():
    file_path = 'sales_data.csv'
    if not os.path.exists(file_path):
        initial_data = pd.DataFrame({
            "Date": ["2023-01-15", "2023-01-20"],
            "Product_ID": ["P001", "P002"],
            "Product Name": ["Laptop", "Mouse"],
            "Category": ["IT", "IT"],
            "Quantity": [10, 50],
            "Unit Price": [25000, 500],
            "Region": ["North", "South"]
        })
        initial_data.to_csv(file_path, index=False)
    return pd.read_csv(file_path)

df = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.2rem;"><span style="background:#1D5CC8;color:#F5F8FF;font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:0.2rem 0.55rem;border-radius:4px;">Dashboard</span></div>', unsafe_allow_html=True)
st.title("Sales Analytics")
st.markdown('<p style="color:#3B68B0;font-size:0.88rem;margin-top:-0.3rem;margin-bottom:1.5rem;border-bottom:1px solid #C5D5EE;padding-bottom:1.2rem;">โครงการทดสอบสมรรถนะรายปี · อาชีพนักวิเคราะห์ข้อมูล</p>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown('<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#3B68B0;font-weight:500;margin-bottom:0.5rem;">เมนูหลัก</p>', unsafe_allow_html=True)
menu = st.sidebar.radio("", [
    "0. จัดการข้อมูล (เพิ่ม/ลบ)",
    "1. ตรวจสอบคุณภาพข้อมูล",
    "2. ทำความสะอาดข้อมูล",
    "3. วิเคราะห์ข้อมูล",
    "4. ความปลอดภัยข้อมูล",
    "5. การแสดงผลข้อมูล (Visualization)"
], label_visibility="collapsed")

# ── Section 0: Manage Data ────────────────────────────────────────────────────
if menu == "0. จัดการข้อมูล (เพิ่ม/ลบ)":
    st.subheader("จัดการฐานข้อมูล")

    with st.expander("➕  เพิ่มข้อมูลยอดขายใหม่"):
        with st.form("add_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            new_date  = c1.date_input("วันที่ขาย")
            new_id    = c2.text_input("รหัสสินค้า")
            new_name  = c3.text_input("ชื่อสินค้า")
            new_cat   = c1.selectbox("หมวดหมู่", ["IT", "Furniture", "Electronics"])
            new_qty   = c2.number_input("จำนวน", min_value=1)
            new_price = c3.number_input("ราคาต่อหน่วย", min_value=1)
            new_reg   = c1.selectbox("ภูมิภาค", ["North", "South", "Central", "East", "West"])
            if st.form_submit_button("บันทึกข้อมูล"):
                new_row = pd.DataFrame([[str(new_date), new_id, new_name, new_cat, new_qty, new_price, new_reg]],
                                       columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv('sales_data.csv', index=False)
                st.success("บันทึกข้อมูลสำเร็จ!")
                st.rerun()

    with st.expander("🗑️  ลบข้อมูลที่ไม่ต้องการ"):
        st.dataframe(df, use_container_width=True)
        delete_idx = st.number_input("ระบุเลขลำดับที่ต้องการลบ", min_value=0, max_value=len(df)-1, step=1)
        if st.button("ยืนยันการลบ"):
            df = df.drop(df.index[delete_idx])
            df.to_csv('sales_data.csv', index=False)
            st.warning("ลบข้อมูลเรียบร้อยแล้ว")
            st.rerun()

# ── Section 1: Quality Check ──────────────────────────────────────────────────
elif menu == "1. ตรวจสอบคุณภาพข้อมูล":
    st.subheader("ตรวจสอบคุณภาพข้อมูล")

    if st.button("เริ่มตรวจสอบ"):
        # Missing values
        st.markdown("**Missing Values**")
        null_rows = df[df.isnull().any(axis=1)]
        if not null_rows.empty:
            st.error(f"พบข้อมูลไม่สมบูรณ์ {len(null_rows)} แถว")
            st.dataframe(null_rows, use_container_width=True)
        else:
            st.success("ข้อมูลทุกแถวครบถ้วน")

        st.divider()

        # Duplicates
        st.markdown("**ข้อมูลซ้ำ (Duplicates)**")
        dup_rows = df[df.duplicated(keep=False)]
        if not dup_rows.empty:
            st.warning(f"พบข้อมูลซ้ำ {len(df[df.duplicated()])} รายการ")
            st.dataframe(dup_rows.sort_values(by=list(df.columns)), use_container_width=True)
        else:
            st.success("ไม่พบข้อมูลซ้ำ")

        st.divider()

        # Data types
        st.markdown("**ชนิดข้อมูลรายช่อง**")
        def check_type(v): return type(v).__name__
        st.dataframe(df.applymap(check_type), use_container_width=True)
        st.info("หากคอลัมน์ตัวเลขแสดงผลเป็น `str` แสดงว่าแถวนั้นมีชนิดข้อมูลผิดพลาด")

# ── Section 2: Data Cleaning ──────────────────────────────────────────────────
elif menu == "2. ทำความสะอาดข้อมูล":
    st.subheader("ทำความสะอาดข้อมูล")
    st.info("เกณฑ์: ลบซ้ำ · กรองค่าติดลบ · แปลงรูปแบบวันที่")

    if st.button("เริ่มทำความสะอาด"):
        df_before = df.copy()

        dup_rows          = df_before[df_before.duplicated()]
        df_clean          = df_before.drop_duplicates()
        wrong_fmt         = df_clean[(df_clean['Quantity'] <= 0) | (df_clean['Unit Price'] <= 0)]
        df_clean          = df_clean[(df_clean['Quantity'] > 0) & (df_clean['Unit Price'] > 0)]
        invalid_date_rows = df_clean[pd.to_datetime(df_clean['Date'], errors='coerce').isna()]
        df_clean['Date']  = pd.to_datetime(df_clean['Date'], errors='coerce')
        df_clean          = df_clean.dropna(subset=['Date'])

        st.session_state['df_clean'] = df_clean
        st.success("ทำความสะอาดเสร็จสิ้น")

        c1, c2, c3 = st.columns(3)
        c1.metric("ข้อมูลซ้ำที่ลบ",         f"{len(dup_rows)} แถว")
        c2.metric("ข้อมูลผิดรูปแบบที่ลบ",   f"{len(wrong_fmt)} แถว")
        c3.metric("วันที่ผิดพลาดที่ลบ",      f"{len(invalid_date_rows)} แถว")

        with st.expander("รายละเอียดรายการที่ถูกลบ"):
            if not dup_rows.empty:
                st.markdown("**ข้อมูลซ้ำ:**"); st.dataframe(dup_rows, use_container_width=True)
            if not wrong_fmt.empty:
                st.markdown("**จำนวน/ราคาติดลบ:**"); st.dataframe(wrong_fmt, use_container_width=True)
            if not invalid_date_rows.empty:
                st.markdown("**วันที่ผิดรูปแบบ:**"); st.dataframe(invalid_date_rows, use_container_width=True)

        st.markdown("**ข้อมูลที่พร้อมใช้งาน**")
        st.dataframe(df_clean, use_container_width=True)

# ── Section 3: Analysis ───────────────────────────────────────────────────────
elif menu == "3. วิเคราะห์ข้อมูล":
    st.subheader("วิเคราะห์ข้อมูลเพื่อหาข้อสรุปเชิงธุรกิจ")

    if 'df_clean' in st.session_state:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = data['Quantity'] * data['Unit Price']

        st.markdown("**ยอดขายรวมต่อเดือน**")
        data['Month']    = data['Date'].dt.to_period('M').astype(str)
        monthly_sales    = data.groupby('Month')['Total_Sales'].sum().reset_index()
        st.table(monthly_sales)

        st.divider()

        st.markdown("**สินค้าขายดีที่สุด 5 อันดับ**")
        top_products = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()
        st.table(top_products)

        st.divider()

        st.markdown("**ยอดขายตามภูมิภาค**")
        region_sales = data.groupby('Region')['Total_Sales'].sum().reset_index()
        st.table(region_sales)

        st.divider()

        best_region  = region_sales.loc[region_sales['Total_Sales'].idxmax(), 'Region']
        best_product = top_products.loc[0, 'Product Name']
        st.success(f"""**ข้อเสนอแนะเชิงธุรกิจ:**  
- ควรทำโปรโมชั่นพ่วงสำหรับ **{best_product}** (สินค้าขายดีอันดับ 1)  
- ทุ่มงบโฆษณาในภูมิภาค **{best_region}** (ยอดซื้อสูงสุด)  
- เตรียมสต็อกล่วงหน้า 1 เดือนตามแนวโน้มรายเดือน""")
    else:
        st.warning("กรุณาดำเนินการ 'ทำความสะอาดข้อมูล' ในขั้นตอนที่ 2 ก่อน")

# ── Section 4: Security ───────────────────────────────────────────────────────
elif menu == "4. ความปลอดภัยข้อมูล":
    st.subheader("ออกแบบความปลอดภัยข้อมูล")

    st.markdown("**การกำหนดสิทธิ์ (RBAC)**")
    st.table(pd.DataFrame([
        {"บทบาท": "Admin (ไอที)",          "สิทธิ์": "ดู / เพิ่ม / แก้ไข / ลบ / จัดการผู้ใช้",  "ระดับ": "สูงสุด"},
        {"บทบาท": "Analyst (นักวิเคราะห์)", "สิทธิ์": "ดูข้อมูล ทำความสะอาด วิเคราะห์",          "ระดับ": "ปานกลาง"},
        {"บทบาท": "Viewer (ผู้บริหาร)",    "สิทธิ์": "ดูรายงานสรุปและ Dashboard เท่านั้น",       "ระดับ": "เริ่มต้น"},
    ]))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.info("**การป้องกันเชิงเทคนิค**\n\n- **Encryption** เข้ารหัสไฟล์ขณะจัดเก็บ\n- **MFA** ยืนยันตัวตน 2 ชั้น\n- **Audit Logs** บันทึกทุกกิจกรรม")
    with col2:
        st.info("**การป้องกันเชิงบริหาร**\n\n- **NDA** สัญญาไม่เปิดเผยข้อมูล\n- **Privacy Policy** สอดคล้อง PDPA\n- **Training** อบรม Cyber Security")

    st.success("แนวทางนี้สอดคล้องกับมาตรฐานความปลอดภัยข้อมูลระดับ 4")

# ── Section 5: Visualization ──────────────────────────────────────────────────
elif menu == "5. การแสดงผลข้อมูล (Visualization)":
    st.subheader("การแสดงผลข้อมูล")

    if 'df_clean' in st.session_state:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = data['Quantity'] * data['Unit Price']
        data['Month']       = data['Date'].dt.to_period('M').astype(str)

        # ── Line chart ────────────────────────────────────────────────────────
        st.markdown("**แนวโน้มยอดขายรายเดือน**")
        monthly_trend = data.groupby('Month')['Total_Sales'].sum().reset_index()

        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(monthly_trend['Month'], monthly_trend['Total_Sales'],
                 color=PALETTE[0], linewidth=2.5, marker='o',
                 markersize=7, markerfacecolor='#F5F8FF',
                 markeredgewidth=2.5, markeredgecolor=PALETTE[0], zorder=5)
        ax1.fill_between(monthly_trend['Month'], monthly_trend['Total_Sales'],
                         alpha=0.12, color=PALETTE[0])
        ax1.set_title("Monthly Sales Trend", loc='left', color='#1A3A6E')
        ax1.set_ylabel("Sales (Baht)", labelpad=12)
        ax1.set_xlabel("")
        ax1.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        fig1.patch.set_facecolor('#F5F8FF')
        ax1.set_facecolor('#F5F8FF')
        plt.tight_layout(pad=1.5)
        st.pyplot(fig1, use_container_width=True)

        st.divider()

        # ── Bar chart ─────────────────────────────────────────────────────────
        st.markdown("**ยอดขายตามภูมิภาค**")
        region_comp = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        bar_colors = [PALETTE[1]] + [PALETTE[0]] * (len(region_comp) - 1)
        bars = ax2.bar(region_comp['Region'], region_comp['Total_Sales'],
                       color=bar_colors, width=0.52, zorder=3,
                       edgecolor='#F5F8FF', linewidth=0.8)
        ax2.set_title("Sales by Region", loc='left', color='#1A3A6E')
        ax2.set_ylabel("Total Sales (Baht)", labelpad=12)
        ax2.set_xlabel("")
        ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        for bar in bars:
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.025,
                     f"{bar.get_height():,.0f}", ha='center', va='bottom',
                     fontsize=8.5, color='#3B68B0', fontweight='600')
        fig2.patch.set_facecolor('#F5F8FF')
        ax2.set_facecolor('#F5F8FF')
        plt.tight_layout(pad=1.5)
        st.pyplot(fig2, use_container_width=True)

        st.divider()

        best_region  = region_comp.loc[0, 'Region']
        best_product = data.groupby('Product Name')['Quantity'].sum().idxmax()
        st.success(f"""**Executive Summary**  
- แนวโน้มรายเดือน: วิเคราะห์จากกราฟเส้นด้านบน  
- ภูมิภาคหลัก: **{best_region}** มียอดขายสูงสุด (แท่งสีเขียว)  
- แผนงานถัดไป: จัดโปรโมชั่น **{best_product}** ในช่วง Peak Month""")
    else:
        st.warning("กรุณาดำเนินการ 'ทำความสะอาดข้อมูล' ในขั้นตอนที่ 2 ก่อน")