import { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Mirror from './pages/Mirror';
import Dashboard from './pages/Dashboard';
import CharacterSetup from './pages/CharacterSetup';

function App() {
  const [character, setCharacter] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://${window.location.hostname}:8000/api/character`)
      .then((res) => res.json())
      .then((data) => {
        setCharacter(data.character);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return null;

  return (
    <div className="app-container">
      <Routes>
        <Route
          path="/"
          element={character ? <Mirror character={character} /> : <Navigate to="/setup" />}
        />
        <Route path="/setup" element={<CharacterSetup />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  );
}

export default App;
