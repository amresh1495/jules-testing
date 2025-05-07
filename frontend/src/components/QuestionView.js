import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getQuestionById, updateQuestionSchedule } from '../api'; // Import API functions

function QuestionView() {
  const { id } = useParams(); // Get the question ID from the URL
  const navigate = useNavigate(); // Hook for navigation
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showSolution, setShowSolution] = useState(false); // State to toggle solution visibility
  const [updateError, setUpdateError] = useState(null); // Separate error state for updates
  const [isUpdating, setIsUpdating] = useState(false); // State to disable buttons during update

  // Spaced repetition intervals
  const intervals = [2, 4, 8, 16, 30];

  useEffect(() => {
    const fetchQuestion = async () => {
      try {
        setLoading(true);
        setError(null); // Reset errors
        setUpdateError(null);
        console.log(`Fetching question with ID: ${id}`);
        const response = await getQuestionById(id);
        setQuestion(response.data);
      } catch (err) {
        console.error(`Error fetching question ${id}:`, err);
        if (err.response && err.response.status === 404) {
            setError(`Question with ID ${id} not found.`);
        } else if (err.request) {
            setError('Failed to fetch question. No response from server.');
        } else {
            setError('Failed to fetch question. Error: ' + err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchQuestion();
  }, [id]); // Re-run effect if ID changes

  const handleScheduleUpdate = async (intervalDays) => {
    if (!question || isUpdating) return; // Prevent update if no question or already updating

    setIsUpdating(true);
    setUpdateError(null); // Reset update error
    try {
      console.log(`Attempting to update question ${id} with interval ${intervalDays}`);
      await updateQuestionSchedule(id, intervalDays);
      console.log(`Successfully updated question ${id}. Navigating home.`);
      navigate('/'); // Navigate back to home page on success
    } catch (err) {
      console.error(`Error updating question ${id}:`, err);
      let errorMsg = 'Failed to update schedule.';
       if (err.response) {
           errorMsg = `Failed to update schedule. Server responded with status: ${err.response.status}`;
       } else if (err.request) {
           errorMsg = 'Failed to update schedule. No response from server.';
       } else {
           errorMsg = 'Failed to update schedule. Error: ' + err.message;
       }
      setUpdateError(errorMsg);
    } finally {
        setIsUpdating(false); // Re-enable buttons
    }
  };

  if (loading) {
    return <p>Loading question details...</p>;
  }

  if (error) {
    // Display fetch error prominently
    return <p style={{ color: 'red' }}>{error}</p>;
  }

  if (!question) {
    // This case might be redundant if error handles 404, but good as a fallback
    return <p>Question not found.</p>;
  }

  return (
    <div>
      <h1>Revise Question</h1>
      <div style={{ border: '1px solid #eee', padding: '15px', marginBottom: '20px' }}>
          <p><strong>Question:</strong></p>
          <p style={{ fontSize: '1.2em' }}>{question.question_text}</p>
      </div>

      {!showSolution && (
        <button onClick={() => setShowSolution(true)}>Show Solution</button>
      )}

      {showSolution && (
        <div style={{ border: '1px solid #eee', padding: '15px', marginBottom: '20px', backgroundColor: '#f9f9f9' }}>
          <p><strong>Solution:</strong></p>
          <p>{question.solution}</p>
          <hr/>
          <p><strong>How well did you remember? (Choose next revision interval):</strong></p>
          <div>
            {intervals.map((days) => (
              <button
                key={days}
                onClick={() => handleScheduleUpdate(days)}
                disabled={isUpdating} // Disable buttons while updating
                style={{ marginRight: '10px', marginBottom: '10px' }}
              >
                {isUpdating ? 'Updating...' : `${days} Days`}
              </button>
            ))}
          </div>
          {/* Display update errors here */}
          {updateError && <p style={{ color: 'red', marginTop: '10px' }}>{updateError}</p>}
        </div>
      )}
       <button onClick={() => navigate('/')} disabled={isUpdating}>
         Back to List
       </button>
    </div>
  );
}

export default QuestionView;
