import React, { useState, useEffect } from 'react';

interface RiddleResponse {
  riddles: string[];
  playerName: string;
}

const App: React.FC = () => {
  const [riddles, setRiddles] = useState<string[]>([]);
  const [playerName, setPlayerName] = useState<string>('');
  const [currentRiddleIndex, setCurrentRiddleIndex] = useState(0);
  const [guess, setGuess] = useState('');
  const [attempts, setAttempts] = useState(0);

  useEffect(() => {
    fetchRiddles();
  }, []);

  const fetchRiddles = async () => {
    const response = await fetch('/riddle');
    const data: RiddleResponse = await response.json();
    setRiddles(data.riddles);
    setPlayerName(data.playerName);
  };

  const handleGuess = () => {
    if (guess.toLowerCase() === playerName.toLowerCase()) {
      alert('Correct!');
      // Reset or perform additional actions
    } else {
      const nextIndex = (currentRiddleIndex + 1) % riddles.length;
      setCurrentRiddleIndex(nextIndex);
      setAttempts(attempts + 1);
      if (attempts >= 5) {
        alert(`Sorry, you've used all attempts. The player was ${playerName}.`);
        // Optionally reset the game or provide an option to try again
      } else {
        alert('Incorrect. Try the next riddle.');
      }
    }
    setGuess(''); // Reset guess input
  };

  return (
    <div>
      <h1>NBA Riddles</h1>
      <p>{riddles[currentRiddleIndex]}</p>
      <input
        type="text"
        value={guess}
        onChange={e => setGuess(e.target.value)}
        placeholder="Guess the player's name"
      />
      <button onClick={handleGuess}>Submit Guess</button>
    </div>
  );
};

export default App;
