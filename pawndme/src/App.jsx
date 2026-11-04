import Header from "./components/Header";
import Hero from "./components/Hero";
import FeaturedPets from "./components/FeaturedPets";
import Categories from "./components/Categories";
import HowItWorks from "./components/HowItWorks";
import Footer from "./components/Footer";

import "./App.css";

export default function App() {
  return (
    <>
      <Header />

      <main>
        <Hero />
        <FeaturedPets />
        <Categories />
        <HowItWorks />
      </main>

      <Footer />
    </>
  );
}
