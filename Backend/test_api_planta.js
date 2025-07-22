const axios = require('axios');

async function testPlantaCreation() {
    console.log('🧪 === PRUEBA DE CREACIÓN DE PLANTA VÍA API ===');
    
    try {
        // 1. Obtener token de autenticación (usar superuser)
        console.log('🔐 Obteniendo token de autenticación...');
        const loginResponse = await axios.post('http://localhost:8000/api/auth/login/', {
            email: 'admin@admin.com',
            password: 'admin123'
        });
        
        const token = loginResponse.data.access;
        console.log('✅ Token obtenido');
        
        // 2. Obtener lista de empresas
        console.log('🏢 Obteniendo empresas...');
        const empresasResponse = await axios.get('http://localhost:8000/api/empresas/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (empresasResponse.data.length === 0) {
            console.log('❌ No se encontraron empresas');
            return;
        }
        
        const empresa = empresasResponse.data[0];
        console.log(`🏢 Empresa seleccionada: ${empresa.nombre} (ID: ${empresa.empresa_id})`);
        
        // 3. Crear nueva planta
        console.log('🏭 Creando nueva planta...');
        const plantaData = {
            nombre: "Planta API Test " + Date.now(),
            direccion: "Dirección de prueba vía API",
            empresa: empresa.empresa_id,
            status: true
        };
        
        const plantaResponse = await axios.post('http://localhost:8000/api/plantas/', plantaData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        const plantaCreada = plantaResponse.data;
        console.log(`✅ Planta creada: ${plantaCreada.nombre} (ID: ${plantaCreada.planta_id})`);
        
        if (plantaCreada._credenciales_usuario) {
            console.log('👤 Credenciales de usuario creadas:');
            console.log(`   - Usuario: ${plantaCreada._credenciales_usuario.usuario}`);
            console.log(`   - Password: ${plantaCreada._credenciales_usuario.password}`);
        }
        
        // 4. Verificar departamentos y puestos creados
        console.log('📊 Verificando estructura creada...');
        
        // Obtener departamentos de la planta
        const deptResponse = await axios.get(`http://localhost:8000/api/departamentos/?planta=${plantaCreada.planta_id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log(`📁 Departamentos creados: ${deptResponse.data.length}`);
        
        // Contar puestos por departamento
        let totalPuestos = 0;
        for (const dept of deptResponse.data) {
            const puestosResponse = await axios.get(`http://localhost:8000/api/puestos/?departamento=${dept.departamento_id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            console.log(`  📁 ${dept.nombre}: ${puestosResponse.data.length} puestos`);
            totalPuestos += puestosResponse.data.length;
            
            // Mostrar primeros 3 puestos de cada departamento
            puestosResponse.data.slice(0, 3).forEach(puesto => {
                console.log(`    - ${puesto.nombre}`);
            });
        }
        
        console.log(`💼 Total puestos creados: ${totalPuestos}`);
        
        // 5. Limpiar - eliminar planta de prueba
        console.log('🧹 Limpiando datos de prueba...');
        await axios.delete(`http://localhost:8000/api/plantas/${plantaCreada.planta_id}/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log('✅ Planta de prueba eliminada');
        
    } catch (error) {
        console.error('❌ Error en prueba:', error.response?.data || error.message);
        if (error.response?.status === 401) {
            console.log('🔒 Error de autenticación. Verifica las credenciales.');
        }
    }
}

// Ejecutar prueba
testPlantaCreation();
