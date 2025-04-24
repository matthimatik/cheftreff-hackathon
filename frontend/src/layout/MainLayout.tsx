import { Outlet, NavLink } from 'react-router-dom';

const MainLayout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow px-6 py-4 flex gap-6">
        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? 'text-blue-600 font-bold' : 'text-gray-600 hover:text-blue-500'
          }
        >
          Home
        </NavLink>
        <NavLink
          to="/upload"
          className={({ isActive }) =>
            isActive ? 'text-blue-600 font-bold' : 'text-gray-600 hover:text-blue-500'
          }
        >
          Upload
        </NavLink>
        <NavLink
          to="/report"
          className={({ isActive }) =>
            isActive ? 'text-blue-600 font-bold' : 'text-gray-600 hover:text-blue-500'
          }
        >
          Report
        </NavLink>
      </nav>
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
};

export default MainLayout;
