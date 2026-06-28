import {
  BarChart3,
  Download,
  Loader2,
  Radio,
  Rocket,
  Target,
} from "lucide-react";
import { useMemo, useState } from "react";
import { buildGtm } from "./api";

const emptyResult = null;

const SEP = " — ";
const STEPS = [
  {
    name: "Website URL",
    label: "https://yourcompany.com",
    detect: (v) => /https?:\/\/|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}/.test(v),
  },
  {
    name: "Year Founded",
    label: "2022",
    detect: (v) => /\b(19|20)\d{2}\b/.test(v),
  },
  {
    name: "ACV Size",
    label: "ACV $20K",
    detect: (v) => /\bacv\b|\$\s*\d+\s*k\b/i.test(v),
  },
  {
    name: "Sales Cycle",
    label: "60-day cycle",
    detect: (v) => /\d+[\s-]?day/i.test(v),
  },
  {
    name: "Current Revenue",
    label: "$1M ARR",
    detect: (v) => /\barr\b|\$[\d.]+\s*[mb]\b/i.test(v),
  },
  {
    name: "Sales Channel",
    label: "Founder-led",
    detect: (v) => /founder.?led|outbound|inbound|\bplg\b|mixed/i.test(v),
  },
];

function getGhostSuggestion(value) {
  if (!value.trim()) return "";
  const missing = STEPS.filter((step) => !step.detect(value));
  if (missing.length === 0) return "";
  return SEP + missing.map((s) => s.label).join(SEP);
}

function SmartInput({ value, onChange, disabled }) {
  const ghost = getGhostSuggestion(value);
  return (
    <div className="smart-input-wrap">
      {ghost && (
        <div className="smart-input-ghost" aria-hidden="true">
          <span className="ghost-typed">{value}</span>
          <span className="ghost-hint">{ghost}</span>
        </div>
      )}
      <input
        value={value}
        onChange={onChange}
        disabled={disabled}
        placeholder="https://yourcompany.com — 2022 — ACV $20K — 60-day cycle — $1M ARR — Founder-led"
        autoComplete="off"
        spellCheck="false"
      />
    </div>
  );
}

function displayText(value) {
  if (value === null || value === undefined || String(value).trim() === "") {
    return "-";
  }
  return String(value);
}

function displayNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function money(value) {
  const number = displayNumber(value);
  return number === null ? "-" : `$${number.toLocaleString()}`;
}

function Pill({ label, value }) {
  const pct = Number(value || 0);
  let className = "pill danger";
  let display = `Bottom ${pct}%`;

  if (pct >= 67) {
    className = "pill good";
    display = `Top ${100 - pct}%`;
  } else if (pct >= 34) {
    className = "pill warn";
    display = `${pct}th %ile`;
  }

  return (
    <div className={className}>
      <span>{label}</span>
      <strong>{display}</strong>
    </div>
  );
}

function SectionTitle({ icon: Icon, title, caption }) {
  return (
    <div className="section-title">
      <div>
        <h2>
          <Icon size={18} />
          {title}
        </h2>
        {caption ? <p>{caption}</p> : null}
      </div>
    </div>
  );
}

function CompanyProfile({ profile }) {
  const metrics = [
    ["Founded", displayText(profile.founding_year)],
    ["Average Deal Size (ACV)", money(profile.acv)],
    ["Sales Cycle Length", profile.sales_cycle_days ? `${profile.sales_cycle_days} days` : "-"],
    ["Annual Recurring Revenue (ARR)", money(profile.arr)],
    ["Sales Approach", displayText(profile.sales_motion)],
    ["Industry", displayText(profile.vertical)],
  ];

  return (
    <section className="section">
      <SectionTitle title="Company Profile" icon={Target} />
      <div className="profile-grid">
        <article className="panel profile-main">
          <div className="eyebrow">
            {displayText(profile.vertical)} / {displayText(profile.sub_vertical)}
          </div>
          <h3>{displayText(profile.company_name)}</h3>
          <div className="subhead">What this company does</div>
          <p>{displayText(profile.overview)}</p>
          <div className="two-col">
            <div>
              <div className="subhead">Main customer problem</div>
              <p>{displayText(profile.problem)}</p>
            </div>
            <div>
              <div className="subhead">How they solve it</div>
              <p>{displayText(profile.solution)}</p>
            </div>
          </div>
        </article>
        <aside className="panel">
          <div className="eyebrow">Business Snapshot</div>
          <div className="metric-list">
            {metrics.map(([label, value]) => (
              <div className="metric" key={label}>
                <span>{label}</span>
                <strong>{value}</strong>
              </div>
            ))}
          </div>
        </aside>
      </div>
    </section>
  );
}

