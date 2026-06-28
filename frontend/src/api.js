export async function buildGtm(founderText) {
  const response = await fetch("/api/build-gtm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ founderText }),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || "Unable to build GTM plan");
  }
  return data;
}
