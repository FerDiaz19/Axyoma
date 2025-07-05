import { Route, Routes } from 'react-router-dom';

// Components
import Dashboard from './components/Dashboard';

const AppRoutes = () => (
    <Routes>
        <Route index element={<Dashboard />} />
    </Routes>
);

export default AppRoutes;
