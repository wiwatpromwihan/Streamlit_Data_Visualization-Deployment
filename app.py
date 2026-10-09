import streamlit as st
import pandas as pd
import numpy as np
import datetime

# --- ตั้งค่าหน้าเว็บ (Page Configuration) ---
st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ฟังก์ชันสร้างข้อมูลตัวอย่าง (Demo Data Generator) ---
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=180, freq="D")
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports"]
    regions = ["North", "Central", "South", "East", "Northeast"]
    
    data = {
        "Date": np.random.choice(dates, size=500),
        "Category": np.random.choice(categories, size=500),
        "Region": np.random.choice(regions, size=500),
        "Sales": np.random.uniform(100, 5000, size=500).round(2),
        "Units_Sold": np.random.randint(1, 20, size=500),
        "Customer_Rating": np.random.uniform(3.0, 5.0, size=500).round(1),
    }
    df = pd.DataFrame(data)
    df["Revenue"] = (df["Sales"] * df["Units_Sold"]).round(2)
    df = df.sort_values(by="Date").reset_index(drop=True)
    return df

# --- ส่วนแถบด้านข้าง (Sidebar) ---
st.sidebar.title("⚙️ การควบคุมและฟิลเตอร์")
st.sidebar.markdown("---")

# เลือกว่าจะใช้ชุดข้อมูลตัวอย่าง หรืออัปโหลดไฟล์ CSV เอง
data_source = st.sidebar.radio(
    "แหล่งข้อมูล (Data Source):",
    ["📊 ชุดข้อมูลตัวอย่าง (Demo Dataset)", "📁 อัปโหลดไฟล์ CSV (Upload CSV)"],
)

if data_source == "📁 อัปโหลดไฟล์ CSV (Upload CSV)":
    uploaded_file = st.sidebar.file_uploader("เลือกไฟล์ CSV ของคุณ", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ อัปโหลดไฟล์สำเร็จ!")
        except Exception as e:
            st.sidebar.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
            df = generate_sample_data()
    else:
        st.sidebar.info("ยังไม่ได้อัปโหลดไฟล์ กำลังใช้ข้อมูลตัวอย่างแทน")
        df = generate_sample_data()
else:
    df = generate_sample_data()

# ฟิลเตอร์ตามหมวดหมู่ (Category Filter)
if "Category" in df.columns:
    all_categories = df["Category"].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "เลือกหมวดหมู่ (Categories):",
        options=all_categories,
        default=all_categories,
    )
    if selected_categories:
        df = df[df["Category"].isin(selected_categories)]

# ฟิลเตอร์ช่วงวันที่ (Date Filter)
if "Date" in df.columns:
    try:
        df["Date"] = pd.to_datetime(df["Date"])
        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        date_range = st.sidebar.date_input(
            "ช่วงวันที่ (Date Range):",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)]
    except Exception:
        pass

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 เกี่ยวกับการ Deployment")
st.sidebar.info(
    """
    **ขั้นตอนการ Deploy ขึ้น Streamlit Cloud:**
    1. อัปโหลดโค้ดขึ้น GitHub Repository
    2. เข้าไปที่ [share.streamlit.io](https://share.streamlit.io)
    3. เชื่อมต่อบัญชี GitHub แล้วเลือก Repository
    4. กำหนดไฟล์หลักเป็น `app.py` แล้วกด **Deploy**
    """
)

# --- ส่วนเนื้อหาหลัก (Main Dashboard) ---
st.title("📈 Streamlit Data Visualization & Deployment Dashboard")
st.markdown("ระบบวิเคราะห์และแสดงผลข้อมูลเชิงโต้ตอบ (Interactive Data Dashboard) พัฒนาด้วย **Streamlit & Python**")
st.markdown("---")

