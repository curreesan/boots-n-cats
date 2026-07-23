import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
} from "@/components/ui/carousel";
import { useProducts } from "../hooks/useProducts";
import { usePets } from "../hooks/usePets";
import ProductCarouselCard from "../components/ProductCarouselCard";
import PetCard from "../components/PetCard";

function Home() {
  const { products, loading: productsLoading } = useProducts();
  const { pets, loading: petsLoading } = usePets();

  return (
    <div className="flex flex-col gap-16 py-12">
      <section className="flex flex-col items-center gap-5 py-8 text-center">
        <span className="inline-flex items-center rounded-full bg-pop-soft px-3 py-1 text-xs font-semibold tracking-wide text-pop uppercase">
          New arrivals every week
        </span>
        <h1 className="max-w-xl text-4xl font-bold tracking-tight text-balance sm:text-5xl">
          Everything your best friend needs
        </h1>
        <p className="max-w-md text-muted-foreground">
          Food, toys, and beds for dogs and cats — plus pets looking for a
          home.
        </p>
        <div className="flex gap-3 pt-2">
          <Button asChild size="lg">
            <Link to="/products">Shop Products</Link>
          </Button>
          <Button asChild size="lg" variant="outline">
            <Link to="/pets">Meet the Pets</Link>
          </Button>
        </div>
      </section>

      <section className="flex flex-col gap-5">
        <div className="flex items-end justify-between">
          <div>
            <h2 className="text-2xl font-semibold">Shop the essentials</h2>
            <p className="text-sm text-muted-foreground">
              Food, toys, beds, and more.
            </p>
          </div>
          <Link
            to="/products"
            className="flex items-center gap-1 text-sm font-medium text-primary hover:underline"
          >
            View all <ArrowRight className="size-4" />
          </Link>
        </div>
        {productsLoading ? (
          <p className="text-sm text-muted-foreground">Loading products...</p>
        ) : (
          <Carousel opts={{ align: "start" }} className="w-full">
            <CarouselContent>
              {products.map((product) => (
                <CarouselItem
                  key={product.id}
                  className="basis-1/2 sm:basis-1/3 lg:basis-1/5"
                >
                  <ProductCarouselCard product={product} />
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        )}
      </section>

      <section className="flex flex-col gap-5">
        <div className="flex items-end justify-between">
          <div>
            <h2 className="text-2xl font-semibold">
              Pets looking for a home
            </h2>
            <p className="text-sm text-muted-foreground">
              Available for adoption right now.
            </p>
          </div>
          <Link
            to="/pets"
            className="flex items-center gap-1 text-sm font-medium text-primary hover:underline"
          >
            View all <ArrowRight className="size-4" />
          </Link>
        </div>
        {petsLoading ? (
          <p className="text-sm text-muted-foreground">Loading pets...</p>
        ) : (
          <Carousel opts={{ align: "start" }} className="w-full">
            <CarouselContent>
              {pets.map((pet) => (
                <CarouselItem
                  key={pet.id}
                  className="basis-1/2 sm:basis-1/3 lg:basis-1/5"
                >
                  <PetCard pet={pet} />
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        )}
      </section>
    </div>
  );
}

export default Home;
