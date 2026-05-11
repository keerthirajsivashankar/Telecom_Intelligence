import { useState } from "react";
import { predictRisk } from "../api/UsageApi";

export default function RiskPrediction() {
  const [form, setForm] = useState({
    region: "",
    avg_usage: "",
    growth_rate: "",
    variability: "",
  });

  const [res, setRes] = useState(null);

  const handleSubmit = async () => {
    const result = await predictRisk({
      ...form,
      avg_usage: Number(form.avg_usage),
      growth_rate: Number(form.growth_rate),
      variability: Number(form.variability),
    });

    setRes(result);
  };

  return (
    <div
      style={{
        padding: "30px",
        background: "#f5f7fa",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "30px",
          borderRadius: "12px",
          boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
          width: "400px",
        }}
      >
        <h2 style={{ marginBottom: "20px", textAlign: "center" }}>
          Risk Prediction
        </h2>

        {/* Inputs */}
        <input
          placeholder="Region"
          style={inputStyle}
          onChange={(e) => setForm({ ...form, region: e.target.value })}
        />

        <input
          placeholder="Avg Usage"
          style={inputStyle}
          onChange={(e) => setForm({ ...form, avg_usage: e.target.value })}
        />

        <input
          placeholder="Growth Rate"
          style={inputStyle}
          onChange={(e) => setForm({ ...form, growth_rate: e.target.value })}
        />

        <input
          placeholder="Variability"
          style={inputStyle}
          onChange={(e) => setForm({ ...form, variability: e.target.value })}
        />

        {/* Button */}
        <button
          onClick={handleSubmit}
          style={{
            width: "100%",
            padding: "12px",
            background: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "bold",
            marginTop: "10px",
          }}
        >
          Predict
        </button>

        {/* Result */}
        {res && (
          <div
            style={{
              marginTop: "20px",
              padding: "15px",
              borderRadius: "10px",
              background:
                res.congestion_risk === "HIGH"
                  ? "#ffdddd"
                  : res.congestion_risk === "MEDIUM"
                    ? "#fff3cd"
                    : "#ddffdd",
            }}
          >
            <h3>Result</h3>
            <p>
              <b>Risk:</b> {res.congestion_risk}
            </p>
            <p>
              <b>Anomaly:</b> {res.anomaly_flag ? "Yes " : "No "}
            </p>
            <p>
              <b>Score:</b> {res.score.toFixed(2)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/*  Reusable input style */
const inputStyle = {
  width: "100%",
  padding: "10px",
  marginBottom: "10px",
  borderRadius: "6px",
  border: "1px solid #ccc",
};
