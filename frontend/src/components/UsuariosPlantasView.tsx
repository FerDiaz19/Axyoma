import React, { useState, useEffect } from 'react';
import api from '../api';
import '../css/UsuariosPlantasView.css';

interface UsuarioPlanta {
  usuario_id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  planta_id: number;
  planta_nombre: string;
  fecha_creacion?: string;
}

interface CredencialUsuario {
  planta_id: number;
  planta_nombre: string;
  usuario_id: number;
  username: string;
  email: string;
  nombre_completo: string;
  is_active: boolean;
  fecha_creacion?: string;
  password_visible: string;
  instrucciones: string;
}

interface UsuariosPlantasViewProps {
  empresaId: number;
}

const UsuariosPlantasView: React.FC<UsuariosPlantasViewProps> = ({ empresaId }) => {
  const [usuarios, setUsuarios] = useState<UsuarioPlanta[]>([]);
  const [credenciales, setCredenciales] = useState<CredencialUsuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [vistaActual, setVistaActual] = useState<'usuarios' | 'credenciales'>('usuarios');
  const [passwordResetData, setPasswordResetData] = useState<any>(null);

  useEffect(() => {
    if (empresaId) {
      cargarUsuarios();
    }
  }, [empresaId]); // Solo dependemos de empresaId para evitar bucles infinitos

  const cargarUsuarios = async () => {
    try {
      setError(null);
      console.log('🔍 Cargando usuarios de planta para empresa:', empresaId);
      
      const response = await api.get(`/plantas/usuarios-planta/?empresa_id=${empresaId}`);
      console.log('👥 Usuarios obtenidos:', response.data);
      setUsuarios(response.data);
    } catch (error: any) {
      console.error('❌ Error cargando usuarios:', error);
      
      if (error.response?.status === 404) {
        setUsuarios([]);
      } else {
        setError(`Error al cargar usuarios: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const cargarCredenciales = async () => {
    try {
      setError(null);
      console.log('🔍 Cargando credenciales para empresa:', empresaId);
      
      const response = await api.get('/plantas/credenciales-usuarios/');
      console.log('🔑 Credenciales obtenidas:', response.data);
      setCredenciales(response.data.credenciales || []);
    } catch (error: any) {
      console.error('❌ Error cargando credenciales:', error);
      setError(`Error al cargar credenciales: ${error.message}`);
    }
  };

  const resetearPassword = async (usuarioId: number) => {
    if (!window.confirm('¿Está seguro de resetear la contraseña de este usuario?')) {
      return;
    }

    try {
      setError(null);
      const response = await api.post('/plantas/resetear-password-usuario/', {
        usuario_id: usuarioId
      });
      
      setPasswordResetData(response.data);
      alert(`Contraseña reseteada exitosamente.\nNueva contraseña: ${response.data.nueva_password}`);
      
      // Recargar usuarios
      await cargarUsuarios();
    } catch (error: any) {
      console.error('❌ Error reseteando contraseña:', error);
      const errorMessage = error.response?.data?.error || 'Error al resetear contraseña';
      setError(errorMessage);
      alert(`Error: ${errorMessage}`);
    }
  };

  const toggleUsuarioStatus = async (usuarioId: number, activo: boolean) => {
    try {
      setError(null);
      const accion = activo ? 'activar' : 'suspender';
      
      await api.post('/plantas/usuarios-planta/toggle-status/', {
        usuario_id: usuarioId,
        accion: accion
      });
      
      await cargarUsuarios();
      alert(`Usuario ${accion} exitosamente`);
    } catch (error: any) {
      console.error('Error cambiando status:', error);
      const errorMessage = error.response?.data?.error || 'Error al cambiar status';
      setError(errorMessage);
      alert(`Error: ${errorMessage}`);
    }
  };

  if (loading) {
    return <div className="loading">Cargando usuarios de planta...</div>;
  }

  return (
    <div className="usuarios-plantas-view">
      <div className="header">
        <h2>Usuarios de Plantas</h2>
        <div className="header-actions">
          <div className="vista-tabs">
            <button 
              className={vistaActual === 'usuarios' ? 'tab-active' : 'tab-inactive'}
              onClick={() => setVistaActual('usuarios')}
            >
              👥 Usuarios
            </button>
            <button 
              className={vistaActual === 'credenciales' ? 'tab-active' : 'tab-inactive'}
              onClick={() => {
                setVistaActual('credenciales');
                cargarCredenciales();
              }}
            >
              🔑 Credenciales
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {vistaActual === 'usuarios' ? (
        <div className="usuarios-section">
          <div className="section-header">
            <h3>👥 Gestión de Usuarios</h3>
            <p className="subtitle">Administradores de planta activos</p>
          </div>

          {usuarios.length === 0 ? (
            <div className="empty-state">
              <p>No hay usuarios de planta registrados</p>
              <p className="help-text">Los usuarios se crean automáticamente al crear plantas</p>
            </div>
          ) : (
            <div className="usuarios-grid">
              {usuarios.map((usuario) => (
                <div key={usuario.usuario_id} className="usuario-card">
                  <div className="usuario-info">
                    <h4>{usuario.first_name} {usuario.last_name}</h4>
                    <p className="username">@{usuario.username}</p>
                    <p className="email">{usuario.email}</p>
                    <p className="planta">🏭 {usuario.planta_nombre}</p>
                    {usuario.fecha_creacion && (
                      <p className="fecha">📅 {new Date(usuario.fecha_creacion).toLocaleDateString()}</p>
                    )}
                  </div>
                  <div className="usuario-status">
                    <span className={`status-badge ${usuario.is_active ? 'active' : 'inactive'}`}>
                      {usuario.is_active ? '✅ Activo' : '❌ Suspendido'}
                    </span>
                  </div>
                  <div className="usuario-actions">
                    <button 
                      className={`btn ${usuario.is_active ? 'btn-warning' : 'btn-success'}`}
                      onClick={() => toggleUsuarioStatus(usuario.usuario_id, !usuario.is_active)}
                    >
                      {usuario.is_active ? 'Suspender' : 'Activar'}
                    </button>
                    <button 
                      className="btn btn-info"
                      onClick={() => resetearPassword(usuario.usuario_id)}
                    >
                      🔄 Resetear Password
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="credenciales-section">
          <div className="section-header">
            <h3>🔑 Credenciales de Usuarios</h3>
            <p className="subtitle">Información de acceso para usuarios de planta</p>
          </div>

          {credenciales.length === 0 ? (
            <div className="empty-state">
              <p>No hay credenciales disponibles</p>
              <p className="help-text">Las credenciales se generan automáticamente al crear plantas</p>
            </div>
          ) : (
            <>
              <div className="credenciales-info">
                <div className="info-card warning">
                  <h4>⚠️ Información Importante</h4>
                  <p>Las contraseñas se generan automáticamente al crear cada planta y aparecen una sola vez en los logs del servidor Django.</p>
                  <p>Use el botón "Resetear Password" para generar nuevas contraseñas cuando sea necesario.</p>
                </div>
              </div>

              <div className="credenciales-grid">
                {credenciales.map((credencial) => (
                  <div key={credencial.usuario_id} className="credencial-card">
                    <div className="credencial-header">
                      <h4>🏭 {credencial.planta_nombre}</h4>
                      <span className={`status-badge ${credencial.is_active ? 'active' : 'inactive'}`}>
                        {credencial.is_active ? '✅ Activo' : '❌ Suspendido'}
                      </span>
                    </div>
                    <div className="credencial-info">
                      <div className="info-row">
                        <strong>👤 Usuario:</strong> <code>{credencial.username}</code>
                      </div>
                      <div className="info-row">
                        <strong>📧 Email:</strong> <code>{credencial.email}</code>
                      </div>
                      <div className="info-row">
                        <strong>👨‍💼 Nombre:</strong> {credencial.nombre_completo}
                      </div>
                      <div className="info-row">
                        <strong>🔑 Contraseña:</strong> 
                        <span className="password-info">{credencial.password_visible}</span>
                      </div>
                      {credencial.fecha_creacion && (
                        <div className="info-row">
                          <strong>📅 Creado:</strong> {new Date(credencial.fecha_creacion).toLocaleDateString()}
                        </div>
                      )}
                    </div>
                    <div className="credencial-actions">
                      <button 
                        className="btn btn-warning"
                        onClick={() => resetearPassword(credencial.usuario_id)}
                      >
                        🔄 Generar Nueva Contraseña
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {passwordResetData && (
        <div className="modal-overlay">
          <div className="modal password-modal">
            <h3>🔑 Nueva Contraseña Generada</h3>
            <div className="password-info-modal">
              <p><strong>Usuario:</strong> {passwordResetData.username}</p>
              <p><strong>Planta:</strong> {passwordResetData.planta}</p>
              <div className="new-password">
                <strong>Nueva Contraseña:</strong>
                <code className="password-code">{passwordResetData.nueva_password}</code>
              </div>
              <p className="instructions">{passwordResetData.instrucciones}</p>
            </div>
            <div className="modal-actions">
              <button 
                className="btn btn-primary"
                onClick={() => {
                  navigator.clipboard.writeText(passwordResetData.nueva_password);
                  alert('Contraseña copiada al portapapeles');
                }}
              >
                📋 Copiar Contraseña
              </button>
              <button 
                className="btn btn-secondary"
                onClick={() => setPasswordResetData(null)}
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UsuariosPlantasView;
