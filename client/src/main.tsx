import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx'; // Add curly braces to import the named export

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

