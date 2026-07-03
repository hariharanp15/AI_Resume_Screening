import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  BarChart3,
  BriefcaseBusiness,
  CheckCircle2,
  Edit3,
  FileText,
  LogOut,
  MessageSquareText,
  Search,
  Sparkles,
  Trash2,
  Upload,
  UserCircle,
  Users,
} from "lucide-react";
import { api, clearSession, getToken, setSession } from "./api/client";
import "./styles/app.css";

function Auth({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ email: "", password: "", full_name: "", role: "HR" });
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      const payload = mode === "login" ? { email: form.email, password: form.password } : form;
      const session = await api(`/auth/${mode === "login" ? "login" : "register"}`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setSession(session);
      onLogin();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="auth">
      <section className="auth-panel">
        <h1>AI Resume Screening & Interview Assistant</h1>
        <form onSubmit={submit}>
          {mode === "register" && (
            <input placeholder="Full name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          )}
          <input placeholder="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input placeholder="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          {mode === "register" && (
            <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
              <option>HR</option>
              <option>Recruiter</option>
            </select>
          )}
          {error && <div className="error">{error}</div>}
          <button>{mode === "login" ? "Login" : "Create account"}</button>
        </form>
        <button className="link" onClick={() => setMode(mode === "login" ? "register" : "login")}>
          {mode === "login" ? "Register?" : "Already have an account?"}
        </button>
      </section>
    </main>
  );
}

function ProfileCard({ profile, onProfile }) {
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ full_name: "", email: "" });

  useEffect(() => {
    if (profile) setForm({ full_name: profile.full_name, email: profile.email });
  }, [profile]);

  async function save(event) {
    event.preventDefault();
    const updated = await api("/users/me", { method: "PUT", body: JSON.stringify(form) });
    localStorage.setItem("name", updated.full_name);
    onProfile(updated);
    setEditing(false);
  }

  if (!profile) return <div className="profile-card">Loading profile...</div>;

  return (
    <section className="profile-card">
      {!editing ? (
        <>
          <strong>{profile.full_name}</strong>
          <span>ID: {profile.id}</span>
          <span>{profile.email}</span>
          <span>{profile.role}</span>
          <button className="ghost" onClick={() => setEditing(true)}>Edit</button>
        </>
      ) : (
        <form onSubmit={save}>
          <input value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <button>Save</button>
          <button type="button" className="ghost" onClick={() => setEditing(false)}>Cancel</button>
        </form>
      )}
    </section>
  );
}

function CandidatesPage({ role, candidates, search, setSearch, refresh, setMessage }) {
  const [editing, setEditing] = useState(null);
  const canManage = role === "HR";

  async function uploadResume(event) {
    const file = event.target.files[0];
    if (!file) return;
    const body = new FormData();
    body.append("file", file);
    await api("/candidates/upload", { method: "POST", body });
    setMessage("Resume uploaded");
    refresh();
  }

  async function updateCandidate(event) {
    event.preventDefault();
    await api(`/candidates/${editing.id}`, { method: "PUT", body: JSON.stringify(editing) });
    setEditing(null);
    refresh();
  }

  async function removeCandidate(id) {
    await api(`/candidates/${id}`, { method: "DELETE" });
    refresh();
  }

  return (
    <section className="grid">
      <div className="panel command-panel">
        <div className="toolbar">
          <Search size={18} />
          <input placeholder="Search candidate by name, email, skills" value={search} onChange={(e) => setSearch(e.target.value)} />
          <button onClick={refresh}>Search</button>
        </div>
        {canManage && (
          <label className="upload upload-zone">
            <span className="upload-icon"><Upload size={22} /></span>
            <span>
              <strong>Upload resume</strong>
              <small>Drop in a PDF or DOCX</small>
            </span>
            <input type="file" accept=".pdf,.docx" onChange={uploadResume} />
          </label>
        )}
        <div className="list card-list">
          {candidates.map((candidate) => (
            <article className="record-card" key={candidate.id}>
              <div className="row">
                <div className="record-title">
                  <span className="avatar">{candidate.name?.slice(0, 1) || "C"}</span>
                  <div>
                  <h3>{candidate.name}</h3>
                  <p>{candidate.email || "No email"} | {candidate.phone || "No phone"}</p>
                  </div>
                </div>
                <div className="record-meta">
                  <span>ID_{candidate.id}</span>
                  </div>
                {canManage && (
                  <div className="actions">
                    <button className="secondary" onClick={() => setEditing({ id: candidate.id, name: candidate.name, email: candidate.email || "", phone: candidate.phone || "" })}>Edit</button>
                    <button className="danger" onClick={() => removeCandidate(candidate.id)}>Delete</button>
                  </div>
                )}
              </div>
              <div>{candidate.skills.map((skill) => <b key={skill}>{skill}</b>)}</div>
            </article>
          ))}
        </div>
      </div>
      {editing && (
        <form className="panel form" onSubmit={updateCandidate}>
          <h2>Update Candidate</h2>
          <input value={editing.name} onChange={(e) => setEditing({ ...editing, name: e.target.value })} placeholder="Name" />
          <input value={editing.email} onChange={(e) => setEditing({ ...editing, email: e.target.value })} placeholder="Email" />
          <input value={editing.phone} onChange={(e) => setEditing({ ...editing, phone: e.target.value })} placeholder="Phone" />
          <button>Save candidate</button>
        </form>
      )}
    </section>
  );
}

