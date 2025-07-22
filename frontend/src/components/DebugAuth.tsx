import React, { useState, useEffect } from 'react';
import api from '../api';

const DebugAuth: React.FC = () => {
  const [authInfo, setAuthInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('authToken');
        const userData = localStorage.getItem('userData');
        
        console.log('🔍 Token:', token);
        console.log('🔍 User Data:', userData);
        
        // Test API call
        const response = await api.get('/evaluaciones/evaluaciones/');
        console.log('🔍 API Response:', response);
        console.log('🔍 Response status:', response.status);
        console.log('🔍 Response headers:', response.headers);
        console.log('🔍 Response data:', response.data);
        
        setAuthInfo({
          token: token ? `${token.substring(0, 10)}...` : null,
          userData,
          apiResponse: response.data,
          hasToken: !!token,
          responseType: Array.isArray(response.data) ? 'array' : 'object',
          count: Array.isArray(response.data) ? response.data.length : (response.data.count || 0),
          status: response.status,
          url: response.config?.url
        });
      } catch (error: any) {
        console.error('❌ Auth check error:', error);
        console.error('❌ Error response:', error.response);
        setAuthInfo({ 
          error: error.message || 'Unknown error',
          status: error.response?.status,
          responseData: error.response?.data
        });
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) return <div>Checking auth...</div>;

  return (
    <div style={{ 
      position: 'fixed', 
      top: 10, 
      right: 10, 
      background: 'white', 
      border: '1px solid #ccc',
      padding: '10px',
      zIndex: 9999,
      fontSize: '12px',
      maxWidth: '300px'
    }}>
      <h4>🔍 Debug Auth Info</h4>
      <pre>{JSON.stringify(authInfo, null, 2)}</pre>
    </div>
  );
};

export default DebugAuth;

// Force TypeScript to treat this as a module
export {};
