// Utilidad para verificar el estado del servidor Backend
// ====================================================

export async function checkServerStatus(port: number = 8000): Promise<boolean> {
  try {
    console.log(`Verificando servidor en puerto ${port}...`);
    
    const response = await fetch(`http://localhost:${port}/api/health-check/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      console.log(`Servidor en puerto ${port} está ACTIVO`);
      return true;
    } else {
      console.warn(`Servidor en puerto ${port} respondió con código ${response.status}`);
      return false;
    }
  } catch (error) {
    console.error(`Servidor en puerto ${port} NO ESTÁ DISPONIBLE`);
    return false;
  }
}

export async function findBackendServer(): Promise<number | null> {
  const possiblePorts = [8000, 8001, 8080];
  
  for (const port of possiblePorts) {
    const isActive = await checkServerStatus(port);
    if (isActive) return port;
  }
  
  return null; // No se encontró ningún servidor activo
}


