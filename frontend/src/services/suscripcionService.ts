// Servicio para gestión de suscripciones con estructura normalizada
import api from '../api';

// ===== TIPOS =====
export interface PlanSuscripcion {
  plan_id: number;
  nombre: string;
  descripcion: string;
  precio: number;
  duracion: number;
  status: boolean;
}

export interface SuscripcionEmpresa {
  suscripcion_id: number;
  empresa_id: number;
  empresa_nombre: string;
  plan_id: number;
  plan_nombre: string;
  plan_precio: number;
  plan_duracion: number;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
  status: boolean;
  dias_restantes?: number;
  esta_activa?: boolean;
  esta_por_vencer?: boolean;
}

export interface Pago {
  pago_id: number;
  suscripcion_id: number;
  empresa_nombre: string;
  plan_nombre: string;
  costo: number;
  monto_pago: number;
  estado_pago: string;
  fecha_pago: string;
  fecha_vencimiento?: string;
  transaccion_id?: string;
  usuario?: string;
}

// ============= FUNCIONES DE UTILIDAD =============
export const formatearPrecio = (precio: number): string => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN'
  }).format(precio);
};

export const formatearDuracion = (dias: number): string => {
  if (dias === 30) return '1 mes';
  if (dias === 90) return '3 meses';
  if (dias === 180) return '6 meses';
  if (dias === 365) return '1 año';
  return `${dias} días`;
};

export const formatearFecha = (fecha: string): string => {
  return new Date(fecha).toLocaleDateString('es-MX');
};

export const getEstadoSuscripcionTexto=(estado:string):string=>{
switch(estado.toLowerCase()){    case 'activa':
      return 'Activa';
    case 'vencida':
      return 'Vencida';
    case 'suspendida':
      return 'Suspendida';
    case 'cancelada':
      return 'Cancelada';
    default:
      return estado;
}
};

export const getEstadoSuscripcionColor=(estado:string):string=>{
switch(estado.toLowerCase()){
case'activa':
return'active';
case'vencida':
return'expired';
case'suspendida':
return'warning';
case'cancelada':
return'inactive';
default:
return'inactive';
}
};

export const getEstadoPagoTexto=(estado:string):string=>{
switch(estado.toLowerCase()){
case'completado':
return'✅Completado';
case'pendiente':
return'⏳Pendiente';
case'fallido':
return'❌Fallido';
case'cancelado':
return'🚫Cancelado';
default:
return estado;
}
};

//=============FUNCIONESDEAPI=============
export const listarPlanes=async():Promise<PlanSuscripcion[]>=>{
try{
console.log('🔍Obteniendolistadeplanes...');
const response=await api.get('/suscripciones/listar_planes/');
console.log('✅Planesobtenidos:',response.data);

if(Array.isArray(response.data)){
return response.data;
}else{
console.warn('⚠️Formatoderespuestainesperado:',response.data);
return[];
}
}catch(error){
console.error('❌Errorobteniendoplanes:',error);
throw error;
}
};

//NuevafunciónespecíficaparaSuperAdminqueincluyeelcampostatus
export const listarPlanesAdmin=async():Promise<PlanSuscripcion[]>=>{
try{
console.log('🔍SuperAdmin:ObteniendoTODOSlosplanes(incluyestatus)...');
const response=await api.get('/superadmin/listar_planes_admin/');
console.log('✅SuperAdmin:Planesobtenidosconstatus:',response.data);

if(Array.isArray(response.data)){
return response.data;
}else{
console.warn('⚠️SuperAdmin:Formatoderespuestainesperado:',response.data);
return[];
}
}catch(error){
console.error('❌SuperAdmin:Errorobteniendoplanes:',error);
throw error;
}
};

export const listarSuscripciones=async():Promise<SuscripcionEmpresa[]>=>{
try{
console.log('🔍Obteniendolistadesuscripciones...');
const response=await api.get('/suscripciones/listar_suscripciones/');
console.log('✅Suscripcionesobtenidas:',response.data);

if(Array.isArray(response.data)){
return response.data;
}else if(response.data&&Array.isArray(response.data.suscripciones)){
return response.data.suscripciones;
}else{
console.warn('⚠️Formatoderespuestainesperado:',response.data);
return[];
}
}catch(error){
console.error('❌Errorobteniendosuscripciones:',error);
throw error;
}
};

