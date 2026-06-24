import api from "../api/axios";

export const getReadingLists =
  async () => {
    const response =
      await api.get(
        "/books/reading-lists/"
      );

    return response.data;
  };

export const createReadingList =
  async (data) => {
    const response =
      await api.post(
        "/books/reading-lists/",
        data
      );

    return response.data;
  };

export const deleteReadingList =
  async (id) => {
    await api.delete(
      `/books/reading-lists/${id}/`
    );
  };

export const getReadingListDetail =
  async (id) => {
    const response =
      await api.get(
        `/books/reading-lists/${id}/`
      );

    return response.data;
  };

export const addBookToReadingList =
  async (
    listId,
    bookId
  ) => {
    const response =
      await api.post(
        `/books/reading-lists/${listId}/books/`,
        {
          book_id: bookId,
        }
      );

    return response.data;
  };

export const removeBookFromReadingList =
  async (
    listId,
    bookId
  ) => {
    await api.delete(
      `/books/reading-lists/${listId}/books/${bookId}/`
    );
  };