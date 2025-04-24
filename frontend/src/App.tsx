
import { Routes, Route } from 'react-router-dom';
import MainLayout from './layout/MainLayout';
import Home from './routes/Home';
import Upload from './routes/Upload';
import Report from './routes/Report';
import CountrySelection from './routes/Onboarding';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route path="/" element={<CountrySelection />} />
        <Route path="/report/:country" element={<Report />} />
        { /*<Route index element={<Home />} />*/ }
        <Route path="upload" element={<Upload />} />
        <Route path="report" element={<Report />} />
      </Route>
    </Routes>
  );
};

export default App;
