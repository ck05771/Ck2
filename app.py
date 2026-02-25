import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

# ── Global CSS: Dark Navy Professional ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:            #0F1117;
    --bg-alt:        #161920;
    --surface:       #1C2030;
    --surface-2:     #222840;
    --surface-3:     #252B42;
    --border:        #2E3550;
    --border-bright: #3D4670;
    --text-primary:  #E8ECF8;
    --text-secondary:#8892B0;
    --text-muted:    #556080;
    --accent:        #6C8EF5;
    --accent-glow:   rgba(108,142,245,0.15);
    --accent-2:      #52C9A0;
    --accent-3:      #F5A623;
    --success:       #52C9A0;
    --warning:       #F5A623;
    --danger:        #F56C6C;
    --radius:        10px;
    --radius-lg:     16px;
    --shadow:        0 4px 24px rgba(0,0,0,0.4);
    --shadow-sm:     0 2px 8px rgba(0,0,0,0.3);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-primary);
}

.stApp { background: var(--bg) !important; }

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 1300px !important;
}

/* ── Headings ── */
h1 {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    color: var(--text-primary) !important;
    margin-bottom: 0 !important;
    line-height: 1.25 !important;
}
h2 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em !important;
    margin-top: 0 !important;
    margin-bottom: 1.2rem !important;
    padding-bottom: 0.6rem !important;
    border-bottom: 1px solid var(--border) !important;
}
h3 {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-alt) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 1rem !important;
}
[data-testid="stSidebar"] section[data-testid="stSidebarContent"] {
    padding: 1.5rem 1.2rem !important;
}
[data-testid="stSidebar"] .stRadio > div {
    gap: 0.15rem !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.82rem !important;
    color: var(--text-secondary) !important;
    padding: 0.55rem 0.75rem !important;
    border-radius: 8px !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
    display: block !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--text-primary) !important;
    background: var(--surface) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.2rem 1.5rem !important;
    box-shadow: var(--shadow-sm) !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
