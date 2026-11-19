// Light-blue wavy shapes between page sections, as in the design.
// "band": a wavy strip between two white sections. "edge": the wavy top of a blue block below.
const paths = {
  band: "M0 22C300 58 960 -6 1440 30V88C1080 124 420 52 0 98Z",
  edge: "M0 62C380 8 1020 96 1440 28V100H0Z",
};

export default function Wave({ variant = "band" }) {
  return (
    <svg className={`wave wave-${variant}`} viewBox="0 0 1440 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">
      <path d={paths[variant]} />
    </svg>
  );
}
