import React, { useState, useEffect } from 'react';
import api from '../api';
import '../css/UsuariosPlanta.css';

interface Usuario {
  id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  correo: string;
  nivel_usuario: string;
  status: boolean;
}

interface Planta {
  id: number;
  nombre: string;
  direccion?: string;
}

interface Credenciales {
  usuario: string;
  password: string;
}

interface UsuarioPlanta {
  id: number;
  usuario: Usuario;
  planta: Planta;
  fecha_asignacion: string;
  status: boolean;
  tiene_password_temporal: boolean;
  credenciales?: Credenciales;
}

const UsuariosPlanta: React.FC = () => {
  const [usuariosPlanta, setUsuariosPlanta] = useState<UsuarioPlanta[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mostrarCredenciales, setMostrarCredenciales] = useState<{ [key: number]: boolean }>({});

  useEffect(() => {
    cargarUsuariosPlanta();
  }, []);

  const cargarUsuariosPlanta = async () => {
    try {
      setLoading(true);
      const response = await api.get('/plantas/usuarios_planta/');
      setUsuariosPlanta(response.data);
      setError(null);
    } catch (err: any) {
      console.error('Error cargando usuarios de planta:', err);
      setError('Error al cargar usuarios de planta');
    } finally {
      setLoading(false);
    }
  };

  const formatearFecha = (fecha: string) => {
    return new Date(fecha).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const obtenerNombreCompleto = (usuario: Usuario) => {
    return `${usuario.nombre} ${usuario.apellido_paterno} ${usuario.apellido_materno || ''}`.trim();
  };

  const toggleMostrarCredenciales = (id: number) => {
    setMostrarCredenciales(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const copiarAlPortapapeles = async (texto: string, tipo: string) => {
    try {
      await navigator.clipboard.writeText(texto);
      // Podrías agregar una notificación aquí
      console.log(`${tipo} copiado al portapapeles`);
    } catch (err) {
      console.error('Error copiando al portapapeles:', err);
    }
  };

  const regenerarPassword = async (plantaId: number) => {
    try {
      const response = await api.post(`/plantas/${plantaId}/regenerar_password/`);
      if (response.data.nuevas_credenciales) {
        // Recargar la lista para obtener la nueva contraseña
        await cargarUsuariosPlanta();
        alert(`Nueva contraseña generada para la planta`);
      }
    } catch (err: any) {
      console.error('Error regenerando contraseña:', err);
      alert('Error al regenerar contraseña');
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando usuarios de planta...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">{error}</p>
        <button onClick={cargarUsuariosPlanta} className="retry-button">
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="usuarios-planta-container">
      <div className="section-header">
        <h2>👤 Usuarios de Planta</h2>
        <p className="section-description">
          Usuarios administradores asignados a las plantas de la empresa
        </p>
      </div>

      {usuariosPlanta.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">👥</div>
          <h3>No hay usuarios de planta</h3>
          <p>No se han asignado usuarios administradores a las plantas de esta empresa.</p>
        </div>
      ) : (
        <div className="usuarios-grid">
          {usuariosPlanta.map((usuarioPlanta) => (
            <div key={usuarioPlanta.id} className="usuario-card">
              <div className="usuario-header">
                <div className="usuario-avatar">
                  <span className="avatar-icon">👤</span>
                </div>
                <div className="usuario-info">
                  <h3 className="usuario-nombre">
                    {obtenerNombreCompleto(usuarioPlanta.usuario)}
                  </h3>
                  <p className="usuario-email">{usuarioPlanta.usuario.correo}</p>
                </div>
                <div className={`usuario-status ${usuarioPlanta.status ? 'active' : 'inactive'}`}>
                  {usuarioPlanta.status ? '✅ Activo' : '❌ Inactivo'}
                </div>
              </div>

              <div className="usuario-details">
                <div className="detail-row">
                  <span className="detail-label">🏭 Planta:</span>
                  <span className="detail-value">{usuarioPlanta.planta.nombre}</span>
                </div>
                
                <div className="detail-row">
                  <span className="detail-label">📍 Dirección:</span>
                  <span className="detail-value">
                    {usuarioPlanta.planta.direccion || 'No especificada'}
                  </span>
                </div>

                <div className="detail-row">
                  <span className="detail-label">👨‍💼 Nivel:</span>
                  <span className="detail-value nivel-badge">
                    {usuarioPlanta.usuario.nivel_usuario}
                  </span>
                </div>

                <div className="detail-row">
                  <span className="detail-label">📅 Asignado:</span>
                  <span className="detail-value">
                    {formatearFecha(usuarioPlanta.fecha_asignacion)}
                  </span>
                </div>

                {usuarioPlanta.credenciales && (
                  <div className="credenciales-section">
                    <div className="detail-row">
                      <span className="detail-label">🔑 Credenciales de Acceso:</span>
                      <button 
                        className="toggle-credenciales-btn"
                        onClick={() => toggleMostrarCredenciales(usuarioPlanta.id)}
                      >
                        {mostrarCredenciales[usuarioPlanta.id] ? '🙈 Ocultar' : '👁️ Mostrar'}
                      </button>
                    </div>
                    
                    {mostrarCredenciales[usuarioPlanta.id] && (
                      <div className="credenciales-content">
                        <div className="credencial-item">
                          <label>Usuario:</label>
                          <div className="credencial-value">
                            <code>{usuarioPlanta.credenciales.usuario}</code>
                            <button 
                              className="copy-btn"
                              onClick={() => copiarAlPortapapeles(usuarioPlanta.credenciales!.usuario, 'Usuario')}
                              title="Copiar usuario"
                            >
                              📋
                            </button>
                          </div>
                        </div>
                        
                        <div className="credencial-item">
                          <label>Contraseña:</label>
                          <div className="credencial-value">
                            <code className="password-value">{usuarioPlanta.credenciales.password}</code>
                            <button 
                              className="copy-btn"
                              onClick={() => copiarAlPortapapeles(usuarioPlanta.credenciales!.password, 'Contraseña')}
                              title="Copiar contraseña"
                            >
                              📋
                            </button>
                          </div>
                        </div>
                        
                        <div className="credenciales-actions">
                          <button 
                            className="regenerar-btn"
                            onClick={() => regenerarPassword(usuarioPlanta.planta.id)}
                            title="Generar nueva contraseña"
                          >
                            🔄 Regenerar Contraseña
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {usuarioPlanta.tiene_password_temporal && !usuarioPlanta.credenciales && (
                  <div className="detail-row">
                    <span className="detail-label">🔑 Contraseña:</span>
                    <span className="detail-value temporal-password">
                      Temporal (debe cambiar)
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UsuariosPlanta;
