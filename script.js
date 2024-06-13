document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.getElementById('chatbox');

    function appendMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.className = className;
        messageElement.innerText = message;
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    async function fetchAIResponse(userMessage) {
        appendMessage(userMessage, 'user-message');
        appendMessage('Thinking...', 'ai-message');

        try {
            const response = await fetch(`/ask?question=${encodeURIComponent(userMessage)}`);
            const data = await response.json();
            const aiMessage = data.answer || 'Sorry, I could not find an answer.';
            const thinkingElement = chatbox.querySelector('.ai-message:last-child');
            thinkingElement.innerText = aiMessage;
        } catch (error) {
            const thinkingElement = chatbox.querySelector('.ai-message:last-child');
            thinkingElement.innerText = 'Error: Could not reach the AI service.';
        }
    }

    window.sendMessage = function () {
        const userInput = document.getElementById('user-input');
        const userMessage = userInput.value.trim();
        if (userMessage) {
            userInput.value = '';
            fetchAIResponse(userMessage);
        }
    };
});
