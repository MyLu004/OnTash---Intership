import { useState } from "react";
import { useNavigate } from "react-router-dom";

//import logo 
import { GiSuperMushroom } from "react-icons/gi";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        username: email,
        password: password,
      }),
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("accessToken", data.access_token);
      localStorage.setItem("userEmail", data.email);
      console.log("loggin successful, navigate to chat")
      console.log("user email:", data.email)
      navigate("/chat");
    } else {
      alert("Login failed: " + data.detail);
    }
  };

  return (
    <div className=" min-h-screen w-screen flex items-center justify-center ">
      

      <form
        onSubmit={handleLogin}
        className="bg-black p-8 rounded-2xl shadow-md w-full max-w-md space-y-4"
      >

        {/* logo */}
        <div className="flex items-center justify-center">
          <GiSuperMushroom className="text-4xl text-white-500" />
        </div> 
        <h2 className="text-2xl font-bold text-center text-white-800">Log In</h2>

        <input
          type="email"
          placeholder="Email"
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          className="w-full bg-[var(--color-accent)] text-black py-2 rounded-lg hover:bg-[var(--color-accent-hover)] hover:text-black transition"
        >
          Login
        </button>

        <button
          type="button"
          onClick={() => navigate("/signup")}
          className="w-full border border-blue-600 py-2 rounded-lg hover:bg-[var(--color-surface)] hover:text-black transition"
        >
          Sign Up
        </button>
      </form>
      
    </div>
  );
}

export default Login;
