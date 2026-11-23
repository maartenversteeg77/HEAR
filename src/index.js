// Doorsturen van oude/alternatieve adressen naar https://hear.nl; verder statische site uit ./site.
// POST /api/aanvraag: het aanvraagformulier (site/aanvraag.html) mailen naar maarten@hear.nl via Resend.
// Vereist secret RESEND_API_KEY (wrangler secret put RESEND_API_KEY) en een geverifieerd afzenderdomein hear.nl bij Resend.
// Geen opslag: de inzending wordt alleen doorgestuurd.

const NAAR = "maarten@hear.nl";
const VAN = "HEAR aanvraag <aanvraag@hear.nl>";

const VELDEN = [
  ["route", "Wil"], ["gesprek", "Gesprek via"], ["gesprek_datum", "Voorkeursdatum gesprek"], ["gesprek_dagdeel", "Dagdeel"],
  ["naam", "Naam"], ["organisatie", "Organisatie"], ["functie", "Functie"], ["email", "E-mail"], ["telefoon", "Telefoon"],
  ["rol", "Aanvrager is"], ["rol_anders", "Aanvrager is, anders"], ["soort", "Soort event"], ["soort_anders", "Soort, anders"], ["event", "Naam event"], ["locatie", "Locatie"], ["datum", "Datum"], ["tijd", "Tijd"],
  ["gasten", "Aantal gasten"], ["doelgroep", "Doelgroep"], ["programma", "Programma"], ["diensten", "Diensten"], ["diensten_anders", "Diensten, anders"], ["communicatie", "Communicatie"], ["communicatie_anders", "Communicatie, anders"],
  ["geluid", "Geluid"], ["scherm", "Scherm"], ["uren_dag", "Uren dagprogramma"], ["uren_dj", "Uren dj"], ["personeel", "Personeel"], ["licht", "Licht en aankleding"], ["logo", "Logo"], ["indicatie", "Indicatie"],
  ["ruimte", "Ruimte"], ["concept", "Concept / programma"], ["bericht", "Bericht"],
  ["budget", "Richtbudget"],
  ["cc_soort", "Playlist"], ["cc_zaak", "Soort zaak"], ["cc_capaciteit", "Capaciteit van de zaak"], ["cc_dienst", "Ontvangen op"], ["cc_playlist", "Link naar favoriete nummers"],
  ["cc_wens", "Coffee cuts, meer weten over"], ["cc_lengte", "Lengte playlist (uur)"], ["cc_sfeer", "Sfeer in de zaak / voorbeeldplek"], ["cc_lijkt", "Moet lijken op"], ["cc_nummers", "Voorbeelden van nummers"],
];

function schoon(v) { return String(v || "").replace(/\r/g, "").trim().slice(0, 4000); }

