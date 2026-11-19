// Paw print from the PawndMe design. Takes the current text color.
export default function Paw({ className = "", style }) {
  return (
    <svg className={`paw ${className}`} style={style} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">
      <ellipse cx="4.6" cy="10.2" rx="2.2" ry="2.9" transform="rotate(-22 4.6 10.2)" />
      <ellipse cx="9.2" cy="5.3" rx="2.3" ry="3.1" transform="rotate(-6 9.2 5.3)" />
      <ellipse cx="14.8" cy="5.3" rx="2.3" ry="3.1" transform="rotate(6 14.8 5.3)" />
      <ellipse cx="19.4" cy="10.2" rx="2.2" ry="2.9" transform="rotate(22 19.4 10.2)" />
      <path d="M12 11.8c-2.5 0-4.2 2.2-5.4 4.1-1.1 1.7-1 4.1 1 4.8 1.4.4 2.8-.3 4.4-.3s3 .7 4.4.3c2-.7 2.1-3.1 1-4.8-1.2-1.9-2.9-4.1-5.4-4.1Z" />
    </svg>
  );
}
