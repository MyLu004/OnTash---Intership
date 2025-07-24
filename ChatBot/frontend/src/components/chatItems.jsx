import { useState } from "react";

function ChatItem({ chat, isActive, onSelect, onDelete, onRename }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="relative group w-full px-3">
      
      {/* Chat title button — triggers onSelect when clicked */}
      <div
        onClick={onSelect}
        className={`truncate text-sm py-2 pr-8 cursor-pointer rounded-md transition ${
          isActive ? "bg-yellow-200 font-bold" : "hover:bg-yellow-300"
        }`}
      >

        {/* Display only first 30 characters of chat title */}
        {chat.title.slice(0, 30)}
      </div>
        
        {/* Vertical dot menu button — only visible on hover */}
      <div className="absolute right-0 top-1/2 -translate-y-1/2 group-hover:flex hidden">
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="text-black p-1 hover:bg-yellow-100 rounded-md"
        >
          ⋮
        </button>
      </div>
      
      {/* Dropdown menu with Rename and Delete options */}
      {menuOpen && (
        <div className="absolute left-55 top-1 bg-white text-black rounded-md shadow z-10 w-32">
          <button
            className="w-full text-left px-3 py-2 hover:bg-gray-100"
            onClick={() => {
              onRename();
              setMenuOpen(false);
            }}
          >
            ✏️ Rename
          </button>

          {/* Delete option */}
          <button
            className="w-full text-left px-3 py-2 hover:bg-gray-100"
            onClick={() => {
              onDelete();
              setMenuOpen(false);
            }}
          >
            🗑️ Delete
          </button>
        </div>
      )}
    </div>
  );
}

export default ChatItem;
