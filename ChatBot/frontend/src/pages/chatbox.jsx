import { useState, useEffect } from "react";
import ChatArea from "../components/chatArea";
// import Sidebar from "../components/sideBar";
import Sidebar from "../components/sideBar";
import { v4 as uuidv4 } from "uuid";

import { FaCog } from "react-icons/fa";
import SettingsPanel from "../components/settingsPanel";
import SearchModal from "../components/searchModal";

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
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [pendingFile, setPendingFile] = useState(null);



  const handleFileSelect = (file) => {
    setPendingFile(file);  // Store for later use
  };

  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "dark";
  });

  useEffect(() => {
    document.body.classList.remove("light-theme", "dark-theme");
    document.body.classList.add(`${theme}-theme`);
    localStorage.setItem("theme", theme);
  }, [theme]);
useEffect(() => {
  const fetchChats = async () => {
    const token = localStorage.getItem("accessToken") || sessionStorage.getItem("accessToken");


    try {
      const res = await fetch("http://localhost:8000/chat/chats/", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Failed to fetch chats:", res.status, errorText);
        setChats([]); //Set empty array to avoid crash
        return;
      }

      const data = await res.json();
      const enriched = data.map(chat => ({
        ...chat,
        messages: chat.messages || [],  // Ensure messages array exists
      }));
      setChats(enriched);
      setActiveChatId(enriched[0]?.id);


    } catch (err) {
      console.error("Error fetching chats:", err);
      setChats([]); // fallback
    }
  };

  fetchChats();
}, []);

useEffect(() => {
  const syncLogout = (event) => {
    if (event.key === "logout") {
      console.log("Logged out in another tab");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("userEmail");
      window.location.href = "/"; // or your login route
    }
  };

  window.addEventListener("storage", syncLogout);
  return () => window.removeEventListener("storage", syncLogout);
}, []);


const saveChatToServer = async (chat) => {
  const token = localStorage.getItem("accessToken");
  

  await fetch("http://localhost:8000/chat/save", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(chat)
  });
};

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

const activeChat = Array.isArray(chats) ? chats.find((c) => c.id === activeChatId) : null;

const generateTitle = async (prompt) => {
  try {
    const titlePrompt = `Generate a short, clear title for this user question:\n"${prompt}"\nReturn only the title.`;
    const titleRes = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
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
        chat.id === activeChatId ? { ...chat, title: cleanTitle } : chat
      )
    );
  } catch (err) {
    console.error("Failed to generate title:", err);
  }
};

const handleSend = async (e, overrideInput = null) => {
  if (e) e.preventDefault();
  const finalInput = overrideInput || input;
  if (!finalInput.trim() && !pendingFile) return;

  setIsLoading(true);

  let extractedText = "";

  if (pendingFile) {
    const formData = new FormData();
    formData.append("file", pendingFile);

    const accessToken = localStorage.getItem("accessToken");

    try {
      // Upload
      await fetch("http://localhost:8000/upload", {
        method: "POST",
        headers: { Authorization: `Bearer ${accessToken}` },
        body: formData,
      });

      // Process
      const processRes = await fetch("http://localhost:8000/process", {
        method: "POST",
        headers: { Authorization: `Bearer ${accessToken}` },
        body: formData,
      });

      const processData = await processRes.json();
      extractedText = processData.text;
    } catch (err) {
      console.error("File processing failed:", err);
    }
  }

  // Build full prompt
  const combinedInput = `${finalInput}\n\n${extractedText ? `---\nAttached document:\n${extractedText}` : ""}`;

  const userMessage = { role: "user", text: finalInput };

  setChats((prev) => {
  const updated = prev.map((chat) =>
    chat.id === activeChatId
      ? { ...chat, messages: [...chat.messages, userMessage] }
      : chat
  );

  const updatedChat = updated.find((c) => c.id === activeChatId);


  if (updatedChat && updatedChat.messages.length === 2 && updatedChat.title === "New Chat") {
    generateTitle(finalInput);  // move your fetch logic to a helper function
  }

  if (updatedChat) saveChatToServer(updatedChat); // call save inside this scope

  return updated;
});




  const accessToken = localStorage.getItem("accessToken");

  

  const activeChat = chats.find(c => c.id === activeChatId);

const history = activeChat.messages
  .map(msg => `${msg.role === "user" ? "User" : "Assistant"}: ${msg.text}`)
  .join("\n");
 

  const structuredPrompt = `
Respond in Markdown. Here is the user’s message:
  ${history}


New user input : ${combinedInput}

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
  const botMessage = { role: "bot", text: data.response || "No response from model." };

  setChats((prev) => {
    const updatedChats = prev.map((chat) =>
      chat.id === activeChatId
        ? { ...chat, messages: [...chat.messages, botMessage] }
        : chat
    );

    const updatedChat = updatedChats.find((c) => c.id === activeChatId);
    if (updatedChat)  saveChatToServer(updatedChat); // Save latest chat to backend

    return updatedChats;
  });
} catch (err) {
  console.error("Error:", err);
}

  

  // Reset input and file
  setInput("");
  setPendingFile(null);
  setIsLoading(false);

  
};

  return (
    <div className="flex h-screen w-screen">

      {/* Floating Settings Button */}
      <button
        onClick={() => setSettingsOpen(true)}
        className="absolute top-4 right-4 z-40 p-2 rounded-full bg-[var(--color-surface)] text-black hover:bg-yellow-300 shadow"
        title="Settings"
      >
        <FaCog size={20} />
      </button>

      {settingsOpen && (
      <SettingsPanel
          onClose={() => setSettingsOpen(false)}
          theme={theme}
          setTheme={setTheme}
        />
      )}

      {searchOpen && (
      <SearchModal
        chats={chats}
        onSelectChat={setActiveChatId}
        onClose={() => setSearchOpen(false)}
      />
      )}

      <Sidebar
        chats={chats}
        sidebarOpen={sidebarOpen}
        toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        activeChatId={activeChatId}
        onNewChat={handleNewChat}
        onSelectChat={setActiveChatId}
        onDeleteChat={handleDeleteChat}
        onRenameChat={handleRenameChat}
        setSearchOpen={setSearchOpen} 
    />
      <ChatArea
        messages={activeChat?.messages || []}
        input={input}
        setInput={setInput}
        handleSend={handleSend}
        isLoading={isLoading}
        selectedModel={selectedModel}
        setSelectedModel={setSelectedModel}
        handleFileUpload={handleFileSelect}
        pendingFile={pendingFile}
        setPendingFile={setPendingFile}

      />
    </div>
  );
}

export default Chatbot;
