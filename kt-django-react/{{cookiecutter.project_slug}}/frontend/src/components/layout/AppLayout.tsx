import { Outlet } from "react-router-dom";
import { Footer } from "./Footer";
import { Navbar } from "./Navbar";

export function AppLayout() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="app-content flex-1 p-4">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}