function JobsPage({ role, jobs, refresh }) {
  const [editing, setEditing] = useState(null);
  const canManage = role === "HR";

  function jobPayload(form) {
    const data = Object.fromEntries(new FormData(form));
    data.required_skills = data.required_skills.split(",").map((skill) => skill.trim()).filter(Boolean);
    return data;
  }

  async function createJob(event) {
    event.preventDefault();
    await api("/jobs", { method: "POST", body: JSON.stringify(jobPayload(event.currentTarget)) });
    event.currentTarget.reset();
    refresh();
  }

  async function updateJob(event) {
    event.preventDefault();
    await api(`/jobs/${editing.id}`, { method: "PUT", body: JSON.stringify(jobPayload(event.currentTarget)) });
    setEditing(null);
    refresh();
  }

  async function removeJob(id) {
    await api(`/jobs/${id}`, { method: "DELETE" });
    refresh();
  }

  return (
    <section className="grid two">
      {canManage && (
        <form className="panel form" onSubmit={editing ? updateJob : createJob}>
          <h2>{editing ? "Update Job" : "Create Job"}</h2>
          <input name="title" placeholder="Job title" defaultValue={editing?.title || ""} required />
          <input name="required_skills" placeholder="Required skills, comma separated" defaultValue={editing?.required_skills?.join(", ") || ""} required />
          <input name="experience_requirement" placeholder="Experience requirement" defaultValue={editing?.experience_requirement || ""} required />
          <input name="location" placeholder="Location" defaultValue={editing?.location || ""} required />
          <select name="employment_type" defaultValue={editing?.employment_type || "Full-time"}>
            <option>Full-time</option>
            <option>Part-time</option>
            <option>Internship</option>
          </select>
          <textarea name="content" placeholder="Job description" defaultValue={editing?.content || ""} required />
          <button>{editing ? "Save job" : "Create job"}</button>
          {editing && <button type="button" className="secondary" onClick={() => setEditing(null)}>Cancel</button>}
        </form>
      )}
      <div className="panel list card-list">
        {jobs.map((job) => (
            <article className="record-card job-card" key={job.id}>
              <div className="row">
              <div className="record-title">
                <span className="avatar job-avatar"><BriefcaseBusiness size={20} /></span>
                <div>
                  <h3>{job.title}</h3>
                  <p>{job.location} | {job.employment_type} | {job.experience_requirement}</p>
                </div>
              </div>
              <div className="record-meta">
                <span>ID_{job.id}</span>
              </div>
              {canManage && (
                <div className="actions">
                  <button className="secondary" onClick={() => setEditing(job)}>Edit</button>
                  <button className="danger" onClick={() => removeJob(job.id)}>Delete</button>
                </div>
              )}
            </div>
            <div>{job.required_skills.map((skill) => <b key={skill}>{skill}</b>)}</div>
            <p>{job.content}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function QuestionItems({ items = [] }) {
  return items.map((item, index) => {
    const question = typeof item === "string" ? item : item.question;
    const answer = typeof item === "string" ? "" : item.answer;
    return (
      <div className="qa" key={`${question}-${index}`}>
        <strong>{question}</strong>
        {answer && <p>{answer}</p>}
      </div>
    );
  });
}

function Suitability({ score }) {
  if (score == null) return <span className="badge neutral">Generated</span>;
  if (score >= 75) return <span className="badge success">Suitable</span>;
  if (score >= 55) return <span className="badge warning">Review gaps</span>;
  return <span className="badge danger-text">Not suitable yet</span>;
}

function EvaluationPage({ candidates, jobs, evaluations, refresh, setMessage }) {
  const [selectedCandidate, setSelectedCandidate] = useState("");
  const [selectedJob, setSelectedJob] = useState("");
  const [result, setResult] = useState(null);
  const [openHistory, setOpenHistory] = useState(null);
  const [loading, setLoading] = useState("");

  async function runAI(kind) {
    setLoading(kind);
    const body = { candidate_id: Number(selectedCandidate), job_id: Number(selectedJob) };
    const endpoint = kind === "full" ? "/ai/evaluate" : kind === "match" ? "/ai/match" : kind === "questions" ? "/ai/questions" : "/ai/summary";
    try {
      const data = await api(endpoint, { method: "POST", body: JSON.stringify(body) });
      setResult({ kind, data });
      setMessage(kind === "full" ? "Full AI evaluation generated" : "AI result generated");
      refresh();
    } finally {
      setLoading("");
    }
  }

  async function deleteHistory(id) {
    await api(`/history/evaluations/${id}`, { method: "DELETE" });
    if (openHistory === id) setOpenHistory(null);
    setMessage("Evaluation history deleted");
    refresh();
  }

  return (
    <section className="grid two">
      <div className="panel form">
        <h2>Evaluation</h2>
        <p className="muted">Select a candidate and role to generate a complete hiring evaluation.</p>
        <select value={selectedCandidate} onChange={(e) => setSelectedCandidate(e.target.value)}>
          <option value="">Select candidate</option>
          {candidates.map((candidate) => <option key={candidate.id} value={candidate.id}>{candidate.id} - {candidate.name}</option>)}
        </select>
        <select value={selectedJob} onChange={(e) => setSelectedJob(e.target.value)}>
          <option value="">Select job</option>
          {jobs.map((job) => <option key={job.id} value={job.id}>{job.id} - {job.title}</option>)}
        </select>
        <button disabled={!selectedCandidate || !selectedJob || loading} onClick={() => runAI("full")}>{loading === "full" ? "Generating..." : "Evaluation"}</button>
        <div className="button-row">
          <button className="secondary" disabled={!selectedCandidate || !selectedJob || loading} onClick={() => runAI("match")}>Match Score</button>
          <button className="secondary" disabled={!selectedCandidate || !selectedJob || loading} onClick={() => runAI("questions")}>Questions</button>
          <button className="secondary" disabled={!selectedCandidate || !selectedJob || loading} onClick={() => runAI("summary")}> Evaluation Summary</button>
        </div>
      </div>
      <div className="panel result">
        <h2>Evaluation Result</h2>
        {!result && <p>Select a candidate and job, then run an evaluation.</p>}
        {(result?.kind === "match" || result?.kind === "full") && (
          <>
            <div className="score-line">
              <div className="score">{result.data.match_score}%</div>
              <div>
                <Suitability score={result.data.match_score} />
                <p className="muted">AI generated match score based on resume skills, job requirements.</p>
              </div>
            </div>
            <p><strong>Missing skills:</strong> {result.data.missing_skills.join(", ") || "None"}</p>
            <div className="insight-grid">
              <div><h3>Strengths</h3>{result.data.strengths.map((item) => <p key={item}>{item}</p>)}</div>
              <div><h3>Weaknesses</h3>{result.data.weaknesses.map((item) => <p key={item}>{item}</p>)}</div>
            </div>
          </>
        )}
        {result?.kind === "questions" && (
          <div className="question-list">
            <h3>Technical</h3><QuestionItems items={result.data.technical} />
            <h3>Scenario Based</h3><QuestionItems items={result.data.scenario_based} />
          </div>
        )}
        {result?.kind === "full" && (
          <div className="question-list">
            <h3>Resume-based questions and answers</h3>
            <QuestionItems items={result.data.questions?.technical} />
            <QuestionItems items={result.data.questions?.scenario_based} />
          </div>
        )}
        {(result?.kind === "summary" || result?.kind === "full") && (
          <>
            <h3>Summary</h3>
            <p><strong>Overview:</strong> {(result.data.summary || result.data).overview}</p>
            <p><strong>Skill:</strong> {(result.data.summary || result.data).skill_assessment}</p>
            <p><strong>Experience:</strong> {(result.data.summary || result.data).experience_summary}</p>
            <p><strong>Recommendation:</strong> {(result.data.summary || result.data).hiring_recommendation}</p>
          </>
        )}
      </div>
      <div className="panel wide">
        <div className="section-head">
          <div>
            <h2>Evaluation History</h2>
            <p className="muted">Open any row to review the stored AI decision details.</p>
          </div>
        </div>
        <div className="table evaluation-table">
          <span>ID</span><span>Candidate</span><span>Job</span><span>Score</span><span>Date Time</span><span>Action</span>
          {evaluations.map((row) => (
            <React.Fragment key={row.id}>
              <span>{row.id}</span>
              <span>{row.candidate_id} - {row.candidate_name}</span>
              <span>{row.job_id || "N/A"} - {row.job_title || "N/A"}</span>
              <span>{row.match_score != null ? `${row.match_score}%` : "Generated"}</span>
              <span>{new Date(row.created_at).toLocaleString()}</span>
              <span className="table-actions">
                <button className="icon-button" title="View evaluation" onClick={() => setOpenHistory(openHistory === row.id ? null : row.id)}><FileText size={16} /></button>
                <button className="icon-button danger" title="Delete evaluation" onClick={() => deleteHistory(row.id)}><Trash2 size={16} /></button>
              </span>
              {openHistory === row.id && (
                <span className="history-detail">
                  <div className="score-line compact">
                    <strong>{row.candidate_name} for {row.job_title || "selected job"}</strong>
                    <Suitability score={row.match_score} />
                  </div>
                  <div className="insight-grid">
                    <div><h3>Strengths</h3>{(row.strengths || []).map((item) => <p key={item}>{item}</p>)}</div>
                    <div><h3>Weaknesses</h3>{(row.weaknesses || []).map((item) => <p key={item}>{item}</p>)}</div>
                  </div>
                  {row.summary && <p><strong>Summary:</strong> {row.summary}</p>}
                  {row.interview_questions && Object.keys(row.interview_questions).length > 0 && (
                    <div className="question-list">
                      <h3>Questions and Answers</h3>
                      {Object.entries(row.interview_questions).map(([group, items]) => (
                        <div key={group}>
                          <h4>{group.replace("_", " ")}</h4>
                          <QuestionItems items={items} />
                        </div>
                      ))}
                    </div>
                  )}
                </span>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    </section>
  );
}

function AnalyticsPage({ analytics }) {
  return (
    <section className="grid two">
      <div className="metric"><Users /><strong>{analytics?.total_candidates ?? 0}</strong><span>Total Candidates</span></div>
      <div className="metric"><BriefcaseBusiness /><strong>{analytics?.total_job_descriptions ?? 0}</strong><span>Total Jobs</span></div>
      <div className="metric"><CheckCircle2 /><strong>{analytics?.average_match_score ?? 0}%</strong><span>Overall Average Score</span></div>
      <div className="panel">
        <div className="section-head">
          <div>
            <h2>Most Asked Skills for Jobs</h2>
            <p className="muted">Calculated from required skills across all job descriptions.</p>
          </div>
          <MessageSquareText />
        </div>
        <div className="skill-bars">
          {(analytics?.most_requested_skills || []).map((item) => (
            <div key={item.skill}>
              <span>{item.skill}</span>
              <div><i style={{ width: `${Math.min(item.count * 18, 100)}%` }} /></div>
              <strong>{item.count}</strong>
            </div>
          ))}
          {(!analytics?.most_requested_skills || analytics.most_requested_skills.length === 0) && <p className="muted">No job skills have been added yet.</p>}
        </div>
      </div>
    </section>
  );
}

function Dashboard() {
  const [tab, setTab] = useState("candidates");
  const [profile, setProfile] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [evaluations, setEvaluations] = useState([]);
  const [search, setSearch] = useState("");
  const [message, setMessage] = useState("");
  const role = profile?.role || localStorage.getItem("role");

  async function refresh() {
    const query = search ? `?semantic=${encodeURIComponent(search)}` : "";
    const [me, candidateData, jobData, evalData, analyticsData] = await Promise.all([
      api("/users/me"),
      api(`/candidates${query}`),
      api("/jobs"),
      api("/history/evaluations"),
      api("/analytics"),
    ]);
    setProfile(me);
    setCandidates(candidateData);
    setJobs(jobData);
    setEvaluations(evalData);
    setAnalytics(analyticsData);
  }

  useEffect(() => {
    refresh().catch((err) => setMessage(err.message));
  }, []);

  const pages = [
    ["candidates", "Candidates", Users],
    ["jobs", "Jobs", BriefcaseBusiness],
    ["evaluation", "Evaluation", Sparkles],
    ["analytics", "Analytics", BarChart3],
  ];
  const currentPage = pages.find(([id]) => id === tab)?.[1];
  const averageScore = analytics?.average_match_score ?? 0;
  const topSkill = analytics?.most_requested_skills?.[0]?.skill || "No skill data";

  return (
    <div className="app">
      <aside>
        <div className="brand">
          
          <div>
            <strong>AI Resume Screening</strong>
            <span>Interview Assistant</span>
          </div>
        </div>
        <ProfileCard profile={profile} onProfile={setProfile} />
        {pages.map(([id, label, Icon]) => (
          <button key={id} className={tab === id ? "active" : ""} onClick={() => setTab(id)}><Icon size={18} />{label}</button>
        ))}
        <button onClick={() => { clearSession(); location.reload(); }}><LogOut size={18} />Logout</button>
      </aside>
      <main>
        <header className="page-hero">
          <div className="hero-copy">
            <span className="eyebrow">{role} workspace</span>
            <h1>{currentPage}</h1>
            <p>AI dashboard for resume intelligence, job matching, and interview readiness.</p>
          </div>
          {message && <span>{message}</span>}
        </header>
        
        {tab === "candidates" && <CandidatesPage role={role} candidates={candidates} search={search} setSearch={setSearch} refresh={refresh} setMessage={setMessage} />}
        {tab === "jobs" && <JobsPage role={role} jobs={jobs} refresh={refresh} />}
        {tab === "evaluation" && <EvaluationPage candidates={candidates} jobs={jobs} evaluations={evaluations} refresh={refresh} setMessage={setMessage} />}
        {tab === "analytics" && <AnalyticsPage analytics={analytics} />}
      </main>
    </div>
  );
}

function App() {
  const [authed, setAuthed] = useState(Boolean(getToken()));
  return authed ? <Dashboard /> : <Auth onLogin={() => setAuthed(true)} />;
}

createRoot(document.getElementById("root")).render(<App />);
