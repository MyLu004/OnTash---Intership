import { useState } from "react";
import ChatArea from "../components/chatArea";
import Sidebar from "../components/sideBar";


const title = "this is a title for content 1";


function Chatbot() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hello! Ask me anything." },
  ]);
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleSend = async (e) => {
  e.preventDefault();
  if (!input.trim()) return;

  const userMessage = { role: "user", text: input };
  setMessages((prev) => [...prev, userMessage]);

  try {
    const res = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "llama3", // Or whatever is selected
        prompt: input,
        stream: false,
      }),
    });

    const data = await res.json();
    const botMessage = { role: "bot", text: data.response };

    setMessages((prev) => [...prev, botMessage]);
  } catch (err) {
    console.error("Error:", err);
    setMessages((prev) => [
      ...prev,
      { role: "bot", text: "Failed to connect to Ollama backend." },
    ]);
  }

  setInput("");
};

  return (
    <div className="flex h-screen w-screen">
      <Sidebar
        sidebarOpen={sidebarOpen}
        toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        //chats={messages.map((m) => m.text)} // simple placeholder for now
        chats={[title]}
      />
      <ChatArea
        messages={messages}
        input={input}
        setInput={setInput}
        handleSend={handleSend}
      />
    </div>
  );
}

export default Chatbot;
