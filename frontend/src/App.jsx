import React, { useState } from "react";

const API_URL = "http://localhost:5000/signup"; // Change this if needed

export default function App() {
  const [formData, setFormData] = useState({ name: "", password: "", img_url: "" });
  const [user, setUser] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignup = async () => {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const data = await res.json();
    if (res.ok) {
      setUser(formData); // Display the user info
      setFormData({ name: "", password: "", img_url: "" }); // Clear input fields
    } else {
      alert("Error: " + data.error);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Signup</h1>
      
      <input 
        name="name" 
        placeholder="Name" 
        value={formData.name}
        onChange={handleChange} 
      />
      
      <input 
        name="password" 
        type="password" 
        placeholder="Password" 
        value={formData.password}
        onChange={handleChange} 
      />
      
      <input 
        name="img_url" 
        placeholder="Profile Image URL" 
        value={formData.img_url}
        onChange={handleChange} 
      />

      <button onClick={handleSignup}>Create Profile</button>

      {user && (
        <div style={{ marginTop: "20px", padding: "10px", border: "1px solid black" }}>
          <h2>Profile Created:</h2>
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>Password:</strong> {user.password}</p>
          {user.img_url && <img src={user.img_url} alt="Profile" style={{ width: "100px" }} />}
        </div>
      )}
    </div>
  );
}
