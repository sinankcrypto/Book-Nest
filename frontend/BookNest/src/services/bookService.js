import api from "../api/axios";

export const getBooks = async (params = {}) => {
  const response = await api.get("/books/",{ params,});

  return response.data;
};

export const getBook = async (id) => {
  const response = await api.get(`/books/${id}/`);

  return response.data;
};

export const createBook = async (formData) => {
    const response = await api.post(
        "/books/",
        formData,
        {
            headers: {
            "Content-Type":
                "multipart/form-data",
            },
        }
        );

    return response.data;
  };

export const deleteBook = async (id) => {
    await api.delete(`/books/${id}/`);
  };