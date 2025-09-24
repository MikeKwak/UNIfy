# Gemini AI Integration for UNIfy

## Overview

The UNIfy system now includes Gemini AI as a fallback recommendation system. This ensures that users always receive high-quality university and accommodation recommendations, even when the ML pipeline encounters edge cases or insufficient data.

## How It Works

### 1. Primary System: ML Pipeline
- First attempts to use the trained ML models
- Provides personalized recommendations based on historical data
- Fast and efficient for common cases

### 2. Fallback System: Gemini AI
- Activates when ML recommendations are insufficient or fail
- Provides intelligent recommendations using Google's Gemini AI
- Handles edge cases and rare disability combinations

## Integration Points

The Gemini AI fallback is triggered in these scenarios:

1. **Insufficient ML Results**: When ML pipeline returns fewer than 2 recommendations
2. **Empty Results**: When ML pipeline returns no recommendations
3. **ML Pipeline Failure**: When the ML system encounters an error
4. **Emergency Fallback**: As a last resort when all other methods fail

## Setup Instructions

### Option 1: With Gemini API Key (Recommended)

1. **Get a Gemini API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key

2. **Set Environment Variable**:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

3. **Test the Integration**:
   ```python
   from ml_pipeline import get_recommendations
   
   result = get_recommendations({
       'mental_health': 'ADHD',
       'physical_health': 'None',
       'courses': 'Computer Science',
       'gpa': 3.8,
       'severity': 'moderate'
   })
   
   print(f"Source: {result.get('source')}")  # Will show 'gemini_ai' if fallback used
   ```

### Option 2: Without API Key (Default Fallback)

If no API key is provided, the system uses intelligent default recommendations:
- Pre-defined high-quality university recommendations
- Context-aware accommodation suggestions
- Still provides excellent results without API costs

## API Response Format

The system returns consistent responses regardless of the source:

```python
{
    'success': True,
    'source': 'ml_pipeline' | 'gemini_ai' | 'default_fallback',
    'needed_accommodations': [
        'Extended time on exams',
        'Academic coaching',
        'Quiet testing environment'
    ],
    'recommendations': [
        {
            'name': 'University of Toronto',
            'score': 4.3,
            'accessibility_rating': 4.5,
            'disability_support_rating': 4.7,
            'available_accommodations': ['Extended time', 'Note-taking services'],
            'location': 'Ontario',
            'reason': 'Strong disability services and comprehensive support'
        }
    ]
}
```

## Testing the Integration

### Test Scripts

1. **Basic Test**:
   ```bash
   python3 test_gemini_fallback.py
   ```

2. **Direct Gemini Test**:
   ```python
   from gemini_recommender import get_gemini_recommendations
   
   result = get_gemini_recommendations(student_profile)
   ```

### Test Scenarios

The system has been tested with:
- Normal student profiles (uses ML pipeline)
- Edge cases with rare disabilities (may use Gemini fallback)
- Completely empty scenarios (uses default fallback)
- ML pipeline failures (uses emergency fallback)

## Benefits

### 1. Reliability
- System never fails to provide recommendations
- Multiple layers of fallback ensure 100% uptime

### 2. Quality
- Gemini AI provides intelligent, context-aware recommendations
- Handles edge cases that ML models might miss

### 3. Cost-Effective
- Only uses Gemini AI when necessary
- Default fallback provides good results without API costs

### 4. Transparency
- Response includes source information
- Easy to monitor which system provided recommendations

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google AI API key (optional)

### Fallback Triggers

You can modify the fallback triggers in `ml_pipeline.py`:

```python
# Current trigger: fewer than 2 recommendations
if not recommendations or len(recommendations) < 2:
    # Trigger Gemini fallback
```

### Custom Prompts

Modify prompts in `gemini_recommender.py` to customize:
- Accommodation recommendation logic
- University selection criteria
- Response format

## Monitoring

The system logs which recommendation source was used:

```
Using ML recommendations: 5 universities found
ML recommendations insufficient, trying Gemini AI fallback...
Using Gemini AI recommendations (source: gemini_ai)
```

## Error Handling

The system gracefully handles:
- Missing API keys
- API rate limits
- Network failures
- Invalid responses
- JSON parsing errors

## Future Enhancements

Potential improvements:
1. **Caching**: Cache Gemini responses to reduce API calls
2. **A/B Testing**: Compare ML vs Gemini recommendation quality
3. **Hybrid Approach**: Combine ML and AI recommendations
4. **Custom Models**: Fine-tune Gemini for specific disability types

## Troubleshooting

### Common Issues

1. **"Warning: No Gemini API key provided"**
   - Solution: Set `GEMINI_API_KEY` environment variable
   - Or ignore if you want to use default fallback

2. **"Gemini AI fallback failed"**
   - Check internet connection
   - Verify API key is valid
   - System will use default fallback

3. **"Failed to parse response"**
   - Gemini returned unexpected format
   - System automatically falls back to defaults

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Support

For issues with the Gemini integration:
1. Check the logs for specific error messages
2. Verify your API key and internet connection
3. Test with the provided test scripts
4. The system will always provide recommendations via fallback mechanisms
