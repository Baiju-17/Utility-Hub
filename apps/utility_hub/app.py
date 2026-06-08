import streamlit as st
from PIL import Image
import io
import os
from pdf2docx import Converter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Page Configuration
st.set_page_config(page_title="Utility Hub - PDF & Image Pro", layout="wide", page_icon="🛠️")

# --- UI FIX: Custom CSS for Visibility and Contrast ---
st.markdown("""
    <style>
    /* Force Sidebar Text Visibility */
    [data-testid="stSidebar"] .st-emotion-cache-17l69k, 
    [data-testid="stSidebar"] .st-emotion-cache-6q9sum,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #111111 !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 1px solid #e0e0e0;
    }

    /* Main Background and Buttons */
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.2em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🛠️ Utility Hub")
menu = ["Home", "Image to PDF", "Image Resizer & Compressor", "PDF to Word", "Text to PDF"]
choice = st.sidebar.radio("Navigation", menu)

# --- Home Page ---
if choice == "Home":
    st.title("🚀 All-in-One PDF & Image Utility Hub")
    st.write("A professional-grade tool for your daily document and image processing needs.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🖼️ **Image Tools**\n- **Image to PDF:** Combine multiple photos into a single PDF.\n- **Resizer & Compressor:** Shrink file size without losing essential quality.")
    with col2:
        st.success("📄 **PDF Tools**\n- **PDF to Word:** Extract editable text from PDF documents.\n- **Text to PDF:** Create high-quality PDFs from simple text or TXT files.")

# --- Image to PDF ---
elif choice == "Image to PDF":
    st.title("🖼️ Image to PDF Converter")
    st.markdown("Combine multiple images into a single professional PDF document.")
    uploaded_files = st.file_uploader("Upload Images (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("Generate Combined PDF"):
            images = []
            for uploaded_file in uploaded_files:
                img = Image.open(uploaded_file).convert("RGB")
                images.append(img)
            
            if images:
                pdf_buffer = io.BytesIO()
                images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
                st.success("✅ PDF Generated Successfully!")
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_buffer.getvalue(),
                    file_name="converted_images_hub.pdf",
                    mime="application/pdf"
                )

# --- FEATURE FIX: Image Resizer & Compressor ---
elif choice == "Image Resizer & Compressor":
    st.title("📏 Image Resizer & Compressor")
    st.markdown("Optimized compression that respects quality and handles all formats correctly.")
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        original_img = Image.open(uploaded_file)
        original_size = len(uploaded_file.getvalue()) / 1024 # KB
        
        st.image(original_img, caption=f"Original Image ({original_size:.2f} KB)", use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            quality = st.slider("Compression Quality (Lower = Smaller File)", 1, 100, 70)
        with col2:
            max_width = st.number_input("Maximum Width (0 for original)", value=0, help="If set, image will be scaled down to this width while maintaining aspect ratio.")
        
        if st.button("Process & Compress"):
            # 1. Convert to RGB (Crucial for PNG/RGBA to JPEG conversion)
            img = original_img.convert("RGB")
            
            # 2. Resize Logic (Dimension reduction if requested or too large)
            current_width, current_height = img.size
            if max_width > 0 and current_width > max_width:
                scale_ratio = max_width / current_width
                new_height = int(current_height * scale_ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # 3. Save with strict quality parameter
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="JPEG", quality=quality, optimize=True)
            
            compressed_size = len(img_buffer.getvalue()) / 1024 # KB
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            # 4. Success summary
            st.success(f"✅ Compression Complete!")
            st.write(f"📊 **Summary:** Original: {original_size:.2f} KB → Compressed: {compressed_size:.2f} KB (Reduced by {reduction:.1f}%)")
            
            st.download_button(
                label="📥 Download Optimized Image",
                data=img_buffer.getvalue(),
                file_name=f"compressed_{uploaded_file.name.split('.')[0]}.jpg",
                mime="image/jpeg"
            )

# --- PDF to Word ---
elif choice == "PDF to Word":
    st.title("📄 PDF to Word Converter")
    st.markdown("Convert PDF documents into editable Word (.docx) files.")
    uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])
    
    if uploaded_file:
        if st.button("Convert to Editable Word"):
            with st.spinner("Converting... please wait."):
                # Save PDF temporarily
                with open("temp_convert.pdf", "wb") as f:
                    f.write(uploaded_file.read())
                
                try:
                    cv = Converter("temp_convert.pdf")
                    cv.convert("output_hub.docx", start=0, end=None)
                    cv.close()
                    
                    with open("output_hub.docx", "rb") as f:
                        st.success("✅ Conversion Successful!")
                        st.download_button(
                            label="📥 Download Word Document",
                            data=f.read(),
                            file_name=f"{uploaded_file.name.split('.')[0]}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    
                    # Cleanup
                    if os.path.exists("temp_convert.pdf"): os.remove("temp_convert.pdf")
                    if os.path.exists("output_hub.docx"): os.remove("output_hub.docx")
                except Exception as e:
                    st.error(f"❌ An error occurred during conversion: {e}")

# --- Text to PDF ---
elif choice == "Text to PDF":
    st.title("✍️ Text to PDF Generator")
    st.markdown("Create a clean, formatted PDF from text input or uploaded text files.")
    text_input = st.text_area("Type or Paste Content:", height=300, placeholder="Start typing here...")
    uploaded_txt = st.file_uploader("Or upload a .txt file", type=["txt"])
    
    if uploaded_txt:
        text_input = uploaded_txt.read().decode("utf-8")
        st.text_area("File Preview:", value=text_input, height=150)

    if st.button("Generate PDF Document"):
        if text_input.strip():
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            width, height = letter
            
            # Basic Formatting
            c.setFont("Helvetica", 11)
            lines = text_input.split('\n')
            y = height - 50
            margin = 50
            
            for line in lines:
                if y < 50: # New Page
                    c.showPage()
                    c.setFont("Helvetica", 11)
                    y = height - 50
                
                # Simple line splitting for long text
                if len(line) > 90:
                    chunks = [line[i:i+90] for i in range(0, len(line), 90)]
                    for chunk in chunks:
                        c.drawString(margin, y, chunk)
                        y -= 15
                else:
                    c.drawString(margin, y, line)
                    y -= 15
            
            c.save()
            st.success("✅ PDF Created!")
            st.download_button(
                label="📥 Download Generated PDF",
                data=pdf_buffer.getvalue(),
                file_name="hub_text_document.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ Please provide some text content first.")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("⚡ Powered by Python & Streamlit")
