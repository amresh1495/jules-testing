import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getQuestions } from '../api'; // Import the API function

function HomePage() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        setLoading(true);
        const response = await getQuestions();
        setQuestions(response.data);
        setError(null);
      } catch (err) {
        console.error("Error fetching questions:", err);
        setError('Failed to load questions.');
        // Handle specific errors (e.g., network error, server error) if needed
        if (err.response) {
            // Server responded with a status code outside 2xx range
            setError(`Failed to load questions. Status: ${err.response.status}`);
        } else if (err.request) {
            // Request was made but no response received
            setError('Failed to load questions. No response from server.');
        } else {
            // Something else happened in setting up the request
            setError('Failed to load questions. Error: ' + err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []); // Empty dependency array means this runs once on mount

  return (
    <div>
      <h1>Spaced Repetition Questions</h1>
      <Link to="/questions/new">
        <button>Add New Question</button>
      </Link>
      {loading && <p>Loading questions...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && !error && (
        <ul>
          {questions.length > 0 ? (
            questions.map((question) => (
              <li key={question.id || question._id}> {/* Use id or _id */}
                {/* Link to the detail view (placeholder for now) */}
                <Link to={`/questions/${question.id || question._id}`}>
                    {question.question_text}
                </Link>
              </li>
            ))
          ) : (
            <p>No questions yet. Add one!</p>
          )}
        </ul>
      )}
    </div>
  );
}

export default HomePage;
