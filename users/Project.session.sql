-- schema.sql
CREATE TABLE IF NOT EXISTS pdf_storage (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    file_data BYTEA,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pdf_comments (
    id SERIAL PRIMARY KEY,
    pdf_id INTEGER REFERENCES pdf_storage(id) ON DELETE CASCADE,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pdf_comments_pdf_id ON pdf_comments (pdf_id);
