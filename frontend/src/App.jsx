import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import RegionExplorer from "./pages/regionExplorer";
import PeakTraffic from "./pages/PeakTraffic";
import RiskPrediction from "./pages/RiskPrediction";
import NavBar from "./components/navbar";

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/region" element={<RegionExplorer />} />
        <Route path="/peak" element={<PeakTraffic />} />
        <Route path="/risk" element={<RiskPrediction />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
