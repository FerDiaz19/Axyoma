import api from "../api";

// Types
export interface EmpresaRegistro {
  nombre: string;
  rfc: string;
  direccion?: string;
  email_contacto?: string;
  telefono_contacto?: string;
  usuario: string;
  password: string;
  nombre_completo: string;
}

export interface EmpresaResponse {
  message: string;
  empresa_id: number;
  empresa: {
    empresa_id: number;
    nombre: string;
    rfc: string;
    direccion?: string;
    status: boolean;
    fecha_registro: string;
  };
}

const context = "empresas/";

export const registrarEmpresa = async (data: EmpresaRegistro): Promise<EmpresaResponse> => {
  const response = await api.post<EmpresaResponse>(`${context}registro/`, data);
  return response.data;
};
