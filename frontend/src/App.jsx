import { Routes, Route } from 'react-router-dom';
import Mirror from './pages/Mirror';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <div className="app-container">
      <Routes>
        <Route path="/" element={<Mirror />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  );
}

export default App;
