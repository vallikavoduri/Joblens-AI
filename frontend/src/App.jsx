import { useEffect, useState } from 'react'

const API_BASE = '/api'

function App() {
  const [health, setHealth] = useState({ state: 'loading', data: null, error: null })

  useEffect(() => {
    let cancelled = false

    async function ping() {
      try {
        const res = await fetch(`${API_BASE}/health`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        if (!cancelled) setHealth({ state: 'ok', data, error: null })
      } catch (err) {
        if (!cancelled) setHealth({ state: 'down', data: null, error: err.message })
      }
    }

    ping()
    const id = setInterval(ping, 10000)
    return () => {
      cancelled = true
      clearInterval(id)
    }
  }, [])

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-50 via-indigo-50 to-purple-50">
      <main className="mx-auto max-w-5xl px-6 py-16">
        <header className="flex items-center justify-between mb-16">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-indigo-500/30">
              J
            </div>
            <span className="text-xl font-semibold text-slate-900">JobLens</span>
          </div>
          <HealthPill state={health.state} />
        </header>

        <section className="text-center">
          <span className="inline-block px-3 py-1 text-xs font-medium tracking-wider uppercase text-indigo-700 bg-indigo-100 rounded-full mb-6">
            In active development &middot; June 2026
          </span>
          <h1 className="text-5xl sm:text-6xl font-bold tracking-tight text-slate-900 leading-tight">
            See your job hunt
            <br />
            <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              with one lens.
            </span>
          </h1>
          <p className="mt-6 max-w-2xl mx-auto text-lg text-slate-600">
            AI-powered tracker for every application across LinkedIn, Naukri, Indeed, and Telegram channels.
            Auto-classifies recruiter emails, scores resume↔JD fit, and visualises your consistency over time.
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-3 text-sm text-slate-700">
            <Chip>FastAPI</Chip>
            <Chip>React + Vite</Chip>
            <Chip>Tailwind v4</Chip>
            <Chip>DistilBERT</Chip>
            <Chip>sentence-transformers</Chip>
            <Chip>MLflow</Chip>
          </div>
        </section>

        <section className="mt-20 grid gap-6 sm:grid-cols-3">
          <FeatureCard
            title="Unified ingestion"
            description="Gmail + Telegram channels + Naukri scraping in one feed. Nothing slips through."
          />
          <FeatureCard
            title="ML email classification"
            description="Fine-tuned DistilBERT auto-tags emails as interview / rejection / offer and updates application status."
          />
          <FeatureCard
            title="Resume ↔ JD match"
            description="Sentence embeddings score every job against your resume. Sort openings by fit."
          />
        </section>

        <section className="mt-16">
          <BackendStatusCard health={health} />
        </section>

        <footer className="mt-20 text-center text-sm text-slate-500">
          Built by Vallika Voduri &middot;{' '}
          <a
            className="underline decoration-dotted hover:text-indigo-700"
            href="https://github.com/vallikavoduri/Joblens-AI"
            target="_blank"
            rel="noreferrer"
          >
            github.com/vallikavoduri/Joblens-AI
          </a>
        </footer>
      </main>
    </div>
  )
}

function Chip({ children }) {
  return (
    <span className="px-3 py-1 rounded-full bg-white/70 border border-slate-200 shadow-sm">
      {children}
    </span>
  )
}

function FeatureCard({ title, description }) {
  return (
    <div className="rounded-2xl bg-white/70 backdrop-blur border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow">
      <h3 className="font-semibold text-slate-900 mb-2">{title}</h3>
      <p className="text-sm text-slate-600 leading-relaxed">{description}</p>
    </div>
  )
}

function HealthPill({ state }) {
  const styles = {
    loading: 'bg-slate-100 text-slate-600 border-slate-200',
    ok: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    down: 'bg-rose-50 text-rose-700 border-rose-200',
  }[state]

  const dotColor = {
    loading: 'bg-slate-400',
    ok: 'bg-emerald-500',
    down: 'bg-rose-500',
  }[state]

  const label = {
    loading: 'Checking backend…',
    ok: 'Backend online',
    down: 'Backend offline',
  }[state]

  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-medium ${styles}`}>
      <span className={`h-2 w-2 rounded-full ${dotColor} ${state === 'ok' ? 'animate-pulse' : ''}`} />
      {label}
    </div>
  )
}

function BackendStatusCard({ health }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Live system check</h2>
          <p className="text-sm text-slate-500 mt-1">
            Frontend polls <code className="text-xs bg-slate-100 px-1.5 py-0.5 rounded">GET /api/health</code> every 10s.
          </p>
        </div>
        <HealthPill state={health.state} />
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4 text-sm">
        <KV label="Status" value={health.data?.status ?? '—'} />
        <KV label="App" value={health.data?.app ?? '—'} />
        <KV label="Env" value={health.data?.env ?? '—'} />
        <KV label="Server time (UTC)" value={health.data?.server_time_utc ?? '—'} mono />
      </div>

      {health.state === 'down' && (
        <div className="mt-6 rounded-lg bg-rose-50 border border-rose-200 p-4 text-sm text-rose-800">
          <p className="font-medium">Cannot reach backend.</p>
          <p className="mt-1 text-rose-700">
            Make sure FastAPI is running:{' '}
            <code className="bg-rose-100 px-1.5 py-0.5 rounded">uvicorn app.main:app --reload</code> from the{' '}
            <code className="bg-rose-100 px-1.5 py-0.5 rounded">backend/</code> folder.
          </p>
          {health.error && (
            <p className="mt-2 text-xs text-rose-600 font-mono">Error: {health.error}</p>
          )}
        </div>
      )}
    </div>
  )
}

function KV({ label, value, mono = false }) {
  return (
    <div>
      <div className="text-xs uppercase tracking-wider text-slate-400">{label}</div>
      <div className={`mt-1 text-slate-900 ${mono ? 'font-mono text-xs' : ''}`}>{value}</div>
    </div>
  )
}

export default App
