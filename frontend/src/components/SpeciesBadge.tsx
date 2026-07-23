import { Badge } from "@/components/ui/badge";

type SpeciesBadgeProps = {
  species: string;
};

function SpeciesBadge({ species }: SpeciesBadgeProps) {
  const isDog = species.toLowerCase() === "dog";
  return (
    <Badge
      className={
        isDog
          ? "bg-sky-100 text-sky-700 capitalize"
          : "bg-pop-soft text-pop capitalize"
      }
    >
      {species}
    </Badge>
  );
}

export default SpeciesBadge;
