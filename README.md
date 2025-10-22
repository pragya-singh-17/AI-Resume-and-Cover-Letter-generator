# Resume & Cover Letter Generator (Python/Streamlit)

A modern web application built with Python and Streamlit that generates professional resumes and cover letters using Google's Gemini AI.

## Features

- 📝 **Professional Resume Generation**: Create well-formatted PDF resumes
- 💼 **AI-Powered Cover Letters**: Generate compelling cover letters using Gemini AI
- 🎨 **Modern UI**: Clean, intuitive interface built with Streamlit
- 📄 **PDF Export**: Download both resume and cover letter as PDF files
- 🔄 **Multi-step Form**: Organized input process for better user experience
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `env.example` to `.env`
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

4. **Get a Gemini API key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

## Usage

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and go to `http://localhost:8501`

3. **Follow the steps**:
   - **Step 1**: Enter personal information
   - **Step 2**: Add skills and work experience
   - **Step 3**: Add education and job description
   - **Step 4**: Generate and download documents

## Project Structure

```
python-resume-generator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── env.example        # Environment variables template
├── .env               # Your environment variables (create this)
└── README.md          # This file
```

## Features in Detail

### Resume Generation
- Professional formatting with proper sections
- Customizable content (experience, education, skills)
- Clean, modern PDF output

### Cover Letter Generation
- AI-powered content using Gemini Pro
- Tailored to specific job descriptions
- Professional tone and structure
- 300-500 word length

### User Interface
- Step-by-step form process
- Real-time validation
- Progress tracking
- Responsive design

## API Configuration

The application uses Google's Gemini API for cover letter generation. Make sure to:

1. Have a valid API key
2. Set the key in your `.env` file
3. Ensure the key has access to Gemini Pro model

## Troubleshooting

### Common Issues

1. **"Gemini API key not configured"**
   - Make sure you have a `.env` file with your API key
   - Restart the application after adding the key

2. **"Error generating cover letter"**
   - Check if your API key is valid
   - Ensure you have internet connection
   - Verify the API key has proper permissions

3. **PDF download issues**
   - Make sure all required fields are filled
   - Check browser download settings

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your API key is working
3. Ensure all dependencies are installed correctly

## Dependencies

- **streamlit**: Web application framework
- **google-generativeai**: Google Gemini AI client
- **reportlab**: PDF generation
- **python-dotenv**: Environment variable management
- **requests**: HTTP requests
