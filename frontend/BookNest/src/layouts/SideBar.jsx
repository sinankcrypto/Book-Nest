import { NavLink } from "react-router-dom";

const Sidebar = () => {
  const links = [
    {
      name: "Home",
      path: "/",
    },
    {
      name: "Browse Books",
      path: "/books",
    },
    {
      name: "Reading Lists",
      path: "/reading-lists",
    },
    {
      name: "Upload Book",
      path: "/books/upload",
    },
  ];

  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-4">
      <h2 className="text-xl font-bold mb-8">
        BookNest
      </h2>

      <nav className="space-y-2">
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              `
              block
              px-4
              py-3
              rounded-lg
              transition
              ${
                isActive
                  ? "bg-yellow-100 text-yellow-700"
                  : "hover:bg-gray-100"
              }
            `
            }
          >
            {link.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;