import {
  useEffect,
  useState,
} from "react";

import toast from "react-hot-toast";

import {
  getReadingLists,
  addBookToReadingList,
} from "../../services/readingListService";

import { createReadingList } from "../../services/readingListService";

const AddToReadingListModal = ({
  bookId,
  open,
  onClose,
}) => {
  const [lists, setLists] =
    useState([]);

  const [selectedList, setSelectedList] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [newListName, setNewListName] =
    useState("");

  const [creatingList, setCreatingList] =
    useState(false);

  useEffect(() => {
    if (!open) return;

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

    fetchLists();
  }, [open]);

  const handleCreateList =
    async () => {
      if (!newListName.trim()) {
        toast.error(
          "Enter a list name"
        );
        return;
      }

      try {
        setCreatingList(true);

        const newList =
          await createReadingList({
            name: newListName,
          });

        setLists((prev) => [
          ...prev,
          newList,
        ]);

        setSelectedList(
          newList.id
        );

        setNewListName("");

        toast.success(
          "Reading list created"
        );
      } catch {
        toast.error(
          "Failed to create list"
        );
      } finally {
        setCreatingList(false);
      }
    };

  const handleAdd =
    async () => {
      if (!selectedList) {
        toast.error(
          "Select a reading list"
        );
        return;
      }

      try {
        setLoading(true);

        await addBookToReadingList(
          selectedList,
          bookId
        );

        toast.success(
          "Book added successfully"
        );

        onClose();
      } catch (error) {
        toast.error(
          error?.response?.data
            ?.detail ||
            "Failed to add book"
        );
      } finally {
        setLoading(false);
      }
    };

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50">
      <div className="bg-white w-full max-w-md rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-5">
          Add To Reading List
        </h2>

        <select
          value={selectedList}
          onChange={(e) =>
            setSelectedList(
              e.target.value
            )
          }
          className="w-full border border-gray-300 rounded-lg px-4 py-3"
        >
          <option value="">
            Select a list
          </option>

          {lists.map((list) => (
            <option
              key={list.id}
              value={list.id}
            >
              {list.name}
            </option>
          ))}
        </select>

        <div className="mt-5 border-t pt-5">
          <p className="text-sm font-medium mb-3">
            Create New Reading List
          </p>

          <div className="flex gap-2">
            <input
              type="text"
              value={newListName}
              onChange={(e) =>
                setNewListName(
                  e.target.value
                )
              }
              placeholder="Favorites"
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3"
            />

            <button
              onClick={handleCreateList}
              disabled={creatingList}
              className="bg-gray-100 hover:bg-gray-200 px-4 rounded-lg"
            >
              {creatingList
                ? "..."
                : "Create"}
            </button>
          </div>
        </div>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg bg-gray-100"
          >
            Cancel
          </button>

          <button
            onClick={handleAdd}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-yellow-400"
          >
            {loading
              ? "Adding..."
              : "Add"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddToReadingListModal;