import {
  useEffect,
  useState,
} from "react";

import {
  Link,
} from "react-router-dom";

import toast from "react-hot-toast";

import MainLayout from "../../layouts/MainLayout";

import {
  getReadingLists,
  createReadingList,
  deleteReadingList,
} from "../../services/readingListService";

const ReadingLists = () => {
  const [lists, setLists] =
    useState([]);

  const [name, setName] =
    useState("");

  const fetchLists =
    async () => {
      try {
        const data =
          await getReadingLists();

        setLists(data.results);
      } catch (error) {
        console.log(error);
      }
    };

  useEffect(() => {
    fetchLists();
  }, []);

  const handleCreate =
    async () => {
      if (!name.trim())
        return;

      try {
        await createReadingList(
          {
            name,
          }
        );

        toast.success(
          "Reading list created"
        );

        setName("");

        fetchLists();
      } catch {
        toast.error(
          "Failed to create list"
        );
      }
    };

  const handleDelete =
    async (id) => {
      try {
        await deleteReadingList(
          id
        );

        toast.success(
          "Reading list deleted"
        );

        fetchLists();
      } catch {
        toast.error(
          "Failed to delete list"
        );
      }
    };

  return (
    <MainLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold">
            Reading Lists
          </h1>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200">
          <div className="flex gap-4">
            <input
              value={name}
              onChange={(e) =>
                setName(
                  e.target.value
                )
              }
              placeholder="List name"
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3"
            />

            <button
              onClick={
                handleCreate
              }
              className="bg-yellow-400 px-5 rounded-lg"
            >
              Create
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {lists.map((list) => (
            <div
              key={list.id}
              className="bg-white border border-gray-200 rounded-xl p-6"
            >
              <div>
                <h3 className="font-semibold text-lg">
                  {list.name}
                </h3>

                <p className="text-sm text-gray-500 mt-1">
                  {list.book_count} books
                </p>
              </div>

              <div className="flex gap-3 mt-6">
                <Link
                  to={`/reading-lists/${list.id}`}
                  className="bg-gray-100 px-4 py-2 rounded-lg"
                >
                  Open
                </Link>

                <button
                  onClick={() =>
                    handleDelete(list.id)
                  }
                  className="bg-red-100 text-red-600 px-4 py-2 rounded-lg"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </MainLayout>
  );
};

export default ReadingLists;