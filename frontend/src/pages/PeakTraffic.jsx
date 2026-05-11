import { useEffect, useState } from "react";
import { getPeak } from "../api/UsageApi";

export default function PeakTraffic() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getPeak().then(setData);
  }, []);

  if (!data) {
    return (
      <div style={{ padding: "30px" }}>
        <h2> Peak Traffic</h2>
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
      <h2 style={{ marginBottom: "20px" }}> Peak Traffic Analysis</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
        }}
      >
        {/*  TOP HOURS CARD */}
        <div style={cardStyle}>
          <h3 style={{ marginBottom: "10px" }}> Top Hours</h3>
          {data.top_hours.map((h, i) => (
            <div key={i} style={rowStyle}>
              <span>Hour {h.hour}</span>
              <span style={{ fontWeight: "bold" }}>
                {h.total_usage.toFixed(2)}
              </span>
            </div>
          ))}
        </div>

        {/*  TOP REGIONS CARD */}
        <div style={cardStyle}>
          <h3 style={{ marginBottom: "10px" }}>📍 Top Regions</h3>
          {data.top_regions.map((r, i) => (
            <div key={i} style={rowStyle}>
              <span>{r.region}</span>
              <span style={{ fontWeight: "bold" }}>
                {r.total_usage.toFixed(2)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/*  CARD STYLE */
const cardStyle = {
  background: "white",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
};

/*  ROW STYLE */
const rowStyle = {
  display: "flex",
  justifyContent: "space-between",
  padding: "10px 0",
  borderBottom: "1px solid #eee",
};
