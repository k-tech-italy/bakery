import axios from "axios";

const restapi = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL,
  });


export interface User {
    userId: number;
    email: string;
    token: string;
    
}

export function getToken() {
    return localStorage.getItem('Token');
}


export function clearToken() {
    localStorage.setItem('Token', '');
}

export function setToken(authToken: string, userData: string) {
    localStorage.setItem('authToken', authToken);
    localStorage.setItem('userData', userData);
}

export function Login(username: string, password: string): Promise<User> {
    console.log( process.env.API_BASE_URL)
    return restapi.post('/api-auth/login/', {
        username,
        password
    }).then(r =>  r.data);
}
