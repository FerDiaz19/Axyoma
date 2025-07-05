-- Script de datos iniciales para pruebas del sistema Axyoma

-- Insertar datos de ejemplo en la base de datos después de las migraciones
-- Este script debe ejecutarse después de crear la base de datos y aplicar las migraciones de Django

-- NOTA: Los IDs de usuarios serán generados automáticamente por Django
-- Estos INSERTs son solo para referencia de la estructura

-- Ejemplo de empresa y empleados que se pueden crear a través del sistema:

/*
-- Usuario administrador de empresa (se crea automáticamente al registrar empresa)
-- Username: admin_codewave
-- Password: admin123
-- Email: admin@codewave.com

-- Empresa de ejemplo:
-- Nombre: CodeWave Solutions
-- RFC: CWS920314ABC
-- Dirección: Av. Tecnológico 123, Col. Innovación, Tijuana, BC
-- Email: contacto@codewave.com
-- Teléfono: 6641234567

-- Plantas de ejemplo (se deben crear manualmente o a través de la administración):
INSERT INTO plantas (nombre, direccion, empresa, fecha_registro, status) VALUES
('Oficina Principal Tijuana', 'Av. Tecnológico 123, Col. Innovación', 1, NOW(), TRUE),
('Sucursal Mexicali', 'Blvd. Benito Juárez 456, Centro', 1, NOW(), TRUE);

-- Departamentos de ejemplo:
INSERT INTO departamentos (nombre, descripcion, planta, fecha_registro, status) VALUES
('Desarrollo de Software', 'Equipo de desarrollo y programación', 1, NOW(), TRUE),
('Recursos Humanos', 'Gestión de personal y contrataciones', 1, NOW(), TRUE),
('Ventas', 'Equipo comercial y ventas', 2, NOW(), TRUE);

-- Puestos de ejemplo:
INSERT INTO puestos (nombre, descripcion, departamento, status) VALUES
('Desarrollador Senior', 'Programador con experiencia avanzada', 1, TRUE),
('Desarrollador Junior', 'Programador en formación', 1, TRUE),
('Gerente de RRHH', 'Responsable del área de recursos humanos', 2, TRUE),
('Ejecutivo de Ventas', 'Responsable de ventas y clientes', 3, TRUE);

-- Empleados de ejemplo (se crean a través del CRUD del sistema):
-- Estos se pueden agregar usando el formulario web una vez que el sistema esté funcionando
*/

-- Para facilitar las pruebas, aquí están los datos que puedes usar:

-- REGISTRO DE EMPRESA:
-- Nombre: CodeWave Solutions
-- RFC: CWS920314ABC
-- Dirección: Av. Tecnológico 123, Col. Innovación, Tijuana, BC
-- Email: contacto@codewave.com
-- Teléfono: 6641234567
-- Usuario Admin: admin_codewave
-- Password Admin: admin123
-- Nombre Admin: Juan Pérez García

-- LOGIN:
-- Usuario: admin_codewave
-- Password: admin123
