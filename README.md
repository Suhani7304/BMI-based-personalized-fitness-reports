# 🧮 BMI-Based Personalized Fitness Reports

A **Flask-based web application** that calculates **BMI (Body Mass Index)** from user input, categorizes it, and generates **personalized fitness recommendations** including diet tips, exercise routines, and lifestyle advice. Users can also **download a detailed PDF report**.

---

## ✅ Features
- **BMI Calculation**: Compute BMI based on height and weight.
- **BMI Category Classification**:
  - Underweight
  - Normal weight
  - Overweight
  - Obesity
- **Personalized Recommendations**:
  - Health implications
  - Diet tips and example meal plans
  - Exercise routines
  - Lifestyle and hydration tips
  - Supplement and cooking advice
- **PDF Report Generation**:
  - Download a well-structured PDF containing BMI, category, and recommendations.
- **Responsive API**:
  - `/` → Calculate BMI and get recommendations.
  - `/generate-pdf` → Download the PDF report.

---

## 🛠️ Tech Stack
- **Backend**: Python (Flask)
- **Frontend**: HTML (Jinja Templates)
- **Data Handling**: Pandas
- **PDF Generation**: `xhtml2pdf (pisa)`
- **Others**: io, datetime


## 📂 Project Structure
