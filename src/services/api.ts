// API Service for UNIfy Backend Integration 
const API_BASE_URL = 'http://127.0.0.1:5000'; // Flask server

export interface StudentProfile {
  mental_health: string;
  physical_health: string;
  courses: string;
  gpa: number;
  severity: string;
}

export interface RecommendationResult {
  success: boolean;
  source: string;
  needed_accommodations: string[];
  recommendations: University[];
  verification_summary?: {
    ml_count: number;
    ai_count: number;
    overlap_count: number;
    total_verified: number;
  };
}

export interface University {
  name: string;
  score: number;
  confidence?: string;
  accessibility_rating: number;
  disability_support_rating: number;
  available_accommodations: string[];
  location: string;
  reason: string;
}

// Step 1: Get initial ML-based recommendations from your database
export const getInitialRecommendations = async (studentProfile: StudentProfile): Promise<RecommendationResult> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(studentProfile),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to get initial recommendations: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting initial recommendations:', error);
    throw error;
  }
};

// Step 2: Verify results with LLM (Gemini AI)
export const verifyWithLLM = async (
  studentProfile: StudentProfile, 
  initialResults: RecommendationResult
): Promise<RecommendationResult> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/recommendations/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...studentProfile,
        initial_results: initialResults
      }),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to verify with LLM: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error verifying with LLM:', error);
    throw error;
  }
};

// Combined function that does both steps
export const generateRoadmapRecommendations = async (studentProfile: StudentProfile): Promise<RecommendationResult> => {
  try {
    // Step 1: Get initial ML recommendations from database
    console.log('Step 1: Getting initial ML recommendations...');
    const initialResults = await getInitialRecommendations(studentProfile);
    
    // Step 2: Verify and enhance with LLM
    console.log('Step 2: Verifying with LLM...');
    const verifiedResults = await verifyWithLLM(studentProfile, initialResults);
    
    return verifiedResults;
  } catch (error) {
    console.error('Error in roadmap generation:', error);
    throw error;
  }
};