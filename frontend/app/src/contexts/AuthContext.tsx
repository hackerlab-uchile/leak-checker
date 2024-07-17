import { QueryType, get_current_user, logout_user } from "@/api/api";
import { User } from "@/models/User";
import { useRouter } from "next/router";
import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";

type authContextType = {
  user: User | null;
  login: () => void;
  logout: () => void;
  ready: boolean;
};

type AuthProps = {
  children: ReactNode;
};

const AuthContext = createContext<authContextType>({
  user: null,
  login: () => {},
  logout: () => {},
  ready: false,
});

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }: AuthProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [ready, setReady] = useState(false);
  const router = useRouter();

  async function login() {
    const user_info = await load_user_info();
    if (user_info) {
      router.push(`/?search=${user_info.value}&type=${user_info.dtype}`, "/");
    }
  }

  async function logout() {
    setUser(null);
    await logout_user();
    router.reload();
  }

  async function load_user_info() {
    const [user_info, errorMsg] = await get_current_user();
    setUser(user_info);
    setReady(true);
    return user_info;
  }

  useEffect(() => {
    load_user_info();
  }, []);

  return (
    <>
      <AuthContext.Provider
        value={{
          user,
          login,
          logout,
          ready,
        }}
      >
        {children}
      </AuthContext.Provider>
    </>
  );
};

export default AuthContext;
