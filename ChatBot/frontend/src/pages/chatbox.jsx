import { useState, useEffect } from "react";
import ChatArea from "../components/chatArea";
import Sidebar from "../components/sideBar";
import { v4 as uuidv4 } from "uuid";

//const title = "this is a title for content 1";

const modelMap = {
  "GPT-3.5": "gpt3.5",
  "GPT-4": "gpt4",
  "LLaMA-3": "llama3",
  "Mistral": "mistral",
};


function Chatbot() {
  const [selectedModel, setSelectedModel] = useState("llama3");
  const [chats, setChats] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeChatId, setActiveChatId] = useState(null);
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // const [messages, setMessages] = useState([
  //   { role: "bot", text: "Hello! Ask me anything." },
  // ]);
  
  //const [title, setTitle] = useState("");

  
  
  // Load from localStorage on first mount
  useEffect(() => {
    const stored = localStorage.getItem("chats");
    if (stored) {
      const parsed = JSON.parse(stored);
      setChats(parsed);
      setActiveChatId(parsed[0]?.id); // Load first chat
    } else {
      handleNewChat(); // Create one if empty
    }
  }, []);

  // Save to localStorage when chats change
  useEffect(() => {
    localStorage.setItem("chats", JSON.stringify(chats));
  }, [chats]);

  // const handleNewChat = () => {
  //   setMessages([{ role: "bot", text: "Hello! Ask me anything." }]);
  //   setInput("");
  //   setTitle("");
  // };


  const handleNewChat = () => {
    const id = uuidv4();
    const newChat = {
      id,
      title: "New Chat",
      messages: [{ role: "bot", text: "Hello! Ask me anything." }],
    };
    setChats((prev) => [newChat, ...prev]);
    setActiveChatId(id);
    setInput("");
  };

  const handleDeleteChat = (chatId) => {
  const updated = chats.filter(c => c.id !== chatId);
  setChats(updated);

  if (activeChatId === chatId && updated.length > 0) {
    setActiveChatId(updated[0].id);
    } else if (updated.length === 0) {
      handleNewChat();
    }
  };

const handleRenameChat = (chatId) => {
  const newTitle = prompt("Enter new chat title:");
  if (newTitle) {
    setChats(prev =>
      prev.map(chat =>
        chat.id === chatId ? { ...chat, title: newTitle } : chat
      ));
    }
  };

  const activeChat = chats.find((c) => c.id === activeChatId);


  const handleSend = async (e) => {
  e.preventDefault();
  if (!input.trim() || !activeChat) return;

  setIsLoading(true);

  const userMessage = { role: "user", text: input };
  //setMessages((prev) => [...prev, userMessage]);

  // Update messages for current chat
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === activeChatId
          ? { ...chat, messages: [...chat.messages, userMessage] }
          : chat
      )
    );
  

  //retrieve access token
  const accessToken = localStorage.getItem("accessToken"); 
    // Generate title for first user input

  if (
      activeChat.messages.length === 1 &&
      activeChat.title === "New Chat"
    ) {
      try {
        const titlePrompt = `Generate a short, clear title for this user question:\n"${input}"\nReturn only the title.`;
        const titleRes = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify({
            prompt: titlePrompt,
            model: modelMap[selectedModel] || "llama3",
          }),
        });

        const titleData = await titleRes.json();
        const cleanTitle = titleData.response.trim().replace(/^["']|["']$/g, "");

        setChats((prev) =>
          prev.map((chat) =>
            chat.id === activeChatId
              ? { ...chat, title: cleanTitle }
              : chat
          )
        );
      } catch (err) {
        console.error("Failed to generate title:", err);
      }
    }

    // Send full prompt to bot
    const structuredPrompt = `
Respond in Markdown. Here is the user’s message:

${input}

- Use **bold** for key terms
- Use bullet points or numbered lists
- Use line breaks between sections or bullet points
- Use headers (###)
- Use section headers with ###
`;



  try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          prompt: structuredPrompt,
          model: modelMap[selectedModel] || "llama3",
        }),
      });

      const data = await res.json();
      console.log("Bot response: ", data)
      const botMessage = { role: "bot", text: data.response || "⚠️ No response from model." };

      // Append bot response
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? { ...chat, messages: [...chat.messages, botMessage] }
            : chat
        )
      );
    } catch (err) {
      console.error("Error:", err);
    }

    setInput("");
    setIsLoading(false);
  };
  return (
    <div className="flex h-screen w-screen">
      <Sidebar
        chats={chats}
        sidebarOpen={sidebarOpen}
        toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        activeChatId={activeChatId}
        onNewChat={handleNewChat}
        onSelectChat={setActiveChatId}
        onDeleteChat={handleDeleteChat}
        onRenameChat={handleRenameChat}
    />
      <ChatArea
        messages={activeChat?.messages || []}
        input={input}
        setInput={setInput}
        handleSend={handleSend}
        isLoading={isLoading}
        selectedModel={selectedModel}
        setSelectedModel={setSelectedModel}
      />
    </div>
  );
}

export default Chatbot;
