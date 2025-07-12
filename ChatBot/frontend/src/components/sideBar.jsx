import { FaBars } from "react-icons/fa";

function Sidebar({ sidebarOpen, toggleSidebar, chats }) {
  return (
    <div className={`${sidebarOpen ? "w-60 items-start" : "w-20 sm:w-15 items-center"} bg-[var(--color-accent)] transition-all duration-300 flex flex-col justify-start`}>
      <button
        onClick={toggleSidebar}
        className="m-3 text-black bg-transparent hover:bg-white/10 p-2 rounded-md transition"
      >
        <FaBars size={25} />
      </button>
      {sidebarOpen && (
        <div className="text-black mt-2 w-full p-3">
          {/* Display stored chats (memory/history) here */}
          {chats.length > 0 ? (
            chats.map((chat, i) => (
              <div key={i} className="truncate text-sm py-1 p-3">
                {chat.slice(0, 30)}...
              </div>
            ))
          ) : (
            <p className="text-sm italic">No saved chats</p>
          )}
        </div>
      )}
    </div>
  );
}

export default Sidebar;
