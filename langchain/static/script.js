document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // Trigger send message on Enter key
    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            sendUserMessage();
        }
    });

    // Trigger send message on button click
    sendButton.addEventListener('click', sendUserMessage);

    async function sendUserMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        // Add user message to chat
        addMessage("user", userMessage);

        // Show typing animation for bot
        const botTyping = addMessage("bot", "Typing...");

        // Call the backend for RUBY's response
        const response = await sendMessageToRUBY(userMessage);

        // Remove typing animation and add bot's actual response
        botTyping.innerHTML = `<img style="height:25px;width:25px;border-radius:10px;" src="static/bot.gif"><span>&nbsp&nbsp${response}</span>`;
        
        // Read aloud the response
        textToSpeech(response);

        // Clear input
        userInput.value = "";
    }

    function addMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', sender);
        messageDiv.innerHTML = `<img style="height:25px;width:25px;border-radius:10px;" src="${sender === 'user' ? 'static/user.jpg' : 'static/bot.gif'}"><span>&nbsp&nbsp${message}</span>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
        return messageDiv;
    }

    async function sendMessageToRUBY(message) {
        try {
            const response = await fetch('/ask_ruby', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: message })
            });
            const data = await response.json();
            return data.answer;
        } catch (error) {
            console.error('Error:', error);
            return "Sorry, something went wrong.";
        }
    }

    // Text to Speech
    const synth = window.speechSynthesis;

    function textToSpeech(string) {
        let voice = new SpeechSynthesisUtterance(string);
        voice.lang = "en-US";
        voice.volume = 1;
        voice.rate = 1;
        voice.pitch = 1;
        synth.speak(voice);
    }
});
