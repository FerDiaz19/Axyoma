// Archivo de prueba para verificar que la API de evaluaciones funciona correctamente
import { evaluacionesOficialesAPI } from './services/evaluacionesOficialesAPI';

console.log("🚀 Iniciando prueba de API de evaluaciones...");

// Función de prueba
async function probarEvaluacionesAPI() {
  try {
    console.log("📥 Obteniendo evaluaciones...");
    const evaluaciones = await evaluacionesOficialesAPI.getEvaluaciones();
    
    console.log("✅ Evaluaciones obtenidas:", evaluaciones);
    console.log("🔢 Cantidad:", evaluaciones.length);
    
    if (evaluaciones.length > 0) {
      const primera = evaluaciones[0];
      console.log("📋 Primera evaluación:");
      console.log("  - ID:", primera.id);
      console.log("  - Nombre:", primera.nombre);
      console.log("  - Tipo norma:", primera.tipo_norma);
      console.log("  - Descripción:", primera.descripcion);
    }
  } catch (error) {
    console.error("❌ Error:", error);
  }
}

// Ejecutar prueba si está en el navegador
if (typeof window !== 'undefined') {
  probarEvaluacionesAPI();
}

export { probarEvaluacionesAPI };
