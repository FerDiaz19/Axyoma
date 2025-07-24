import { useState, useEffect } from 'react';

/**
 * Hook para aplicar debounce a valores que cambian frecuentemente
 * @param value El valor a aplicar debounce
 * @param delay Tiempo de espera en ms (default: 500ms)
 * @returns El valor con debounce aplicado
 */
export default function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    // Configurar temporizador para actualizar el valor después del retraso
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Limpiar temporizador si el valor cambia antes del retraso o si el componente se desmonta
    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}
