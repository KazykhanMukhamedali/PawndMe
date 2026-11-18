import { useState } from "react";

export default function Header({ path, user, simple }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="header">
      <div className="container header-content">
        <a className="logo" href="#/">
          Pawnd<span>Me</span>
        </a>

        {!simple && <><button
          className="menu-toggle"
          aria-label="Toggle navigation"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰
        </button>

        <nav className={`nav ${menuOpen ? "nav-open" : ""}`}>
          <a href="#/" aria-current={path === "/" ? "page" : undefined} onClick={() => setMenuOpen(false)}>
            Home
          </a>
          <a href="#/pets" aria-current={path === "/pets" ? "page" : undefined} onClick={() => setMenuOpen(false)}>
            Explore Pets
          </a>
          {user?.account_type !== "shelter_staff" && <a href="#/favorites" aria-current={path === "/favorites" ? "page" : undefined} onClick={() => setMenuOpen(false)}>
            Favorites
          </a>}
          <a href="#/about" aria-current={path === "/about" ? "page" : undefined} onClick={() => setMenuOpen(false)}>
            About Us
          </a>
        </nav>

        <a href={user ? "#/account" : "#/login"} className="login-btn">
          {user ? "My Account" : "Login/Register"}
        </a></>}
      </div>
    </header>
  );
}
