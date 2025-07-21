// Script para probar la creación de plantas desde el frontend con las nuevas credenciales

const apiUrl = 'http://localhost:8000/api';

// 1. Login como admin_empresa
async function loginAdmin() {
    const response = await fetch(`${apiUrl}/auth/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: 'admin_empresa',
            password: 'admin123'
        })
    });
    
    const data = await response.json();
    return data.token;
}

// 2. Crear una nueva planta
async function crearPlanta(token) {
    const response = await fetch(`${apiUrl}/plantas/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
        },
        body: JSON.stringify({
            nombre: 'Planta Frontend Test',
            direccion: 'Av. Frontend 999'
        })
    });
    
    if (response.ok) {
        const data = await response.json();
        console.log('✅ Planta creada exitosamente:');
        console.log('📋 Datos de la planta:', {
            id: data.planta_id,
            nombre: data.nombre,
            direccion: data.direccion,
            empresa: data.empresa_nombre
        });
        
        if (data.credenciales_usuario_planta) {
            console.log('🔑 CREDENCIALES DE ACCESO:');
            console.log('   👤 Usuario:', data.credenciales_usuario_planta.usuario);
            console.log('   🔒 Contraseña:', data.credenciales_usuario_planta.password);
            console.log('   🆔 Admin ID:', data.credenciales_usuario_planta.admin_planta_id);
        }
        
        return data;
    } else {
        console.error('❌ Error creando planta:', await response.text());
        return null;
    }
}

// 3. Probar login con el usuario de planta
async function probarLoginPlanta(credenciales) {
    console.log('\n🧪 Probando login con usuario de planta...');
    
    const response = await fetch(`${apiUrl}/auth/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: credenciales.usuario,
            password: credenciales.password
        })
    });
    
    if (response.ok) {
        const loginData = await response.json();
        console.log('✅ Login exitoso del usuario de planta');
        console.log('   🎫 Token:', loginData.token.substring(0, 20) + '...');
        console.log('   👤 Nombre:', loginData.first_name, loginData.last_name);
        return loginData.token;
    } else {
        console.error('❌ Error en login de planta:', await response.text());
        return null;
    }
}

// Función principal
async function main() {
    try {
        console.log('🚀 Iniciando prueba de creación de planta con credenciales\n');
        
        // Login admin
        console.log('1. Iniciando sesión como admin_empresa...');
        const adminToken = await loginAdmin();
        if (!adminToken) {
            console.error('❌ Error en login de admin');
            return;
        }
        console.log('✅ Admin logueado correctamente\n');
        
        // Crear planta
        console.log('2. Creando nueva planta...');
        const plantaData = await crearPlanta(adminToken);
        if (!plantaData || !plantaData.credenciales_usuario_planta) {
            console.error('❌ Error creando planta o no se generaron credenciales');
            return;
        }
        
        // Probar login de planta
        console.log('\n3. Probando acceso con usuario de planta...');
        const plantaToken = await probarLoginPlanta(plantaData.credenciales_usuario_planta);
        
        if (plantaToken) {
            console.log('\n🎉 ¡PRUEBA COMPLETADA EXITOSAMENTE!');
            console.log('✅ La planta se creó correctamente');
            console.log('✅ Se generaron las credenciales automáticamente');
            console.log('✅ El usuario de planta puede hacer login');
        }
        
    } catch (error) {
        console.error('❌ Error durante la prueba:', error);
    }
}

// Ejecutar si estamos en Node.js
if (typeof window === 'undefined') {
    main();
}
