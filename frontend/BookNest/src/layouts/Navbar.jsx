import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import { logout } from "../services/authService";

const Navbar = () => {
  const navigate = useNavigate();

  const { user, setUser } =
    useAuth();

  const handleLogout =
    async () => {
      try {
        await logout();

        setUser(null);

        navigate("/login");
      } catch (error) {
        console.log(error);
      }
    };

  return (
    <header className="h-16 bg-white border-b border-gray-200 px-6 flex items-center justify-between">
      <div>
        <h1 className="font-semibold text-lg">
          Digital Library
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <span>
          {user?.username}
        </span>

        <button
          onClick={handleLogout}
          className="bg-gray-100 px-4 py-2 rounded-lg hover:bg-gray-200"
        >
          Logout
        </button>
      </div>
    </header>
  );
};

export default Navbar;