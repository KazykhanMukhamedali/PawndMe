export default function Hero() {
  return (
    <section className="hero" id="home">
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
            <a href="#pets" className="primary-btn">
              Explore Pets →
            </a>

            <a href="#how-it-works" className="video-btn">
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

          <div className="adopted-badge">
            <strong>28</strong>
            <span>
              Pets Adopted
              <small>this week</small>
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
