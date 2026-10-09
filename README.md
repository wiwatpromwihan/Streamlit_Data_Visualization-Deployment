# 📊 Streamlit Data Visualization & Deployment Dashboard

โปรเจกต์แดชบอร์ดแสดงผลข้อมูลเชิงโต้ตอบ (Interactive Data Dashboard) พัฒนาด้วย **Streamlit** และ **Python** พร้อมสำหรับการ Deploy ขึ้น **Streamlit Community Cloud** หรือ Cloud Platform อื่นๆ

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)
```text
streamlit_data_viz/
├── app.py              # โค้ดหลักของ Streamlit App (UI, Charts, Data processing)
├── requirements.txt    # รายการแพ็กเกจที่ต้องใช้สำหรับ Deploy
├── .gitignore          # ละเว้นไฟล์ที่ไม่ต้องการอัปโหลดขึ้น Git เช่น .venv/
└── README.md           # คู่มือการติดตั้ง รันโปรแกรม และการ Deploy
```

---

## 💻 วิธีการรันบนเครื่องตนเอง (Local Development)

1. **เข้าสู่โฟลเดอร์โปรเจกต์**:
   ```bash
   cd "69-1 คอมพิวเตอร์ชั้นสูง/streamlit_data_viz"
   ```

2. **เปิดใช้งาน Virtual Environment (ถ้ามี)**:
   - macOS / Linux:
     ```bash
     source .venv/bin/activate
     ```
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```

3. **ติดตั้ง Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **รัน Streamlit App**:
   ```bash
   streamlit run app.py
   ```
   โปรแกรมจะเปิดเบราว์เซอร์อัตโนมัติที่ `http://localhost:8501`

---

## 🚀 คู่มือการ Deployment ขึ้น Streamlit Community Cloud (ฟรี)

1. **สร้าง Git Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Streamlit Data Visualization App"
   ```

2. **Push โค้ดขึ้น GitHub**:
   - สร้าง New Repository บน [GitHub.com](https://github.com)
   - เชื่อมต่อและ Push โค้ดขึ้นไป:
     ```bash
     git remote add origin <URL-ของ-GitHub-Repository>
     git branch -M main
     git push -u origin main
     ```

3. **Deploy บน Streamlit Cloud**:
   - ไปที่ [share.streamlit.io](https://share.streamlit.io) แล้วล็อกอินด้วย GitHub
   - คลิกปุ่ม **"Create app"**
   - เลือก Repository, Branch (`main`), และ Main file path (`app.py`)
   - กดปุ่ม **"Deploy!"**
   - ภายในไม่กี่นาที คุณจะได้ URL สาธารณะที่ทุกคนสามารถเข้าชมแดชบอร์ดได้ทันที!
