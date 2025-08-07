import React, { useState, useEffect, useCallback } from 'react';
import api from '../api';
import { crearPlanta, actualizarPlanta, eliminarPlantaCompleta } from '../services/organizacionService';
import '../css/GestionPlantas.css';

interface Planta {
  planta_id: number;
  nombre: string;
  direccion: string;
  status: boolean;
  empresa_id: number;
  empresa_nombre: string;
}

interface GestionPlantasProps {
  empresaId: number;
  userData?: any; // Agregar userData para verificar permisos
}

const GestionPlantas: React.FC<GestionPlantasProps> = ({ empresaId, userData }) => {
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [plantasFiltradas, setPlantasFiltradas] = useState<Planta[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingPlanta, setEditingPlanta] = useState<Planta | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [filtroNombre, setFiltroNombre] = useState('');
  const [formData, setFormData] = useState({
    nombre: '',
    direccion: '',
  });

  // Verificar si el usuario puede eliminar plantas (superadmin o admin de empresa)
  const canDeletePlants = userData?.nivel_usuario?.toLowerCase() === 'superadmin' || 
                          userData?.nivel_usuario?.toLowerCase() === 'super_admin' || 
                          userData?.nivel_usuario?.toLowerCase() === 'super-admin' ||
                          userData?.nivel_usuario?.toLowerCase() === 'admin_empresa' ||
                          userData?.nivel_usuario?.toLowerCase() === 'admin-empresa' ||
                          userData?.tipo_dashboard?.toLowerCase() === 'admin-empresa';
  
  console.log('🔍 Debug userData en GestionPlantas:', userData);
  console.log('🔍 Debug nivel_usuario:', userData?.nivel_usuario);
  console.log('🔍 Debug tipo_dashboard:', userData?.tipo_dashboard);
  console.log('🔍 Debug canDeletePlants:', canDeletePlants);

  const cargarPlantas = useCallback(async () => {
    try {
      setError(null);
      console.log('🔍 Cargando plantas para empresa:', empresaId);
      console.log('🔗 URL completa:', `http://localhost:8000/api/plantas/?empresa_id=${empresaId}&incluir_suspendidas=true`);
      console.log('🔑 Token en localStorage:', localStorage.getItem('authToken') ? 'SÍ' : 'NO');

      // Filtrar plantas por empresa (incluir suspendidas para poder reactivarlas)
      const response = await api.get(`/plantas/?empresa_id=${empresaId}&incluir_suspendidas=true`);
      console.log('📦 Plantas obtenidas:', response.data);
      console.log('📊 Cantidad de plantas:', response.data.length);
      setPlantas(response.data);
    } catch (error: any) {
      console.error('❌ Error cargando plantas:', error);
      console.error('📋 Error response:', error.response?.data);
      console.error('🔢 Status code:', error.response?.status);

      if (error.response?.status === 500) {
        setError(`Error del servidor (500): Problema en el backend al obtener plantas para empresa ${empresaId}. Revisa los logs del servidor Django.`);
      } else if (error.response?.status === 404) {
        setError(`No se encontraron plantas para la empresa ${empresaId}`);
      } else if (error.response?.status === 403) {
        setError(`Sin permisos para acceder a las plantas de la empresa ${empresaId}`);
      } else if (error.code === 'NETWORK_ERROR' || error.message.includes('Network Error')) {
        setError('Error de conexión: Verifique que el backend esté ejecutándose en http://localhost:8000');
      } else {
        setError(`Error al cargar las plantas: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  }, [empresaId]); // Dependencias del useCallback

  useEffect(() => {
    if (empresaId) {
      cargarPlantas();
    }
  }, [empresaId, cargarPlantas]); // Incluir cargarPlantas en las dependencias

  useEffect(() => {
    // Aplicar filtros
    let plantasFiltradas = plantas;

    if (filtroNombre.trim()) {
      plantasFiltradas = plantasFiltradas.filter(planta =>
        planta.nombre.toLowerCase().includes(filtroNombre.toLowerCase()) ||
        planta.direccion.toLowerCase().includes(filtroNombre.toLowerCase())
      );
    }

    setPlantasFiltradas(plantasFiltradas);
  }, [plantas, filtroNombre]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      console.log('📝 Datos del formulario a enviar:', formData);
      console.log('🔑 Token disponible:', localStorage.getItem('authToken') ? 'SÍ' : 'NO');

      if (editingPlanta) {
        // Actualizar planta existente
        const result = await actualizarPlanta(editingPlanta.planta_id, formData);
        console.log('✅ Planta actualizada exitosamente:', result);
      } else {
        // Crear nueva planta
        const result = await crearPlanta(formData);
        console.log('✅ Planta creada exitosamente:', result);
      }

      // Recargar lista y resetear formulario
      await cargarPlantas();
      resetForm();
    } catch (error: any) {
      console.error('❌ Error completo:', error);
      console.error('❌ Respuesta del servidor:', error.response?.data);
      console.error('❌ Status code:', error.response?.status);
      console.error('❌ Headers de respuesta:', error.response?.headers);

      setError(error.message || 'Error al guardar la planta');
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (planta: Planta) => {
    setEditingPlanta(planta);
    setFormData({
      nombre: planta.nombre,
      direccion: planta.direccion,
    });
    setShowForm(true);
  };

  const handleToggleStatus = async (planta: Planta) => {
    const accion = planta.status ? 'suspender' : 'activar';
    const confirmMessage = planta.status
      ? `¿Suspender la planta "${planta.nombre}"? Esto también suspenderá todos los departamentos, puestos y empleados asociados.`
      : `¿Activar la planta "${planta.nombre}"? Esto también activará todos los departamentos, puestos y empleados asociados.`;

    if (window.confirm(confirmMessage)) {
      try {
        setError(null);
        setSaving(true);

        // Llamar al endpoint de toggle_status
        await api.post(`/plantas/${planta.planta_id}/toggle_status/`);

        await cargarPlantas();
        alert(`Planta ${accion}da exitosamente`);
      } catch (error: any) {
        console.error(`Error ${accion}ndo planta:`, error);
        const errorMessage = error.response?.data?.error || error.response?.data?.message || `Error al ${accion} la planta`;
        setError(errorMessage);
        alert(`Error al ${accion} la planta: ${errorMessage}`);
      } finally {
        setSaving(false);
      }
    }
  };

  const handleEliminarPlanta = async (planta: Planta) => {
    const confirmMessage = `⚠️ ELIMINAR COMPLETAMENTE LA PLANTA "${planta.nombre}"

Esta acción es IRREVERSIBLE y eliminará:
• La planta
• Todos los departamentos
• Todos los puestos de trabajo
• Todos los empleados
• El administrador de planta

¿Está ABSOLUTAMENTE SEGURO de que desea continuar?`;

    if (window.confirm(confirmMessage)) {
      const finalConfirmation = window.confirm(
        `🚨 ÚLTIMA CONFIRMACIÓN\n\n¿Realmente desea ELIMINAR PERMANENTEMENTE la planta "${planta.nombre}" y TODOS sus datos relacionados?\n\nEsta acción NO se puede deshacer.`
      );

      if (finalConfirmation) {
        try {
          setError(null);
          setSaving(true);

          await eliminarPlantaCompleta(planta.planta_id);
          await cargarPlantas();
          alert(`✅ Planta "${planta.nombre}" eliminada exitosamente junto con todos sus datos relacionados.`);
        } catch (error: any) {
          console.error('Error eliminando planta:', error);
          const errorMessage = error.message || 'Error al eliminar la planta';
          setError(errorMessage);
          alert(`❌ Error al eliminar la planta: ${errorMessage}`);
        } finally {
          setSaving(false);
        }
      }
    }
  };

  const resetForm = () => {
    setFormData({ nombre: '', direccion: '' });
    setEditingPlanta(null);
    setShowForm(false);
  };

  if (loading) {
    return <div className="loading">Cargando plantas...</div>;
  }

  return (
    <div className="gestion-plantas">
      <div className="header">
        <h2>Gestión de Plantas</h2>
        <div className="header-actions">
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
          >
            + Agregar Planta
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Filtros */}
      <div className="filtros">
        <div className="filtro-group">
          <label>Buscar por nombre o dirección:</label>
          <input
            type="text"
            placeholder="Escriba para filtrar..."
            value={filtroNombre}
            onChange={(e) => setFiltroNombre(e.target.value)}
            className="filtro-input"
          />
        </div>
        {filtroNombre && (
          <div className="filtro-info">
            Mostrando {plantasFiltradas.length} de {plantas.length} plantas
          </div>
        )}
      </div>

      {/* Lista de plantas */}
      <div className="plantas-grid">
        {plantasFiltradas.map((planta) => (
          <div key={planta.planta_id} className="planta-card">
            <h3>{planta.nombre}</h3>
            <p className="direccion">{planta.direccion}</p>
            <p className={`status ${planta.status ? 'activa' : 'inactiva'}`}>
              Estado: {planta.status ? 'Activa' : 'Inactiva'}
            </p>
            <div className="actions">
              <button
                className="btn btn-secondary"
                onClick={() => handleEdit(planta)}
                disabled={saving}
              >
                Editar
              </button>
              <button
                className={`btn ${planta.status ? 'btn-warning' : 'btn-success'}`}
                onClick={() => handleToggleStatus(planta)}
                disabled={saving}
              >
                {planta.status ? 'Suspender' : 'Activar'}
              </button>
              {canDeletePlants ? (
                <button
                  className="btn btn-danger"
                  onClick={() => handleEliminarPlanta(planta)}
                  disabled={saving}
                  title="Eliminar planta completa"
                  style={{ marginLeft: '8px' }}
                >
                  🗑️ Eliminar
                </button>
              ) : (
                <span style={{ fontSize: '12px', color: '#888', marginLeft: '8px' }}>
                  (Solo administradores pueden eliminar)
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      {plantasFiltradas.length === 0 && plantas.length > 0 && (
        <div className="no-results">
          <p>No se encontraron plantas que coincidan con "{filtroNombre}"</p>
        </div>
      )}

      {plantas.length === 0 && (
        <div className="empty-state">
          <p>No hay plantas registradas</p>
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
          >
            Agregar Primera Planta
          </button>
        </div>
      )}

      {/* Modal/Formulario */}
      {showForm && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>{editingPlanta ? 'Editar Planta' : 'Nueva Planta'}</h3>
            <form onSubmit={handleSubmit}>
              {error && (
                <div className="form-error">
                  {error}
                </div>
              )}

              <div className="form-group">
                <label>Nombre de la Planta:</label>
                <input
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Dirección:</label>
                <textarea
                  value={formData.direccion}
                  onChange={(e) => setFormData({ ...formData, direccion: e.target.value })}
                  required
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? 'Guardando...' : (editingPlanta ? 'Actualizar' : 'Guardar')}
                </button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={resetForm}
                  disabled={saving}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionPlantas;
