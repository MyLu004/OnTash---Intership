import { FaBars, FaPlus } from "react-icons/fa";

function Sidebar({ sidebarOpen, toggleSidebar, chats, activeChatId, onNewChat, onSelectChat }) {
  return (
    <div
      className={`${
        sidebarOpen ? "w-60 items-start" : "w-20 sm:w-15 items-center"
      } bg-[var(--color-accent)] transition-all duration-300 flex flex-col justify-start`}
    >
      {/* Toggle Button */}
      <button
        onClick={toggleSidebar}
        className="m-3 text-black bg-transparent hover:bg-white/10 p-2 rounded-md transition"
      >
        <FaBars size={25} />
      </button>

      {/* Sidebar content when open */}
      {sidebarOpen && (
        <div className="text-black mt-2 w-full p-3 space-y-4">
          {/* New Chat Button */}
          <button
            onClick={onNewChat}
            className="flex items-center gap-2 text-sm bg-white text-black font-semibold px-3 py-1 rounded-md hover:bg-yellow-200 transition"
          >
            <FaPlus /> New Chat
          </button>

          {/* Chat List */}
          {chats.length > 0 ? (
            chats.map((chat) => (
              <div
                key={chat.id}
                onClick={() => onSelectChat(chat.id)}
                className={`truncate text-sm py-1 px-3 cursor-pointer rounded-md transition 
                ${chat.id === activeChatId ? "bg-yellow-200 font-bold" : "hover:bg-yellow-300"}`}
              >
                {chat.title.slice(0, 30)}
              </div>
            ))
          ) : (
            <p className="text-sm italic text-black">No saved chats</p>
          )}
        </div>
      )}
    </div>
  );
}

export default Sidebar;
