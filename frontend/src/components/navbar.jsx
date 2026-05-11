import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <nav
      style={{
        padding: "15px 30px",
        background: "#1e293b",
        color: "white",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      {/* ✅ LOGO / APP NAME */}
      <h2 style={{ margin: 0 }}>📡 Telecom AI</h2>

      {/* ✅ NAV LINKS */}
      <div style={{ display: "flex", gap: "20px" }}>
        <StyledLink to="/">Dashboard</StyledLink>
        <StyledLink to="/region">Region</StyledLink>
        <StyledLink to="/peak">Peak</StyledLink>
        <StyledLink to="/risk">Prediction</StyledLink>
      </div>
    </nav>
  );
}

/* ✅ REUSABLE LINK STYLE */
function StyledLink({ to, children }) {
  return (
    <Link
      to={to}
      style={{
        color: "#e2e8f0",
        textDecoration: "none",
        fontWeight: "500",
        transition: "0.2s",
      }}
      onMouseOver={(e) => (e.target.style.color = "#38bdf8")}
      onMouseOut={(e) => (e.target.style.color = "#e2e8f0")}
    >
      {children}
    </Link>
  );
}
