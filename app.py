import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_cover_letter(user_data, job_description):
    """Generate cover letter using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Generate a professional cover letter for the following candidate applying to this job:
        
        Candidate Information:
        - Name: {user_data['name']}
        - Email: {user_data['email']}
        - Phone: {user_data['phone']}
        - Current Role: {user_data.get('current_role', 'Not specified')}
        - Years of Experience: {user_data.get('years_of_experience', 'Not specified')}
        
        Key Skills: {', '.join(user_data.get('skills', [])) if user_data.get('skills') else 'Not specified'}
        
        Work Experience Summary:
        {chr(10).join([f"- {exp['title']} at {exp['company']} ({exp['duration']}): {exp['description']}" for exp in user_data.get('experience', [])]) if user_data.get('experience') else 'Not specified'}
        
        Education: {', '.join([f"{edu['degree']} from {edu['institution']}" for edu in user_data.get('education', [])]) if user_data.get('education') else 'Not specified'}
        
        Job Description:
        {job_description}
        
        Please generate a compelling, professional cover letter that:
        1. Addresses the hiring manager professionally
        2. Explains why the candidate is interested in this specific role
        3. Highlights relevant experience and skills that match the job requirements
        4. Shows enthusiasm and fit for the company
        5. Ends with a call to action for an interview
        6. Is between 300-500 words
        7. Uses a professional tone throughout
        
        Format the response as a proper cover letter with paragraphs and professional formatting.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating cover letter: {str(e)}")
        return None

def create_resume_pdf(user_data):
    """Create PDF resume using ReportLab"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_LEFT
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        alignment=TA_LEFT
    )
    
    normal_style = styles['Normal']
    
    # Header
    story.append(Paragraph(user_data['name'], title_style))
    story.append(Paragraph(user_data['email'], normal_style))
    story.append(Paragraph(user_data['phone'], normal_style))
    story.append(Spacer(1, 20))
    
    # Professional Summary
    if user_data.get('summary'):
        story.append(Paragraph('PROFESSIONAL SUMMARY', heading_style))
        story.append(Paragraph(user_data['summary'], normal_style))
        story.append(Spacer(1, 12))
    
    # Work Experience
    if user_data.get('experience'):
        story.append(Paragraph('PROFESSIONAL EXPERIENCE', heading_style))
        for exp in user_data['experience']:
            exp_title = f"{exp['title']} - {exp['company']}"
            story.append(Paragraph(exp_title, normal_style))
            story.append(Paragraph(exp['duration'], normal_style))
            story.append(Paragraph(f"• {exp['description']}", normal_style))
            story.append(Spacer(1, 12))
    
    # Education
    if user_data.get('education'):
        story.append(Paragraph('EDUCATION', heading_style))
        for edu in user_data['education']:
            edu_text = f"{edu['degree']} - {edu['institution']}"
            if edu.get('year'):
                edu_text += f" ({edu['year']})"
            story.append(Paragraph(edu_text, normal_style))
            story.append(Spacer(1, 6))
    
    # Skills
    if user_data.get('skills'):
        story.append(Paragraph('SKILLS', heading_style))
        skills_text = ', '.join(user_data['skills'])
        story.append(Paragraph(skills_text, normal_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_cover_letter_pdf(cover_letter_text, user_data):
    """Create PDF cover letter using ReportLab"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    normal_style = styles['Normal']
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        alignment=TA_LEFT
    )
    
    # Header
    story.append(Paragraph(user_data['name'], heading_style))
    story.append(Paragraph(user_data['email'], normal_style))
    story.append(Paragraph(user_data['phone'], normal_style))
    story.append(Spacer(1, 20))
    
    # Date
    today = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(today, normal_style))
    story.append(Spacer(1, 20))
    
    # Cover letter content
    paragraphs = cover_letter_text.split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            story.append(Paragraph(paragraph, normal_style))
            story.append(Spacer(1, 12))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def main():
    st.set_page_config(
        page_title="Resume & Cover Letter Generator",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Resume & Cover Letter Generator")
    st.markdown("Generate professional resumes and cover letters using AI")
    
    # Check if API key is configured
    if not os.getenv('GEMINI_API_KEY'):
        st.error("⚠️ Gemini API key not configured. Please create a `.env` file with your `GEMINI_API_KEY`.")
        st.stop()
    
    # Initialize session state
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'name': '',
            'email': '',
            'phone': '',
            'current_role': '',
            'years_of_experience': '',
            'summary': '',
            'skills': [],
            'experience': [],
            'education': [],
            'job_description': ''
        }
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        if st.button("Step 1: Personal Info", use_container_width=True):
            st.session_state.current_step = 1
        if st.button("Step 2: Skills & Experience", use_container_width=True):
            st.session_state.current_step = 2
        if st.button("Step 3: Education & Job", use_container_width=True):
            st.session_state.current_step = 3
        if st.button("Step 4: Generate", use_container_width=True):
            st.session_state.current_step = 4
        
        st.markdown("---")
        st.markdown("**Current Step:** " + str(st.session_state.current_step))
    
    # Step 1: Personal Information
    if st.session_state.current_step == 1:
        st.header("Step 1: Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.user_data['name'] = st.text_input(
                "Full Name *", 
                value=st.session_state.user_data['name'],
                placeholder="John Doe"
            )
            
            st.session_state.user_data['email'] = st.text_input(
                "Email *", 
                value=st.session_state.user_data['email'],
                placeholder="john.doe@email.com"
            )
            
            st.session_state.user_data['phone'] = st.text_input(
                "Phone *", 
                value=st.session_state.user_data['phone'],
                placeholder="+1 (555) 123-4567"
            )
        
        with col2:
            st.session_state.user_data['current_role'] = st.text_input(
                "Current Role", 
                value=st.session_state.user_data['current_role'],
                placeholder="Software Engineer"
            )
            
            st.session_state.user_data['years_of_experience'] = st.text_input(
                "Years of Experience", 
                value=st.session_state.user_data['years_of_experience'],
                placeholder="5"
            )
        
        st.session_state.user_data['summary'] = st.text_area(
            "Professional Summary",
            value=st.session_state.user_data['summary'],
            placeholder="Brief professional summary...",
            height=100
        )
        
        if st.button("Next: Skills & Experience", type="primary"):
            if st.session_state.user_data['name'] and st.session_state.user_data['email'] and st.session_state.user_data['phone']:
                st.session_state.current_step = 2
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")
    
    # Step 2: Skills & Experience
    elif st.session_state.current_step == 2:
        st.header("Step 2: Skills & Experience")
        
        # Skills
        skills_input = st.text_input(
            "Skills (comma-separated)",
            value=', '.join(st.session_state.user_data['skills']),
            placeholder="JavaScript, React, Node.js, Python, SQL"
        )
        st.session_state.user_data['skills'] = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        
        # Work Experience
        st.subheader("Work Experience")
        
        if 'experience' not in st.session_state:
            st.session_state.experience = []
        
        for i, exp in enumerate(st.session_state.user_data['experience']):
            with st.expander(f"Experience {i+1}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    exp['title'] = st.text_input(f"Job Title {i+1}", value=exp.get('title', ''), key=f"title_{i}")
                    exp['company'] = st.text_input(f"Company {i+1}", value=exp.get('company', ''), key=f"company_{i}")
                
                with col2:
                    exp['duration'] = st.text_input(f"Duration {i+1}", value=exp.get('duration', ''), key=f"duration_{i}", placeholder="2020 - Present")
                
                exp['description'] = st.text_area(f"Description {i+1}", value=exp.get('description', ''), key=f"desc_{i}", height=80)
                
                if st.button(f"Remove Experience {i+1}", key=f"remove_exp_{i}"):
                    st.session_state.user_data['experience'].pop(i)
                    st.rerun()
        
        if st.button("Add Experience"):
            st.session_state.user_data['experience'].append({
                'title': '', 'company': '', 'duration': '', 'description': ''
            })
            st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous: Personal Info"):
                st.session_state.current_step = 1
                st.rerun()
        
        with col2:
            if st.button("Next: Education & Job", type="primary"):
                st.session_state.current_step = 3
                st.rerun()
    
    # Step 3: Education & Job Description
    elif st.session_state.current_step == 3:
        st.header("Step 3: Education & Job Description")
        
        # Education
        st.subheader("Education")
        
        for i, edu in enumerate(st.session_state.user_data['education']):
            with st.expander(f"Education {i+1}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    edu['degree'] = st.text_input(f"Degree {i+1}", value=edu.get('degree', ''), key=f"degree_{i}")
                    edu['institution'] = st.text_input(f"Institution {i+1}", value=edu.get('institution', ''), key=f"institution_{i}")
                
                with col2:
                    edu['year'] = st.text_input(f"Year {i+1}", value=edu.get('year', ''), key=f"year_{i}", placeholder="2020")
                
                if st.button(f"Remove Education {i+1}", key=f"remove_edu_{i}"):
                    st.session_state.user_data['education'].pop(i)
                    st.rerun()
        
        if st.button("Add Education"):
            st.session_state.user_data['education'].append({
                'degree': '', 'institution': '', 'year': ''
            })
            st.rerun()
        
        # Job Description
        st.subheader("Job Description")
        st.session_state.user_data['job_description'] = st.text_area(
            "Paste the job description here",
            value=st.session_state.user_data['job_description'],
            placeholder="Paste the job description for which you want to generate a cover letter...",
            height=200
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous: Skills & Experience"):
                st.session_state.current_step = 2
                st.rerun()
        
        with col2:
            if st.button("Next: Generate Documents", type="primary"):
                st.session_state.current_step = 4
                st.rerun()
    
    # Step 4: Generate Documents
    elif st.session_state.current_step == 4:
        st.header("Step 4: Generate Documents")
        
        # Display summary
        st.subheader("Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Personal Info:**")
            st.write(f"Name: {st.session_state.user_data['name']}")
            st.write(f"Email: {st.session_state.user_data['email']}")
            st.write(f"Phone: {st.session_state.user_data['phone']}")
            st.write(f"Current Role: {st.session_state.user_data['current_role']}")
            st.write(f"Experience: {st.session_state.user_data['years_of_experience']} years")
        
        with col2:
            st.write("**Skills:**")
            st.write(', '.join(st.session_state.user_data['skills']))
            st.write(f"**Experience Entries:** {len(st.session_state.user_data['experience'])}")
            st.write(f"**Education Entries:** {len(st.session_state.user_data['education'])}")
        
        if st.button("Generate Resume & Cover Letter", type="primary"):
            with st.spinner("Generating documents..."):
                try:
                    # Generate cover letter
                    cover_letter_text = generate_cover_letter(
                        st.session_state.user_data, 
                        st.session_state.user_data['job_description']
                    )
                    
                    if cover_letter_text:
                        # Create PDFs
                        resume_pdf = create_resume_pdf(st.session_state.user_data)
                        cover_letter_pdf = create_cover_letter_pdf(cover_letter_text, st.session_state.user_data)
                        
                        # Display results
                        st.success("Documents generated successfully!")
                        
                        # Display cover letter
                        st.subheader("Generated Cover Letter")
                        st.text_area("Cover Letter", value=cover_letter_text, height=400, disabled=True)
                        
                        # Download buttons
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.download_button(
                                label="📄 Download Resume (PDF)",
                                data=resume_pdf.getvalue(),
                                file_name=f"{st.session_state.user_data['name'].replace(' ', '_')}_resume.pdf",
                                mime="application/pdf"
                            )
                        
                        with col2:
                            st.download_button(
                                label="📄 Download Cover Letter (PDF)",
                                data=cover_letter_pdf.getvalue(),
                                file_name=f"{st.session_state.user_data['name'].replace(' ', '_')}_cover_letter.pdf",
                                mime="application/pdf"
                            )
                        
                        # Copy cover letter text
                        st.text_area("Copy Cover Letter Text", value=cover_letter_text, height=200, disabled=True)
                        
                    else:
                        st.error("Failed to generate cover letter. Please check your API key and try again.")
                
                except Exception as e:
                    st.error(f"Error generating documents: {str(e)}")
        
        if st.button("Previous: Education & Job"):
            st.session_state.current_step = 3
            st.rerun()

if __name__ == "__main__":
    main() 