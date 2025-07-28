import React, { useState } from 'react';
import { registrarEmpresa, type RegistroEmpresaData } from '../services/empresaService';

interface RegisterProps {
  onNavigateToLogin: () => void;
}

const Register: React.FC<RegisterProps> = ({ onNavigateToLogin }) => {
  const [formData, setFormData] = useState<RegistroEmpresaData>({
    nombre: '',
    rfc: '',
    direccion: '',
    email_contacto: '',
    telefono_contacto: '',
    usuario: '',
    password: '',
    nombre_completo: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev: RegistroEmpresaData) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Limpiar errores previos
    setError('');
    setSuccessMessage('');
    
    // Validaciones básicas del frontend
    if (!formData.nombre.trim()) {
      setError('El nombre de la empresa es requerido');
      return;
    }
    
    if (!formData.email_contacto.trim()) {
      setError('El email de contacto es requerido');
      return;
    }
    
    if (!formData.usuario.trim()) {
      setError('El nombre de usuario es requerido');
      return;
    }
    
    if (!formData.password.trim()) {
      setError('La contraseña es requerida');
      return;
    }
    
    // Validar formato de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email_contacto)) {
      setError('Por favor ingrese un email válido');
      return;
    }
    
    setLoading(true);
    
    try {
      console.log('🔄 Enviando formulario de registro...');
      const result = await registrarEmpresa(formData);
      
      setSuccessMessage(`¡Registro exitoso! La empresa "${result.nombre}" ha sido registrada correctamente.`);
      
      // Limpiar formulario
      setFormData({
        nombre: '',
        rfc: '',
        direccion: '',
        email_contacto: '',
        telefono_contacto: '',
        usuario: '',
        password: '',
        nombre_completo: ''
      });
      
      // Redirigir después de 2 segundos
      setTimeout(() => {
        onNavigateToLogin();
      }, 2000);
      
    } catch (error: any) {
      console.error('❌ Error en registro:', error);
      
      // Mostrar el mensaje de error mejorado
      setError(error.message || 'Error desconocido al registrar la empresa');
      
      // Scroll hacia arriba para mostrar el error
      window.scrollTo({ top: 0, behavior: 'smooth' });
      
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-form">
        <h2>Registro de Empresa</h2>
        
        {error && (
          <div className="error-message" style={{ 
            marginBottom: '20px', 
            padding: '15px', 
            backgroundColor: '#fee', 
            border: '1px solid #fcc',
            borderRadius: '5px',
            color: '#c33'
          }}>
            <strong>⚠️ Error:</strong>
            <br />
            {error}
            <br />
            <small style={{ marginTop: '10px', display: 'block', color: '#666' }}>
              Si el problema persiste, puede intentar:
              <ul style={{ marginTop: '5px', paddingLeft: '20px' }}>
                <li>Usar un email diferente</li>
                <li>Elegir otro nombre de usuario</li>
                <li>Verificar que no tenga una cuenta existente</li>
                <li>Contactar al soporte técnico</li>
              </ul>
            </small>
          </div>
        )}

        {successMessage && (
          <div className="success-message" style={{ 
            marginBottom: '20px', 
            padding: '15px', 
            backgroundColor: '#dfd', 
            border: '1px solid #9c9',
            borderRadius: '5px',
            color: '#060'
          }}>
            <strong>✅ Éxito:</strong>
            <br />
            {successMessage}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="nombre">Nombre de la Empresa *</label>
            <input
              type="text"
              id="nombre"
              name="nombre"
              value={formData.nombre}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="rfc">RFC</label>
            <input
              type="text"
              id="rfc"
              name="rfc"
              value={formData.rfc}
              onChange={handleInputChange}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email_contacto">Email de Contacto *</label>
            <input
              type="email"
              id="email_contacto"
              name="email_contacto"
              value={formData.email_contacto}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="telefono_contacto">Teléfono de Contacto</label>
            <input
              type="tel"
              id="telefono_contacto"
              name="telefono_contacto"
              value={formData.telefono_contacto}
              onChange={handleInputChange}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="direccion">Dirección</label>
            <textarea
              id="direccion"
              name="direccion"
              value={formData.direccion}
              onChange={handleInputChange}
              rows={3}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="nombre_completo">Nombre Completo del Administrador *</label>
            <input
              type="text"
              id="nombre_completo"
              name="nombre_completo"
              value={formData.nombre_completo}
              onChange={handleInputChange}
              required
              disabled={loading}
              placeholder="Nombre Apellido Paterno Apellido Materno"
            />
          </div>

          <div className="form-group">
            <label htmlFor="usuario">Nombre de Usuario *</label>
            <input
              type="text"
              id="usuario"
              name="usuario"
              value={formData.usuario}
              onChange={handleInputChange}
              required
              disabled={loading}
              placeholder="Usuario para acceder al sistema"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña *</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              disabled={loading}
              placeholder="Contraseña para acceder al sistema"
            />
          </div>

          <div className="form-actions">
            <button 
              type="submit" 
              disabled={loading}
              className="btn-primary"
            >
              {loading ? 'Registrando...' : 'Registrar Empresa'}
            </button>
            
            <button 
              type="button" 
              onClick={onNavigateToLogin}
              disabled={loading}
              className="btn-secondary"
            >
              Volver al Login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
