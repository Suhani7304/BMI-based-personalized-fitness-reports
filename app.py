from flask import Flask, request, jsonify, render_template, send_file # send_file sends pdf etc as response
from xhtml2pdf import pisa  # converts html object into pdf
import pandas as pd
import io  # create files to be sent directly via send_file without saving them to disk
from datetime import datetime

app = Flask(__name__)

# Load the dataset once at startup
try:
    df_bmi = pd.read_csv("BMI_Diet_Recommendations_Corrected.csv")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    df_bmi = pd.DataFrame()  # Fallback if the file fails to load

def calculate_bmi(height, weight):
    try:
        return round(weight / (height ** 2), 2)
    except ZeroDivisionError:
        return None

def determine_bmi_category(bmi):
    if bmi is None:
        return "Invalid"
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def format_recommendations_bmi(row):
    """
    Format recommendations in a structured format for JSON response.
    """
    row = row.fillna('N/A')  # Fill missing values with 'N/A'
    diet_plan = row['Example Diet Plan']
    meals = diet_plan.split('; ') # list
    return {
        "Category": row['Category'],
        "Health Implications": row['Health Implications'],
        "Diet Tips": row['Diet Tips'],
        "Examples of Foods": row['Examples of Foods'],
        "Exercise Routine": row['Exercise Routine'],
        "Lifestyle Tips": row['Lifestyle Tips'],
        "Snack Ideas": row['Snack Ideas'],
        "Hydration Tips": row['Hydration Tips'],
        "Supplements": row['Supplements'],
        "Cooking Tips": row['Cooking Tips'],
        "Daily Calorie Range": row['Daily Calorie Range'],
        "Example Diet Plan": meals
    }

@app.route("/", methods=["GET", "POST"])
def bmi():
    if request.method == "GET":
        return render_template("bmi.html")  # Render the HTML page

    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        height = data.get("height")
        weight = data.get("weight")

        if not isinstance(height, (int, float)) or not isinstance(weight, (int, float)):
            return jsonify({"error": "Height and weight must be numbers"}), 400

        bmi_value = calculate_bmi(height, weight)
        category = determine_bmi_category(bmi_value)
        row = df_bmi[df_bmi['Category'] == category].iloc[0]
        recommendations_bmi = format_recommendations_bmi(row)
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Return all data from format_recommendations
        return jsonify({
            "height": height,
            "weight": weight,
            "current_date": current_date,
            "bmi": bmi_value,
            "category": category,
            "recommendations_bmi": recommendations_bmi
        })



@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Extract data
    height = data.get("height", "N/A")
    weight = data.get("weight", "N/A")
    current_date = data.get("current_date", datetime.now().strftime("%Y-%m-%d"))
    bmi = data.get("bmi", "N/A")
    category = data.get("category", "N/A")
    recommendations_bmi = data.get("recommendations_bmi", {})

    # Render HTML template for PDF
    rendered_html = render_template(
        "pdf_template.html", 
        height=height,
        weight=weight,
        bmi=bmi, 
        category=category, 
        recommendations_bmi=recommendations_bmi,
        current_date=current_date
    )

    # Generate PDF
    # io.BytesIO(): Creates an in-memory binary stream to hold the PDF output.
    # pisa.CreatePDF:
    # Converts the rendered HTML into a PDF.
    # The io.StringIO(rendered_html) provides the HTML content to pisa.
    # The dest=pdf_output specifies the output destination as the in-memory binary stream (pdf_output).
   
    pdf_output = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(rendered_html), dest=pdf_output)

    if pisa_status.err:
        return jsonify({"error": "Failed to generate PDF"}), 500

    pdf_output.seek(0) #Resets the stream's pointer to the beginning to ensure the PDF file is read from the start.
    return send_file(pdf_output, download_name="BMI_Report.pdf", as_attachment=True) #Sends the PDF file to the client.....as_attachment=True Ensures the file is downloaded rather than displayed in the brow

if __name__ == "__main__":
    app.run(debug=True)