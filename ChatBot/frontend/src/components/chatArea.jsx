import {  useRef, useEffect } from "react";
import ModelSelector from "../components/modelSelector";
import FileUpload from "../components/fileUpload"; 

import { marked } from "marked";    // Converts Markdown to HTML
import DOMPurify from "dompurify";  // Sanitizes HTML to prevent XSS

// Helper function to parse markdown text and sanitize it
function parseMarkdown(text) {
  if (!text) return "";
  return DOMPurify.sanitize(marked(text)); // convert and clean user input
}

function ChatArea({  
  messages,           // list of the chat message 
  input,              // input filed state
  setInput,           // function to update input
  handleSend,         // function to handle message send
  isLoading,          // boolean indicating if bot is processing
  selectedModel,      // currently selected LLM model
  setSelectedModel,   // Function to change model
  handleFileUpload,   // Function to handle file uploads
  pendingFile,        // Currently selected file (if any)
  setPendingFile,     // Function to cler selected file
}) {
  
  const bottomRef = useRef(null); // reference to scroll to bottom

  // scroll to bottm effect (scroll to bottol when chat reach the window limit)
  useEffect(() => {
  if (bottomRef.current) {
    bottomRef.current.scrollIntoView({ behavior: "smooth" });
  }
}, [messages]);

  return (
    <div className="flex flex-col flex-1 bg-[var(--color-bg)] text-white p-10">
      
      {/* Dropdown to select model */}
      <ModelSelector
        selectedModel={selectedModel}
        setSelectedModel={setSelectedModel}
      />

       {/* Message history area */}
      <div className="flex-1 overflow-y-auto p-6  space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[60%] w-fit min-w-[2rem] px-4 py-2 rounded-lg break-words ${
              msg.role === "user"
                ? "bg-gray-300 text-black self-end ml-auto"
                : "bg-[var(--color-accent)] text-black self-start mr-auto"
            }`}
            
          >
            
            <div dangerouslySetInnerHTML={{ __html: parseMarkdown(msg.text) }} />

             
          </div>
        ))}

        <div ref={bottomRef} />

      </div>

      <form
        onSubmit={handleSend}
        className="p-2 bg-[var(--color-surface)] flex items-center gap-1 text-black rounded-md"
      >
         {/* If a file is selected, show preview with remove option */}
        {pendingFile && (
          <div className="text-black bg-white p-2 rounded-md mb-2 flex justify-between items-center">
            <span className="text-sm font-medium truncate max-w-[200px]">{pendingFile.name}</span>
                <button
              type="button"
              className="ml-2 text-red-600 text-sm hover:underline"
              onClick={() => setPendingFile(null)} // clears the file correctly
            >
              Remove
            </button>
          </div>
        )}

        {/* Text input field */}
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
          className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black font-bold"
        />
        
        {/* Submit button */}
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
