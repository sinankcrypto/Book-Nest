import Sidebar from "./SideBar";
import Navbar from "./Navbar";

const MainLayout = ({
  children,
}) => {
  return (
    <div className="h-screen flex bg-gray-50">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <Navbar />

        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;