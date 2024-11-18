import {   useState } from "react";
import {  Login, setToken } from "../service/auth";
import { useNavigate } from "react-router-dom";

function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();



  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);


    Login(username, password)
      .then((res) => {

         setToken( res.token, res.email );
         navigate('/')
      })
      .catch((error) => setError(error.message)).finally(() => setLoading(false));
  };

  return (
    <div className="login-container">
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        required
                        data-testid="username-input"
                    />
                </div>
                <div className="form-group">
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                        data-testid="password-input"
                    />
                </div>
                
                {error && <div className="error-message">{error}</div>}
                
                <button 
                    type="submit" 
                    disabled={loading}
                    data-testid="login-button"
                >
                    {loading ? (
                        <span data-testid="loading-spinner">Loading...</span>
                    ) : (
                        'Login'
                    )}
                </button>
            </form>
        </div>
  );
}

export default LoginScreen;
