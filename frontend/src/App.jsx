import {
  BarChart3,
  Check,
  Download,
  Loader2,
  Radio,
  Rocket,
  Target,
  Zap,
} from "lucide-react";
import { useMemo, useState } from "react";
import { buildGtm } from "./api";

const emptyResult = null;

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

function Icp({ result }) {
  const data = result.icp || {};
  const fields = [
    ["Company Profile", data.company_profile],
    ["Economic Buyer", data.buyer_title],
    ["Champion", data.champion_title],
    ["Trigger Event", data.trigger_event],
    ["Who to Avoid", data.negative_icp],
  ];

  return (
    <section className="section">
      <SectionTitle title="Your ICP" icon={Target} />
      <div className="stack">
        {fields.map(([label, value]) => (
          <article className="panel compact" key={label}>
            <div className="eyebrow">{label}</div>
            <p>{displayText(value)}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function Positioning({ result }) {
  const pos = result.positioning || {};
  return (
    <section className="section">
      <SectionTitle title="Positioning" icon={Zap} />
      <article className="panel positioning">
        <div className="eyebrow">Wedge</div>
        <h3>{displayText(pos.wedge)}</h3>
        <div className="eyebrow">ROI</div>
        <p>{displayText(pos.roi)}</p>
        <div className="divider" />
        <div className="objection-grid">
          <div>
            <div className="eyebrow danger-text">Top Objection</div>
            <p>{displayText(pos.objection)}</p>
          </div>
          <div>
            <div className="eyebrow good-text">Response</div>
            <p>{displayText(pos.objection_response)}</p>
          </div>
        </div>
      </article>
    </section>
  );
}

function Distribution({ result }) {
  const dist = result.distribution || {};
  const engines = [dist.engine_1 || {}, dist.engine_2 || {}, dist.engine_3 || {}];
  return (
    <section className="section">
      <SectionTitle title="Distribution Engines" icon={Rocket} />
      <div className="three-col">
        {engines.map((engine, index) => (
          <article className="panel compact" key={index}>
            <h3>{displayText(engine.channel)}</h3>
            <p>{displayText(engine.rationale)}</p>
            <div className="next-step">{displayText(engine.action)}</div>
          </article>
        ))}
      </div>
    </section>
  );
}

function Actions({ result }) {
  const data = result.actions || {};
  const actions = [data.action_1, data.action_2, data.action_3];
  const milestones = [
    ["Day 30", data.day_30],
    ["Day 60", data.day_60],
    ["Day 90", data.day_90],
  ];

  return (
    <section className="section">
      <SectionTitle title="Execution Plan" icon={Check} />
      <div className="execution-grid">
        <article>
          <h3>This Week</h3>
          <div className="stack">
            {actions.map((action, index) => (
              <div className="action-item" key={index}>
                <Check size={16} />
                <span>{displayText(action)}</span>
              </div>
            ))}
          </div>
        </article>
        <article>
          <h3>90-Day Milestones</h3>
          <div className="timeline">
            {milestones.map(([day, value]) => (
              <div className="milestone" key={day}>
                <strong>{day}</strong>
                <p>{displayText(value)}</p>
              </div>
            ))}
          </div>
        </article>
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
        <form className="search" onSubmit={onSubmit}>
          <input
            value={founderText}
            onChange={(event) => setFounderText(event.target.value)}
            placeholder="https://acme.com - 2022 - ACV $18K - 60-day cycle - $1.2M ARR - Founder-led"
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
          <Icp result={result} />
          <Positioning result={result} />
          <Distribution result={result} />
          <Actions result={result} />
          <DownloadSnapshot result={result} />
        </>
      ) : null}
    </main>
  );
}