# 1. แสดงตัวชี้วัดสำคัญ (Key Performance Indicators - KPIs)
st.subheader("📌 ภาพรวมตัวชี้วัดสำคัญ (Key Metrics)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_records = len(df)
kpi1.metric("จำนวนรายการทั้งหมด", f"{total_records:,} รายการ")

if "Revenue" in df.columns:
    total_revenue = df["Revenue"].sum()
    avg_revenue = df["Revenue"].mean()
    kpi2.metric("ยอดรวมรายได้ (Revenue)", f"฿{total_revenue:,.2f}")
    kpi3.metric("รายได้เฉลี่ยต่อรายการ", f"฿{avg_revenue:,.2f}")
else:
    kpi2.metric("จำนวนคอลัมน์", f"{len(df.columns)} คอลัมน์")
    kpi3.metric("ข้อมูลสมบูรณ์", "100%")

if "Customer_Rating" in df.columns:
    avg_rating = df["Customer_Rating"].mean()
    kpi4.metric("คะแนนเฉลี่ยลูกค้า", f"{avg_rating:.2f} ⭐")
elif "Units_Sold" in df.columns:
    total_units = df["Units_Sold"].sum()
    kpi4.metric("ยอดขายรวม (ชิ้น)", f"{total_units:,} ชิ้น")
else:
    kpi4.metric("สถานะระบบ", "พร้อมใช้งาน ✅")

st.markdown("---")

# 2. กราฟและการแสดงผลข้อมูล (Data Visualizations)
st.subheader("📊 กราฟวิเคราะห์ข้อมูล (Visualizations)")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 📅 แนวโน้มตามช่วงเวลา (Trend Over Time)")
    if "Date" in df.columns and "Revenue" in df.columns:
        trend_df = df.groupby(df["Date"].dt.date)["Revenue"].sum().reset_index()
        trend_df = trend_df.set_index("Date")
        st.line_chart(trend_df, use_container_width=True)
    elif "Date" in df.columns:
        trend_df = df.groupby(df["Date"].dt.date).size().rename("Count")
        st.line_chart(trend_df, use_container_width=True)
    else:
        st.info("ไม่พบคอลัมน์วันที่สำหรับแสดงกราฟแนวโน้ม")

with col_right:
    st.markdown("#### 🏷️ ยอดรวมแยกตามหมวดหมู่ (By Category)")
    if "Category" in df.columns and "Revenue" in df.columns:
        cat_df = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
        st.bar_chart(cat_df, use_container_width=True)
    elif "Category" in df.columns:
        cat_df = df["Category"].value_counts()
        st.bar_chart(cat_df, use_container_width=True)
    else:
        st.info("ไม่พบคอลัมน์หมวดหมู่สำหรับแสดงกราฟแท่ง")

# แถวกราฟที่ 2 (ภูมิภาคและความสัมพันธ์)
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🗺️ สัดส่วนตามภูมิภาค (By Region)")
    if "Region" in df.columns and "Revenue" in df.columns:
        region_df = df.groupby("Region")["Revenue"].sum().reset_index()
        st.bar_chart(region_df.set_index("Region"), use_container_width=True)
    elif "Region" in df.columns:
        st.bar_chart(df["Region"].value_counts(), use_container_width=True)
    else:
        st.info("ไม่พบคอลัมน์ภูมิภาค")

with col4:
    st.markdown("#### 🎯 ความสัมพันธ์ ยอดขาย vs หน่วยสินค้า")
    if "Sales" in df.columns and "Units_Sold" in df.columns:
        scatter_df = df[["Sales", "Units_Sold"]].dropna()
        st.scatter_chart(scatter_df, x="Sales", y="Units_Sold", use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลตัวเลขเพียงพอสำหรับสร้าง Scatter chart")

st.markdown("---")

# 3. ตารางข้อมูลดิบ (Data Explorer Table)
st.subheader("📋 ตารางข้อมูล (Data Table)")
with st.expander("🔍 คลิกเพื่อดูหรือดาวน์โหลดข้อมูลทั้งหมด", expanded=True):
    st.dataframe(df, use_container_width=True, height=280)
    
    # ปุ่มดาวน์โหลดข้อมูลเป็นไฟล์ CSV
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 ดาวน์โหลดข้อมูลที่กรองแล้ว (Download CSV)",
        data=csv_data,
        file_name=f"filtered_data_{datetime.date.today()}.csv",
        mime="text/csv",
    )

# --- ส่วนล่าง (Footer) ---
st.markdown("---")
st.caption("พัฒนาเพื่อการศึกษา: วิชาคอมพิวเตอร์ชั้นสูง • สร้างด้วย Streamlit & Python")
