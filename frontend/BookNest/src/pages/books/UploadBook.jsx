import {
  useState,
} from "react";

import { useNavigate } from "react-router-dom";

import toast from "react-hot-toast";

import MainLayout from "../../layouts/MainLayout";

import { createBook } from "../../services/bookService";

const UploadBook = () => {
  const navigate = useNavigate();

  const [loading, setLoading] =
    useState(false);

  const [formData, setFormData] =
    useState({
      title: "",
      author: "",
      genre: "",
      publication_date: "",
      description: "",
    });

  const [coverImage, setCoverImage] =
    useState(null);

  const [pdfFile, setPdfFile] =
    useState(null);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]:
        e.target.value,
    }));
  };

  const handleSubmit = async (
    e
  ) => {
    e.preventDefault();

    if (!pdfFile) {
      toast.error(
        "Please upload a PDF file."
      );
      return;
    }

    try {
      setLoading(true);

      const data =
        new FormData();

      data.append(
        "title",
        formData.title
      );

      data.append(
        "author",
        formData.author
      );

      data.append(
        "genre",
        formData.genre
      );

      data.append(
        "publication_date",
        formData.publication_date
      );

      data.append(
        "description",
        formData.description
      );

      data.append(
        "pdf_file",
        pdfFile
      );

      if (coverImage) {
        data.append(
          "cover_image",
          coverImage
        );
      }

      await createBook(data);

      toast.success(
        "Book uploaded successfully."
      );

      navigate("/books");
    } catch (error) {
      console.log(error);

      toast.error(
        "Failed to upload book."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout>
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Upload Book
          </h1>

          <p className="text-gray-500 mt-2">
            Share a book with the
            BookNest community.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-white p-8 rounded-2xl border border-gray-200 space-y-6"
        >
          <div>
            <label className="block mb-2 font-medium">
              Title
            </label>

            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={
                handleChange
              }
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Author
            </label>

            <input
              type="text"
              name="author"
              value={formData.author}
              onChange={
                handleChange
              }
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Genre
            </label>

            <input
              type="text"
              name="genre"
              value={formData.genre}
              onChange={
                handleChange
              }
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Publication Date
            </label>

            <input
              type="date"
              name="publication_date"
              value={
                formData.publication_date
              }
              onChange={
                handleChange
              }
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Description
            </label>

            <textarea
              rows="5"
              name="description"
              value={
                formData.description
              }
              onChange={
                handleChange
              }
              className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Cover Image
            </label>

            <input
              type="file"
              accept="image/*"
              onChange={(e) =>
                setCoverImage(
                  e.target.files[0]
                )
              }
            />
            {coverImage && (
            <p className="text-sm mt-2 text-gray-500">
                {coverImage.name}
            </p>
            )}
          </div>

          <div>
            <label className="block mb-2 font-medium">
              PDF File
            </label>

            <input
              type="file"
              accept=".pdf"
              onChange={(e) =>
                setPdfFile(
                  e.target.files[0]
                )
              }
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-yellow-400 hover:bg-yellow-500 transition py-3 rounded-lg font-medium disabled:opacity-50"
          >
            {loading
              ? "Uploading..."
              : "Upload Book"}
          </button>
        </form>
      </div>
    </MainLayout>
  );
};

export default UploadBook;