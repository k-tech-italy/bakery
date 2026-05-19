import { useAuth } from "../../context/AuthContext";
import { EXTERNAL_LINKS } from "../../constants";
import { Button } from "../ui/Button";

export function Navbar() {
  const { logout } = useAuth();

  return (
    <header className="border-b bg-white px-4 py-3">
      <nav className="mx-auto flex max-w-7xl items-center justify-between">
        <span className="text-lg font-semibold">{{ cookiecutter.project_name }}</span>
        <div className="flex items-center gap-3">
          <a className="text-sm text-gray-600 hover:text-gray-900" href={EXTERNAL_LINKS.ADMIN} target="_blank" rel="noreferrer">
            Admin
          </a>
          <a className="text-sm text-gray-600 hover:text-gray-900" href={EXTERNAL_LINKS.SWAGGER_UI} target="_blank" rel="noreferrer">
            API Docs
          </a>
          <Button variant="secondary" onClick={logout}>
            Logout
          </Button>
        </div>
      </nav>
    </header>
  );
}