/**
 * Script para probar la conexión con el backend (ESM Version)
 * Ejecutar con: node testConnection.mjs
 */

import fetch from 'node-fetch';

async function testBackendConnection() {
  const ports = [8000, 8001, 8080];
  console.log("🔍 Probando conexión con backend...");
  
  for (const port of ports) {
    try {
      console.log(`\nIntentando conectar a puerto ${port}...`);
      const response = await fetch(`http://localhost:${port}/api/health-check/`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      });
      
      if (response.ok) {
        console.log(`✅ ÉXITO: Servidor encontrado en puerto ${port}`);
        return port;
      } else {
        console.log(`⚠️ Servidor en puerto ${port} responde con error: ${response.status}`);
      }
    } catch (error) {
      console.log(`❌ No se pudo conectar al puerto ${port}: ${error.message}`);
    }
  }
  
  console.log("\n⚠️ No se encontró ningún servidor activo. Verifica que Django esté corriendo.");
  return null;
}

// Auto-ejecutar
(async () => {
  try {
    const port = await testBackendConnection();
    if (port) {
      console.log("\n=================================");
      console.log(`✅ Backend disponible en puerto ${port}`);
      console.log("=================================");
    } else {
      console.log("\n=================================");
      console.log("❌ No se detectó ningún backend activo");
      console.log("=================================");
    }
  } catch (err) {
    console.error("❌ Error ejecutando prueba:", err);
  }
})();
