import { useState, useEffect } from 'react';
import './App.css';
import { apiConfig } from './config/api';

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
  const [isAnyEvaluating, setIsAnyEvaluating] = useState<boolean>(false);
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

        fetch(apiConfig.endpoints.validate, {
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
            handleStartInterview();
          }
        })
        .catch(() => {
          localStorage.removeItem('interview-session');
          handleStartInterview();
        });
      } catch (error) {
        console.error('Error loading saved session:', error);
        localStorage.removeItem('interview-session');
        handleStartInterview();
      }
    } else {
      handleStartInterview();
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

      const response = await fetch(apiConfig.endpoints.start, {
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

  const handleRefreshInterview = async () => {
    const confirmRefresh = window.confirm(
      'Are you sure you want to start a new interview? This will reset your current progress and give you a new question.'
    );

    if (confirmRefresh) {
      try {
        if (sessionId) {
          await fetch(apiConfig.endpoints.end(sessionId), {
            method: 'DELETE',
          });
        }
      } catch (err) {
        console.error('Error ending interview session:', err);
      }

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

      // Start a new interview
      handleStartInterview();
    }
  };

  const handleEvaluateSection = async (sectionKey: keyof InterviewNotes, sectionName: string) => {
    try {
      setEvaluatingSection(sectionKey);
      setIsAnyEvaluating(true);

      const response = await fetch(apiConfig.endpoints.evaluate, {
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
      setIsAnyEvaluating(false);
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


  return (
    <div className="App interview-mode">
      <header className="interview-header">
        <div className="header-left">
          <h1>System Design Interview</h1>
          <div className="info-button-container">
            <button className="info-button">
              ℹ️
            </button>
            <div className="info-popup">
              <p>Practice system design interviews with AI-powered feedback. Get random questions and work through the structured interview process step by step.</p>
              <p>This tool guides you through clarifying requirements, defining functional and non-functional requirements, creating high-level designs, and deep-diving into implementation details.</p>
            </div>
          </div>
        </div>
        <button onClick={handleRefreshInterview} className="refresh-button">
          🔄 New Question
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
                    disabled={isAnyEvaluating || !notes.resourceEstimation.trim()}
                  >
                    {evaluatingSection === 'resourceEstimation' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Use this space to jot down rough calculations about scale, storage, bandwidth, throughput, or 
                  latency. This doesn’t have to be perfect or immediate — think of it as a scratchpad you can 
                  revisit as your design evolves.
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
                    disabled={isAnyEvaluating || !notes.assumptions.trim() || !isStepAccessible(1)}
                  >
                    {evaluatingSection === 'assumptions' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  List the key assumptions you’re making about the problem (e.g., scale, users, constraints) and write down the 
                  clarifying questions you’d ask an interviewer. This helps frame the scope and ensures alignment before diving 
                  into design.
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
                    disabled={isAnyEvaluating || !notes.functionalRequirements.trim() || !isStepAccessible(2)}
                  >
                    {evaluatingSection === 'functionalRequirements' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Capture the core capabilities the system must provide from a user’s perspective (e.g., “users can upload photos,” 
                  “system supports search by keyword”). Focus on the “what,” not the “how.”
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
                    disabled={isAnyEvaluating || !notes.nonFunctionalRequirements.trim() || !isStepAccessible(3)}
                  >
                    {evaluatingSection === 'nonFunctionalRequirements' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  List the qualities and constraints the system must satisfy — scalability, availability, latency, consistency, 
                  reliability, security, etc. These guide trade-offs in your design choices.
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
                    disabled={isAnyEvaluating || !notes.highLevelDesign.trim() || !isStepAccessible(4)}
                  >
                    {evaluatingSection === 'highLevelDesign' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Sketch the big picture: the main building blocks of your system (clients, APIs, services, databases, queues, caches, etc.) and 
                  how they interact. Keep it at an architectural level, not implementation details.
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
                    disabled={isAnyEvaluating || !notes.deepDive.trim() || !isStepAccessible(5)}
                  >
                    {evaluatingSection === 'deepDive' ? '⏳ Evaluating...' : '🤖 AI Evaluate'}
                  </button>
                </div>
                <p className="phase-description">
                  Choose 1–2 areas to explore in detail (e.g., database schema, sharding, caching strategy, consistency model). 
                  Demonstrate your ability to reason deeply about trade-offs and technical decisions.
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
            <div className="evaluations-list">
              {['Resource Estimation Notes', '1. Assumptions & Clarifying Questions', '2. Functional Requirements', '3. Non-Functional Requirements', '4. High-Level Components & Design', '5. Deep Dive Topics'].map((sectionName) => {
                const evaluation = evaluations.find(e => e.section === sectionName);
                const sectionKey = {
                  'Resource Estimation Notes': 'resourceEstimation',
                  '1. Assumptions & Clarifying Questions': 'assumptions',
                  '2. Functional Requirements': 'functionalRequirements',
                  '3. Non-Functional Requirements': 'nonFunctionalRequirements',
                  '4. High-Level Components & Design': 'highLevelDesign',
                  '5. Deep Dive Topics': 'deepDive'
                }[sectionName];
                const isEvaluating = evaluatingSection === sectionKey;

                return (
                  <div key={sectionName} className="evaluation-item">
                    <div className="evaluation-header">
                      <h4>{sectionName}</h4>
                      {evaluation && (
                        <>
                          <span className="evaluation-time">{evaluation.timestamp}</span>
                          {evaluation.score && (
                            <span className="evaluation-score">{evaluation.score}/5</span>
                          )}
                        </>
                      )}
                    </div>
                    <div className="evaluation-feedback">
                      {isEvaluating ? (
                        <div className="evaluation-spinner">
                          <div className="spinner"></div>
                          <span>Evaluating...</span>
                        </div>
                      ) : evaluation ? (
                        evaluation.feedback
                      ) : (
                        <span className="no-evaluation">Click "AI Evaluate" to get feedback</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
