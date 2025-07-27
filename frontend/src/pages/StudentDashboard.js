import React, { useState, useEffect } from 'react';
import { getDashboard } from '../api/analytics';
import { listCertificatesForUser } from '../api/certificate';
import { useAuth } from '../contexts/AuthContext';

export default function StudentDashboard() {
  const { user } = useAuth();
  const [progress, setProgress] = useState([]);
  const [quizScores, setQuizScores] = useState([]);
  const [certificates, setCertificates] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const dashResp = await getDashboard(1); // assume workshop id 1
        setProgress(dashResp.data.completion);
        setQuizScores(dashResp.data.quiz_scores);
        const certs = await listCertificatesForUser(user?.id || 1);
        setCertificates(certs.data);
      } catch (err) {
        console.error(err);
      }
    }
    fetchData();
  }, [user]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Student Dashboard</h1>
      <h2>Your Progress</h2>
      <ul>
        {progress.map((p) => (
          <li key={p.user_id}>Workshop completion: {p.percent_complete}%</li>
        ))}
      </ul>
      <h2>Quiz Scores</h2>
      <ul>
        {quizScores.map((q) => (
          <li key={q.user_id}>Average Score: {q.average_score}%</li>
        ))}
      </ul>
      <h2>Certificates</h2>
      <ul>
        {certificates.map((c) => (
          <li key={c.id}>{c.file_url}</li>
        ))}
      </ul>
    </div>
  );
}