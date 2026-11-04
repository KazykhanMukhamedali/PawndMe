import { useState } from "react";

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="header">
      <div className="container header-content">
        <a className="logo" href="#home">
          Pawnd<span>Me</span>
        </a>

        <button
          className="menu-toggle"
          aria-label="Toggle navigation"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰
        </button>

        <nav className={`nav ${menuOpen ? "nav-open" : ""}`}>
          <a href="#home" onClick={() => setMenuOpen(false)}>
            Home
          </a>
          <a href="#pets" onClick={() => setMenuOpen(false)}>
            Explore Pets
          </a>
          <a href="#favorites" onClick={() => setMenuOpen(false)}>
            Favorites
          </a>
          <a href="#about" onClick={() => setMenuOpen(false)}>
            About Us
          </a>
        </nav>

        <a href="#login" className="login-btn">
          Login/Register
        </a>
      </div>
    </header>
  );
}
