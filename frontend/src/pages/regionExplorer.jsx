import { useState } from "react";
import { getRegion } from "../api/UsageApi";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function RegionExplorer() {
  const [region, setRegion] = useState("");
  const [data, setData] = useState(null);

  const handleSearch = async () => {
    const res = await getRegion(region);
    setData(res);
  };

  return (
    <div
      style={{
        padding: "30px",
        background: "#f5f7fa",
        minHeight: "100vh",
      }}
    >
      <h2 style={{ marginBottom: "20px" }}>🌍 Region Explorer</h2>

      {/* ✅ Search Box Card */}
      <div
        style={{
          background: "white",
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          marginBottom: "20px",
          display: "flex",
          gap: "10px",
        }}
      >
        <input
          value={region}
          onChange={(e) => setRegion(e.target.value)}
          placeholder="Enter region (e.g. Centro)"
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ccc",
          }}
        />

        <button
          onClick={handleSearch}
          style={{
            padding: "10px 20px",
            background: "#2196F3",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Search
        </button>
      </div>

      {/* ✅ DATA TABLE */}
      {data && (
        <div
          style={{
            background: "white",
            padding: "20px",
            borderRadius: "12px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          }}
        >
          <h3>Hourly Distribution</h3>

          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              marginTop: "15px",
            }}
          >
            <thead>
              <tr style={{ background: "#eee" }}>
                <th style={th}>Hour</th>
                <th style={th}>Calls</th>
                <th style={th}>SMS</th>
                <th style={th}>Internet MB</th>
              </tr>
            </thead>

            <tbody>
              {data.hourly_distribution.map((row, i) => (
                <tr key={i} style={{ textAlign: "center" }}>
                  <td style={td}>{row.hour}</td>
                  <td style={td}>{row.calls}</td>
                  <td style={td}>{row.sms}</td>
                  <td style={td}>{row.internet_mb.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

/* ✅ TABLE STYLES */
const th = {
  padding: "10px",
  borderBottom: "1px solid #ccc",
};

const td = {
  padding: "10px",
  borderBottom: "1px solid #eee",
};
