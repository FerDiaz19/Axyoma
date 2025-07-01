import Sidebar from './Sidebar';
import Header from './Header';
import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <div className="flex flex-col w-full h-screen">
      {/* Sidebar con estado de colapso */}
      <Header />

      <div className='flex flex-1 w-full h-full bg-gray-200'>
        <Sidebar />

        <div className="flex-1 flex flex-col w-[80%] bg-gray-100">

          <main className="flex-1 p-4 overflow-auto">
            <Outlet /> {/* Aquí se renderizan las páginas */}
          </main>
        </div>
      </div>
    </div>
  );
};

export default Layout;
