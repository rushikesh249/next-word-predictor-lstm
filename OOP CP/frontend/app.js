// Configuration
const isLocalhost = (location.hostname === 'localhost' || location.hostname === '127.0.0.1');
const isFile = location.protocol === 'file:';
const API_BASE = (isLocalhost || isFile)
  ? 'http://127.0.0.1:5000'
  : `${location.origin}`;

// DOM Elements
const textEl = document.getElementById('text');
const numEl = document.getElementById('num');
const btnEl = document.getElementById('predict');
const resultEl = document.getElementById('result');
const statusEl = document.getElementById('status');
const statusTextEl = document.getElementById('status-text');
const charCounterEl = document.getElementById('char-counter');
const btnTextEl = document.getElementById('btn-text');
const btnLoadingEl = document.getElementById('btn-loading');

// State management
let isBackendConnected = false;
let isLoading = false;

// Check backend connection
async function checkBackendStatus() {
  try {
    const response = await fetch(`${API_BASE}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (response.ok) {
      isBackendConnected = true;
      updateStatus('✅ Backend connected', 'connected');
      btnEl.disabled = false;
    } else {
      throw new Error('Backend not responding');
    }
  } catch (error) {
    isBackendConnected = false;
    updateStatus('❌ Backend disconnected - Please start server.py', 'disconnected');
    btnEl.disabled = true;
  }
}

// Update status display
function updateStatus(message, type) {
  statusTextEl.textContent = message;
  statusEl.className = `status-bar ${type}`;
}

// Update character counter
function updateCharCounter() {
  const length = textEl.value.length;
  charCounterEl.textContent = `${length}/500`;
  
  if (length > 450) {
    charCounterEl.style.color = '#ef4444';
  } else if (length > 300) {
    charCounterEl.style.color = '#f59e0b';
  } else {
    charCounterEl.style.color = '#9ca3af';
  }
}

// Set loading state
function setLoadingState(loading) {
  isLoading = loading;
  btnEl.disabled = loading || !isBackendConnected;
  
  if (loading) {
    btnTextEl.classList.add('hidden');
    btnLoadingEl.classList.remove('hidden');
  } else {
    btnTextEl.classList.remove('hidden');
    btnLoadingEl.classList.add('hidden');
  }
}

// Display result
function displayResult(data, originalText) {
  const completion = data.completion || '';
  const words = data.words || [];
  
  if (!completion) {
    resultEl.innerHTML = `
      <div class="result-error">
        🤔 No prediction available. Try a different prompt or check if the model is trained.
      </div>
    `;
    return;
  }
  
  resultEl.innerHTML = `
    <div class="result-success">
      <div class="result-header">
        <h4>🎯 AI Prediction Result</h4>
      </div>
      <div class="result-content">
        <div class="original-text">
          <strong>Your text:</strong> "${originalText}"
        </div>
        <div class="predicted-text">
          <strong>Predicted completion:</strong> "<span class="highlight">${completion}</span>"
        </div>
        <div class="full-sentence">
          <strong>Complete sentence:</strong> "${originalText} ${completion}"
        </div>
        <div class="word-breakdown">
          <strong>Individual words:</strong> ${words.map(word => `<span class="word-tag">${word}</span>`).join(' ')}
        </div>
      </div>
    </div>
  `;
}

// Display error
function displayError(error) {
  resultEl.innerHTML = `
    <div class="result-error">
      <div class="error-header">
        <h4>❌ Prediction Error</h4>
      </div>
      <div class="error-content">
        <p><strong>Error:</strong> ${error}</p>
        <p><strong>Possible solutions:</strong></p>
        <ul>
          <li>Make sure the backend server is running (python server.py)</li>
          <li>Check if the model is trained (model.h5 file exists)</li>
          <li>Try a different text prompt</li>
          <li>Ensure the dataset file is available</li>
        </ul>
      </div>
    </div>
  `;
}

// Main prediction function
async function predict() {
  const text = (textEl.value || '').trim();
  const num = parseInt(numEl.value || '1', 10);
  
  // Validation
  if (!text) {
    displayError('Please enter some text to get predictions.');
    return;
  }
  
  if (!isBackendConnected) {
    displayError('Backend server is not connected. Please start the server first.');
    return;
  }
  
  try {
    setLoadingState(true);
    
    const response = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, num_words: num })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || `Server error: ${response.status}`);
    }
    
    displayResult(data, text);
    
  } catch (error) {
    console.error('Prediction error:', error);
    displayError(error.message);
  } finally {
    setLoadingState(false);
  }
}

// Set example text
function setExampleText(text) {
  textEl.value = text;
  updateCharCounter();
  textEl.focus();
}

// Event Listeners
btnEl.addEventListener('click', predict);

// Character counter
textEl.addEventListener('input', updateCharCounter);

// Enter key to predict
textEl.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === 'Enter') {
    e.preventDefault();
    predict();
  }
});

// Example buttons
document.addEventListener('DOMContentLoaded', () => {
  const exampleButtons = document.querySelectorAll('.example-btn');
  exampleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.getAttribute('data-text');
      setExampleText(text);
    });
  });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  updateCharCounter();
  checkBackendStatus();
  
  // Periodically check backend status
  setInterval(checkBackendStatus, 10000); // Check every 10 seconds
});

// Add helpful tooltips
const helpTexts = {
  'text': 'Enter 2-5 words for best results. The LSTM model works better with meaningful phrases.',
  'num': 'Choose how many words to predict (1-10). More words = longer completion.',
  'predict': 'Click to generate AI predictions, or press Ctrl+Enter'
};

// Add title attributes for tooltips
Object.keys(helpTexts).forEach(id => {
  const element = document.getElementById(id);
  if (element) {
    element.title = helpTexts[id];
  }
});


