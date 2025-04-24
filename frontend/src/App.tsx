
import { Routes, Route } from 'react-router-dom';
import MainLayout from './layout/MainLayout';
import Home from './routes/Home';
import Upload from './routes/Upload';
import Report from './routes/Report';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Home />} />
        <Route path="upload" element={<Upload />} />
        <Route path="report" element={<Report />} />
      </Route>
    </Routes>
  );
};

export default App;
