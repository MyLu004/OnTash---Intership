import { FaTimes } from "react-icons/fa";
import { useEffect, useState } from "react";

function SettingsPanel({ onClose, theme, setTheme }) {
  const [userEmail, setUserEmail] = useState("");

  // Load user info (from localStorage, token, or API)
  useEffect(() => {
    const email = localStorage.getItem("userEmail"); // or decode from token
    if (email) setUserEmail(email);
  }, []);

  const handleLogout = () => {
    // Clear all auth/session info
    localStorage.removeItem("accessToken");
    localStorage.removeItem("userEmail");
    // Optional: redirect to login page
    window.location.href = "/"; // change path to your login route
  };

  return (
    <div className="absolute top-0 right-0 m-4 p-6 bg-white text-black rounded-lg shadow-lg z-50 w-64">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-bold">Settings</h2>
        <button onClick={onClose}>
          <FaTimes />
        </button>
      </div>

      {/* User Info */}
      <div className="mb-4 border-b pb-3">
        <p className="text-sm text-gray-600">Signed in as</p>
        <p className="font-semibold truncate">{userEmail || "Unknown User"}</p>
      </div>

      <div className="space-y-3">
        {/* Theme */}
        <div>
          <label className="block text-sm font-semibold">Theme</label>
          <select className="w-full border p-1 rounded"
                value={theme}
                onChange={(e) => setTheme(e.target.value)}>
            <option value="dark">Dark</option>
            <option value="light">Light</option>
          </select>
        </div>

        <button className="bg-yellow-400 hover:bg-yellow-300 text-black px-3 py-1 rounded w-full mt-2">
          Save Settings
        </button>

        {/* Log Out */}
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-400 text-white px-3 py-1 rounded w-full mt-2"
        >
          Log Out
        </button>
      </div>
    </div>
  );
}

export default SettingsPanel;
