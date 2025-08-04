import React, { useState } from "react";
import { motion } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";
import { FaBook } from "react-icons/fa";
import authService from "../../services/authServices";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const data = await authService.login(email, password);
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("role", data.role);

            // Arahkan sesuai role
            if (data.role === "admin") {
                navigate("/admin");
            } else {
                navigate("/user");
            }
        } catch (err) {
            setError("Email atau password salah!");
        }
    };

    return (
        <div
            className="login-container d-flex align-items-center justify-content-center"
            style={{ height: "100vh", background: "#F8F9FA" }}
        >
            <motion.div
                className="card p-4 shadow-lg"
                style={{ width: "380px", borderRadius: "12px" }}
                initial={{ opacity: 0, y: -50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                <div className="text-center mb-3">
                    <FaBook size={40} color="#2D6A4F" />
                    <h3
                        style={{
                            color: "#2D6A4F",
                            fontWeight: "bold",
                            marginTop: "10px",
                        }}
                    >
                        Sistem Perpustakaan
                    </h3>
                </div>
                {error && <div className="alert alert-danger">{error}</div>}
                <form onSubmit={handleLogin}>
                    <div className="mb-3">
                        <label className="form-label">Email</label>
                        <input
                            type="email"
                            className="form-control"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="btn w-100"
                        style={{
                            background: "#2D6A4F",
                            color: "#fff",
                            fontWeight: "bold",
                        }}
                        onMouseOver={(e) => (e.target.style.background = "#1B4332")}
                        onMouseOut={(e) => (e.target.style.background = "#2D6A4F")}
                    >
                        Login
                    </button>
                </form>

                {/* Link ke Register */}
                <p className="mt-3 text-center">
                    Belum punya akun?{" "}
                    <Link to="/register" style={{ color: "#2D6A4F", fontWeight: "bold" }}>
                        Daftar di sini
                    </Link>
                </p>
            </motion.div>
        </div>
    );
}