async function aanvraag(request, env) {
  const fd = await request.formData();
  if (schoon(fd.get("website"))) return antwoord(request, true); // honeypot: doen alsof het gelukt is
  const d = {};
  for (const [k] of VELDEN) d[k] = (k === "diensten" || k === "diensten_anders" || k === "programma" || k === "communicatie" || k === "cc_wens" || k === "licht" || k === "scherm") ? [...new Set(fd.getAll(k).map(schoon).filter(Boolean))].join(", ") : schoon(fd.get(k));
  if (fd.get("budget_onbekend")) d.budget = "weet ik nog niet";
  else if (fd.has("budget_ingevuld") && !schoon(fd.get("budget_ingevuld"))) d.budget = fd.has("budget_van") ? "niet ingevuld" : ""; // schuif niet aangeraakt: de beginstand is geen antwoord
  else if (fd.get("budget_van") || fd.get("budget_tot")) d.budget = `€ ${schoon(fd.get("budget_van"))} – € ${schoon(fd.get("budget_tot"))}`;
  const hoofdformulier = !schoon(fd.get("bron")); // aanvraagformulier: naam, e-mail en telefoon verplicht; bij een call ook het contactmoment
  if (hoofdformulier && d.route === "voorstel") { d.gesprek = ""; d.gesprek_datum = ""; d.gesprek_dagdeel = ""; }
  const route = d.route;
  if (!d.naam || !d.email || (hoofdformulier && (!d.telefoon || (d.route === "call" && !d.gesprek_datum))) || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) return antwoord(request, false, 400);

  // leesbare waarden in de mail
  const LABEL = { voorstel: "een vrijblijvend voorstel", call: "een call", bellen: "telefoon", teams: "Microsoft Teams", meet: "Google Meet", zakelijk: "zakelijk (netwerk)event", lezing: "lezing of seminar",
    personeelsfeest: "personeelsfeest", merkactivatie: "merkactivatie", dance: "dance event", anders: "anders" };
  const MAAND = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"];
  const datum = (v) => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v); return m ? `${+m[3]} ${MAAND[+m[2] - 1]} ${m[1]}` : v; };
  const eur = (v) => Number(v).toLocaleString("nl-NL");
  for (const k of ["route", "gesprek", "soort"]) if (LABEL[d[k]]) d[k] = LABEL[d[k]];
  for (const k of ["gesprek_datum", "datum"]) if (d[k]) d[k] = datum(d[k]);
  if (!fd.get("budget_onbekend") && fd.get("budget_van") && !(fd.has("budget_ingevuld") && !schoon(fd.get("budget_ingevuld")))) d.budget = `€ ${eur(fd.get("budget_van"))} – € ${eur(fd.get("budget_tot"))}${+fd.get("budget_tot") >= 20000 ? "+" : ""}`;
  const regels = VELDEN.filter(([k]) => d[k]).map(([k, l]) => `${l}: ${d[k]}`).join("\n");
  const bron = schoon(fd.get("bron"));
  const soortMail = bron === "Coffee cuts" ? "Coffee cuts-aanvraag" : /maartenversteeg/i.test(bron) ? "DJ-boeking via maartenversteeg.nl" : "Aanvraag via hear.nl";
  const herkomst = /maartenversteeg/i.test(request.headers.get("Origin") || "") && bron === "Coffee cuts" ? " (via maartenversteeg.nl)" : "";
  const onderwerp = `${soortMail}${herkomst}: ${d.organisatie || d.naam}${d.datum ? ", " + d.datum : ""}`;
  // Onderaan de mail: via welke pagina en (bij advertenties) via welke bron de aanvraag kwam. De pagina vult "utm" uit de utm_-parameters in het adres.
  const utm = schoon(fd.get("utm")).slice(0, 300);
  const extra = [bron && `Pagina: ${bron}`, utm && `Herkomst: ${utm}`].filter(Boolean).map((r) => "\n" + r).join("");
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: VAN, to: [NAAR], reply_to: d.email, subject: onderwerp, text: regels + extra + "\n",
      ...(hoofdformulier ? { html: opgemaakt(d, schoon(fd.get("overzicht")), [bron && `Pagina: ${bron}`, utm && `Herkomst: ${utm}`].filter(Boolean)) } : {}) }),
  });
  return antwoord(request, r.ok, r.ok ? 200 : 502, route);
}

