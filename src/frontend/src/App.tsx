import { useState, useEffect } from 'react';
import './App.css';

interface InterviewNotes {
  assumptions: string;
  functionalRequirements: string;
  nonFunctionalRequirements: string;
  resourceEstimation: string;
  highLevelDesign: string;
  deepDive: string;
}

interface Evaluation {
  section: string;
  feedback: string;
  timestamp: string;
  score?: number;
}

function App() {
  const [interviewStarted, setInterviewStarted] = useState(false);
  const [question, setQuestion] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [sessionId, setSessionId] = useState<string>('');
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [evaluatingSection, setEvaluatingSection] = useState<string>('');
  const [notes, setNotes] = useState<InterviewNotes>({
    assumptions: '',
    functionalRequirements: '',
    nonFunctionalRequirements: '',
    resourceEstimation: '',
    highLevelDesign: '',
    deepDive: ''
  });

  useEffect(() => {
    const savedSession = localStorage.getItem('interview-session');
    if (savedSession) {
      try {
        const sessionData = JSON.parse(savedSession);

        fetch(`http://localhost:8000/api/interview/validate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ session_id: sessionData.sessionId })
        })
        .then(response => {
          if (response.ok) {
            setSessionId(sessionData.sessionId);
            setQuestion(sessionData.question);
            setNotes(sessionData.notes);
            setEvaluations(sessionData.evaluations);
            setInterviewStarted(true);
          } else {
            localStorage.removeItem('interview-session');
          }
        })
        .catch(() => {
          localStorage.removeItem('interview-session');
        });
      } catch (error) {
        console.error('Error loading saved session:', error);
        localStorage.removeItem('interview-session');
      }
    }
  }, []);

  useEffect(() => {
    if (interviewStarted && sessionId) {
      const sessionData = {
        sessionId,
        question,
        notes,
        evaluations
      };
      localStorage.setItem('interview-session', JSON.stringify(sessionData));
    } else if (!interviewStarted) {
      localStorage.removeItem('interview-session');
    }
  }, [interviewStarted, sessionId, question, notes, evaluations]);

  const handleStartInterview = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await fetch('http://localhost:8000/api/interview/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error('Failed to start interview session');
      }

      const data = await response.json();
      setSessionId(data.session_id);
      setQuestion(data.question);
      setInterviewStarted(true);
    } catch (err) {
      setError('Failed to start interview. Please try again.');
      console.error('Error starting interview:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEndInterview = async () => {
    const confirmEnd = window.confirm(
      'Are you sure you want to end the interview session? This will reset your progress.'
    );

    if (confirmEnd) {
      try {
        if (sessionId) {
          await fetch(`http://localhost:8000/api/interview/${sessionId}`, {
            method: 'DELETE',
          });
        }
      } catch (err) {
        console.error('Error ending interview session:', err);
      }

      setInterviewStarted(false);
      setQuestion('');
      setError('');
      setSessionId('');
      setEvaluations([]);
      setEvaluatingSection('');
      setNotes({
        assumptions: '',
        functionalRequirements: '',
        nonFunctionalRequirements: '',
        resourceEstimation: '',
        highLevelDesign: '',
        deepDive: ''
      });
    }
  };

  const handleEvaluateSection = async (sectionKey: keyof InterviewNotes, sectionName: string) => {
    try {
      setEvaluatingSection(sectionKey);

      const response = await fetch('http://localhost:8000/api/interview/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          section: sectionKey,
          content: notes[sectionKey]
        })
      });

      if (!response.ok) {
        throw new Error('Failed to evaluate section');
      }

      const data = await response.json();

      const newEvaluation: Evaluation = {
        section: sectionName,
        feedback: data.feedback,
        timestamp: new Date().toLocaleTimeString(),
        score: data.score
      };

      setEvaluations(prev => {
        // Replace existing evaluation for this section or add new one
        const filtered = prev.filter(evaluation => evaluation.section !== sectionName);
        return [...filtered, newEvaluation];
      });

    } catch (err) {
      console.error('Error evaluating section:', err);
      setError('Failed to get AI evaluation. Please try again.');
    } finally {
      setEvaluatingSection('');
    }
  };

  const updateNotes = (field: keyof InterviewNotes, value: string) => {
    setNotes(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const isStepCompleted = (step: keyof InterviewNotes): boolean => {
    return notes[step].trim().length > 0;
  };

  const getCurrentStep = (): number => {
    const steps: (keyof InterviewNotes)[] = ['assumptions', 'functionalRequirements', 'nonFunctionalRequirements', 'highLevelDesign', 'deepDive'];
    for (let i = 0; i < steps.length; i++) {
      if (!isStepCompleted(steps[i])) {
        return i + 1; // 1-indexed for display
      }
    }
    return steps.length; // All steps completed
  };

  const isStepAccessible = (stepNumber: number): boolean => {
    const currentStep = getCurrentStep();
    return stepNumber <= currentStep;
  };

  if (!interviewStarted) {
    return (
      <div className="App">
        <div className="container">
          <h1>System Design Interview Companion</h1>
          <div className="description">
            <p>
              Practice system design interviews with AI-powered feedback.
              Get random questions from our curated collection and work through
              the structured interview process step by step.
            </p>
            <p>
              This tool will guide you through clarifying requirements,
              defining functional and non-functional requirements, creating
              high-level designs, and deep-diving into implementation details.
            </p>
          </div>
          <button
            className="start-button"
            onClick={handleStartInterview}
          >
            Start Interview
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="App interview-mode">
      <header className="interview-header">
        <h1>System Design Interview</h1>
        <button onClick={handleEndInterview} className="end-button">
          End Interview
        </button>
      </header>

      <div className="interview-layout">
        <div className="interview-main">
          {loading && (
            <div className="loading">
              <h2>Loading interview question...</h2>
            </div>
          )}

          {error && (
            <div className="error">
              <h2>Error</h2>
              <p>{error}</p>
              <button onClick={handleStartInterview} className="retry-button">
                Try Again
              </button>
            </div>
          )}

          {!loading && !error && question && (
            <div className="interview-phases">
              <div className="question-section">
                <h2>Your Challenge</h2>
                <div className="question-card">
                  <p className="question-text">{question}</p>
                </div>
              </div>
              <div className="phase-section notes-section">
                <div className="section-header">
                  <h3>📝 Resource Estimation Notes</h3>
                  <button
                    className="evaluate-button"
                    onClick={() => handleEvaluateSection('resourceEstimation', 'Resource Estimation Notes')}
                    disabled={evaluatingSection === 'resourceEstimation' || !notes.resourceEstimation.trim()}
                  >
                    {evaluatingSection === 'resourceEstimation' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Use this area to jot down resource estimation notes throughout the interview.
                  It's most useful after designing the system. Key numbers to consider: DAU (Daily Active Users),
                  number of items for your specific application, QPS, storage requirements, etc.
                </p>
                <textarea
                  className="phase-textarea"
                  placeholder="Notes: DAU, QPS, storage estimates, bandwidth calculations..."
                  value={notes.resourceEstimation}
                  onChange={(e) => updateNotes('resourceEstimation', e.target.value)}
                />
              </div>

              <div className={`phase-section ${!isStepAccessible(1) ? 'phase-disabled' : ''} ${getCurrentStep() === 1 ? 'phase-current' : ''} ${isStepCompleted('assumptions') ? 'phase-completed' : ''}`}>
                <div className="section-header">
                  <h3>1. Assumptions & Clarifying Questions {isStepCompleted('assumptions') ? '✓' : ''}</h3>
                  <button
                    className="evaluate-button"
                    onClick={() => handleEvaluateSection('assumptions', '1. Assumptions & Clarifying Questions')}
                    disabled={evaluatingSection === 'assumptions' || !notes.assumptions.trim() || !isStepAccessible(1)}
                  >
                    {evaluatingSection === 'assumptions' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  State your assumptions about the problem and ask clarifying questions about requirements, scale, and constraints.
                </p>
                <textarea
                  className="phase-textarea"
                  placeholder="Write your assumptions and clarifying questions here..."
                  value={notes.assumptions}
                  onChange={(e) => updateNotes('assumptions', e.target.value)}
                  disabled={!isStepAccessible(1)}
                />
              </div>

              <div className={`phase-section ${!isStepAccessible(2) ? 'phase-disabled' : ''} ${getCurrentStep() === 2 ? 'phase-current' : ''} ${isStepCompleted('functionalRequirements') ? 'phase-completed' : ''}`}>
                <div className="section-header">
                  <h3>2. Functional Requirements {isStepCompleted('functionalRequirements') ? '✓' : ''}</h3>
                  <button
                    className="evaluate-button"
                    onClick={() => handleEvaluateSection('functionalRequirements', '2. Functional Requirements')}
                    disabled={evaluatingSection === 'functionalRequirements' || !notes.functionalRequirements.trim() || !isStepAccessible(2)}
                  >
                    {evaluatingSection === 'functionalRequirements' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Define what the system should do. List the core features and functionalities.
                </p>
                <textarea
                  className="phase-textarea"
                  placeholder="List the functional requirements here..."
                  value={notes.functionalRequirements}
                  onChange={(e) => updateNotes('functionalRequirements', e.target.value)}
                  disabled={!isStepAccessible(2)}
                />
              </div>

              <div className={`phase-section ${!isStepAccessible(3) ? 'phase-disabled' : ''} ${getCurrentStep() === 3 ? 'phase-current' : ''} ${isStepCompleted('nonFunctionalRequirements') ? 'phase-completed' : ''}`}>
                <div className="section-header">
                  <h3>3. Non-Functional Requirements {isStepCompleted('nonFunctionalRequirements') ? '✓' : ''}</h3>
                  <button
                    className="evaluate-button"
                    onClick={() => handleEvaluateSection('nonFunctionalRequirements', '3. Non-Functional Requirements')}
                    disabled={evaluatingSection === 'nonFunctionalRequirements' || !notes.nonFunctionalRequirements.trim() || !isStepAccessible(3)}
                  >
                    {evaluatingSection === 'nonFunctionalRequirements' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Define scalability, performance, availability, consistency, and other quality attributes.
                </p>
                <textarea
                  className="phase-textarea"
                  placeholder="Define scalability, performance, availability requirements..."
                  value={notes.nonFunctionalRequirements}
                  onChange={(e) => updateNotes('nonFunctionalRequirements', e.target.value)}
                  disabled={!isStepAccessible(3)}
                />
              </div>

              <div className={`phase-section ${!isStepAccessible(4) ? 'phase-disabled' : ''} ${getCurrentStep() === 4 ? 'phase-current' : ''} ${isStepCompleted('highLevelDesign') ? 'phase-completed' : ''}`}>
                <div className="section-header">
                  <h3>4. High-Level Components & Design {isStepCompleted('highLevelDesign') ? '✓' : ''}</h3>
                  <button
                    className="evaluate-button"
                    onClick={() => handleEvaluateSection('highLevelDesign', '4. High-Level Components & Design')}
                    disabled={evaluatingSection === 'highLevelDesign' || !notes.highLevelDesign.trim() || !isStepAccessible(4)}
                  >
                    {evaluatingSection === 'highLevelDesign' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Design the overall architecture. Identify main components, services, and their interactions.
                </p>
                <textarea
                  className="phase-textarea"
                  placeholder="Design the high-level architecture, main components, APIs..."
                  value={notes.highLevelDesign}
                  onChange={(e) => updateNotes('highLevelDesign', e.target.value)}
                  disabled={!isStepAccessible(4)}
                />
              </div>

              <div className={`phase-section ${!isStepAccessible(5) ? 'phase-disabled' : ''} ${getCurrentStep() === 5 ? 'phase-current' : ''} ${isStepCompleted('deepDive') ? 'phase-completed' : ''}`}>
                <div className="section-header">
                  <h3>5. Deep Dive Topics {isStepCompleted('deepDive') ? '✓' : ''}</h3>
                  <button
                    className="evaluate-button"
                    onClick={() => handleEvaluateSection('deepDive', '5. Deep Dive Topics')}
                    disabled={evaluatingSection === 'deepDive' || !notes.deepDive.trim() || !isStepAccessible(5)}
                  >
                    {evaluatingSection === 'deepDive' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Dive deeper into specific components, discuss data models, algorithms, edge cases, and trade-offs.
                </p>
                <textarea
                  className="phase-textarea"
                  placeholder="Deep dive into specific components, data models, algorithms..."
                  value={notes.deepDive}
                  onChange={(e) => updateNotes('deepDive', e.target.value)}
                  disabled={!isStepAccessible(5)}
                />
              </div>
            </div>
        )}
        </div>

        <div className="evaluation-sidebar">
          <div className="sidebar-content">
            <h3>🤖 AI Evaluations</h3>
            {evaluations.length === 0 ? (
              <p className="no-evaluations">
                Click "AI Evaluate" on any section to get feedback from the AI interviewer.
              </p>
            ) : (
              <div className="evaluations-list">
                {evaluations.map((evaluation, index) => (
                  <div key={index} className="evaluation-item">
                    <div className="evaluation-header">
                      <h4>{evaluation.section}</h4>
                      <span className="evaluation-time">{evaluation.timestamp}</span>
                      {evaluation.score && (
                        <span className="evaluation-score">{evaluation.score}/5</span>
                      )}
                    </div>
                    <div className="evaluation-feedback">
                      {evaluation.feedback}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
