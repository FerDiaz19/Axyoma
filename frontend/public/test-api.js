// Script de prueba para la API de evaluaciones oficiales
// Ejecutar en la consola del navegador

// Función para probar la conexión con la API
async function probarAPI() {
  console.log('🧪 Iniciando pruebas de API...');
  
  try {
    // Probar GET - obtener preguntas existentes
    console.log('📥 Probando GET preguntas NOM-035...');
    const response = await fetch('http://localhost:8000/api/evaluaciones/oficial/normativa/nom_035/');
    const data = await response.json();
    console.log('✅ GET exitoso:', data.total_preguntas, 'preguntas encontradas');
    
    // Probar POST - crear nueva pregunta
    console.log('📤 Probando POST nueva pregunta...');
    const nuevaPregunta = {
      texto: "¿Pregunta de prueba desde JavaScript?",
      tipo: "multiple",
      opciones: ["Sí", "No", "Tal vez"],
      obligatoria: true,
      normativa: "nom_035"
    };
    
    const postResponse = await fetch('http://localhost:8000/api/evaluaciones/oficial/preguntas-oficiales/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(nuevaPregunta)
    });
    
    if (postResponse.ok) {
      const preguntaCreada = await postResponse.json();
      console.log('✅ POST exitoso:', preguntaCreada);
      return preguntaCreada.id;
    } else {
      const error = await postResponse.text();
      console.error('❌ Error POST:', postResponse.status, error);
    }
    
  } catch (error) {
    console.error('❌ Error de conexión:', error);
  }
}

// Función para probar el servicio de React
async function probarServicioReact() {
  console.log('⚛️ Probando servicio React...');
  
  try {
    // Importar el servicio (esto funcionará solo si está en el contexto de React)
    const { evaluacionesOficialesAPI } = await import('./services/evaluacionesOficialesAPI');
    
    console.log('📥 Obteniendo preguntas NOM-035 via servicio React...');
    const preguntas = await evaluacionesOficialesAPI.getPreguntasPorNormativa('nom_035');
    console.log('✅ Servicio React funciona:', preguntas.total_preguntas, 'preguntas');
    
    console.log('📤 Creando pregunta via servicio React...');
    const nuevaPregunta = await evaluacionesOficialesAPI.crearPregunta({
      texto: "¿Pregunta de prueba desde servicio React?",
      tipo: "multiple",
      opciones: ["Opción 1", "Opción 2"],
      obligatoria: true,
      normativa: "nom_035"
    });
    console.log('✅ Pregunta creada via React:', nuevaPregunta);
    
  } catch (error) {
    console.error('❌ Error en servicio React:', error);
  }
}

console.log('🧪 Scripts de prueba cargados. Ejecuta:');
console.log('  probarAPI() - para probar conexión directa');
console.log('  probarServicioReact() - para probar servicio React');
