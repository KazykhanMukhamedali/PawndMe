import Paw from "./Paw";

const categories = [
  {
    name: "Dogs",
    image: "/images/category-dogs.jpg",
    className: "category-blue",
    paw: "paw-dog",
    href: "#/pets?type=dog",
  },
  {
    name: "Cats",
    image: "/images/category-cats.jpg",
    className: "category-pink",
    paw: "paw-cat",
    href: "#/pets?type=cat",
  },
  {
    name: "Other Animals",
    image: null,
    className: "category-gray",
    paw: "paw-other",
    href: "#/pets?type=other",
  },
];

export default function Categories() {
  return (
    <section className="categories section">
      <div className="container">
        <h2 className="section-title">
          Browse by Category
        </h2>

        <div className="category-grid">
          {categories.map((category) => (
            <a
              href={category.href}
              key={category.name}
              className={`category-card ${category.className}`}
            >
              <div className="category-text">
                <Paw className={`category-paw ${category.paw}`} />
                <h3>{category.name}</h3>
              </div>

              {category.image && (
                <img
                  src={category.image}
                  alt={category.name}
                />
              )}
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
