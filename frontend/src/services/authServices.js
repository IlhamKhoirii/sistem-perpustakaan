import api from "./api";

const login = async (email, password) => {
  const res = await api.post("/auth/login", { email, password });
  return res.data;
};

const register = async (nama, email, password) => {
  const res = await api.post("/auth/register", { nama, email, password });
  return res.data;
};

export default { login, register };
