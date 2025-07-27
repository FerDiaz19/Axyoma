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
    setProcesando(true);
    
    try {
      const { procesarPagoSimple } = await import('../services/suscripcionService');
      
      const resultado = await procesarPagoSimple({
        empresa_id: empresaId,
        plan_id: planSeleccionado.plan_id,
        metodo_pago: metodoPago,
        referencia_pago: referenciaPago
      });
      
      // Mostrar notificación de éxito
      alert(`🎉 ¡Pago Procesado Exitosamente!
      
Empresa: ${resultado.suscripcion.empresa}
Plan: ${resultado.suscripcion.plan}
Válido hasta: ${new Date(resultado.suscripcion.fecha_fin).toLocaleDateString()}
Referencia: ${resultado.pago.referencia}

Se ha enviado una confirmación por email.`);
      
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
          <h2>💳 Confirmar Pago</h2>
          <button className="btn-close" onClick={onCancelar}>❌</button>
        </div>
        
        <div className="plan-resumen">
          <h3>📋 Resumen del Plan</h3>
          <div className="plan-info">
            <p><strong>Plan:</strong> {planSeleccionado.nombre}</p>
            <p><strong>Duración:</strong> {planSeleccionado.duracion} días</p>
            <p><strong>Precio:</strong> ${planSeleccionado.precio}</p>
            <p><strong>Descripción:</strong> {planSeleccionado.descripcion}</p>
          </div>
        </div>
        
        <div className="pago-form">
          <h3>💰 Información de Pago</h3>
          
          <div className="form-group">
            <label>Método de Pago:</label>
            <select 
              value={metodoPago} 
              onChange={(e) => setMetodoPago(e.target.value)}
              className="form-select"
            >
              <option value="Transferencia">🏦 Transferencia Bancaria</option>
              <option value="Tarjeta">💳 Tarjeta de Crédito/Débito</option>
              <option value="Efectivo">💵 Efectivo</option>
              <option value="Cheque">📝 Cheque</option>
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
