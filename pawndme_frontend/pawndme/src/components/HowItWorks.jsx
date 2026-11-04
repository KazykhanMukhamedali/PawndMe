const steps = [
  {
    number: "01",
    icon: "⌕",
    title: "Search & Discover",
    description:
      "Browse pets and find the one who feels just right.",
    color: "step-blue",
  },
  {
    number: "02",
    icon: "♡",
    title: "View Their Story",
    description:
      "Learn about their personality, needs, and history.",
    color: "step-pink",
  },
  {
    number: "03",
    icon: "✓",
    title: "Apply to Adopt",
    description:
      "Send a simple application to their trusted shelter.",
    color: "step-green",
  },
  {
    number: "04",
    icon: "🐾",
    title: "Welcome Them Home",
    description:
      "Meet your new best friend and begin your story.",
    color: "step-yellow",
  },
];

export default function HowItWorks() {
  return (
    <section
      className="how-it-works section"
      id="how-it-works"
    >
      <div className="container">
        <div className="section-heading">
          <span className="eyebrow">A SIMPLE JOURNEY</span>
          <h2 className="section-title">How It Works</h2>
          <p>
            From browsing to bringing them home, we make
            adoption feel simple and joyful.
          </p>
        </div>

        <div className="steps-grid">
          {steps.map((step) => (
            <div className="step" key={step.number}>
              <div className={`step-icon ${step.color}`}>
                {step.icon}
              </div>

              <span className="step-number">
                {step.number}
              </span>

              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
