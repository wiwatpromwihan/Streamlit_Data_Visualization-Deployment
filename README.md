# ♻️ ระบบวิเคราะห์ข้อมูลปริมาณขยะมูลฝอย ปี 2568
### Streamlit Data Visualization & Deployment

เว็บแอปพลิเคชันวิเคราะห์และแสดงผลข้อมูลเชิงโต้ตอบ (Interactive Data Visualization) พัฒนาด้วย **Python, Pandas, Plotly และ Streamlit**  
ชุดข้อมูล: **ปริมาณขยะมูลฝอย ปี 2568 (กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช)**  
ดึงข้อมูลจาก API: **Open Government Data of Thailand (data.go.th)**

---

## 🌟 ฟีเจอร์เด่นของระบบ
- 📡 **เชื่อมต่อ API อัตโนมัติ**: ดึงข้อมูลสดจากฐานข้อมูล CKAN Datastore ของ data.go.th พร้อมระบบ Local Cache สำรอง
- 🎛️ **Interactive Widgets (5 รูปแบบ)**:
  1. เลือกสังกัดหน่วยงาน (Selectbox)
  2. เลือกเดือน (Multiselect)
  3. สไลเดอร์กรองปริมาณขยะขั้นต่ำ (Slider)
  4. ช่องค้นหาชื่อหน่วยงาน (Text Input)
  5. สลับหน่วยแสดงผล กิโลกรัม / ตัน (Radio Button)
- 📌 **สรุปตัวชี้วัดสำคัญ (Key Metrics)**:
  - ปริมาณขยะที่เกิดขึ้นรวม
  - ปริมาณขยะที่นำไปใช้ประโยชน์
  - ปริมาณขยะที่ส่งกำจัด
  - อัตราส่วนการนำไปใช้ประโยชน์ (%)
- 📊 **กราฟวิเคราะห์ข้อมูล (Visualizations)**:
  1. **กราฟแท่ง (Horizontal Bar Chart)**: 10 อันดับหน่วยงานที่มีปริมาณขยะสูงสุด
  2. **กราฟวงกลม (Donut Chart)**: สัดส่วนการจัดการขยะ (ใช้ประโยชน์ vs ส่งกำจัด)
  3. **กราฟเส้น (Multi-line Chart)**: แนวโน้มปริมาณขยะรายเดือนทั้ง 3 ประเภท
- 📋 **Data Explorer & Export**:
  - ตารางแสดงข้อมูลรายละเอียดที่ผ่านการกรอง
  - ปุ่มดาวน์โหลดข้อมูลที่ผ่านการกรองออกมาเป็นไฟล์ CSV

---

## 💻 วิธีการรันบนเครื่องคอมพิวเตอร์ (Local Development)

```bash
# 1. เข้าสู่โฟลเดอร์โปรเจกต์
cd streamlit_data_viz

# 2. ติดตั้งแพ็กเกจที่จำเป็น
pip install -r requirements.txt

# 3. รัน Streamlit
streamlit run app.py
```

---

## 🚀 การ Deployment บน Streamlit Community Cloud
1. โค้ดโปรเจกต์นี้ถูก Push ขึ้น GitHub Repository:
   `https://github.com/wiwatpromwihan/Streamlit_Data_Visualization-Deployment.git`
2. เข้าไปที่ [share.streamlit.io](https://share.streamlit.io)
3. เลือก Repository: `wiwatpromwihan/Streamlit_Data_Visualization-Deployment`
4. ตั้งค่า Main file path: `app.py`
5. กดปุ่ม **Deploy!**