export const listarPagos=async():Promise<Pago[]>=>{
try{
console.log('🔍Obteniendolistadepagos...');
const response=await api.get('/subscriptions/pagos/');
console.log('✅Pagosobtenidos:',response.data);

if(Array.isArray(response.data)){
return response.data;
}else if(response.data&&Array.isArray(response.data.pagos)){
return response.data.pagos;
}else{
console.warn('⚠️Formatoderespuestainesperadoparapagos:',response.data);
return[];
}
}catch(error){
console.error('❌Errorobteniendopagos:',error);
throw error;
}
};

export const crearPlan=async(planData:Omit<PlanSuscripcion,'plan_id'>):Promise<PlanSuscripcion>=>{
try{
console.log('🔄Creandonuevoplan:',planData);
const response=await api.post('/subscriptions/crear-plan/',planData);
console.log('✅Plancreado:',response.data);
return response.data.plan;
}catch(error){
console.error('❌Errorcreandoplan:',error);
throw error;
}
};

export const editarPlan=async(planId:number,planData:Partial<PlanSuscripcion>):Promise<any>=>{
try{
console.log(`🔧Editandoplan${planId}:`,planData);
const response=await api.put('/subscriptions/editar-plan/',{
plan_id:planId,
...planData
});
console.log('✅Planeditado:',response.data);
return response.data;
}catch(error){
console.error('❌Erroreditandoplan:',error);
throw error;
}
};

export const cambiarEstadoPlan=async(planId:number,nuevoEstado:boolean):Promise<any>=>{
try{
console.log(`🔄Cambiandoestadodelplan${planId}a${nuevoEstado}...`);
const response=await api.put('/subscriptions/editar-plan/',{
plan_id:planId,
status:nuevoEstado
});
console.log('✅Estadodelplancambiado:',response.data);
return response.data;
}catch(error){
console.error('❌Errorcambiandoestadodelplan:',error);
throw error;
}
};

export const crearSuscripcion=async(empresaId:number,planId:number):Promise<any>=>{
try{
console.log(`🔄Creandosuscripciónparaempresa${empresaId}conplan${planId}...`);
const response=await api.post('/suscripciones/crear_suscripcion/',{
empresa_id:empresaId,
plan_id:planId
});
console.log('✅Suscripcióncreada:',response.data);
return response.data;
}catch(error){
console.error('❌Errorcreandosuscripción:',error);
throw error;
}
};

export const renovarSuscripcion=async(empresaId:number,planId:number):Promise<any>=>{
try{
console.log(`🔄Renovandosuscripciónparaempresa${empresaId}conplan${planId}...`);
const response=await api.post('/suscripciones/crear_suscripcion/',{
empresa_id:empresaId,
plan_id:planId
});
console.log('✅Suscripciónrenovada:',response.data);
return response.data;
}catch(error){
console.error('❌Errorrenovandosuscripción:',error);
throw error;
}
};

export const suspenderSuscripcion=async(suscripcionId:number):Promise<any>=>{
try{
console.log(`🔄Suspendiendosuscripción${suscripcionId}...`);
const response=await api.post('/subscriptions/suspender-suscripcion/',{
suscripcion_id:suscripcionId
});
console.log('✅Suscripciónsuspendida:',response.data);
return response.data;
}catch(error){
console.error('❌Errorsuspendiendosuscripción:',error);
throw error;
}
};

export const reactivarSuscripcion=async(suscripcionId:number):Promise<any>=>{
try{
console.log(`🔄Reactivandosuscripción${suscripcionId}...`);
const response=await api.post('/subscriptions/reactivar-suscripcion/',{
suscripcion_id:suscripcionId
});
console.log('✅Suscripciónreactivada:',response.data);
return response.data;
}catch(error){
console.error('❌Errorreactivandosuscripción:',error);
throw error;
}
};

export const procesarPago=async(suscripcionId:number,montoPago:number,transaccionId?:string):Promise<any>=>{
try{
console.log(`🔄Procesandopagoparasuscripción${suscripcionId}...`);
const response=await api.post('/subscriptions/procesar-pago/',{
suscripcion_id:suscripcionId,
monto_pago:montoPago,
transaccion_id:transaccionId||`PAY-${Date.now()}`
});
console.log('✅Pagoprocesado:',response.data);
return response.data;
}catch(error){
console.error('❌Errorprocesandopago:',error);
throw error;
}
};

export const obtenerInfoSuscripcionEmpresa=async(empresaId:number):Promise<any>=>{
try{
console.log(`🔍Obteniendoinformacióndesuscripciónparaempresa${empresaId}...`);
const response=await api.get(`/subscriptions/info-empresa/?empresa_id=${empresaId}`);
console.log('✅Informacióndesuscripciónobtenida:',response.data);
return response.data;
}catch(error){
console.error('❌Errorobteniendoinformacióndesuscripción:',error);
throw error;
}
};

