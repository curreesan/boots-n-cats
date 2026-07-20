import { Link } from "react-router-dom";
import "../styles/Home.css";

function Home() {
  return (
    <div className="home">
      <h1 className="home__heading">Boots n' Cats</h1>
      <p className="home__tagline">
        Shop for your pets, or find a new one to adopt.
      </p>
      <div className="home__actions">
        <Link to="/products" className="home__button home__button--primary">
          Shop Products
        </Link>
        <Link to="/pets" className="home__button home__button--secondary">
          Meet the Pets
        </Link>
      </div>
    </div>
  );
}

export default Home;
