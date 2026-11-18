export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-grid site-footer-grid">
          <div className="footer-brand">
            <a href="#/" className="logo">Pawnd<span>Me</span></a>
            <p>Helping loving hearts find their perfect furry companions, one adoption at a time.</p>
          </div>
          <div className="footer-links">
            <h4>Discover</h4>
            <a href="#/pets">Explore Pets</a>
            <a href="#/pets?type=dog">Dogs</a>
            <a href="#/pets?type=cat">Cats</a>
            <a href="#/pets?type=other">Other Animals</a>
          </div>
          <div className="footer-links">
            <h4>Learn</h4>
            <a href="#/about">About Us</a>
            <a href="#/about?section=how-it-works">How It Works</a>
          </div>
        </div>
        <div className="footer-bottom"><span>© PawndMe</span></div>
      </div>
    </footer>
  );
}
