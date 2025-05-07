import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import HomePage from './components/HomePage';
import AddQuestionForm from './components/AddQuestionForm';
import QuestionView from './components/QuestionView'; // Placeholder component
import './App.css'; // Keep basic styling or create a new one

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          {/* Optional: Basic navigation */}
          <Link to="/">Home</Link>
        </nav>
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/questions/new" element={<AddQuestionForm />} />
            {/* The route for viewing a specific question */}
            <Route path="/questions/:id" element={<QuestionView />} />
            {/* Add other routes as needed */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