// Opgemaakte versie van de aanvraagmail: dezelfde indeling als het overzicht in het formulier.
// "overzicht" is JSON uit het formulier ([{kop, items}]): de keuzes per programmadeel. Ontbreekt het of klopt het niet, dan vallen we terug op de platte lijsten.
function esc(t) { return String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
function opgemaakt(d, overzicht, voet) {
  const kop = (t) => `<p style="margin:22px 0 4px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:bold;color:#D47763">${esc(t)}</p>`;
  const blok = (t, regels) => { const r = regels.filter(Boolean); return r.length ? kop(t) + `<p style="margin:0">${r.map(esc).join("<br>")}</p>` : ""; };
  let delen = [];
  try { const j = JSON.parse(overzicht || "[]"); if (Array.isArray(j)) delen = j.slice(0, 12).map((x) => ({ kop: String(x.kop || "").slice(0, 120), items: (Array.isArray(x.items) ? x.items : []).slice(0, 30).map((i) => String(i).slice(0, 400)) })).filter((x) => x.kop); } catch (e) { delen = []; }
  let h = `<div style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.55;color:#191A19;max-width:580px">`;
  h += `<p style="margin:0 0 2px;font-size:21px">${esc(d.organisatie || d.naam)}</p>`;
  if (d.route) h += `<p style="margin:0;font-size:16px"><b>Wil ${esc(d.route)}</b>${d.gesprek_datum ? esc(` · ${[d.gesprek, d.gesprek_datum, d.gesprek_dagdeel].filter(Boolean).join(", ")}`) : ""}</p>`;
  else if (d.gesprek_datum) h += `<p style="margin:0;font-size:16px"><b>Gesprek</b>${esc(` · ${[d.gesprek, d.gesprek_datum, d.gesprek_dagdeel].filter(Boolean).join(", ")}`)}</p>`;
  h += blok("Contact", [d.naam, d.organisatie, d.functie, d.email, d.telefoon]);
  h += blok("Event", [d.event, d.soort, d.datum, d.tijd, d.locatie, d.gasten && `${d.gasten} gasten`, d.doelgroep]);
  if (delen.length) for (const x of delen) h += kop(x.kop) + (x.items.length ? `<p style="margin:0">${x.items.map(esc).join("<br>")}</p>` : "");
  else h += blok("Programma", [d.programma]) + blok("Diensten", [d.diensten, d.diensten_anders]) + blok("Communicatie", [d.communicatie, d.communicatie_anders]);
  h += blok("Richtbudget", [d.budget]);
  h += blok("Toelichting", [d.ruimte, d.concept, d.bericht]);
  if (voet.length) h += `<p style="margin:26px 0 0;font-size:12px;color:#777">${voet.map(esc).join("<br>")}</p>`;
  return h + "</div>";
}

// Formulieren op maartenversteeg.nl (en de testversie op workers.dev) mogen ook hierheen posten.
function cors(request) {
  const o = request.headers.get("Origin") || "";
  return /^https:\/\/((www\.)?maartenversteeg\.nl|[a-z0-9-]+\.[a-z0-9-]+\.workers\.dev)$/.test(o) ? { "Access-Control-Allow-Origin": o, "Vary": "Origin" } : {};
}

function antwoord(request, ok, status = 200, route = "") {
  if ((request.headers.get("Accept") || "").includes("application/json"))
    return new Response(JSON.stringify({ ok }), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...cors(request) } });
  const terug = new URL(request.url);
  const en = (request.headers.get("Referer") || "").includes("/en/");
  terug.pathname = (en ? "/en" : "") + "/aanvraag.html";
  terug.search = ok ? "?verzonden=1" + (route === "call" ? "&route=call" : "") : "?fout=1";
  return Response.redirect(terug.toString(), 303);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname !== "hear.nl" || url.protocol === "http:") {
      url.hostname = "hear.nl";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    // oude paginanamen (hernoemd 28 okt 2026) permanent doorsturen naar de nieuwe
    const OUD = { "corporate": "zakelijke-events", "venue-owners": "bijzondere-eventlocaties", "av-as-a-service": "aankoopadvies", "special-projects": "custom-dj-mix" };
    const om = /^(\/en)?\/(corporate|venue-owners|av-as-a-service|special-projects)(\.html)?\/?$/.exec(url.pathname);
    if (om) {
      const doel = new URL((om[1] || "") + "/" + OUD[om[2]] + ".html", url);
      doel.search = url.search; doel.hash = url.hash;
      return Response.redirect(doel.toString(), 301);
    }
    // de samensteller (proef, 20 nov 2026) is weggehaald; oude adressen gaan naar het aanvraagformulier
    if (/^\/(conscious|samenstellen)(-met-prijzen|-zonder-prijzen)?(\.html)?\/?$/.test(url.pathname)) {
      const doel = new URL("/aanvraag", url);
      doel.search = url.search;
      return Response.redirect(doel.toString(), 302);
    }
    // korte advertentie-URL: hear.nl/coffeecuts is een eigen deelpagina (site/coffeecuts.html: eigen titel en deelbeeld,
    // stuurt door naar het Coffee cuts-blok). Varianten sturen daarheen; /coffeecuts zelf wordt als pagina geserveerd.
    const kort = url.pathname.toLowerCase().replace(/\/+$/, "");
    if ((kort === "/coffee-cuts" || kort === "/en/coffee-cuts" || url.pathname !== kort) && /^(\/en)?\/coffee-?cuts$/.test(kort)) {
      const doel = new URL(kort.replace("coffee-cuts", "coffeecuts"), url);
      doel.search = url.search;
      return Response.redirect(doel.toString(), 301);
    }
    // /coffeecuts zelf: gewoon doorvallen naar de statische assets (auto-trailing-slash serveert coffeecuts.html)
    if (url.pathname === "/api/aanvraag") {
      if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
      if (!env.RESEND_API_KEY) return antwoord(request, false, 503);
      try { return await aanvraag(request, env); } catch (e) { return antwoord(request, false, 500); }
    }
    return env.ASSETS.fetch(request);
  },
};
