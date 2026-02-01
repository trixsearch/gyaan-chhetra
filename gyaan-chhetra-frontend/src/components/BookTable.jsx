export default function BookTable({ books, admin }) {
    return (
      <table width="100%">
        <thead>
          <tr>
            <th>Title</th>
            <th>Writer</th>
            <th>Available</th>
            {admin && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {books.map(b => (
            <tr key={b.uuid}>
              <td>{b.title}</td>
              <td>{b.writer}</td>
              <td>{b.quantity}</td>
              {admin && <td>Edit | Delete</td>}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
  