import { useEffect, useState } from "react";
import { getSummary } from "../api/UsageApi";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getSummary().then(setData);
  }, []);

  if (!data) {
    return (
      <div style={{ padding: "30px" }}>
        <h2> Usage Dashboard</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div
      style={{
        padding: "30px",
        background: "#f5f7fa",
        minHeight: "100vh",
      }}
    >
      <h1 style={{ marginBottom: "20px" }}> Telecom Dashboard</h1>

      {/*  KPI GRID */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px",
        }}
      >
        {renderCard(" Total Calls", data.total_calls, "#4CAF50")}
        {renderCard(" Total SMS", data.total_sms, "#2196F3")}
        {renderCard(
          " Internet MB",
          data.total_internet_mb.toFixed(2),
          "#FF9800",
        )}
        {renderCard(" Peak Hour", data.peak_hour, "#9C27B0")}
        {renderCard(" Busiest Region", data.busiest_region, "#F44336")}
      </div>
    </div>
  );
}

/*  KPI CARD BUILDER */
function renderCard(title, value, color) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "12px",
        padding: "20px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
        borderTop: `5px solid ${color}`,
      }}
    >
      <p style={{ color: "gray", fontSize: "14px" }}>{title}</p>
      <h2 style={{ margin: "10px 0" }}>{value}</h2>
    </div>
  );
}
