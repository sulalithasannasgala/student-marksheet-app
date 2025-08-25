import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        'Name', 'Subject1', 'Subject2', 'Subject3', 'Subject4', 'Subject5',
        'Subject6', 'Subject7', 'Subject8', 'Subject9', 'Subject10',
        'Total', 'Average', 'Rank'
    ])
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# PDF generation function
def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Student Marksheet Report", ln=True, align='C')
    pdf.ln(10)

    # Header row
    for col in df.columns:
        pdf.cell(20, 10, txt=str(col), border=1)
    pdf.ln()

    # Data rows
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(20, 10, txt=str(item), border=1)
        pdf.ln()

    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()

# Title
st.title("📘 Student Marksheet App with PDF Export")

# Entry form
if not st.session_state.submitted:
    with st.form("entry_form"):
        name = st.text_input("Student Name")
        subjects = [st.text_input(f"Subject {i+1}") for i in range(10)]
        submitted = st.form_submit_button("Submit")

        if submitted and name:
            try:
                marks = [float(m) if m.strip() else 0.0 for m in subjects]
            except ValueError:
                st.error("❌ All marks must be numeric.")
                st.stop()

            total = sum(marks)
            count = sum(1 for m in subjects if m.strip())
            average = total / count if count else 0.0

            new_entry = {
                'Name': name,
                **{f'Subject{i+1}': subjects[i] for i in range(10)},
                'Total': total,
                'Average': average,
                'Rank': 0
            }

            st.session_state.data = pd.concat([
                st.session_state.data,
                pd.DataFrame([new_entry])
            ], ignore_index=True)

            st.session_state.data['Rank'] = st.session_state.data['Total'].rank(ascending=False, method='min').astype(int)
            st.success("✅ Entry submitted and ranked!")
            st.session_state.submitted = True

elif st.button("➕ Add Another Entry"):
    st.session_state.submitted = False

# Display entries
if not st.session_state.data.empty:
    st.subheader("📊 All Entries")
    st.dataframe(st.session_state.data)

    st.markdown(f"**Max Total:** {st.session_state.data['Total'].max():.2f} | **Average Total:** {st.session_state.data['Total'].mean():.2f}")

    # Search
    st.subheader("🔍 Search by Name")
    search_name = st.text_input("Enter name to search")
    if search_name:
        result = st.session_state.data[st.session_state.data['Name'].str.contains(search_name, case=False)]
        st.write(result if not result.empty else "No match found.")

    # PDF Export
    st.subheader("📄 Export to PDF")
    if st.button("Generate PDF"):
        pdf_bytes = generate_pdf(st.session_state.data)
        st.download_button(
            label="📥 Download Marksheet PDF",
            data=pdf_bytes,
            file_name="marksheet_report.pdf",
            mime="application/pdf"
        )
