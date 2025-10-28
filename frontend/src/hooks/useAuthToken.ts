import { useEffect, useState } from 'react';
import { fetchAuthSession } from 'aws-amplify/auth';

export const useAuthToken = () => {
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getToken = async () => {
      try {
        const session = await fetchAuthSession();
        const accessToken = session.tokens?.accessToken?.toString();
        setToken(accessToken || null);
      } catch (error) {
        console.error('Error fetching auth token:', error);
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    getToken();
  }, []);

  const refreshToken = async () => {
    setLoading(true);
    try {
      const session = await fetchAuthSession({ forceRefresh: true });
      const accessToken = session.tokens?.accessToken?.toString();
      setToken(accessToken || null);
    } catch (error) {
      console.error('Error refreshing auth token:', error);
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  return { token, loading, refreshToken };
};
