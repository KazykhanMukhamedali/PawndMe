import { useState } from "react";

export default function Footer() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  function handleSubscribe(event) {
    event.preventDefault();

    setMessage("Thanks for subscribing!");
    setEmail("");
  }

  return (
    <footer className="footer" id="about">
      <div className="container">
        <div className="footer-grid">
          <div className="footer-brand">
            <a href="#home" className="logo">
              Pawnd<span>Me</span>
            </a>

            <p>
              Helping loving hearts find their perfect
              furry companions, one adoption at a time.
            </p>

            <div className="social-links">
              <a href="https://facebook.com" aria-label="Facebook">
                f
              </a>
              <a href="https://instagram.com" aria-label="Instagram">
                ◎
              </a>
              <a href="https://telegram.org" aria-label="Telegram">
                ➤
              </a>
            </div>
          </div>

          <div className="footer-links">
            <h4>Discover</h4>
            <a href="#pets">Explore Pets</a>
            <a href="#dogs">Dogs</a>
            <a href="#cats">Cats</a>
            <a href="#other-animals">Other Animals</a>
          </div>

          <div className="footer-links">
            <h4>Learn</h4>
            <a href="#how-it-works">How It Works</a>
            <a href="#adoption-guide">Adoption Guide</a>
            <a href="#pet-care">Pet Care Tips</a>
            <a href="#stories">Success Stories</a>
          </div>

          <div className="newsletter">
            <h4>Stay in the loop</h4>
            <p>
              Sweet stories and new friends,
              delivered weekly.
            </p>

            <form onSubmit={handleSubscribe}>
              <input
                type="email"
                placeholder="Your email address"
                aria-label="Email address"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                required
              />
              <button type="submit" aria-label="Subscribe">
                →
              </button>
            </form>

            {message && <small>{message}</small>}
          </div>
        </div>

        <div className="footer-bottom">
          <span>
            © 2025 PawndMe. Made with love for every paw.
          </span>

          <span>
            <a href="#privacy">Privacy Policy</a>
            {" · "}
            <a href="#terms">Terms of Use</a>
          </span>
        </div>
      </div>
    </footer>
  );
}