//=============FUNCIONESFALTANTESCORREGIDAS=============

//✅Funciónparaobtenersuscripciónactual(SINparámetrospordefecto-usaempresaIddeuserData)
export const obtenerSuscripcionActual=async(empresaId?:number):Promise<SuscripcionEmpresa|null>=>{
try{
//SinoseproporcionaempresaId,intentarobtenerlodelcontextoolocalStorage
let targetEmpresaId=empresaId;
if(!targetEmpresaId){
const userData=JSON.parse(localStorage.getItem('userData')||'{}');
targetEmpresaId=userData.empresa_id;
}

if(!targetEmpresaId){
console.warn('⚠️Nosepudodeterminarelempresa_idparaobtenersuscripciónactual');
return null;
}

console.log(`🔍Obteniendosuscripciónactualparaempresa${targetEmpresaId}...`);
const response=await api.get(`/subscriptions/info-empresa/?empresa_id=${targetEmpresaId}`);
console.log('✅Informacióndesuscripciónobtenida:',response.data);

//Sielresponsecontienelainformacióndesuscripción,laretornamos
if(response.data&&response.data.tiene_suscripcion){
//ConstruirobjetoSuscripcionEmpresadesdelarespuesta
const suscripcionData:SuscripcionEmpresa={
suscripcion_id:response.data.suscripcion_id||0,
empresa_id:targetEmpresaId,
empresa_nombre:response.data.empresa_nombre||'',
plan_id:response.data.plan_id||0,
plan_nombre:response.data.plan_nombre||'',
plan_precio:response.data.precio||0,
plan_duracion:response.data.duracion||0,
fecha_inicio:response.data.fecha_inicio||'',
fecha_fin:response.data.fecha_fin||'',
estado:response.data.estado||'Activa',
status:response.data.esta_activa||false,
dias_restantes:response.data.dias_restantes||0,
esta_activa:response.data.esta_activa||false,
esta_por_vencer:response.data.esta_por_vencer||false
};

return suscripcionData;
}

return null;
}catch(error){
console.error('❌Errorobteniendosuscripciónactual:',error);
return null;
}
};

//✅Funciónparasuscribirseaunplan(CONempresaIdyplanIdcomoparámetrosrequeridos)
export const suscribirseAPlan=async(planId:number,empresaId?:number,datosPago?:any):Promise<any>=>{
try{
//SinoseproporcionaempresaId,intentarobtenerlodelcontexto
let targetEmpresaId=empresaId;
if(!targetEmpresaId){
const userData=JSON.parse(localStorage.getItem('userData')||'{}');
targetEmpresaId=userData.empresa_id;
}

if(!targetEmpresaId){
throw new Error('Nosepudodeterminarelempresa_idparalasuscripción');
}

console.log(`🔄Suscribiendoempresa${targetEmpresaId}alplan${planId}...`);

//Primerocrearlasuscripción
const suscripcion=await crearSuscripcion(targetEmpresaId,planId);

//Siseproporcionandatosdepago,procesarlos
if(datosPago&&suscripcion.suscripcion_id){
const pago=await procesarPago(
suscripcion.suscripcion_id,
datosPago.monto||datosPago.precio||0,
datosPago.transaccion_id
);

console.log('✅Suscripciónypagocompletados:',{suscripcion,pago});
return{suscripcion,pago};
}

console.log('✅Suscripcióncreada(sinpago):',suscripcion);
return{suscripcion};
}catch(error){
console.error('❌Errorensuscribirseaplan:',error);
throw error;
}
};

//✅Funciónparaprocesarpagosimple(CORREGIRparámetros)
export const procesarPagoSimple=async(datosPago:{
empresa_id:number;
plan_id:number;
monto_pago:number;
metodo_pago?:string;
transaccion_id?:string;
}):Promise<any>=>{
try{
console.log('🔄Procesandopagosimple:',datosPago);

//Usarelendpointdepagosimpledelbackend
const response=await api.post('/subscriptions/pago-simple/',{
empresa_id:datosPago.empresa_id,
plan_id:datosPago.plan_id,
monto_pago:datosPago.monto_pago
});

console.log('✅Pagosimpleprocesado:',response.data);
return response.data;
}catch(error){
console.error('❌Errorprocesandopagosimple:',error);
throw error;
}
};

