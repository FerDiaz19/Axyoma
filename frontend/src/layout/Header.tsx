import React, { useState, useRef, useEffect } from "react";


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
        className="w-8 h-8 bg-green-100 text-green-800 font-semibold rounded-full flex items-center justify-center hover:bg-green-200 transition-colors cursor-pointer"
      >
        {userInitials}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border border-gray-200">
          <div className="px-4 py-2 text-sm text-gray-700 border-b border-gray-100">
            <div className="font-medium">Mi cuenta</div>
            <div className="text-xs text-gray-500 truncate">{user?.email}</div>
          </div>
          <button
            onClick={onLogout}
            className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
          >
            Cerrar sesión
          </button>
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
      sessionStorage.removeItem('user');
      sessionStorage.removeItem('token');
      
      // Recargar la página para volver al login
      window.location.reload();
    } catch (e) {
      console.error("Error cerrando sesión", e);
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white h-12 py-4 border-b border-gray-200 flex items-center justify-between px-4 ">
      <div className="flex items-center gap-4">
        {logo ? (
          <img src={logo} alt="Logo" className="w-8 h-8 object-contain rounded" />
        ) : (
          <div className="w-8 h-8 bg-black text-white flex items-center justify-center rounded">
            {companyName ? companyName.charAt(0).toUpperCase() : "E"}
          </div>
        )}
        {companyName && (
          <span className="text-sm font-semibold text-gray-700 truncate max-w-[150px]">
            {companyName}
          </span>
        )}
      </div>

      <div className="flex-1 max-w-lg mx-4">
        <input
          type="text"
          placeholder="Search or type a command (Ctrl + G)"
          className="w-full px-4  text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="flex items-center gap-4">
        <button className="text-gray-500 hover:text-gray-700">🔔</button>
        <div className="text-sm text-gray-600 cursor-pointer hover:text-gray-800">Help ▾</div>
        <UserDropdown userInitials={userInitials} onLogout={handleLogout} user={user} />
      </div>
    </header>
  );
};

export default Header;
