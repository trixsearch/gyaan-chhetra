import { useEffect, useState } from "react";
import api from "../../api/axios";
import BookTable from "../../components/BookTable";
import SearchBar from "../../components/SearchBar";
import Pagination from "../../components/Pagination";

export default function ManageBooks() {
  const [books, setBooks] = useState([]);
  const [page, setPage] = useState(1);

  useEffect(() => {
    api.get(`/admin/books/?page=${page}`)
      .then(res => setBooks(res.data.results));
  }, [page]);

  return (
    <>
      <SearchBar onSearch={q => api.get(`/admin/books/?q=${q}`).then(r => setBooks(r.data.results))} />
      <BookTable books={books} admin />
      <Pagination page={page} setPage={setPage} />
    </>
  );
}