[data-testid="stMetricLabel"] {
    font-size: 0.68rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

/* ── Tables ── */
[data-testid="stTable"] table, .stDataFrame table {
    font-size: 0.81rem;
    border-collapse: collapse;
    width: 100%;
    background: var(--surface);
}
[data-testid="stTable"] thead th, .stDataFrame thead th {
    background: var(--surface-2) !important;
    color: var(--text-muted) !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    padding: 0.7rem 1rem !important;
    border-bottom: 1px solid var(--border-bright) !important;
    border-top: none !important;
}
[data-testid="stTable"] tbody td, .stDataFrame tbody td {
    padding: 0.6rem 1rem !important;
    border-bottom: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    background: var(--surface) !important;
}
[data-testid="stTable"] tbody tr:nth-child(even) td,
.stDataFrame tbody tr:nth-child(even) td {
    background: var(--surface-3) !important;
}
[data-testid="stTable"] tbody tr:hover td,
.stDataFrame tbody tr:hover td {
    background: var(--accent-glow) !important;
    color: #fff !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0F1117 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.4rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 0 0 0 rgba(108,142,245,0) !important;
}
.stButton > button:hover {
    background: #7FA3FF !important;
    box-shadow: 0 0 20px rgba(108,142,245,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Alerts ── */
.stSuccess { background: rgba(82,201,160,0.1) !important; border: 1px solid rgba(82,201,160,0.3) !important; border-left: 3px solid var(--success) !important; border-radius: var(--radius) !important; color: var(--text-primary) !important; }
.stInfo    { background: var(--accent-glow) !important; border: 1px solid rgba(108,142,245,0.3) !important; border-left: 3px solid var(--accent) !important; border-radius: var(--radius) !important; color: var(--text-primary) !important; }
.stWarning { background: rgba(245,166,35,0.1) !important; border: 1px solid rgba(245,166,35,0.3) !important; border-left: 3px solid var(--warning) !important; border-radius: var(--radius) !important; color: var(--text-primary) !important; }
.stError   { background: rgba(245,108,108,0.1) !important; border: 1px solid rgba(245,108,108,0.3) !important; border-left: 3px solid var(--danger) !important; border-radius: var(--radius) !important; color: var(--text-primary) !important; }

/* ── Expander ── */
details {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
}
summary {
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    padding: 0.4rem 0.2rem !important;
}
summary:hover { color: var(--text-primary) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.8rem 0 !important; }

/* ── Forms ── */
.stTextInput input, .stNumberInput input {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-size: 0.84rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: border-color 0.15s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stDateInput > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}

/* ── Markdown bold ── */
strong { color: var(--accent) !important; }

/* ── Section label ── */
.step-label {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--surface-2);
    border: 1px solid var(--border-bright);
    color: var(--accent);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.18rem 0.65rem;
    border-radius: 999px;
    margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ─────────────────────────────────────────────────────
PALETTE = ["#6C8EF5", "#52C9A0", "#F5A623", "#F56C6C", "#C084FC", "#38BDF8"]
BG_CHART = "#1C2030"
mpl.rcParams.update({
    "font.family":          "sans-serif",
    "font.sans-serif":      ["Plus Jakarta Sans", "Helvetica Neue", "Arial"],
    "axes.spines.top":      False,
    "axes.spines.right":    False,
    "axes.spines.left":     False,
    "axes.spines.bottom":   False,
    "axes.grid":            True,
    "grid.color":           "#2E3550",
    "grid.linewidth":       0.8,
    "grid.alpha":           1.0,
    "axes.facecolor":       BG_CHART,
    "figure.facecolor":     BG_CHART,
    "axes.labelcolor":      "#8892B0",
    "xtick.color":          "#8892B0",
    "ytick.color":          "#8892B0",
    "xtick.labelsize":      9,
    "ytick.labelsize":      9,
    "axes.titlesize":       12,
    "axes.titleweight":     "600",
    "axes.titlepad":        16,
    "axes.edgecolor":       "#2E3550",
    "figure.dpi":           130,
    "text.color":           "#E8ECF8",
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
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.8rem; padding-bottom:1.2rem; border-bottom:1px solid #2E3550;">
  <div>
    <div style="display:inline-flex; align-items:center; gap:0.4rem; background:#222840; border:1px solid #3D4670; color:#6C8EF5; font-size:0.65rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; padding:0.2rem 0.65rem; border-radius:999px; margin-bottom:0.5rem;">
      ● LIVE DASHBOARD
    </div>
    <h1 style="margin:0; padding:0;">Sales Analytics</h1>
    <p style="color:#556080; font-size:0.84rem; margin:0.3rem 0 0 0;">โครงการทดสอบสมรรถนะรายปี · อาชีพนักวิเคราะห์ข้อมูล</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown('<p style="font-size:0.65rem; text-transform:uppercase; letter-spacing:0.12em; color:#556080; font-weight:700; margin-bottom:0.8rem; padding-bottom:0.6rem; border-bottom:1px solid #2E3550;">Navigation</p>', unsafe_allow_html=True)
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
                 markersize=7, markerfacecolor=BG_CHART,
                 markeredgewidth=2.5, markeredgecolor=PALETTE[0], zorder=5)
        ax1.fill_between(monthly_trend['Month'], monthly_trend['Total_Sales'],
                         alpha=0.18, color=PALETTE[0])
        ax1.set_title("Monthly Sales Trend", loc='left', color='#E8ECF8', pad=14)
        ax1.set_ylabel("Sales (Baht)", labelpad=12)
        ax1.set_xlabel("")
        ax1.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        fig1.patch.set_facecolor(BG_CHART)
        ax1.set_facecolor(BG_CHART)
        plt.tight_layout(pad=1.5)
        st.pyplot(fig1, use_container_width=True)

        st.divider()

        # ── Bar chart ─────────────────────────────────────────────────────────
        st.markdown("**ยอดขายตามภูมิภาค**")
        region_comp = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        bar_colors = [PALETTE[1]] + [PALETTE[0]] * (len(region_comp) - 1)
        bars = ax2.bar(region_comp['Region'], region_comp['Total_Sales'],
                       color=bar_colors, width=0.5, zorder=3,
                       edgecolor=BG_CHART, linewidth=1.2)
        ax2.set_title("Sales by Region", loc='left', color='#E8ECF8', pad=14)
        ax2.set_ylabel("Total Sales (Baht)", labelpad=12)
        ax2.set_xlabel("")
        ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        for bar in bars:
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.025,
                     f"{bar.get_height():,.0f}", ha='center', va='bottom',
                     fontsize=8.5, color='#8892B0', fontweight='600')
        fig2.patch.set_facecolor(BG_CHART)
        ax2.set_facecolor(BG_CHART)
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