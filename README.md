# UNIfy

A university accommodation recommendation system that helps students with disabilities find universities that best match their needs.

## Project Structure

```
UNIfy/
├── frontend/           # React + TypeScript frontend
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API service layer
│   │   └── ...
│   ├── public/         # Static assets
│   ├── package.json    # Frontend dependencies
│   └── vite.config.ts  # Vite configuration
├── server/             # Flask API server
│   ├── app.py         # Main Flask application
│   ├── requirements.txt # Python dependencies
│   ├── Procfile       # Heroku deployment config
│   └── Unify.db       # SQLite database
├── package.json        # Root package.json for scripts
└── README.md          # This file
```

## Features

- **Student Profile Input**: Collect student information including mental health, physical health, courses, GPA, and severity level
- **AI-Powered Recommendations**: Get personalized university recommendations using Google's Gemini AI
- **Intelligent Fallback**: Automatic fallback to mock recommendations if AI service is unavailable
- **Accessibility Focus**: Designed with accessibility in mind for students with disabilities
- **Clean Architecture**: Separated frontend and backend for maintainability

## Quick Start

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd UNIfy
   ```

2. **Install all dependencies**
   ```bash
   npm run install:all
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   # Add your Gemini API key: GEMINI_API_KEY=your_api_key_here
   ```

### Development

**Start both frontend and server:**
```bash
npm run dev
```

**Start only frontend:**
```bash
npm run dev:frontend
```

**Start only server:**
```bash
npm run dev:server
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

### Building for Production

```bash
npm run build
```

## API Endpoints

### Health Check
- **GET** `/` - Server health status

### Recommendations
- **POST** `/api/recommendations` - Get university recommendations (uses Gemini AI with fallback)
- **POST** `/api/gemini` - Get recommendations directly from Gemini AI
- **GET** `/api/test` - Test endpoint with sample data

### Example Request

```json
POST /api/recommendations
{
  "mental_health": "ADHD",
  "physical_health": "None",
  "courses": "Computer Science",
  "gpa": 3.8,
  "severity": "moderate"
}
```

### Example Response

```json
{
  "success": true,
  "source": "gemini_ai",
  "needed_accommodations": ["Extended time", "Academic coaching"],
  "recommendations": [
    {
      "name": "University of Toronto",
      "score": 4.3,
      "accessibility_rating": 4.5,
      "disability_support_rating": 4.7,
      "available_accommodations": ["Extended time", "Note-taking services"],
      "location": "Ontario",
      "reason": "Strong disability services"
    }
  ]
}
```

## Technology Stack

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Router** - Client-side routing

### Backend
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Google Gemini AI** - AI-powered recommendations
- **SQLite** - Database (for future use)

## Development Notes

### Current Scope
This is the first scope of the project, focusing on:
- Clean project structure
- Basic UI/UX for student input
- AI-powered recommendations using Gemini
- Intelligent fallback system
- API foundation for future enhancements

### Future Enhancements
- Machine learning integration for personalized recommendations
- Real university data integration
- User authentication and profiles
- Advanced filtering and search
- Mobile responsiveness improvements

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
