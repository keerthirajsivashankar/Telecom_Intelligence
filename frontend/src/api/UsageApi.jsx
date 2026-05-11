const BASE = import.meta.env.VITE_API_BASE;

export const getSummary = async () => {
  const res = await fetch(`${BASE}/usage/summary`);
  if (!res.ok) throw new Error("Summary failed");
  return res.json();
};

export const getRegion = async (region) => {
  const res = await fetch(`${BASE}/usage/region/${region}`);
  return res.json();
};

export const getPeak = async () => {
  const res = await fetch(`${BASE}/usage/peak`);
  return res.json();
};

export const predictRisk = async (body) => {
  const res = await fetch(`${BASE}/predict-usage-risk`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
};
