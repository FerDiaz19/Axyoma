import React, { useState, useCallback } from 'react';
import useDebounce from '../hooks/useDebounce';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  className?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({ 
  onSearch, 
  placeholder = "Buscar...",
  className = ""
}) => {
  // Estado local para el texto de búsqueda
  const [searchText, setSearchText] = useState('');
  
  // Aplicar debounce al texto de búsqueda (500ms)
  const debouncedSearchText = useDebounce(searchText, 500);
  
  // Efecto para ejecutar la búsqueda solo cuando debouncedSearchText cambie
  React.useEffect(() => {
    // Ejecutar la función de búsqueda con el texto con debounce
    onSearch(debouncedSearchText);
  }, [debouncedSearchText, onSearch]);
  
  // Manejar cambios en el input sin causar recargas
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    // Evitar comportamiento predeterminado si es necesario
    e.preventDefault();
    // Actualizar el estado local
    setSearchText(e.target.value);
  }, []);
  
  // Prevenir recarga al presionar Enter
  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
  }, []);

  return (
    <form onSubmit={handleSubmit} className={`search-form ${className}`}>
      <input
        type="text"
        value={searchText}
        onChange={handleChange}
        placeholder={placeholder}
        className="search-input"
      />
      {/* Opcionalmente, agregar un botón de búsqueda */}
      <button type="submit" className="search-button">
        🔍
      </button>
    </form>
  );
};

export default SearchBar;
