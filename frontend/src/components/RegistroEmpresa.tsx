import React, { useState } from 'react';
import { registrarEmpresa } from '../services/empresaService';
import '../css/RegistroEmpresa.css';

interface RegistroEmpresaProps {
  onRegistroSuccess: () => void;
  onSwitchToLogin?: () => void;
}

const RegistroEmpresa: React.FC<RegistroEmpresaProps> = ({ onRegistroSuccess, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    rfc: '',
    direccion: '',
    logotipo: '',
    email_contacto: '',
    telefono_contacto: '',
    admin_username: '',
    admin_password: '',
    admin_email: '',
    admin_nombre: '',
    admin_apellido_paterno: '',
    admin_apellido_materno: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const registroData = {
        nombre: formData.nombre.trim(),
        rfc: formData.rfc.trim(),
        direccion: formData.direccion.trim(),
        email_contacto: formData.email_contacto.trim(),
        telefono_contacto: formData.telefono_contacto.trim(),
        usuario: formData.admin_username.trim(),
        password: formData.admin_password,
        nombre_completo: `${formData.admin_nombre} ${formData.admin_apellido_paterno} ${formData.admin_apellido_materno}`.trim()
      };

      console.log('Datos a enviar:', registroData); // Debug
      
      await registrarEmpresa(registroData);
      alert('Empresa registrada exitosamente');
      onRegistroSuccess();
    } catch (err: any) {
      console.error('Error en registro:', err); // Debug
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message || 
                          err.response?.data?.error ||
                          JSON.stringify(err.response?.data) ||
                          'Error al registrar empresa';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="registro-container">
      <form onSubmit={handleSubmit} className="registro-form">
        <h2>Registrar Empresa</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-section">
          <h3>Datos de la Empresa</h3>
          
          <div className="form-group">
            <label htmlFor="nombre">Nombre de la Empresa:</label>
            <input
              type="text"
              id="nombre"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="rfc">RFC:</label>
            <input
              type="text"
              id="rfc"
              name="rfc"
              value={formData.rfc}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="direccion">Dirección:</label>
            <textarea
              id="direccion"
              name="direccion"
              value={formData.direccion}
              onChange={handleChange}
              rows={3}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email_contacto">Email de Contacto:</label>
            <input
              type="email"
              id="email_contacto"
              name="email_contacto"
              value={formData.email_contacto}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="telefono_contacto">Teléfono de Contacto:</label>
            <input
              type="tel"
              id="telefono_contacto"
              name="telefono_contacto"
              value={formData.telefono_contacto}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="logotipo">URL del Logotipo:</label>
            <input
              type="url"
              id="logotipo"
              name="logotipo"
              value={formData.logotipo}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-section">
          <h3>Datos del Administrador</h3>
          
          <div className="form-group">
            <label htmlFor="admin_username">Usuario:</label>
            <input
              type="text"
              id="admin_username"
              name="admin_username"
              value={formData.admin_username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="admin_password">Contraseña:</label>
            <input
              type="password"
              id="admin_password"
              name="admin_password"
              value={formData.admin_password}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="admin_email">Email:</label>
            <input
              type="email"
              id="admin_email"
              name="admin_email"
              value={formData.admin_email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="admin_nombre">Nombre:</label>
            <input
              type="text"
              id="admin_nombre"
              name="admin_nombre"
              value={formData.admin_nombre}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="admin_apellido_paterno">Apellido Paterno:</label>
            <input
              type="text"
              id="admin_apellido_paterno"
              name="admin_apellido_paterno"
              value={formData.admin_apellido_paterno}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="admin_apellido_materno">Apellido Materno:</label>
            <input
              type="text"
              id="admin_apellido_materno"
              name="admin_apellido_materno"
              value={formData.admin_apellido_materno}
              onChange={handleChange}
            />
          </div>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Registrando...' : 'Registrar Empresa'}
        </button>

        {onSwitchToLogin && (
          <div className="switch-to-login">
            <p>¿Ya tienes cuenta?</p>
            <button type="button" onClick={onSwitchToLogin} className="login-link">
              Iniciar Sesión
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

export default RegistroEmpresa;
