import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

// Layout
import Home from './layout/Home';


const AppRoutes = () => (
    <Routes>
        {/* Public routes */}
        <Route index element={<Home />} />
    </Routes>
);

export default AppRoutes;
