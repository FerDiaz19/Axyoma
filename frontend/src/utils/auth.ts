// Utilidad para manejar tokens de autenticación
export const getAuthToken = (): string | null => {
  // Prioridad: authToken, luego token para compatibilidad
  return localStorage.getItem('authToken') || localStorage.getItem('token');
};

export const isAuthenticated = (): boolean => {
  return !!getAuthToken();
};

export const getAuthHeaders = (): Record<string, string> => {
  const token = getAuthToken();
  return token ? {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  } : {
    'Content-Type': 'application/json'
  };
};

export const handleAuthError = (response: Response): boolean => {
  if (response.status === 401) {
    // Token inválido, limpiar datos y redirigir al login
    localStorage.removeItem('authToken');
    localStorage.removeItem('token');
    localStorage.removeItem('userData');
    localStorage.removeItem('empresaData');
    
    // Redirigir al login
    window.location.href = '/login';
    return true;
  }
  return false;
};
