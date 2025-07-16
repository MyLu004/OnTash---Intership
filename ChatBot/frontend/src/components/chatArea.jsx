

import {  useRef, useEffect } from "react";
import ModelSelector from "../components/modelSelector"; // adjust path if needed
import FileUpload from "../components/fileUpload"; // adjust path if needed


import { marked } from "marked";
import DOMPurify from "dompurify";

//import { parseFormattedText } from "../utils/formatting";


function parseMarkdown(text) {
  if (!text) return "";
  return DOMPurify.sanitize(marked(text));
}

function ChatArea({  messages, input, setInput, handleSend, isLoading, selectedModel, setSelectedModel  }) {
  
  const bottomRef = useRef(null);
  
  //const [selectedModel, setSelectedModel] = useState("");
  
  

  const handleFileUpload = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const accessToken = localStorage.getItem("accessToken");

  try {
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      body: formData,
    });

    const data = await res.json();
    console.log("Uploaded file info:", data);
  } catch (err) {
    console.error("Upload failed:", err);
  }
};

  useEffect(() => {
  if (bottomRef.current) {
    bottomRef.current.scrollIntoView({ behavior: "smooth" });
  }
}, [messages]);


  return (
    <div className="flex flex-col flex-1 bg-[var(--color-bg)] text-white p-10">

      {/* Model Selector Dropdown */}
      <ModelSelector
        selectedModel={selectedModel}
        setSelectedModel={setSelectedModel}
      />

      <div className="flex-1 overflow-y-auto p-6  space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[60%] w-fit min-w-[2rem] px-4 py-2 rounded-lg break-words ${
              msg.role === "user"
                ? "bg-gray-300 text-black self-end ml-auto"
                : "bg-[var(--color-accent)] text-black self-start mr-auto"
            }`}
            //  dangerouslySetInnerHTML={{ __html: parseFormattedText(msg.text) }}
          >
            {/* {msg.text} */}
            <div dangerouslySetInnerHTML={{ __html: parseMarkdown(msg.text) }} />

             
          </div>
        ))}

        {/*  Invisible div that we scroll into view */}
        <div ref={bottomRef} />

      </div>

      <form
        onSubmit={handleSend}
        className="p-2 bg-[var(--color-surface)] flex items-center gap-1 text-black rounded-md"
      >
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
          className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black font-bold"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-[var(--color-accent)] text-black font-bold px-4 py-2 rounded-lg hover:bg-[var(--color-accent-hover)]"
        >
          Send
        </button>

        <FileUpload onFileUpload={handleFileUpload} />

      </form>
    </div>
  );
}

export default ChatArea;
