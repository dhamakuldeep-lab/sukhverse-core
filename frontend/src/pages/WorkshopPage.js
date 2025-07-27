import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getWorkshop, updateProgress } from '../api/workshop';

/**
 * Enhanced workshop page implementing a tabbed layout.  Modules are displayed as
 * large buttons at the top.  When a module is selected, its substeps are shown
 * below with locking indicators and the currently active substep highlighted.
 */
export default function WorkshopPage() {
  const { id } = useParams();
  const [workshop, setWorkshop] = useState(null);
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const [activeSubIndex, setActiveSubIndex] = useState(0);

  useEffect(() => {
    async function fetchWorkshop() {
      const resp = await getWorkshop(id);
      setWorkshop(resp.data);
    }
    fetchWorkshop();
  }, [id]);

  if (!workshop) return <div>Loading...</div>;

  const currentStep = workshop.steps[activeStepIndex];
  const currentSub = currentStep.substeps[activeSubIndex];

  /**
   * Simulate progress completion.  In a real implementation the backend would track
   * which substeps are unlocked.  Here we assume the first substep of each module
   * is unlocked and subsequent ones are locked until completion.
   */
  const isUnlocked = (stepIdx, subIdx) => {
    return subIdx === 0;
  };

  const handleComplete = async () => {
    const stepId = currentStep.id;
    const subId = currentSub.id;
    await updateProgress({
      user_id: 1,
      workshop_id: workshop.id,
      step_id: stepId,
      substep_id: subId,
      status: 'completed',
    });
    alert('Progress updated');
  };

  return (
    <div style={{ padding: '1.5rem' }}>
      <h1>{workshop.title}</h1>
      <p>{workshop.description}</p>
      {/* Module list */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '1rem' }}>
        {workshop.steps.map((step, idx) => (
          <button
            key={step.id}
            onClick={() => {
              setActiveStepIndex(idx);
              setActiveSubIndex(0);
            }}
            style={{
              backgroundColor: idx === activeStepIndex ? '#2563eb' : '#3b82f6',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              padding: '0.5rem 1rem',
              cursor: 'pointer',
            }}
          >
            {step.title}
          </button>
        ))}
      </div>
      {/* Substep tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
        {currentStep.substeps.map((sub, idx) => {
          const unlocked = isUnlocked(activeStepIndex, idx);
          const selected = idx === activeSubIndex;
          return (
            <button
              key={sub.id}
              onClick={() => unlocked && setActiveSubIndex(idx)}
              disabled={!unlocked}
              style={{
                flex: 1,
                padding: '0.4rem 0.6rem',
                border: 'none',
                borderRadius: '6px',
                backgroundColor: selected ? '#ef4444' : unlocked ? '#d1d5db' : '#e5e7eb',
                color: selected ? '#fff' : '#374151',
                cursor: unlocked ? 'pointer' : 'default',
                position: 'relative',
              }}
            >
              {!unlocked && (
                <span
                  style={{ position: 'absolute', left: '0.4rem', top: '50%', transform: 'translateY(-50%)' }}
                >
                  🔒
                </span>
              )}
              {sub.title}
            </button>
          );
        })}
      </div>
      {/* Content area */}
      <div
        style={{
          backgroundColor: '#fff',
          border: '1px solid #e5e7eb',
          borderRadius: '8px',
          padding: '1rem',
          marginTop: '1rem',
        }}
      >
        <h2>{currentSub.title}</h2>
        <p>
          {/* Show a placeholder description; in a real app this would be the
          content of the substep. */}
          This is a placeholder for the {currentSub.substep_type} content of this
          substep. Explore the material here.
        </p>
        <button
          onClick={handleComplete}
          style={{
            marginTop: '1rem',
            backgroundColor: '#10b981',
            color: '#fff',
            padding: '0.5rem 1rem',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
          }}
        >
          Mark complete
        </button>
      </div>
    </div>
  );
}