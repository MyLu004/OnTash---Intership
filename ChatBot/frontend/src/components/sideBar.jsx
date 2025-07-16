import { FaBars, FaPlus } from "react-icons/fa";
import ChatItem from "./chatItems";

function Sidebar({
  sidebarOpen,
  toggleSidebar,
  chats,
  activeChatId,
  onNewChat,
  onSelectChat,
  onDeleteChat,
  onRenameChat,
}) {
  return (
    <div
      className={`${
        sidebarOpen ? "w-60 items-start" : "w-20 sm:w-15 items-center"
      } bg-[var(--color-accent)] transition-all duration-300 flex flex-col justify-start`}
    >
      {/* Toggle Sidebar */}
      <button
        onClick={toggleSidebar}
        className="m-3 text-black bg-transparent hover:bg-white/10 p-2 rounded-md transition"
      >
        <FaBars size={25} />
      </button>

      {/* Sidebar content */}
      {sidebarOpen && (
        <div className="text-black mt-2 w-full py-3 space-y-4">
          {/* New Chat Button */}
          <div className="w-full px-3">
            <button
              onClick={onNewChat}
              className="flex items-center gap-2 text-sm bg-white text-black font-semibold px-3 py-1 rounded-md hover:bg-yellow-200 transition w-full"
            >
              <FaPlus /> New Chat
            </button>
          </div>

          {/* Chat List */}
          <div className="w-full flex flex-col px-1 space-y-1">
            {chats.length > 0 ? (
              chats.map((chat) => (
                <ChatItem
                  key={chat.id}
                  chat={chat}
                  isActive={chat.id === activeChatId}
                  onSelect={() => onSelectChat(chat.id)}
                  onDelete={() => onDeleteChat(chat.id)}
                  onRename={() => onRenameChat(chat.id)}
                />
              ))
            ) : (
              <p className="text-sm italic text-black px-3">No saved chats</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Sidebar;
