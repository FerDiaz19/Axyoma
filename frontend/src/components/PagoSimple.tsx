import React, { useState } from 'react';
import '../css/PagoSimple.css';

interface PagoSimpleProps {
  empresaId: number;
  planSeleccionado: any;
  onPagoCompletado: (resultado: any) => void;
  onCancelar: () => void;
}

const PagoSimple: React.FC<PagoSimpleProps> = ({ 
  empresaId, 
  planSeleccionado, 
  onPagoCompletado, 
  onCancelar 
}) => {
  const [metodoPago, setMetodoPago] = useState('Transferencia');
  const [referenciaPago, setReferenciaPago] = useState('');
  const [procesando, setProcesando] = useState(false);

  const handlePagar = async () => {
    if (!planSeleccionado) {
      alert('Debe seleccionar un plan');
      return;
    }

    if (!metodoPago) {
      alert('Debe seleccionar un método de pago');
      return;
    }

    if (!referenciaPago.trim()) {
      alert('Debe ingresar una referencia de pago');
      return;
    }

    setProcesando(true);
    
    try {
      const { procesarPagoSimple } = await import('../services/suscripcionService');
      
      const resultado = await procesarPagoSimple({
        empresa_id: empresaId,
        plan_id: planSeleccionado.plan_id,
        monto_pago: planSeleccionado.precio, // ✅ Agregar monto_pago que faltaba
        metodo_pago: metodoPago,
        transaccion_id: referenciaPago // ✅ Cambiar referencia_pago por transaccion_id
      });
      
      // Mostrar notificación de éxito
      alert(`¡Pago procesado exitosamente!
      
Plan: ${planSeleccionado.nombre}
Monto: $${planSeleccionado.precio}
Referencia: ${referenciaPago}`);
      
      // Limpiar formulario
      setMetodoPago('');
      setReferenciaPago('');
      
      // Notificar al componente padre si existe
      onPagoCompletado(resultado);
      
    } catch (error: any) {
      console.error('Error procesando pago:', error);
      alert('Error al procesar el pago: ' + error.message);
    } finally {
      setProcesando(false);
    }
  };

  return (
    <div className="pago-simple-modal">
      <div className="pago-simple-content">
        <div className="pago-header">
          <h2>
            <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '1.5rem', height: '1.5rem', marginRight: '8px', verticalAlign: 'middle' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg> Confirmar Pago
          </h2>
          <button className="btn-close" onClick={onCancelar}>
            <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '1rem', height: '1rem' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="plan-resumen">
          <h3>
            <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '1.2rem', height: '1.2rem', marginRight: '8px', verticalAlign: 'middle' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg> Resumen del Plan
          </h3>
          <div className="plan-info">
            <p><strong>Plan:</strong> {planSeleccionado.nombre}</p>
            <p><strong>Duración:</strong> {planSeleccionado.duracion} días</p>
            <p><strong>Precio:</strong> ${planSeleccionado.precio}</p>
            <p><strong>Descripción:</strong> {planSeleccionado.descripcion}</p>
          </div>
        </div>
        
        <div className="pago-form">
          <h3>
            <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '1.2rem', height: '1.2rem', marginRight: '8px', verticalAlign: 'middle' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg> Información de Pago
          </h3>
          
          <div className="form-group">
            <label>Método de Pago:</label>
            <select 
              value={metodoPago} 
              onChange={(e) => setMetodoPago(e.target.value)}
              className="form-select"
            >              <option value="Transferencia">
                <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '1rem', height: '1rem', marginRight: '5px' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1" />
                </svg> Transferencia Bancaria
              </option>
              <option value="Tarjeta">
                <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '1rem', height: '1rem', marginRight: '5px' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg> Tarjeta de Crédito/Débito
              </option>
              <option value="Efectivo">💵 Efectivo</option>
              <option value="Cheque">
                <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '1rem', height: '1rem', marginRight: '5px' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg> Cheque
              </option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Referencia de Pago (Opcional):</label>
            <input
              type="text"
              value={referenciaPago}
              onChange={(e) => setReferenciaPago(e.target.value)}
              placeholder="Ej: Folio, número de cheque, etc."
              className="form-input"
            />
          </div>
          
          <div className="info-importante">
            <h4>ℹ️ Información Importante:</h4>
            <ul>
              <li>✅ El pago se marcará como completado inmediatamente</li>
              <li>📧 Recibirá confirmación por email</li>
              <li>🔄 Su suscripción se activará automáticamente</li>
              <li>📊 Podrá acceder a evaluaciones NOM-035 (empresas &lt; 50 empleados)</li>
              <li>⏰ Trial gratuito de 30 días incluido</li>
            </ul>
          </div>
        </div>
        
        <div className="pago-actions">
          <button 
            className="btn-pagar" 
            onClick={handlePagar}
            disabled={procesando}
          >
            {procesando ? '⏳ Procesando...' : `💳 Confirmar Pago $${planSeleccionado.precio}`}
          </button>
          <button 
            className="btn-cancelar" 
            onClick={onCancelar}
            disabled={procesando}
          >
            ❌ Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default PagoSimple;
