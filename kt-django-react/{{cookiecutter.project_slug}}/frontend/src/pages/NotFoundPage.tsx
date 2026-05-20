import { useNavigate } from "react-router-dom";
import { ROUTES } from "../constants";
import { Button } from "../components/ui/Button";

export function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <section className="flex min-h-screen flex-col items-center justify-center gap-4">
      <p className="text-6xl font-bold text-gray-300">404</p>
      <p className="text-lg text-gray-600">Page not found</p>
      <Button onClick={() => navigate(ROUTES.HOME)}>Back to Home</Button>
    </section>
  );
}