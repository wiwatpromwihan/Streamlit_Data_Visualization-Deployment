import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import urllib.request
import json
import os

# --- ตั้งค่าหน้าเว็บ (Page Config) ---
st.set_page_config(
    page_title="ระบบวิเคราะห์ปริมาณขยะมูลฝอย ปี 2568",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ลำดับเดือนภาษาไทยสำหรับการจัดเรียงข้อมูล ---
THAI_MONTHS = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

# --- ฟังก์ชันโหลดข้อมูล (Data Loader with Cache) ---
@st.cache_data(ttl=3600)
def load_data():
    api_url = "https://data.go.th/api/3/action/datastore_search?resource_id=1a83a733-7ca2-4310-8299-ee75a5715ee2&limit=500"
    df = None
    data_source_msg = "API สด (data.go.th)"

    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                raw = json.loads(response.read().decode("utf-8"))
                records = raw.get("result", {}).get("records", [])
                if records:
                    df = pd.DataFrame(records)
    except Exception:
        df = None

    # กรณีต่อ API ไม่ได้ ให้ใช้แคชข้อมูลสำรองในเครื่อง
    if df is None or df.empty:
        csv_cache_path = os.path.join(os.path.dirname(__file__), "data_cache.csv")
        if os.path.exists(csv_cache_path):
            df = pd.read_csv(csv_cache_path)
            data_source_msg = "แคชข้อมูลสำรองในเครื่อง (Local Cache)"
        else:
            st.error("ไม่สามารถเชื่อมต่อ API และไม่พบไฟล์แคชสำรอง")
            return pd.DataFrame(), "Error"

    # แปลงคอลัมน์ตัวเลขให้ถูกต้อง
    numeric_cols = [
        "ขยะที่เกิดขึ้น (กก.)",
        "ใช้ประโยชน์ (กก.)",
        "ขยะที่ส่งกำจัด (กก.)",
        "ร้อยละส่งกำจัดลดลง",
        "คนเฉลี่ย",
        "วันทำงาน",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    # จัดเรียงลำดับเดือน
    if "เดือน" in df.columns:
        df["เดือน_ลำดับ"] = df["เดือน"].apply(lambda m: THAI_MONTHS.index(m) if m in THAI_MONTHS else 99)

    return df, data_source_msg

# โหลดข้อมูล
df_raw, source_status = load_data()

# --- ส่วนหัวของหน้าเว็บ (Header) ---
st.title("♻️ ระบบวิเคราะห์ข้อมูลปริมาณขยะมูลฝอย ปี 2568")
st.markdown(
    """
    **การวิเคราะห์และแสดงผลข้อมูลเชิงโต้ตอบ (Data Visualization & Deployment)**  
    ชุดข้อมูล: *ปริมาณขยะมูลฝอย ปี 2568 กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช*  
    🔗 แหล่งข้อมูลต้นทาง: **Open Government Data of Thailand (data.go.th)**
    """
)
st.caption(f"📡 สถานะการดึงข้อมูล: **{source_status}** • จำนวนข้อมูลทั้งหมด: **{len(df_raw)}** แถว")
st.markdown("---")

if df_raw.empty:
    st.warning("ไม่มีข้อมูลที่จะแสดงผล กรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")
    st.stop()

# --- แถบตัวกรอง (Sidebar - Interactive Widgets) ---
st.sidebar.header("🎛️ ตัวกรองข้อมูล (Filters)")

# Widget 1: เลือกสังกัด
affiliations = ["ทั้งหมด"] + sorted(df_raw["สังกัด"].dropna().unique().tolist())
selected_affil = st.sidebar.selectbox("1. เลือกสังกัดหน่วยงาน:", affiliations)

# Widget 2: เลือกเดือน (Multiselect)
available_months = [m for m in THAI_MONTHS if m in df_raw["เดือน"].values]
selected_months = st.sidebar.multiselect(
    "2. เลือกเดือนที่ต้องการดู:",
    options=available_months,
    default=available_months,
)

# Widget 3: ปริมาณขยะขั้นต่ำ (Slider)
max_waste = float(df_raw["ขยะที่เกิดขึ้น (กก.)"].max())
waste_threshold = st.sidebar.slider(
    "3. กรองปริมาณขยะที่เกิดขึ้นขั้นต่ำ (กก.):",
    min_value=0.0,
    max_value=float(np.ceil(max_waste)),
    value=0.0,
    step=10.0,
)

# Widget 4: ช่องค้นหาชื่อหน่วยงาน
search_unit = st.sidebar.text_input("4. ค้นหาชื่อหน่วยงาน:", placeholder="เช่น สำนักบริหาร...")

# Widget 5: สลับหน่วยแสดงผล (กก. หรือ ตัน)
unit_option = st.sidebar.radio(
    "5. หน่วยการแสดงผลตัวเลข:",
    options=["กิโลกรัม (กก.)", "ตัน (Tons)"],
    horizontal=True,
)
divisor = 1000.0 if "ตัน" in unit_option else 1.0
unit_label = "ตัน" if "ตัน" in unit_option else "กก."

# กรองข้อมูลตามเงื่อนไขของผู้ใช้
df_filtered = df_raw.copy()

if selected_affil != "ทั้งหมด":
    df_filtered = df_filtered[df_filtered["สังกัด"] == selected_affil]

if selected_months:
    df_filtered = df_filtered[df_filtered["เดือน"].isin(selected_months)]

if waste_threshold > 0:
    df_filtered = df_filtered[df_filtered["ขยะที่เกิดขึ้น (กก.)"] >= waste_threshold]

if search_unit.strip():
    df_filtered = df_filtered[df_filtered["หน่วยงาน"].str.contains(search_unit.strip(), na=False)]

# --- สรุปภาพรวมตัวชี้วัด (KPI Metrics) ---
st.subheader("📌 ตัวชี้วัดสำคัญ (Key Metrics)")

total_generated = df_filtered["ขยะที่เกิดขึ้น (กก.)"].sum() / divisor
total_utilized = df_filtered["ใช้ประโยชน์ (กก.)"].sum() / divisor
total_disposed = df_filtered["ขยะที่ส่งกำจัด (กก.)"].sum() / divisor
utilization_rate = (
    (df_filtered["ใช้ประโยชน์ (กก.)"].sum() / df_filtered["ขยะที่เกิดขึ้น (กก.)"].sum() * 100)
    if df_filtered["ขยะที่เกิดขึ้น (กก.)"].sum() > 0
    else 0.0
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(f"🗑️ ขยะที่เกิดขึ้นรวม ({unit_label})", f"{total_generated:,.2f}")
kpi2.metric(f"🌱 นำไปใช้ประโยชน์ ({unit_label})", f"{total_utilized:,.2f}")
kpi3.metric(f"🚛 ส่งไปกำจัด ({unit_label})", f"{total_disposed:,.2f}")
kpi4.metric("♻️ อัตราการนำไปใช้ประโยชน์", f"{utilization_rate:.1f}%")

st.markdown("---")

# --- กราฟแสดงผล (Visualizations) ---
st.subheader("📊 กราฟวิเคราะห์ข้อมูล (Data Visualizations)")

# แถวกราฟที่ 1
col_graph1, col_graph2 = st.columns([1.2, 0.8])

# กราฟที่ 1: กราฟแท่ง 10 อันดับหน่วยงานที่มีขยะเกิดขึ้นสูงสุด
with col_graph1:
    st.markdown("#### 1️⃣ กราฟแท่ง: 10 อันดับหน่วยงานที่มีปริมาณขยะสูงสุด")
    top_units = (
        df_filtered.groupby("หน่วยงาน")["ขยะที่เกิดขึ้น (กก.)"]
        .sum()
        .reset_index()
        .sort_values(by="ขยะที่เกิดขึ้น (กก.)", ascending=False)
        .head(10)
    )
    top_units["ค่าที่แสดง"] = top_units["ขยะที่เกิดขึ้น (กก.)"] / divisor

    fig_bar = px.bar(
        top_units,
        x="ค่าที่แสดง",
        y="หน่วยงาน",
        orientation="h",
        color="ค่าที่แสดง",
        color_continuous_scale="Tealgrn",
        labels={"ค่าที่แสดง": f"ปริมาณขยะ ({unit_label})", "หน่วยงาน": "หน่วยงาน"},
    )
    fig_bar.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=20, r=20, t=20, b=20),
        height=380,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# กราฟที่ 3: สัดส่วนการจัดการขยะ (Donut Chart)
with col_graph2:
    st.markdown("#### 2️⃣ กราฟวงกลม: สัดส่วนการจัดการขยะ")
    pie_data = pd.DataFrame({
        "ประเภท": ["นำไปใช้ประโยชน์", "ส่งไปกำจัด"],
        "ปริมาณ": [
            df_filtered["ใช้ประโยชน์ (กก.)"].sum() / divisor,
            df_filtered["ขยะที่ส่งกำจัด (กก.)"].sum() / divisor,
        ],
    })
    fig_pie = px.pie(
        pie_data,
        names="ประเภท",
        values="ปริมาณ",
        hole=0.45,
        color="ประเภท",
        color_discrete_map={"นำไปใช้ประโยชน์": "#2EC4B6", "ส่งไปกำจัด": "#E71D36"},
    )
    fig_pie.update_traces(textinfo="percent+label", textposition="inside")
    fig_pie.update_layout(
        margin=dict(l=10, r=10, t=20, b=20),
        height=380,
        showlegend=False,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# กราฟที่ 2: กราฟเส้นแนวโน้มรายเดือน
st.markdown("#### 3️⃣ กราฟเส้น: แนวโน้มปริมาณขยะในแต่ละเดือน")
monthly_df = (
    df_filtered.groupby(["เดือน_ลำดับ", "เดือน"])[["ขยะที่เกิดขึ้น (กก.)", "ใช้ประโยชน์ (กก.)", "ขยะที่ส่งกำจัด (กก.)"]]
    .sum()
    .reset_index()
    .sort_values(by="เดือน_ลำดับ")
)

monthly_df["ขยะที่เกิดขึ้น"] = monthly_df["ขยะที่เกิดขึ้น (กก.)"] / divisor
monthly_df["นำไปใช้ประโยชน์"] = monthly_df["ใช้ประโยชน์ (กก.)"] / divisor
monthly_df["ส่งไปกำจัด"] = monthly_df["ขยะที่ส่งกำจัด (กก.)"] / divisor

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=monthly_df["เดือน"],
    y=monthly_df["ขยะที่เกิดขึ้น"],
    mode="lines+markers",
    name=f"ขยะที่เกิดขึ้น ({unit_label})",
    line=dict(color="#FF9F1C", width=3),
    marker=dict(size=8),
))
fig_line.add_trace(go.Scatter(
    x=monthly_df["เดือน"],
    y=monthly_df["นำไปใช้ประโยชน์"],
    mode="lines+markers",
    name=f"นำไปใช้ประโยชน์ ({unit_label})",
    line=dict(color="#2EC4B6", width=2.5),
    marker=dict(size=7),
))
fig_line.add_trace(go.Scatter(
    x=monthly_df["เดือน"],
    y=monthly_df["ส่งไปกำจัด"],
    mode="lines+markers",
    name=f"ส่งไปกำจัด ({unit_label})",
    line=dict(color="#E71D36", width=2, dash="dash"),
    marker=dict(size=6),
))
fig_line.update_layout(
    xaxis_title="เดือน",
    yaxis_title=f"ปริมาณขยะ ({unit_label})",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=30, b=20),
    height=360,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# --- ตารางข้อมูลและการดาวน์โหลด (Data Table & Download) ---
st.subheader("📋 ตารางข้อมูลรายละเอียด (Filtered Data)")
with st.expander("🔍 คลิกเพื่อดูตารางข้อมูลและดาวน์โหลด", expanded=True):
    show_cols = [
        "ปี", "สังกัด", "หน่วยงาน", "เดือน", "คนเฉลี่ย", "วันทำงาน",
        "ขยะที่เกิดขึ้น (กก.)", "ใช้ประโยชน์ (กก.)", "ขยะที่ส่งกำจัด (กก.)", "ร้อยละส่งกำจัดลดลง"
    ]
    display_df = df_filtered[[c for c in show_cols if c in df_filtered.columns]].copy()
    st.dataframe(display_df, use_container_width=True, height=280)

    csv_bytes = display_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 ดาวน์โหลดข้อมูลที่กรองแล้ว (CSV)",
        data=csv_bytes,
        file_name="waste_management_data_2568.csv",
        mime="text/csv",
    )

# --- ส่วนท้าย (Footer) ---
st.markdown("---")
col_foot1, col_foot2 = st.columns(2)
with col_foot1:
    st.caption("👨‍💻 ผู้พัฒนา: wiwatpromwihan • มหาวิทยาลัยราชภัฏภูเก็ต (PKRU)")
with col_foot2:
    st.caption("🚀 GitHub: [Streamlit_Data_Visualization-Deployment](https://github.com/wiwatpromwihan/Streamlit_Data_Visualization-Deployment)")
