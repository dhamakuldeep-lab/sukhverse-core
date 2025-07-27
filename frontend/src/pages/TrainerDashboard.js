import React, { useState, useEffect } from 'react';
import { getDashboard, getAtRiskStudents } from '../api/analytics';

export default function TrainerDashboard() {
  const [progress, setProgress] = useState([]);
  const [quizScores, setQuizScores] = useState([]);
  const [atRisk, setAtRisk] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const dashResp = await getDashboard(1);
        setProgress(dashResp.data.completion);
        setQuizScores(dashResp.data.quiz_scores);
        const riskResp = await getAtRiskStudents();
        setAtRisk(riskResp.data);
      } catch (err) {
        console.error(err);
      }
    }
    fetchData();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Trainer Dashboard</h1>
      <h2>Student Progress</h2>
      <ul>
        {progress.map((p) => (
          <li key={p.user_id}>User {p.user_id}: {p.percent_complete}% complete</li>
        ))}
      </ul>
      <h2>Quiz Scores</h2>
      <ul>
        {quizScores.map((q) => (
          <li key={q.user_id}>User {q.user_id}: Avg {q.average_score}% (pass: {q.pass_fail.toString()})</li>
        ))}
      </ul>
      <h2>At Risk Students</h2>
      <ul>
        {atRisk.map((r) => (
          <li key={r.user_id}>User {r.user_id}: Risk {r.risk_score} – {r.reason}</li>
        ))}
      </ul>
    </div>
  );
}