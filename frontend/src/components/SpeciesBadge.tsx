import "../styles/SpeciesBadge.css";

type SpeciesBadgeProps = {
  species: string;
};

function SpeciesBadge({ species }: SpeciesBadgeProps) {
  const className = `species-badge species-badge--${species.toLowerCase()}`;
  return <span className={className}>{species}</span>;
}

export default SpeciesBadge;
