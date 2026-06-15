import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ROUTES } from "../constants";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";

export function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  if (isAuthenticated) {
    navigate(ROUTES.HOME, { replace: true });
    return null;
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await login(username, password);
      navigate(ROUTES.HOME, { replace: true });
    } catch {
      setError("Invalid username or password");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="auth-page">
      <article className="auth-card">
        <header className="auth-header">
          <h1 className="auth-title">{{ cookiecutter.project_name }}</h1>
          <p className="auth-subtitle">Sign in to your account</p>
        </header>
        <form onSubmit={handleSubmit} className="auth-form" noValidate>
          <Input
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
          {error && <p role="alert" className="field-error">{error}</p>}
          <Button type="submit" disabled={isLoading} className="mt-2 w-full">
            {isLoading ? "Signing in…" : "Sign in"}
          </Button>
        </form>
      </article>
    </section>
  );
}