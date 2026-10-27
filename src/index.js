// Doorsturen van oude/alternatieve adressen naar https://hear.nl; verder statische site uit ./site.
// POST /api/aanvraag: het aanvraagformulier (site/aanvraag.html) mailen naar maarten@hear.nl via Resend.
// Vereist secret RESEND_API_KEY (wrangler secret put RESEND_API_KEY) en een geverifieerd afzenderdomein hear.nl bij Resend.
// Geen opslag: de inzending wordt alleen doorgestuurd.

const NAAR = "maarten@hear.nl";
const VAN = "HEAR aanvraag <aanvraag@hear.nl>";

const VELDEN = [
  ["naam", "Naam"], ["organisatie", "Organisatie"], ["functie", "Functie"], ["email", "E-mail"], ["telefoon", "Telefoon"],
  ["soort", "Soort event"], ["soort_anders", "Soort, anders"], ["event", "Naam event"], ["datum", "Datum"], ["tijd", "Tijd"],
  ["gasten", "Aantal gasten"], ["doelgroep", "Doelgroep"], ["diensten", "Diensten"], ["diensten_anders", "Diensten, anders"],
  ["bericht", "Bericht"], ["concept", "Concept / programma"], ["m2", "Ruimte m²"], ["diepte", "Diepte (m)"], ["ruimte", "Ruimte"],
  ["budget", "Richtbudget"],
];

function schoon(v) { return String(v || "").replace(/\r/g, "").trim().slice(0, 4000); }

async function aanvraag(request, env) {
  const fd = await request.formData();
  if (schoon(fd.get("website"))) return antwoord(request, true); // honeypot: doen alsof het gelukt is
  const d = {};
  for (const [k] of VELDEN) d[k] = k === "diensten" ? fd.getAll("diensten").map(schoon).filter(Boolean).join(", ") : schoon(fd.get(k));
  if (fd.get("budget_onbekend")) d.budget = "weet ik nog niet";
  else if (fd.get("budget_van") || fd.get("budget_tot")) d.budget = `€ ${schoon(fd.get("budget_van"))} – € ${schoon(fd.get("budget_tot"))}`;
  if (!d.naam || !d.email || !d.telefoon || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) return antwoord(request, false, 400);

  const regels = VELDEN.filter(([k]) => d[k]).map(([k, l]) => `${l}: ${d[k]}`).join("\n");
  const onderwerp = `Aanvraag via hear.nl: ${d.organisatie || d.naam}${d.datum ? ", " + d.datum : ""}`;
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: VAN, to: [NAAR], reply_to: d.email, subject: onderwerp, text: regels + "\n" }),
  });
  return antwoord(request, r.ok, r.ok ? 200 : 502);
}

function antwoord(request, ok, status = 200) {
  if ((request.headers.get("Accept") || "").includes("application/json"))
    return new Response(JSON.stringify({ ok }), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  const terug = new URL(request.url);
  const en = (request.headers.get("Referer") || "").includes("/en/");
  terug.pathname = (en ? "/en" : "") + "/aanvraag.html";
  terug.search = ok ? "?verzonden=1" : "?fout=1";
  return Response.redirect(terug.toString(), 303);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname !== "hear.nl") {
      url.hostname = "hear.nl";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    if (url.pathname === "/api/aanvraag") {
      if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
      if (!env.RESEND_API_KEY) return antwoord(request, false, 503);
      try { return await aanvraag(request, env); } catch (e) { return antwoord(request, false, 500); }
    }
    return env.ASSETS.fetch(request);
  },
};
