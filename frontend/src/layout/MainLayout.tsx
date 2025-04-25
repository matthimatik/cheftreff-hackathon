import { Outlet, NavLink } from 'react-router-dom';

const MainLayout = () => {
    // This is the main layout component that wraps around all pages
    // it has a header and a footer and a main content area
    return (
        <div className="flex flex-col min-h-screen">
            <header className="bg-gray-800 text-white p-4">
                <nav className="flex justify-between">
                    <div className="text-lg font-bold">World Food Programme</div>
                    <div>
                        <NavLink to="/" className="mx-2 hover:text-gray-400">Start</NavLink>
                        <NavLink to="/compare" className="mx-2 hover:text-gray-400">Compare</NavLink>
                        <NavLink to="/about" className="mx-2 hover:text-gray-400">About</NavLink>
                    </div>
                </nav>
            </header>

            <main className="flex-grow p-6">
                <Outlet />
            </main>

            <footer className="bg-gray-800 text-white p-4 text-center">
                &copy; 2025 TEAM Chäffchen
            </footer>
        </div>
    );
};

export default MainLayout;
