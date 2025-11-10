// Sign Language Detector Web Application JavaScript

let statusCheckInterval;
let sentenceUpdateInterval;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Setup event listeners
    setupEventListeners();
    
    // Start status updates
    startStatusUpdates();
}

function setupEventListeners() {
    // Clear button
    document.getElementById('clearBtn').addEventListener('click', clearSentence);
    
    // Backspace button
    document.getElementById('backspaceBtn').addEventListener('click', removeLastWord);
    
    // TTS toggle button
    document.getElementById('ttsToggleBtn').addEventListener('click', toggleTTS);
}

function startStatusUpdates() {
    // Update sentence every 500ms
    sentenceUpdateInterval = setInterval(updateSentence, 500);
    
    // Update status every 2 seconds
    statusCheckInterval = setInterval(updateStatus, 2000);
}

function updateSentence() {
    fetch('/api/sentence')
        .then(response => response.json())
        .then(data => {
            const sentenceText = document.getElementById('sentenceText');
            if (data.sentence && data.sentence.trim()) {
                sentenceText.textContent = data.sentence;
                sentenceText.classList.remove('empty');
            } else {
                sentenceText.textContent = 'Make gestures to build your sentence...';
                sentenceText.classList.add('empty');
            }
        })
        .catch(error => {
            console.error('Error fetching sentence:', error);
        });
}

function updateStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            // Update TTS status
            updateTTSStatus(data.tts_enabled);
            
            // Update current sign display
            updateSignDisplay(data.current_sign);
        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });
}

function updateTTSStatus(enabled) {
    const ttsStatus = document.getElementById('ttsStatus');
    if (enabled) {
        ttsStatus.textContent = 'TTS: ON';
        ttsStatus.classList.remove('inactive');
        ttsStatus.classList.add('active');
    } else {
        ttsStatus.textContent = 'TTS: OFF';
        ttsStatus.classList.remove('active');
        ttsStatus.classList.add('inactive');
    }
}

function updateSignDisplay(sign) {
    const signDisplay = document.getElementById('signDisplay');
    if (signDisplay) {
        if (sign) {
            signDisplay.innerHTML = `<p class="detected">${sign}</p>`;
        } else {
            signDisplay.innerHTML = '<p>No sign detected</p>';
        }
    }
}

// Make updateSignDisplay available globally for inline script
window.updateSignDisplay = updateSignDisplay;
window.updateCameraStatus = updateCameraStatus;

function clearSentence() {
    fetch('/api/sentence', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateSentence();
                showNotification('Sentence cleared');
            }
        })
        .catch(error => {
            console.error('Error clearing sentence:', error);
            showNotification('Error clearing sentence', 'error');
        });
}

function removeLastWord() {
    fetch('/api/sentence/backspace', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateSentence();
                showNotification('Last word removed');
            }
        })
        .catch(error => {
            console.error('Error removing last word:', error);
            showNotification('Error removing last word', 'error');
        });
}

function toggleTTS() {
    fetch('/api/tts/toggle', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateTTSStatus(data.tts_enabled);
                const message = data.tts_enabled ? 'TTS enabled' : 'TTS disabled';
                showNotification(message);
            }
        })
        .catch(error => {
            console.error('Error toggling TTS:', error);
            showNotification('Error toggling TTS', 'error');
        });
}

// Camera status is managed by the inline script in index.html
function updateCameraStatus(connected) {
    const cameraStatus = document.getElementById('cameraStatus');
    if (cameraStatus) {
        if (connected) {
            cameraStatus.textContent = 'Camera: Connected';
            cameraStatus.classList.remove('inactive');
            cameraStatus.classList.add('active');
        } else {
            cameraStatus.textContent = 'Camera: Disconnected';
            cameraStatus.classList.remove('active');
            cameraStatus.classList.add('inactive');
        }
    }
}

function showNotification(message, type = 'success') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#dc3545' : '#28a745'};
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
    if (sentenceUpdateInterval) {
        clearInterval(sentenceUpdateInterval);
    }
});

