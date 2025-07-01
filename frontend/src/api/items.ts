import axios from "axios";

const API_URL = "http://localhost:8000/api/items/";

export async function getItems() {
  const response = await axios.get(API_URL);
  return response.data;
}