from models import Book, Author, Category, User, Publisher

def build_sql_query(params):
    # Memulai dengan query dasar untuk tabel Book
    query = Book.query

    # Filter berdasarkan judul buku (case-insensitive)
    if 'title' in params:
        query = query.filter(Book.title.ilike(f"%{params['title']}%"))
    
    # Filter berdasarkan nama penulis (case-insensitive)
    if 'author' in params:
        query = query.join(Author).filter(Author.name.ilike(f"%{params['author']}%"))
    
    # Filter berdasarkan kategori (case-insensitive)
    if 'category' in params:
        query = query.join(Category).filter(Category.name.ilike(f"%{params['category']}%"))
    
    # Filter berdasarkan rentang harga buku
    if 'price_min' in params and 'price_max' in params:
        query = query.filter(Book.price.between(params['price_min'], params['price_max']))

    # Filter berdasarkan nama penerbit (case-insensitive)
    if 'publisher' in params:
        query = query.join(Publisher).filter(Publisher.name.ilike(f"%{params['publisher']}%"))

    # Filter berdasarkan nama pengguna yang memiliki buku di wishlist (case-insensitive)
    if 'username' in params:
        query = query.join(User, Book.wishlist_items).filter(User.username.ilike(f"%{params['username']}%"))
    
    # Mengembalikan semua hasil yang sesuai dengan filter yang diterapkan
    return query.all()
