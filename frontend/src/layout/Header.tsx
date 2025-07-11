import React, { useState, useRef, useEffect } from "react";
import "../css/Header.css";


interface User {
  pk: number;
  email: string;
  username: string;
  full_name: string;
  role: string;
  fk_company: string | number;
}

const UserDropdown = ({
  userInitials,
  onLogout,
  user,
}: {
  userInitials: string;
  onLogout: () => void;
  user: User | null;
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="user-dropdown-button flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 shadow-sm"
      >
        <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg flex items-center justify-center font-semibold shadow-sm avatar-gradient">
          {userInitials}
        </div>
        <span className="hidden sm:block max-w-[120px] truncate">
          {user?.full_name || user?.username || 'Usuario'}
        </span>
        <svg 
          className={`w-4 h-4 transition-transform duration-200 svg-icon ${isOpen ? 'rotate-180' : ''}`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>        {isOpen && (
          <div className="absolute right-0 mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-50 user-dropdown-menu animate-in fade-in-0 zoom-in-95">
            <div className="px-4 py-3 border-b border-gray-100">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg flex items-center justify-center font-semibold avatar-gradient">
                  {userInitials}
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900 truncate max-w-[160px]">
                    {user?.full_name || user?.username || 'Usuario'}
                  </p>
                  <p className="text-xs text-gray-500 truncate max-w-[160px]">
                    {user?.email || 'Sin email'}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="py-1">
              <button
                onClick={() => {
                  setIsOpen(false);
                  // Aquí puedes agregar más acciones de perfil
                }}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4 svg-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Ver perfil
              </button>
              
              <button
                onClick={() => {
                  setIsOpen(false);
                  // Aquí puedes agregar configuración
                }}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4 svg-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Configuración
              </button>
            </div>
            
            <div className="border-t border-gray-100 py-1">
              <button
                onClick={() => {
                  setIsOpen(false);
                  onLogout();
                }}
                className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4 svg-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Cerrar sesión
              </button>
            </div>
          </div>
        )}
    </div>
  );
};

const Header = () => {
  //const { logout } = useAuth();
  const storedUser = localStorage.getItem("user") || sessionStorage.getItem("user");
  const user = storedUser ? JSON.parse(storedUser) : null;
  const logo = user?.company?.logo;
  const companyName = user?.company?.name;

  const userInitials = user?.full_name
    ? user.full_name
        .split(" ")
        .map((n: string) => n[0])
        .join("")
        .slice(0, 2)
        .toUpperCase()
    : "JD";

  const handleLogout = async () => {
    try {
      // Limpiar localStorage y sessionStorage
      localStorage.removeItem('user');
      localStorage.removeItem('token');
      localStorage.removeItem('authToken');
      localStorage.removeItem('empresaData');
      localStorage.removeItem('userData');
      sessionStorage.removeItem('user');
      sessionStorage.removeItem('token');
      
      // Redireccionar a localhost:3000
      window.location.href = 'http://localhost:3000';
    } catch (e) {
      console.error("Error cerrando sesión", e);
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white h-16 border-b border-gray-200 flex items-center justify-between px-6 shadow-sm">
      <div className="flex items-center gap-4">
        {logo ? (
          <img src={logo} alt="Logo" className="w-10 h-10 object-contain rounded" />
        ) : (
          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 text-white flex items-center justify-center rounded-lg font-bold">
            {companyName ? companyName.charAt(0).toUpperCase() : "E"}
          </div>
        )}
        {companyName && (
          <span className="text-lg font-semibold text-gray-800 truncate max-w-[200px]">
            {companyName}
          </span>
        )}
      </div>

      <div className="flex-1 max-w-2xl mx-8">
        <input
          type="text"
          placeholder="Search or type a command (Ctrl + G)"
          className="search-input w-full px-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50"
        />
      </div>

      <div className="flex items-center gap-6">
        <button className="header-button text-gray-500 hover:text-gray-700 p-2 rounded-full hover:bg-gray-100 transition-colors">
          <span className="text-lg">🔔</span>
        </button>
        <div className="header-button text-sm text-gray-600 cursor-pointer hover:text-gray-800 px-3 py-1 rounded-md hover:bg-gray-100 transition-colors">
          Help ▾
        </div>
        <UserDropdown userInitials={userInitials} onLogout={handleLogout} user={user} />
      </div>
    </header>
  );
};

export default Header;
