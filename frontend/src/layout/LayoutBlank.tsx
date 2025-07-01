import { Outlet } from 'react-router-dom';

const LayoutBlank = () => {
  return (
    <div className="w-full min-h-screen bg-white">
      <main className="p-4">
        <Outlet />
      </main>
    </div>
  );
};

export default LayoutBlank;
