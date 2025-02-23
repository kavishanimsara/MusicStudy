document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chatbot-form");
    const input = document.getElementById("chatbot-input");
    const messages = document.getElementById("chatbot-messages");
    const toggleButton = document.getElementById("chatbot-toggle-button");
    const chatbotBox = document.querySelector(".chatbot-box");
  
    // Toggle chatbot visibility
    toggleButton.addEventListener("click", () => {
      chatbotBox.classList.toggle("d-none");
    });
  
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
  
      const userMessage = input.value.trim();
      if (userMessage === "") return;
  
      addMessage("You", userMessage);
  
      const response = await fetch("/chatbot-response/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify({ message: userMessage }),
      });
  
      if (response.ok) {
        const data = await response.json();
        addMessage("", data.reply); // No prefix for bot replies
      } else {
        addMessage("", "Something went wrong. Please try again.");
      }
  
      input.value = "";
    });
  
    function addMessage(sender, text) {
        const message = document.createElement("div");
    
        // Only add "You:" prefix for user messages, leave bot replies plain
        if (sender === "You") {
            message.textContent = `${sender}: ${text}`;
        } else {
            message.textContent = text; // No prefix for bot replies
        }
    
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
    }
    
  
    function getCsrfToken() {
      const cookies = document.cookie.split(";");
      for (const cookie of cookies) {
        const [name, value] = cookie.trim().split("=");
        if (name === "csrftoken") return decodeURIComponent(value);
      }
      return null;
    }
  });
  
