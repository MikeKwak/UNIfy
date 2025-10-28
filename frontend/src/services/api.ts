/**
 * API service for UNIfy Flask backend integration
 */

import { fetchAuthSession } from 'aws-amplify/auth';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://main.d1234567890.amplifyapp.com';

/**
 * Get authentication headers for API requests
 */
async function getAuthHeaders(): Promise<HeadersInit> {
  try {
    console.log('Attempting to get auth session...');
    const session = await fetchAuthSession();
    console.log('Auth session:', session);
    
    const token = session.tokens?.accessToken?.toString();
    console.log('Access token:', token ? 'Present' : 'Missing');
    
    if (token) {
      console.log('Using Bearer token for API request');
      return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      };
    } else {
      console.warn('No access token available, making request without authentication');
    }
  } catch (error) {
    console.error('Error getting auth token:', error);
  }
  
  return {
    'Content-Type': 'application/json',
  };
}

export interface StudentProfile {
  mental_health: string;
  physical_health: string;
  courses: string;
  gpa: number;
  severity: 'mild' | 'moderate' | 'severe';
}

export interface University {
  name: string;
  score: number;
  accessibility_rating: number;
  disability_support_rating: number;
  available_accommodations: string[];
  location: string;
  reason: string;
}

export interface RecommendationResponse {
  success: boolean;
  source: string;
  needed_accommodations: string[];
  recommendations: University[];
  error?: {
    code: string;
    message: string;
  };
}

/**
 * Get university recommendations from the Flask API
 */
export async function getRecommendations(profile: StudentProfile): Promise<RecommendationResponse> {
  try {
    console.log('API Base URL:', API_BASE_URL);
    console.log('Sending profile:', profile);

    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/api/recommendations`, {
      method: 'POST',
      headers,
      body: JSON.stringify(profile),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || `HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

/**
 * Test the API connection
 */
export async function testAPI(): Promise<any> {
  try {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/api/test`, {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Test Error:', error);
    throw error;
  }
}

/**
 * Get recommendations directly from Gemini AI
 */
export async function getGeminiRecommendations(profile: StudentProfile): Promise<RecommendationResponse> {
  try {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/api/gemini`, {
      method: 'POST',
      headers,
      body: JSON.stringify(profile),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || `HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Gemini API Error:', error);
    throw error;
  }
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<any> {
  try {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Health Check Error:', error);
    throw error;
  }
}
