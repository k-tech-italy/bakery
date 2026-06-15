import { useNavigate } from "react-router-dom";
import { ROUTES } from "../constants";
import { Button } from "../components/ui/Button";

export function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <section className="not-found-page">
      <p className="not-found-code">404</p>
      <p className="not-found-message">Page not found</p>
      <Button onClick={() => navigate(ROUTES.HOME)}>Back to Home</Button>
    </section>
  );
}