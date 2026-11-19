import { ArrowRight } from "lucide-react";
import Paw from "./Paw";

// [color, top, left, size, rotation] for the paw prints scattered over the hero
const heroPaws = [
  ["beige", "6%", "3%", 30, -18],
  ["pink", "6%", "48%", 30, 14],
  ["beige", "30%", "44%", 28, 20],
  ["pink", "84%", "12%", 30, -12],
  ["beige", "72%", "44%", 32, 16],
  ["blue", "88%", "31%", 20, 8],
  ["beige", "38%", "91%", 30, 22],
  ["pink", "70%", "74%", 30, -16],
  ["blue", "4%", "88%", 18, -10],
];

export default function Hero() {
  return (
    <section className="hero" id="home">
      <div className="hero-paws" aria-hidden="true">
        {heroPaws.map(([color, top, left, size, angle], index) => (
          <Paw key={index} className={`paw-${color}`}
            style={{ top, left, width: size, height: size, transform: `rotate(${angle}deg)` }} />
        ))}
      </div>
      <div className="container hero-content">
        <div className="hero-text">
          <span className="hero-tag">
            Your best friend is waiting
          </span>

          <h1>
            Find Your New
            <br />
            <span>Best Friend</span>
          </h1>

          <p>
            Open your heart and home to a loyal companion.
            Thousands of loving pets are waiting to make
            your everyday brighter.
          </p>

          <div className="hero-actions">
            <a href="#/pets" className="primary-btn">
              Explore Pets <ArrowRight size={18} aria-hidden="true" />
            </a>

            <a href="#/about?section=how-it-works" className="video-btn">
              <span className="play-icon">▶</span>
              How It Works
            </a>
          </div>
        </div>

        <div className="hero-visual">
          <div className="hero-dog">
            <img
              src="/images/hero-dog.jpg"
              alt="Happy dog"
            />
          </div>

          <div className="hero-cat">
            <img
              src="/images/hero-cat.jpg"
              alt="Cute cat"
            />
          </div>

          <div className="hero-note">
            <span>♥</span>
            Ready for love
            <small>Meet your match today</small>
          </div>

        </div>
      </div>
    </section>
  );
}
