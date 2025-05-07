import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { addQuestion } from '../api'; // Import the API function

function AddQuestionForm() {
  const [questionText, setQuestionText] = useState('');
  const [solution, setSolution] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent default form submission
    setSubmitting(true);
    setError(null);

    if (!questionText.trim() || !solution.trim()) {
      setError('Both question text and solution are required.');
      setSubmitting(false);
      return;
    }

    try {
      // Prepare data - api.js handles adding defaults for other fields
      const questionData = {
        question_text: questionText,
        solution: solution,
      };
      await addQuestion(questionData);
      // If successful, navigate back to the home page
      navigate('/');
    } catch (err) {
      console.error("Error adding question:", err);
      setError('Failed to add question. Please try again.');
       // Provide more specific error feedback if possible
       if (err.response) {
           setError(`Failed to add question. Server responded with status: ${err.response.status}`);
       } else if (err.request) {
           setError('Failed to add question. No response from server.');
       } else {
           setError('Failed to add question. Error: ' + err.message);
       }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h1>Add New Question</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="questionText">Question Text:</label>
          <textarea
            id="questionText"
            value={questionText}
            onChange={(e) => setQuestionText(e.target.value)}
            required
            rows={3}
            style={{ width: '100%', marginBottom: '10px' }}
          />
        </div>
        <div>
          <label htmlFor="solution">Solution:</label>
          <textarea
            id="solution"
            value={solution}
            onChange={(e) => setSolution(e.target.value)}
            required
            rows={5}
            style={{ width: '100%', marginBottom: '10px' }}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit" disabled={submitting}>
          {submitting ? 'Adding...' : 'Add Question'}
        </button>
         {/* Add a button to cancel and go back */}
         <button type="button" onClick={() => navigate('/')} style={{ marginLeft: '10px' }} disabled={submitting}>
             Cancel
         </button>
      </form>
    </div>
  );
}

export default AddQuestionForm;
