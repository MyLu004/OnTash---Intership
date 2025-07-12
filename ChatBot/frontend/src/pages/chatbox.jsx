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


  //retrieve access token
  const accessToken = localStorage.getItem("accessToken"); 

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`, 
      },
      body: JSON.stringify({
        prompt: input,
        model: "llama3", // or use selectedModel
      }),
    });

    const data = await res.json();
    const botMessage = { role: "bot", text: data.response };

    setMessages((prev) => [...prev, botMessage]);
  } catch (err) {
    console.error("Error:", err);
    setMessages((prev) => [
      ...prev,
      { role: "bot", text: "Error: Unable to reach chatbot." },
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
