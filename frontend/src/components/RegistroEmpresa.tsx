import React, { useState } from 'react';
import { registrarEmpresa } from '../services/empresaService';
import PlanSelection from './PlanSelection';
import styles from '../css/RegistroEmpresa.module.css';

interface RegistroEmpresaProps {
  onRegistroSuccess: () => void;
  onSwitchToLogin?: () => void;
}

const RegistroEmpresa: React.FC<RegistroEmpresaProps> = ({ onRegistroSuccess, onSwitchToLogin }) => {
  const [paso, setPaso] = useState<'registro' | 'seleccion_plan'>('registro');
  const [empresaRegistrada, setEmpresaRegistrada] = useState<{id: number, nombre: string} | null>(null);
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
      
      console.log('🔧 Datos a enviar al backend:', registroData);
      
      const response = await registrarEmpresa(registroData);
      
      console.log('✅ Empresa registrada exitosamente:', response);
      
      // Si el registro fue exitoso, pasar a selección de plan
      setEmpresaRegistrada({
        id: response.empresa_id,
        nombre: response.nombre
      });
      
      // Mostrar mensaje de éxito
      alert(`🎉 ¡Empresa "${response.nombre}" registrada exitosamente!\n\n✅ Se ha creado automáticamente:\n• Una planta principal\n• Departamentos básicos\n• Puestos de trabajo estándar\n\nAhora puedes seleccionar un plan de suscripción.`);
      
      setPaso('seleccion_plan');
      
    } catch (err: any) {
      console.error('🔥 Error completo:', err);
      console.error('🔥 Response data:', err.response?.data);
      console.error('🔥 Response status:', err.response?.status);
      
      let errorMessage = 'Error al registrar empresa';
      
      if (err.response?.status === 500) {
        errorMessage = 'Error interno del servidor. Por favor intente nuevamente en unos momentos.';
      } else if (err.response?.status === 400) {
        // Errores de validación
        const errorData = err.response.data;
        
        if (typeof errorData === 'string') {
          errorMessage = errorData;
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.error) {
          errorMessage = errorData.error;
        } else if (errorData.message) {
          errorMessage = errorData.message;
        } else if (errorData.non_field_errors && Array.isArray(errorData.non_field_errors)) {
          errorMessage = errorData.non_field_errors.join(', ');
        } else {
          // Mostrar errores de campos específicos
          const fieldErrors = [];
          for (const [field, errors] of Object.entries(errorData)) {
            if (Array.isArray(errors)) {
              fieldErrors.push(`${field}: ${errors.join(', ')}`);
            } else if (typeof errors === 'string') {
              fieldErrors.push(`${field}: ${errors}`);
            }
          }
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join('\n');
          }
        }
      } else if (err.code === 'NETWORK_ERROR' || err.message === 'Network Error') {
        errorMessage = 'Error de conexión. Verifique su conexión a internet y que el servidor esté funcionando.';
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handlePlanSelected = () => {
    // Plan seleccionado exitosamente, completar el registro
    alert(`🎉 ¡Registro completado exitosamente!\n\n✅ Tu empresa "${empresaRegistrada?.nombre}" está lista.\n✅ Plan de suscripción activado.\n✅ Ya puedes acceder a tu cuenta.\n\n¡Bienvenido a Axyoma!`);
    onRegistroSuccess();
  };

  const handleSkipPlan = () => {
    // Usuario decidió omitir la selección de plan
    alert(`✅ Empresa "${empresaRegistrada?.nombre}" registrada exitosamente.\n\n📝 Puedes seleccionar un plan más tarde desde tu panel de administración.\n\n¡Bienvenido a Axyoma!`);
    onRegistroSuccess();
  };

  // Si estamos en el paso de selección de plan, mostrar el componente correspondiente
  if (paso === 'seleccion_plan' && empresaRegistrada) {
    return (
      <PlanSelection
        empresaId={empresaRegistrada.id}
        onPlanSelected={handlePlanSelected}
        onSkip={handleSkipPlan}
      />
    );
  }

  return (
    <div className={styles['registro-container']}>
      <form onSubmit={handleSubmit} className={styles['registro-form']}>
        <div className={styles['form-header']}>
          <h2>🏢 Registrar Nueva Empresa</h2>
          <p>Completa el formulario para crear tu cuenta empresarial</p>
        </div>

        {error && (
          <div className={styles['error-message']}>
            <span>❌</span>
            {error}
          </div>
        )}

        <div className={styles['form-section']}>
          <h3>📋 Datos de la Empresa</h3>

          <div className={styles['form-group']}>
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

          <div className={styles['form-group']}>
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

          <div className={styles['form-group']}>
            <label htmlFor="direccion">Dirección:</label>
            <textarea
              id="direccion"
              name="direccion"
              value={formData.direccion}
              onChange={handleChange}
              rows={3}
            />
          </div>

          <div className={styles['form-group']}>
            <label htmlFor="email_contacto">Email de Contacto:</label>
            <input
              type="email"
              id="email_contacto"
              name="email_contacto"
              value={formData.email_contacto}
              onChange={handleChange}
            />
          </div>

          <div className={styles['form-group']}>
            <label htmlFor="telefono_contacto">Teléfono de Contacto:</label>
            <input
              type="tel"
              id="telefono_contacto"
              name="telefono_contacto"
              value={formData.telefono_contacto}
              onChange={handleChange}
            />
          </div>

          <div className={styles['form-group']}>
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

        <div className={styles['form-section']}>
          <h3>👤 Datos del Administrador</h3>
          <p>Esta será la cuenta principal para administrar tu empresa</p>

          <div className={styles['form-group']}>
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

          <div className={styles['form-group']}>
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

          <div className={styles['form-group']}>
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

          <div className={styles['form-group']}>
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

          <div className={styles['form-group']}>
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

          <div className={styles['form-group']}>
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

        <div className={styles['form-buttons']}>
          <button type="submit" disabled={loading} className={styles['btn-submit']}>
            {loading ? (
              <>
                <span className={styles['spinner']}>⏳</span>
                Registrando empresa...
              </>
            ) : (
              <>
                <span>🚀</span>
                Registrar Empresa
              </>
            )}
          </button>
        </div>

        <div className={styles['form-footer']}>
          {onSwitchToLogin && (
            <div className={styles['back-to-login']}>
              <button type="button" onClick={onSwitchToLogin} className={styles['btn-back']}>
                ← Volver al Login
              </button>
              <p>¿Ya tienes cuenta? <span onClick={onSwitchToLogin} className={styles['login-link']}>Iniciar Sesión</span></p>
            </div>
          )}
        </div>
      </form>
    </div>
  );
};

export default RegistroEmpresa;
