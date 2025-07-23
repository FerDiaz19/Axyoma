/**
 * Utilidad para verificar si el servidor backend está disponible
 */
export async function checkServerStatus(port: number = 8000): Promise<boolean> {
  try {
    console.log(`🔍 Verificando servidor en puerto ${port}...`);
    const response = await fetch(`http://localhost:${port}/api/health-check/`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      // Timeout corto para no bloquear la UI
      signal: AbortSignal.timeout(3000)
    });
    
    if (response.ok) {
      console.log(`✅ Servidor en puerto ${port} está ACTIVO`);
      return true;
    } else {
      console.warn(`⚠️ Servidor en puerto ${port} respondió con código ${response.status}`);
      return false;
    }
  } catch (error) {
    console.error(`❌ Servidor en puerto ${port} NO ESTÁ DISPONIBLE`);
    return false;
  }
}

/**
 * Verifica múltiples puertos posibles para encontrar el servidor
 */
export async function findBackendServer(): Promise<number | null> {
  const possiblePorts = [8000, 8001, 8080];
  
  for (const port of possiblePorts) {
    const isActive = await checkServerStatus(port);
    if (isActive) return port;
  }
  
  return null; // No se encontró ningún servidor activo
}
