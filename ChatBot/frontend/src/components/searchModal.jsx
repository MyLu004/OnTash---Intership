import { FaTimes } from "react-icons/fa";
import { useState } from "react";

function SearchModal({ onClose, chats, onSelectChat }) {
  const [query, setQuery] = useState("");

  const filtered = chats.filter(chat =>
    chat.title.toLowerCase().includes(query.toLowerCase()) ||
    chat.messages.some(m => m.text.toLowerCase().includes(query.toLowerCase()))
  );

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div className="bg-[var(--color-bg)] text-white w-full max-w-lg rounded-xl shadow-lg">
        {/* Top bar with search input and close */}
        <div className="flex items-center border-b border-gray-700 p-3">
          <input
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search chat titles or messages..."
            className="flex-1 bg-transparent text-white text-sm outline-none px-2"
          />
          <button onClick={onClose} className="text-gray-400 hover:text-white p-1">
            <FaTimes />
          </button>
        </div>

        {/* Results */}
        <div className="max-h-96 overflow-y-auto p-2">
          {filtered.length ? (
            filtered.map((chat) => (
              <div
                key={chat.id}
                onClick={() => {
                  onSelectChat(chat.id);
                  onClose();
                }}
                className="p-2 hover:bg-white/10 rounded-md cursor-pointer"
              >
                <p className="text-sm font-semibold truncate">{chat.title}</p>
              </div>
            ))
          ) : (
            <p className="text-sm text-gray-400 px-2 py-4 text-center">No results found</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default SearchModal;
