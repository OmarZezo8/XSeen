# Xseen - PLATFORM FOR EXOPLANETS DISCOVERY

Xseen is a web-based AI-powered platform for exoplanet exploration and classification. It combines machine learning with conversational AI to help users learn about exoplanets, detection methods, and classify potential exoplanet candidates.

## Features

- **XSeen-net AI Assistant**: An intelligent chatbot powered by Groq's Llama model that provides accurate information about exoplanets, detection methods, planetary characteristics, space missions, and astronomical discoveries
- **Exoplanet Classification**: A machine learning tool that classifies celestial objects as exoplanets, candidates, or non-exoplanets based on transit photometry data
- **Earth Comparison**: Compare exoplanet characteristics with Earth's values to assess similarity
- **Interactive Documentation**: Comprehensive documentation about exoplanets and the platform
- **Modern Web Interface**: Clean, responsive UI with real-time chat and classification results

## Project Structure

```
xseen/
├── app.py                 # Main Flask application
├── model.pkl              # Pre-trained ML classification model (~780MB)
├── requirements.txt       # Python dependencies
├── static/
│   ├── Logo.png          # Application logo
│   └── style.css         # Custom styles
└── templates/
    ├── app.html          # Main chat interface
    ├── classification.html # Classification form
    ├── contact.html      # Contact page
    └── documentation.html # Documentation page
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

The required packages are:
- flask
- groq
- numpy
- scikit-learn
- pandas
- joblib

3. **Configure API Key**:
   - The application currently uses a hardcoded Groq API key in `app.py` (line 12)
   - **Security Warning**: For production use, replace the hardcoded key with an environment variable:
   ```python
   api_key = os.environ.get('GROQ_API_KEY')
   ```
   - Set your environment variable:
   ```bash
   # Windows (PowerShell)
   $env:GROQ_API_KEY="your_api_key_here"
   
   # Windows (Command Prompt)
   set GROQ_API_KEY=your_api_key_here
   
   # Linux/Mac
   export GROQ_API_KEY="your_api_key_here"
   ```

4. **Ensure model.pkl is present**:
   - The `model.pkl` file contains the pre-trained classification model
   - This file is large (~780MB) and should be in the project root directory
   - You can get the model file from this link https://drive.google.com/drive/folders/1SsuxdIalEoDmyoSCwlLzDnYXVeyCQ6Es?usp=sharing

## Usage

### Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will run on `http://0.0.0.0:5000` by default.

### Accessing the Features

1. **Xseen-net AI Chat** (`http://localhost:5000/`):
   - Ask questions about exoplanets, detection methods, space missions, etc.
   - Use the suggestion cards for quick common questions
   - Responses are formatted with markdown

2. **Classification Tool** (`http://localhost:5000/classification`):
   - Enter the following parameters:
     - **Orbital Period** (days)
     - **Impact Parameter** (0-1)
     - **Transit Duration** (hours)
     - **Transit Depth** (percentage)
     - **Planet Radius** (Earth radii)
     - **Signal-to-Noise Ratio**
   - The ML model will classify the object and compare it to Earth

3. **Documentation** (`http://localhost:5000/documentation`):
   - Learn about exoplanets and detection methods

4. **Contact** (`http://localhost:5000/contact`):
   - Contact information page

## API Endpoints

### POST `/xeno`
Chat endpoint for the AI assistant.

**Request Body**:
```json
{
  "message": "Your question about exoplanets"
}
```

**Response**:
```json
{
  "response": "AI-generated response in markdown format"
}
```

### POST `/classify`
Classification endpoint for exoplanet detection.

**Request Body**:
```json
{
  "orbitalPeriod": 365.25,
  "impactParameter": 0.0,
  "transitDuration": 13.0,
  "transitDepth": 0.0084,
  "planetRadius": 1.0,
  "signalToNoise": 100.0
}
```

**Response**:
```json
{
  "prediction": 2,
  "result_type": "Confirmed Exoplanet",
  "description": "The data strongly indicates this is a confirmed exoplanet.",
  "earth_comparison": {
    "orbitalPeriod": {
      "value": 365.25,
      "earthValue": 365.25,
      "similarity": 100.0
    },
    ...
  }
}
```

**Classification Labels**:
- `0`: Not an Exoplanet
- `1`: Exoplanet Candidate
- `2`: Confirmed Exoplanet

## Machine Learning Model

The classification model uses transit photometry data to identify potential exoplanets. The model considers six key features:

1. **Orbital Period**: Time for one complete orbit around the host star
2. **Impact Parameter**: Geometric impact parameter of the transit (0-1)
3. **Transit Duration**: Length of the transit event in hours
4. **Transit Depth**: Fraction of stellar flux blocked during transit
5. **Planet Radius**: Size of the planet relative to Earth
6. **Signal-to-Noise Ratio**: Detection confidence metric

The model also provides Earth similarity comparisons for each parameter to help assess potential habitability.

## Technologies Used

- **Backend**: Flask (Python web framework)
- **AI/LLM**: Groq API with Meta Llama 4 Maverick 17B
- **Machine Learning**: scikit-learn, joblib
- **Data Processing**: NumPy, Pandas
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Markdown Rendering**: Marked.js

## Security Notes

⚠️ **Important Security Considerations**:

1. The API key is currently hardcoded in `app.py`. This is a security risk for production deployments.
2. Always use environment variables for sensitive credentials in production.
3. The application runs in debug mode by default. Disable this in production:
   ```python
   app.run(host="0.0.0.0", port=5000, debug=False)
   ```
4. Consider adding authentication and rate limiting for production use.

## Development

### Adding New Features

- Routes are defined in `app.py`
- HTML templates are in the `templates/` directory
- Static assets (CSS, images) are in the `static/` directory
- The ML model can be retrained and saved using joblib

### Customizing the AI

Modify the system prompt in `app.py` (line 62) to change the AI's behavior and knowledge domain.

## Troubleshooting

**Model fails to load**:
- Ensure `model.pkl` exists in the project root
- Check that all dependencies are installed correctly

**Groq API errors**:
- Verify your API key is valid
- Check your internet connection
- Ensure you have API quota available

**Port already in use**:
- Change the port in `app.py`:
  ```python
  app.run(host="0.0.0.0", port=5001, debug=True)
  ```

## License

This project is provided as-is for educational and research purposes.

## Acknowledgments

- Groq for providing the AI API
- NASA and the exoplanet science community for data and research
- The open-source community for the tools and libraries used