function Signals({ result }) {
  return (
    <section className="section">
      <SectionTitle
        title="Market Signals"
        icon={Radio}
        caption={`${result.signals?.length || 0} signals collected for ${displayText(
          result.profile?.vertical || "B2B SaaS"
        )}`}
      />
      <div className="signal-list">
        {(result.signals || []).map((signal, index) => (
          <article className="signal" key={`${signal.source}-${index}`}>
            <div>
              <span>{signal.tone}</span>
              <strong>{signal.source}</strong>
              <small>{signal.time}</small>
            </div>
            <p>{signal.title}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function Benchmarking({ result }) {
  const bench = result.benchmarking || {};
  const profile = result.profile || {};
  const scorecard = [
    ["ACV", bench.acv_percentile],
    ["Sales Cycle", bench.cycle_percentile],
    ["Revenue Eff.", bench.revenue_efficiency_percentile],
    ["GTM Motion", bench.gtm_motion_percentile],
    ["Deal Velocity", bench.deal_velocity_percentile],
    ["Overall", bench.overall_percentile],
  ];

  return (
    <section className="section">
      <SectionTitle title="Benchmarking" icon={BarChart3} />
      <div className="benchmark-grid">
        <article className="benchmark-card purple">
          <h3>Vertical + Stage peers</h3>
          <p>Compares against companies in the same vertical and revenue band.</p>
          <ul>
            <li>ACV vs. vertical median</li>
            <li>Sales cycle vs. stage peers</li>
            <li>Revenue growth rate vs. cohort</li>
            <li>Deal volume efficiency</li>
          </ul>
        </article>
        <article className="benchmark-card green">
          <h3>Percentile ranking</h3>
          <p>
            Overall GTM health score: <strong>{bench.overall_percentile || 0}th percentile</strong>
          </p>
          <ul>
            <li>Per-metric breakdown below</li>
            <li>Biggest gap: {displayText(bench.biggest_gap)}</li>
          </ul>
        </article>
        <article className="benchmark-card rust">
          <h3>Top quartile gap analysis</h3>
          <ul>
            <li>
              Top quartile ACV: {money(bench.acv_top_quartile)} vs your {money(profile.acv)}
            </li>
            <li>Cycle target: {displayText(bench.cycle_top_quartile_days)} days</li>
            <li>Highest leverage: {displayText(bench.highest_leverage_lever)}</li>
          </ul>
        </article>
      </div>
      <div className="scorecard">
        {scorecard.map(([label, value]) => (
          <Pill key={label} label={label} value={value} />
        ))}
      </div>
    </section>
  );
}

function DownloadSnapshot({ result }) {
  const href = useMemo(() => {
    const blob = new Blob([result.snapshot || ""], { type: "text/plain" });
    return URL.createObjectURL(blob);
  }, [result.snapshot]);

  const company = displayText(result.profile?.company_name || "company")
    .toLowerCase()
    .replace(/\s+/g, "_");

  return (
    <a className="download" href={href} download={`gtm_snapshot_${company}.txt`}>
      <Download size={16} />
      Download GTM Snapshot
    </a>
  );
}

export default function App() {
  const [founderText, setFounderText] = useState("");
  const [result, setResult] = useState(emptyResult);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event) {
    event.preventDefault();
    if (!founderText.trim() || loading) return;

    setLoading(true);
    setError("");
    try {
      setResult(await buildGtm(founderText));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <section className="hero">
        <p className="kicker">GPS for GTM</p>
        <h1>
          You have PMF.
          <br />
          Now build the motion.
        </h1>
        <p className="hero-copy">
          Describe your company. Get a GTM plan grounded in your numbers.
        </p>
        <div className="input-fields-hint">
          {STEPS.map((step, i) => {
            const filled = step.detect(founderText);
            return (
              <span key={step.name} className={filled ? "hint-filled" : ""}>
                {i > 0 && <span className="hint-sep">·</span>}
                {step.name}
              </span>
            );
          })}
        </div>
        <form className="search" onSubmit={onSubmit}>
          <SmartInput
            value={founderText}
            onChange={(event) => setFounderText(event.target.value)}
            disabled={loading}
          />
          <button type="submit" disabled={loading || !founderText.trim()}>
            {loading ? <Loader2 className="spin" size={17} /> : <Rocket size={17} />}
            Build GTM
          </button>
        </form>
        {error ? <div className="error">{error}</div> : null}
      </section>

      {loading ? (
        <section className="loading-panel">
          <Loader2 className="spin" size={24} />
          <span>Reading, analyzing, and assembling the GTM plan...</span>
        </section>
      ) : null}

      {result ? (
        <>
          <CompanyProfile profile={result.profile || {}} />
          <Signals result={result} />
          <Benchmarking result={result} />
          <DownloadSnapshot result={result} />
        </>
      ) : null}
    </main>
  );
}
