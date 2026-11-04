const categories = [
  {
    name: "Dogs",
    image: "/images/category-dogs.jpg",
    className: "category-blue",
    href: "#dogs",
  },
  {
    name: "Cats",
    image: "/images/category-cats.jpg",
    className: "category-pink",
    href: "#cats",
  },
  {
    name: "Other Animals",
    image: null,
    className: "category-gray",
    href: "#other-animals",
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
                <span className="category-paw">🐾</span>
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