//✅Funciónparaobtenerinformacióncompletadesuscripciónporempresa
export const obtenerInfoCompleta=async(empresaId:number):Promise<{
suscripcion:SuscripcionEmpresa|null;
tiene_suscripcion:boolean;
requiere_pago:boolean;
acceso_reportes:boolean;
mensaje?:string;
}>=>{
try{
console.log(`🔍Obteniendoinformacióncompletaparaempresa${empresaId}...`);

const response=await api.get(`/subscriptions/info-empresa/?empresa_id=${empresaId}`);
const data=response.data;

let suscripcion=null;
if(data.tiene_suscripcion){
suscripcion=await obtenerSuscripcionActual(empresaId);
}

return{
suscripcion,
tiene_suscripcion:data.tiene_suscripcion||false,
requiere_pago:data.requiere_pago||false,
acceso_reportes:data.acceso_reportes||false,
mensaje:data.mensaje
};
}catch(error){
console.error('❌Errorobteniendoinformacióncompleta:',error);
return{
suscripcion:null,
tiene_suscripcion:false,
requiere_pago:true,
acceso_reportes:false,
mensaje:'Erroralobtenerinformacióndesuscripción'
};
}
};

//✅Funciónparaverificarestadodesuscripción
export const verificarEstadoSuscripcion=async(empresaId:number):Promise<{
activa:boolean;
vencida:boolean;
porVencer:boolean;
diasRestantes:number;
mensaje:string;
}>=>{
try{
const info=await obtenerInfoCompleta(empresaId);

if(!info.suscripcion){
return{
activa:false,
vencida:false,
porVencer:false,
diasRestantes:0,
mensaje:'Nohaysuscripciónactiva'
};
}

const diasRestantes=info.suscripcion.dias_restantes||0;
const activa=info.suscripcion.esta_activa||false;
const vencida=diasRestantes<=0&&!activa;
const porVencer=activa&&diasRestantes<=7;

let mensaje='';
if(vencida){
mensaje='Sususcripciónhavencido.Renueveparacontinuar.';
}else if(porVencer){
mensaje=`Sususcripciónvenceen${diasRestantes}día(s).`;
}else if(activa){
mensaje=`Suscripciónactiva.${diasRestantes}díasrestantes.`;
}

return{
activa,
vencida,
porVencer,
diasRestantes,
mensaje
};
}catch(error){
console.error('❌Errorverificandoestadodesuscripción:',error);
return{
activa:false,
vencida:true,
porVencer:false,
diasRestantes:0,
mensaje:'Erroralverificarsuscripción'
};
}
};

//✅Funcióncombinadaparasuscribirseypagar(RESTAURADA)
export const suscribirseYPagar=async(empresaId:number,planId:number,datosPago:any):Promise<any>=>{
try{
console.log(`🔄Procesandosuscripciónypagoparaempresa${empresaId}...`);

//Primerocrearlasuscripción
const suscripcion=await crearSuscripcion(empresaId,planId);

//Luegoprocesarelpago
const pago=await procesarPago(suscripcion.suscripcion_id,datosPago.monto,datosPago.transaccion_id);

console.log('✅Suscripciónypagocompletados:',{suscripcion,pago});
return{suscripcion,pago};
}catch(error){
console.error('❌Errorensuscripciónypago:',error);
throw error;
}
};

//=============ALIASESPARACOMPATIBILIDAD=============
export const obtenerSuscripciones=listarSuscripciones;
export const obtenerPagos=listarPagos;

//=============EXPORTPORDEFECTOSINDUPLICACIONES=============
export default{
//Planes
listarPlanes,
listarPlanesAdmin,//←Agregarnuevafunción
crearPlan,
editarPlan,
cambiarEstadoPlan,

//Suscripciones
listarSuscripciones,
obtenerSuscripciones,
crearSuscripcion,
renovarSuscripcion,
suspenderSuscripcion,
reactivarSuscripcion,
obtenerInfoSuscripcionEmpresa,
obtenerSuscripcionActual,//✅Agregar
suscribirseAPlan,//✅Agregar
obtenerInfoCompleta,//✅Agregar
verificarEstadoSuscripcion,//✅Agregar

//Pagos
listarPagos,
obtenerPagos,
procesarPago,
procesarPagoSimple,//✅Agregar
suscribirseYPagar,//✅Restaurar

//Utilidades
formatearPrecio,
formatearDuracion,
formatearFecha,
getEstadoSuscripcionTexto,
getEstadoSuscripcionColor,
getEstadoPagoTexto
};
