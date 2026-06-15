import { useAuth } from "../../context/AuthContext";
import { EXTERNAL_LINKS } from "../../constants";
import { Button } from "../ui/Button";

export function Navbar() {
  const { logout } = useAuth();

  return (
    <header className="nav-bar">
      <nav className="nav-content">
        <span className="nav-brand">{{ cookiecutter.project_name }}</span>
        <div className="nav-actions">
          <a className="nav-link" href={EXTERNAL_LINKS.ADMIN} target="_blank" rel="noreferrer">
            Admin
          </a>
          <a className="nav-link" href={EXTERNAL_LINKS.SWAGGER_UI} target="_blank" rel="noreferrer">
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