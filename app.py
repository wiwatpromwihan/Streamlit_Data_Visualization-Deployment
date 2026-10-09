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
    page_title="ระบบวิเคราะห์ปริมาณขยะมูลฝอย ปี 2568 | Waste Analytics",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ปรับแต่ง Custom CSS สำหรับ UX/UI สไตล์ Modern Glassmorphism & Executive Dashboard ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Prompt', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* Hero Banner Header */
    .hero-container {
        background: linear-gradient(135deg, #0F766E 0%, #0D9488 45%, #0284C7 100%);
        border-radius: 20px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(13, 148, 136, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 12px;
        letter-spacing: 0.3px;
    }
    .hero-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 8px 0;
        line-height: 1.25;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 14.5px;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        line-height: 1.5;
    }

    /* Status Pill */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ECFDF5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #A7F3D0;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3);
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 18px;
        padding: 20px 22px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 8px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 22px rgba(0, 0, 0, 0.07);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .kpi-title {
        font-size: 13.5px;
        font-weight: 500;
        color: #64748B;
        margin: 0;
    }
    .kpi-icon-box {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }
    .kpi-footer {
        font-size: 12px;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Section Headers */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #1E293B;
        margin: 20px 0 14px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-header {
        padding: 10px 0 16px 0;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }

    /* Tab bar aesthetic */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
        padding: 8px 18px;
        color: #64748B;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #0D9488 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }

    /* Metric callout container */
    .glass-panel {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    </style>
    """,
    unsafe_allow_html=True,
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

df_raw, source_status = load_data()

# --- แถบตัวกรอง (Sidebar) ---
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-header">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: #0D9488; color: white; width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                    ♻️
                </div>
                <div>
                    <div style="font-weight: 700; font-size: 16px; color: #0F172A;">Waste Analytics</div>
                    <div style="font-size: 11px; color: #64748B;">ปีงบประมาณ 2568</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎛️ ตัวกรองการวิเคราะห์")

    # Widget 1: สังกัด
    affiliations = ["ทั้งหมด"] + sorted(df_raw["สังกัด"].dropna().unique().tolist())
    selected_affil = st.selectbox("1. สังกัดหน่วยงาน:", affiliations)

    # Widget 2: เดือน
    available_months = [m for m in THAI_MONTHS if m in df_raw["เดือน"].values]
    selected_months = st.multiselect(
        "2. เลือกเดือนที่วิเคราะห์:",
        options=available_months,
        default=available_months,
    )

    # Widget 3: ปริมาณขยะขั้นต่ำ
    max_waste = float(df_raw["ขยะที่เกิดขึ้น (กก.)"].max()) if not df_raw.empty else 1000.0
    waste_threshold = st.slider(
        "3. ปริมาณขยะขั้นต่ำ (กก.):",
        min_value=0.0,
        max_value=float(np.ceil(max_waste)),
        value=0.0,
        step=50.0,
    )

    # Widget 4: ค้นหาหน่วยงาน
    search_unit = st.text_input("4. ค้นหาชื่อหน่วยงาน:", placeholder="เช่น ส่วนกลาง, สาขา...")

    st.markdown("---")
    st.markdown("### ⚙️ ปรับแต่งการแสดงผล")

    # Widget 5: หน่วยตัวเลข
    unit_option = st.radio(
        "5. หน่วยปริมาณขยะ:",
        options=["กิโลกรัม (กก.)", "ตัน (Tons)"],
        horizontal=True,
    )
    divisor = 1000.0 if "ตัน" in unit_option else 1.0
    unit_label = "ตัน" if "ตัน" in unit_option else "กก."

    st.markdown("---")
    st.markdown(
        """
        <div style="padding: 12px; background: #F1F5F9; border-radius: 12px; font-size: 12px; color: #475569;">
            <div style="font-weight: 600; margin-bottom: 4px;">🚀 สถานะ Deployment</div>
            <div>• แพลตฟอร์ม: Streamlit Cloud</div>
            <div>• ซอร์สโค้ด: <a href="https://github.com/wiwatpromwihan/Streamlit_Data_Visualization-Deployment" target="_blank" style="color: #0D9488; text-decoration: none; font-weight: 600;">GitHub Repo</a></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- กรองข้อมูล ---
df_filtered = df_raw.copy()

if selected_affil != "ทั้งหมด":
    df_filtered = df_filtered[df_filtered["สังกัด"] == selected_affil]

if selected_months:
    df_filtered = df_filtered[df_filtered["เดือน"].isin(selected_months)]

if waste_threshold > 0:
    df_filtered = df_filtered[df_filtered["ขยะที่เกิดขึ้น (กก.)"] >= waste_threshold]

if search_unit.strip():
    df_filtered = df_filtered[df_filtered["หน่วยงาน"].str.contains(search_unit.strip(), na=False)]

# --- Hero Banner ---
st.markdown(
    f"""
    <div class="hero-container">
        <div class="hero-badge">
            <span>🌿 กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช</span>
            <span>•</span>
            <span>ปีงบประมาณ 2568</span>
        </div>
        <h1 class="hero-title">ระบบวิเคราะห์ข้อมูลปริมาณขยะมูลฝอย</h1>
        <p class="hero-subtitle">
            แดชบอร์ดบริหารจัดการสิ่งแวดล้อม ติดตามปริมาณขยะมูลฝอย การนำไปใช้ประโยชน์ และการส่งกำจัด 
            เชื่อมต่อข้อมูลแบบเปิดจาก <b>Open Government Data of Thailand (data.go.th)</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ข้อมูลสรุปสถานะการกรอง
col_stat_l, col_stat_r = st.columns([1, 1])
with col_stat_l:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13.5px; color: #475569;">
            <span class="status-badge"><span class="pulse-dot"></span> เชื่อมต่อ: {source_status}</span>
            <span>กำลังแสดงข้อมูล <b>{len(df_filtered):,}</b> จากทั้งหมด {len(df_raw):,} รายการ</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_stat_r:
    st.markdown(
        f"""
        <div style="text-align: right; font-size: 13px; color: #64748B;">
            หน่วยแสดงผล: <b>{unit_option}</b> | สังกัด: <b>{selected_affil}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# --- คำนวณค่า KPIs ---
total_gen = df_filtered["ขยะที่เกิดขึ้น (กก.)"].sum() / divisor
total_util = df_filtered["ใช้ประโยชน์ (กก.)"].sum() / divisor
total_disp = df_filtered["ขยะที่ส่งกำจัด (กก.)"].sum() / divisor
util_pct = (
    (df_filtered["ใช้ประโยชน์ (กก.)"].sum() / df_filtered["ขยะที่เกิดขึ้น (กก.)"].sum() * 100)
    if df_filtered["ขยะที่เกิดขึ้น (กก.)"].sum() > 0
    else 0.0
)
disp_pct = 100.0 - util_pct if util_pct <= 100 else 0.0

# --- แสดง KPI Cards 4 ช่อง ดีไซน์หรูหรา ---
kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)

with kpi_c1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">ขยะที่เกิดขึ้นรวม</span>
                <div class="kpi-icon-box" style="background: #FEF3C7; color: #D97706;">🗑️</div>
            </div>
            <div class="kpi-value">{total_gen:,.2f} <span style="font-size: 15px; font-weight: 500; color: #64748B;">{unit_label}</span></div>
            <div class="kpi-footer">
                <span>ปริมาณขยะทั้งหมดที่บันทึก</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_c2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">นำไปใช้ประโยชน์</span>
                <div class="kpi-icon-box" style="background: #CCFBF1; color: #0D9488;">🌱</div>
            </div>
            <div class="kpi-value" style="color: #0D9488;">{total_util:,.2f} <span style="font-size: 15px; font-weight: 500; color: #0D9488;">{unit_label}</span></div>
            <div class="kpi-footer">
                <span style="color: #0D9488; font-weight: 600;">{util_pct:.1f}%</span> ของขยะที่เกิดขึ้น
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_c3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">ส่งไปกำจัด</span>
                <div class="kpi-icon-box" style="background: #FEE2E2; color: #DC2626;">🚛</div>
            </div>
            <div class="kpi-value" style="color: #DC2626;">{total_disp:,.2f} <span style="font-size: 15px; font-weight: 500; color: #DC2626;">{unit_label}</span></div>
            <div class="kpi-footer">
                <span style="color: #DC2626; font-weight: 600;">{disp_pct:.1f}%</span> ส่งหลุมฝังกลบ/เผา
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_c4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">อัตราการรีไซเคิล/ใช้ซ้ำ</span>
                <div class="kpi-icon-box" style="background: #E0E7FF; color: #4F46E5;">♻️</div>
            </div>
            <div class="kpi-value" style="color: #4F46E5;">{util_pct:.1f}%</div>
            <div class="kpi-footer">
                <span>ประสิทธิภาพคัดแยกขยะ</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# --- จัดแบ่งเนื้อหาเป็น Tabs เพื่อการใช้งานที่ราบรื่น (Tabs Layout) ---
tab_dash, tab_deep, tab_data = st.tabs([
    "📊 แดชบอร์ดหลักและแนวโน้ม (Dashboard & Trends)",
    "🏢 เจาะลึกรายสังกัดและหน่วยงาน (Agency Deep Dive)",
    "📋 ตารางข้อมูลและส่งออก (Data Explorer & Export)",
])

# ==================== TAB 1: ภาพรวมและแนวโน้ม ====================
with tab_dash:
    col_chart1, col_chart2 = st.columns([1.25, 0.75])

    # กราฟแท่ง 10 อันดับหน่วยงาน
    with col_chart1:
        st.markdown(
            """
            <div class="section-title">
                <span>🏆 10 อันดับหน่วยงานที่มีปริมาณขยะเกิดขึ้นสูงสุด</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        top10 = (
            df_filtered.groupby("หน่วยงาน")["ขยะที่เกิดขึ้น (กก.)"]
            .sum()
            .reset_index()
            .sort_values(by="ขยะที่เกิดขึ้น (กก.)", ascending=False)
            .head(10)
        )
        top10["แสดงผล"] = top10["ขยะที่เกิดขึ้น (กก.)"] / divisor

        fig_bar = px.bar(
            top10,
            x="แสดงผล",
            y="หน่วยงาน",
            orientation="h",
            color="แสดงผล",
            color_continuous_scale=[
                [0.0, "#A7F3D0"],
                [0.5, "#14B8A6"],
                [1.0, "#0F766E"],
            ],
            labels={"แสดงผล": f"ปริมาณ ({unit_label})", "หน่วยงาน": ""},
        )
        fig_bar.update_layout(
            yaxis={"categoryorder": "total ascending"},
            font=dict(family="Prompt", size=12),
            margin=dict(l=10, r=20, t=10, b=20),
            height=370,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        )
        fig_bar.update_traces(
            marker=dict(cornerradius=8),
            hovertemplate="<b>%{y}</b><br>ปริมาณขยะ: %{x:,.2f} " + unit_label + "<extra></extra>",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # กราฟวงกลม สัดส่วนการจัดการ
    with col_chart2:
        st.markdown(
            """
            <div class="section-title">
                <span>🍩 สัดส่วนการจัดการขยะ</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        pie_df = pd.DataFrame({
            "ประเภท": ["นำไปใช้ประโยชน์ (Recycled)", "ส่งไปกำจัด (Disposed)"],
            "ปริมาณ": [total_util, total_disp],
        })
        fig_donut = px.pie(
            pie_df,
            names="ประเภท",
            values="ปริมาณ",
            hole=0.55,
            color="ประเภท",
            color_discrete_map={
                "นำไปใช้ประโยชน์ (Recycled)": "#0D9488",
                "ส่งไปกำจัด (Disposed)": "#EF4444",
            },
        )
        fig_donut.update_traces(
            textposition="outside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#FFFFFF", width=3)),
            hovertemplate="<b>%{label}</b><br>ปริมาณ: %{value:,.2f} " + unit_label + " (%{percent})<extra></extra>",
        )
        fig_donut.update_layout(
            font=dict(family="Prompt", size=12),
            margin=dict(l=10, r=10, t=10, b=10),
            height=370,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[
                dict(
                    text=f"<b>{util_pct:.1f}%</b><br><span style='font-size:11px;color:#64748B;'>ใช้ประโยชน์</span>",
                    x=0.5, y=0.5,
                    font_size=18,
                    showarrow=False,
                    font_family="Prompt",
                )
            ],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # กราฟเส้น แนวโน้มรายเดือนแบบละเอียด
    st.markdown(
        """
        <div class="section-title">
            <span>📈 แนวโน้มปริมาณขยะตลอด 12 เดือน (เปรียบเทียบ 3 มิติ)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    month_data = (
        df_filtered.groupby(["เดือน_ลำดับ", "เดือน"])[["ขยะที่เกิดขึ้น (กก.)", "ใช้ประโยชน์ (กก.)", "ขยะที่ส่งกำจัด (กก.)"]]
        .sum()
        .reset_index()
        .sort_values(by="เดือน_ลำดับ")
    )

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=month_data["เดือน"],
        y=month_data["ขยะที่เกิดขึ้น (กก.)"] / divisor,
        mode="lines+markers",
        name=f"ขยะที่เกิดขึ้น ({unit_label})",
        line=dict(color="#F59E0B", width=3.5, shape="spline"),
        marker=dict(size=8, color="#F59E0B"),
        hovertemplate="ขยะที่เกิดขึ้น: %{y:,.2f} " + unit_label,
    ))
    fig_line.add_trace(go.Scatter(
        x=month_data["เดือน"],
        y=month_data["ใช้ประโยชน์ (กก.)"] / divisor,
        mode="lines+markers",
        name=f"นำไปใช้ประโยชน์ ({unit_label})",
        line=dict(color="#0D9488", width=3, shape="spline"),
        marker=dict(size=8, color="#0D9488"),
        hovertemplate="ใช้ประโยชน์: %{y:,.2f} " + unit_label,
    ))
    fig_line.add_trace(go.Scatter(
        x=month_data["เดือน"],
        y=month_data["ขยะที่ส่งกำจัด (กก.)"] / divisor,
        mode="lines+markers",
        name=f"ส่งไปกำจัด ({unit_label})",
        line=dict(color="#EF4444", width=2.5, dash="dash", shape="spline"),
        marker=dict(size=7, color="#EF4444"),
        hovertemplate="ส่งกำจัด: %{y:,.2f} " + unit_label,
    ))
    fig_line.update_layout(
        font=dict(family="Prompt", size=12),
        hovermode="x unified",
        margin=dict(l=10, r=10, t=20, b=20),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=f"ปริมาณ ({unit_label})"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E2E8F0",
            borderwidth=1,
        ),
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ==================== TAB 2: เจาะลึกรายสังกัดและหน่วยงาน ====================
with tab_deep:
    c_deep1, c_deep2 = st.columns(2)

    with c_deep1:
        st.markdown(
            """
            <div class="section-title">
                <span>🏢 เปรียบเทียบตามสังกัด (ส่วนกลาง vs ส่วนภูมิภาค)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        affil_summary = (
            df_filtered.groupby("สังกัด")[["ขยะที่เกิดขึ้น (กก.)", "ใช้ประโยชน์ (กก.)", "ขยะที่ส่งกำจัด (กก.)"]]
            .sum()
            .reset_index()
        )
        affil_summary["ขยะที่เกิดขึ้น"] = affil_summary["ขยะที่เกิดขึ้น (กก.)"] / divisor
        affil_summary["นำไปใช้ประโยชน์"] = affil_summary["ใช้ประโยชน์ (กก.)"] / divisor
        affil_summary["ส่งไปกำจัด"] = affil_summary["ขยะที่ส่งกำจัด (กก.)"] / divisor

        fig_affil = px.bar(
            affil_summary,
            x="สังกัด",
            y=["นำไปใช้ประโยชน์", "ส่งไปกำจัด"],
            barmode="group",
            color_discrete_sequence=["#0D9488", "#EF4444"],
            labels={"value": f"ปริมาณ ({unit_label})", "variable": "ประเภท"},
        )
        fig_affil.update_layout(
            font=dict(family="Prompt", size=12),
            margin=dict(l=10, r=10, t=20, b=20),
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        )
        fig_affil.update_traces(marker=dict(cornerradius=6))
        st.plotly_chart(fig_affil, use_container_width=True)

    with c_deep2:
        st.markdown(
            """
            <div class="section-title">
                <span>👥 ความสัมพันธ์: จำนวนคน vs ปริมาณขยะที่เกิดขึ้น</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_scatter = px.scatter(
            df_filtered,
            x="คนเฉลี่ย",
            y="ขยะที่เกิดขึ้น (กก.)",
            color="สังกัด",
            size="ใช้ประโยชน์ (กก.)",
            hover_data=["หน่วยงาน", "เดือน"],
            color_discrete_sequence=["#0D9488", "#3B82F6"],
            labels={
                "คนเฉลี่ย": "จำนวนคนเฉลี่ยในหน่วยงาน",
                "ขยะที่เกิดขึ้น (กก.)": "ปริมาณขยะที่เกิดขึ้น (กก.)",
            },
        )
        fig_scatter.update_layout(
            font=dict(family="Prompt", size=12),
            margin=dict(l=10, r=10, t=20, b=20),
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# ==================== TAB 3: ตารางข้อมูลและส่งออก ====================
with tab_data:
    st.markdown(
        """
        <div class="section-title">
            <span>📋 ตารางข้อมูลสืบค้นและส่งออก (Filtered Data Explorer)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    show_cols = [
        "ปี", "สังกัด", "หน่วยงาน", "เดือน", "คนเฉลี่ย", "วันทำงาน",
        "ขยะที่เกิดขึ้น (กก.)", "ใช้ประโยชน์ (กก.)", "ขยะที่ส่งกำจัด (กก.)", "ร้อยละส่งกำจัดลดลง"
    ]
    disp_df = df_filtered[[c for c in show_cols if c in df_filtered.columns]].copy()

    col_btn_l, col_btn_r = st.columns([1, 1])
    with col_btn_l:
        st.caption(f"แสดงข้อมูลที่ผ่านการกรองจำนวน {len(disp_df):,} แถว")
    with col_btn_r:
        csv_bytes = disp_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์ CSV ข้อมูลชุดนี้",
            data=csv_bytes,
            file_name="waste_data_2568_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.dataframe(
        disp_df,
        use_container_width=True,
        height=380,
    )

# --- Footer ---
st.markdown("---")
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown(
        "<div style='font-size: 13px; color: #64748B;'>🌿 มหาวิทยาลัยราชภัฏภูเก็ต (PKRU) • วิชาคอมพิวเตอร์ชั้นสูง</div>",
        unsafe_allow_html=True,
    )
with f_col2:
    st.markdown(
        "<div style='text-align: right; font-size: 13px; color: #64748B;'>🚀 Deploy พร้อมใช้งานบน <a href='https://share.streamlit.io' target='_blank' style='color:#0D9488;'>Streamlit Community Cloud</a></div>",
        unsafe_allow_html=True,
    )
