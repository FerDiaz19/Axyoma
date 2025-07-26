import React, { useState, useEffect } from 'react';

interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'textarea' | 'select' | 'checkbox' | 'number';
  required?: boolean;
  options?: { value: string | number; label: string }[];
  disabled?: boolean;
}

interface EditModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  initialData: Record<string, any>;
  fields: FormField[];
  onSave: (data: Record<string, any>) => Promise<void>;
  loading?: boolean;
  infoMessage?: string;
  infoType?: 'info' | 'warning' | 'success';
}

const EditModal: React.FC<EditModalProps> = ({
  isOpen,
  onClose,
  title,
  initialData,
  fields,
  onSave,
  loading = false,
  infoMessage,
  infoType = 'info'
}) => {
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (isOpen && initialData) {
      setFormData({ ...initialData });
      setErrors({});
    }
  }, [isOpen, initialData]);

  const handleInputChange = (name: string, value: any) => {
    //console.log(`Campo "${name}" cambiado a:`, value); // Log para depuración
    
    // Actualizar el estado del formulario
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error al cambiar el valor
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    fields.forEach(field => {
      if (field.required && (!formData[field.name] || formData[field.name].toString().trim() === '')) {
        newErrors[field.name] = `${field.label} es requerido`;
      }
      
      if (field.type === 'email' && formData[field.name]) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData[field.name])) {
          newErrors[field.name] = 'Email inválido';
        }
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }

    setSaving(true);
    try {
      await onSave(formData);
      onClose();
    } catch (error) {
      console.error('Error guardando:', error);
      // El error se maneja en el componente padre
    } finally {
      setSaving(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose} onKeyDown={handleKeyDown}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{title}</h3>
          <button className="modal-close" onClick={onClose} disabled={saving}>
            ✕
          </button>
        </div>

        {loading ? (
          <div className="modal-loading">
            <div className="loading-spinner"></div>
            <div>Cargando datos...</div>
          </div>
        ) : (
          <>
            {infoMessage && (
              <div className={`modal-info ${infoType}`}>
                <span className="modal-info-icon">
                  {infoType === 'warning' ? '⚠️' : infoType === 'success' ? '✅' : 'ℹ️'}
                </span>
                <span>{infoMessage}</span>
              </div>
            )}
            
            <form className="modal-form" onSubmit={(e) => e.preventDefault()}>
              {fields.map((field) => (
                <div key={field.name} className="form-group">
                  <label htmlFor={field.name}>
                    {field.label}
                    {field.required && <span style={{ color: '#dc3545' }}> *</span>}
                  </label>
                  
                  {field.type === 'textarea' ? (
                    <textarea
                      id={field.name}
                      className={`form-textarea ${errors[field.name] ? 'error' : ''}`}
                      value={formData[field.name] || ''}
                      onChange={(e) => handleInputChange(field.name, e.target.value)}
                      disabled={field.disabled || saving}
                      placeholder={`Ingrese ${field.label.toLowerCase()}`}
                    />
                  ) : field.type === 'select' ? (
                    <select
                      id={field.name}
                      className={`form-select ${errors[field.name] ? 'error' : ''}`}
                      value={formData[field.name] || ''}
                      onChange={(e) => handleInputChange(field.name, e.target.value)}
                      disabled={field.disabled || saving}
                    >
                      <option value="">Seleccione una opción</option>
                      {field.options?.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  ) : field.type === 'checkbox' ? (
                    <div className="form-checkbox-group">
                      <input
                        id={field.name}
                        type="checkbox"
                        className="form-checkbox"
                        checked={!!formData[field.name]}
                        onChange={(e) => handleInputChange(field.name, e.target.checked)}
                        disabled={field.disabled || saving}
                      />
                      <label htmlFor={field.name} style={{ fontWeight: 'normal' }}>
                        {field.label}
                      </label>
                    </div>
                  ) : (
                    <input
                      id={field.name}
                      type={field.type}
                      className={`form-input ${errors[field.name] ? 'error' : ''}`}
                      value={formData[field.name] || ''}
                      onChange={(e) => {
                        const newValue = field.type === 'number' ? Number(e.target.value) : e.target.value;
                        console.log(`Actualizando ${field.name} a:`, newValue);
                        handleInputChange(field.name, newValue);
                      }}
                      disabled={field.disabled || saving}
                      placeholder={`Ingrese ${field.label.toLowerCase()}`}
                      autoComplete="off" // Deshabilitar autocompletado para evitar problemas
                    />
                  )}
                  
                  {errors[field.name] && (
                    <div className="error-message">
                      ⚠️ {errors[field.name]}
                    </div>
                  )}
                </div>
              ))}
            </form>

            <div className="modal-actions">
              <button 
                className="modal-btn modal-btn-cancel" 
                onClick={onClose}
                disabled={saving}
              >
                ✕ Cancelar
              </button>
              <button 
                className="modal-btn modal-btn-save" 
                onClick={handleSave}
                disabled={saving}
              >
                {saving ? (
                  <>
                    <div className="loading-spinner" style={{ width: '16px', height: '16px', border: '2px solid rgba(255,255,255,0.3)', borderTop: '2px solid white' }}></div>
                    Guardando...
                  </>
                ) : (
                  <>
                    💾 Guardar
                  </>
                )}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default EditModal;
